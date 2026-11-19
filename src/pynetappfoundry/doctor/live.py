"""Live checks for ``nf doctor``: one read-only request per configured API.

Every request is a ``GET``. The one exception is the Console OAuth token request,
which is a ``POST`` to the token endpoint: it creates and changes no Console
resource, and every API call after it is a ``GET`` (ADR-0035). The first contact with
an ONTAP or AIQUM host records its TLS fingerprint in the local trust store, as
``nf utils validate`` does.

A result describes a failure only as ``HTTP <status>`` or the exception class name.
Only ``ConfigurationError`` and ``ConsoleAuthError`` messages are shown, since both
are secret-free by design. Client classes are imported lazily and can be injected.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import requests

from pynetappfoundry.clients.console import ConsoleAuthError
from pynetappfoundry.clients.trust import HostIdentityChangedError
from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.core.config_checks import CheckResult, CheckSection, CheckStatus
from pynetappfoundry.doctor import API_NAMES

logger = logging.getLogger(__name__)

SPEC_HINT = (
    "Copy the spec file into <config>/apis/<api>/; "
    "see docs/getting-started/configuration.md (Spec files)."
)


@dataclass
class Factories:
    """Client factories, replaced in tests so no real client is built.

    Attributes:
        ontap: Called as ``factory(cluster=..., config=...)``.
        aiqum: Called as ``factory(name, config)``.
        dii: Called as ``factory(config, name)``.
        console_api: Called as ``factory(config)`` or ``factory(config, scope=scope)``.
        console_agent: Called as ``factory(config, agent_id, token_provider=..., scope=...)``.
    """

    ontap: Callable[..., Any] | None = None
    aiqum: Callable[..., Any] | None = None
    dii: Callable[..., Any] | None = None
    console_api: Callable[..., Any] | None = None
    console_agent: Callable[..., Any] | None = None


def _chain(exc: BaseException) -> list[BaseException]:
    """Return ``exc`` and its causes, so a wrapped error is still recognised."""
    seen: list[BaseException] = []
    current: BaseException | None = exc
    while current is not None and current not in seen:
        seen.append(current)
        current = current.__cause__ or current.__context__
    return seen


def _failure(
    exc: BaseException, *, credentials_hint: str | None = None, forbidden_warns: bool = False
) -> tuple[str, str | None, CheckStatus]:
    """Describe a failed request without quoting the response or the exception text.

    Args:
        exc: The exception raised by the client.
        credentials_hint: Advice for a 401 or 403.
        forbidden_warns: Report a 403 as a warning instead of an error.

    Returns:
        ``(label, hint, status)``.
    """
    for item in _chain(exc):
        if isinstance(item, HostIdentityChangedError):
            return "identity changed", item.reset_hint, CheckStatus.ERROR
    if isinstance(exc, requests.HTTPError):
        code = exc.response.status_code if exc.response is not None else None
        if code == 401:
            return (
                "HTTP 401",
                credentials_hint or "Check the stored credentials.",
                CheckStatus.ERROR,
            )
        if code == 403:
            hint = "The account authenticated but lacks permission for this read-only request."
            if credentials_hint:
                hint += f" {credentials_hint}"
            return "HTTP 403", hint, CheckStatus.WARNING if forbidden_warns else CheckStatus.ERROR
        return f"HTTP {code}", "Check the service state and re-run.", CheckStatus.ERROR
    if isinstance(exc, (requests.ConnectionError, requests.Timeout)):
        return (
            f"unreachable ({type(exc).__name__})",
            "Check the address, the network path and any proxy.",
            CheckStatus.ERROR,
        )
    if isinstance(exc, FileNotFoundError):
        return "spec file missing", SPEC_HINT, CheckStatus.SKIPPED
    if isinstance(exc, (ConfigurationError, ConsoleAuthError)):
        return str(exc), "See nf config validate.", CheckStatus.ERROR
    logger.debug("Live check failed", exc_info=exc)
    return (
        f"failed ({type(exc).__name__})",
        "Re-run with --debug for the traceback.",
        CheckStatus.ERROR,
    )


def _failed_row(
    subject: str,
    name: str,
    exc: BaseException,
    *,
    credentials_hint: str | None = None,
    forbidden_warns: bool = False,
) -> CheckResult:
    """Build the result row of a failed request."""
    detail, hint, status = _failure(
        exc, credentials_hint=credentials_hint, forbidden_warns=forbidden_warns
    )
    label = f"{name}: {detail}"
    errors = (label,) if status is CheckStatus.ERROR else ()
    return CheckResult(subject, status, label, errors, hint)


def _in_scope(config: Config, data_type: str, scope: str | None) -> list[str]:
    """Return the names of the ``data_type`` objects to probe."""
    return [
        name
        for name in config.data.get(data_type, {})
        if scope is None or config.get_scope(data_type, name) == scope
    ]


def check_ontap(
    config: Config,
    clusters: dict[str, dict[str, Any]],
    *,
    client_factory: Callable[..., Any] | None = None,
) -> list[CheckResult]:
    """``GET /cluster`` on each cluster and compare the reported name with the key."""
    from pynetappfoundry.clients.ontap.probe import probe_cluster

    results: list[CheckResult] = []
    for name, details in clusters.items():
        subject = f"live.ontap.{name}"
        try:
            probe = probe_cluster(name, details, config, client_factory=client_factory)
        except Exception as e:
            results.append(
                _failed_row(
                    subject,
                    name,
                    e,
                    credentials_hint=(
                        f"Set them with: nf config set-credential --cluster {name} --user USER"
                    ),
                )
            )
            continue
        if probe.name_matches:
            results.append(CheckResult(subject, CheckStatus.OK, f"{name}: connected"))
        else:
            results.append(
                CheckResult(
                    subject,
                    CheckStatus.WARNING,
                    f"{name}: Config name {name} does not match cluster name {probe.cluster_name}",
                    hint="Rename the [clusters] key or check its ip.",
                )
            )
    return results


def check_aiqum(
    config: Config,
    scope: str | None,
    *,
    client_factory: Callable[..., Any] | None = None,
) -> list[CheckResult]:
    """``GET /datacenter/cluster/clusters?max_records=1`` on each AIQUM instance."""
    results: list[CheckResult] = []
    for name in _in_scope(config, "aiqums", scope):
        subject = f"live.aiqum.{name}"
        try:
            factory = client_factory
            if factory is None:
                from pynetappfoundry.clients.aiqum.api import AIQUMAPIClient

                factory = AIQUMAPIClient
            client = factory(name, config)
            client.call_endpoint("/datacenter/cluster/clusters", query_params={"max_records": 1})
        except Exception as e:
            results.append(
                _failed_row(
                    subject,
                    name,
                    e,
                    credentials_hint=(
                        f"Set them with: nf config set-credential --type aiqums --name {name} "
                        "--user USER"
                    ),
                )
            )
        else:
            results.append(CheckResult(subject, CheckStatus.OK, f"{name}: connected"))
    return results


def check_dii(
    config: Config,
    scope: str | None,
    *,
    client_factory: Callable[..., Any] | None = None,
) -> list[CheckResult]:
    """``GET /assets/storages/count`` per Cloud Insights tenant (or ``[general]``).

    A 403 is a warning: DII tokens are scoped by API category, so the token
    authenticated but may lack the Assets read scope.
    """
    tenants: list[str | None] = list(_in_scope(config, "cloudinsights", scope))
    if not tenants and scope is None and "general" in config.settings.get("diiapi", {}):
        tenants = [None]
    results: list[CheckResult] = []
    for tenant in tenants:
        shown = tenant or "general"
        subject = f"live.dii.{shown}"
        try:
            factory = client_factory
            if factory is None:
                from pynetappfoundry.clients.dii.api import DIIAPIClient

                factory = DIIAPIClient
            client = factory(config, tenant)
            client.call_endpoint("/assets/storages/count")
        except Exception as e:
            hint = (
                "Store the token with: nf config set-credential --type cloudinsights "
                f"--name {tenant} --user token"
                if tenant
                else "Set the token in <config>/apis/dii/diiapi.toml."
            )
            results.append(
                _failed_row(subject, shown, e, credentials_hint=hint, forbidden_warns=True)
            )
        else:
            results.append(CheckResult(subject, CheckStatus.OK, f"{shown}: connected"))
    return results


def check_console(
    config: Config,
    scope: str | None,
    *,
    api_client_factory: Callable[..., Any] | None = None,
    agent_client_factory: Callable[..., Any] | None = None,
) -> list[CheckResult]:
    """Check each Console account: its token, its organizations and its active agents."""
    try:
        accounts = config.console_account_scopes()
    except ConfigurationError as e:
        label = f"Console: {e}"
        return [
            CheckResult(
                "live.console", CheckStatus.ERROR, label, (label,), "See nf config validate."
            )
        ]
    if scope is not None:
        accounts = [a for a in accounts if a == scope]
    if not accounts:
        return [CheckResult("live.console", CheckStatus.SKIPPED, "No Console account configured")]

    api_factory = api_client_factory
    if api_factory is None:
        from pynetappfoundry.clients.console.api import ConsoleAPIClient

        api_factory = ConsoleAPIClient
    agent_factory = agent_client_factory
    if agent_factory is None:
        from pynetappfoundry.clients.console.agent import ConsoleAgentClient

        agent_factory = ConsoleAgentClient

    results: list[CheckResult] = []
    for account in accounts:
        shown = account or "root"
        subject = f"live.console.{shown}"
        try:
            client = api_factory(config) if account is None else api_factory(config, scope=account)
            organizations = client.list_organizations()
        except Exception as e:
            results.append(
                _failed_row(
                    subject,
                    shown,
                    e,
                    credentials_hint="Check consoleapi.toml and the stored credentials.",
                )
            )
            continue
        results.append(
            CheckResult(
                subject,
                CheckStatus.OK,
                f"{shown}: token works, {len(organizations)} organization(s)",
            )
        )
        provider = client.user_token_provider or client.service_token_provider
        for org in organizations:
            org_name = org.name or org.id
            try:
                agents = client.list_agents(org.id)
            except Exception as e:
                results.append(_failed_row(f"{subject}.{org.id}", f"{shown}/{org_name}", e))
                continue
            for agent in agents:
                agent_subject = f"{subject}.{org.id}.{agent.agent_id}"
                label = f"{shown}/{org_name}/{agent.name or agent.agent_id}"
                if agent.status != "active":
                    results.append(
                        CheckResult(
                            agent_subject,
                            CheckStatus.WARNING,
                            f"{label}: inactive in Console; not probed",
                            hint="Start the agent in Console, then re-run.",
                        )
                    )
                    continue
                try:
                    agent_factory(
                        config, agent.agent_id, token_provider=provider, scope=account
                    ).about()
                except Exception as e:
                    results.append(_failed_row(agent_subject, label, e))
                else:
                    results.append(
                        CheckResult(agent_subject, CheckStatus.OK, f"{label}: reachable")
                    )
    return results


def run_live_checks(
    config: Config,
    *,
    apis: tuple[str, ...] = API_NAMES,
    scope: str | None,
    clusters: dict[str, dict[str, Any]],
    factories: Factories | None = None,
) -> list[CheckSection]:
    """Run the live checks of the selected APIs; a section appears only when it has rows."""
    f = factories or Factories()
    sections: list[CheckSection] = []
    if "ontap" in apis:
        sections.append(
            CheckSection("ONTAP", tuple(check_ontap(config, clusters, client_factory=f.ontap)))
        )
    if "aiqum" in apis:
        sections.append(
            CheckSection("AIQUM", tuple(check_aiqum(config, scope, client_factory=f.aiqum)))
        )
    if "dii" in apis:
        sections.append(CheckSection("DII", tuple(check_dii(config, scope, client_factory=f.dii))))
    if "console" in apis:
        sections.append(
            CheckSection(
                "Console (live)",
                tuple(
                    check_console(
                        config,
                        scope,
                        api_client_factory=f.console_api,
                        agent_client_factory=f.console_agent,
                    )
                ),
            )
        )
    return [section for section in sections if section.results]
