"""Live checks for ``nf doctor``: one read-only request per configured API.

Every request is a ``GET``, with three exceptions (ADR-0035). The Console OAuth token
request is a ``POST`` to the token endpoint: it creates and changes no Console
resource, and every API call after it is a ``GET``. The Digital Advisor probe is a
GraphQL query sent as a ``POST``, checked by ``ensure_read_only``. A Digital Advisor
refresh-token client also ``POST`` s to its token endpoint and writes the rotated tokens
to ``digitaladvisorapi.toml``, but only when the stored access token is missing, expired
or rejected by the server. The first contact with
an ONTAP or AIQUM host records its TLS fingerprint in the local trust store, as
``nf utils validate`` does.

A result describes a failure only as ``HTTP <status>`` or the exception class name.
Only ``ConfigurationError``, ``ConsoleAuthError`` and Digital Advisor token refresh
messages are shown, since all are secret-free by design.
Client classes are imported lazily and can be injected.
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
from pynetappfoundry.core.config_checks import (
    CheckResult,
    CheckSection,
    CheckStatus,
    spec_download_hint,
)
from pynetappfoundry.doctor import API_NAMES

logger = logging.getLogger(__name__)


@dataclass
class Factories:
    """Client factories, replaced in tests so no real client is built.

    Attributes:
        ontap: Called as ``factory(cluster=..., config=...)``.
        aiqum: Called as ``factory(name, config)``.
        dii: Called as ``factory(config, name)``, and as
            ``factory(config, name, read_write=True)`` for the read-write key row.
        console_api: Called as ``factory(config)`` or ``factory(config, scope=scope)``.
        console_agent: Called as ``factory(config, agent_id, token_provider=..., scope=...)``.
        digitaladvisor: Called as
            ``factory(config, token_provider=..., session=..., retry_config=...)``.
    """

    ontap: Callable[..., Any] | None = None
    aiqum: Callable[..., Any] | None = None
    dii: Callable[..., Any] | None = None
    console_api: Callable[..., Any] | None = None
    console_agent: Callable[..., Any] | None = None
    digitaladvisor: Callable[..., Any] | None = None


def _chain(exc: BaseException) -> list[BaseException]:
    """Return ``exc`` and its causes, so a wrapped error is still recognised."""
    seen: list[BaseException] = []
    current: BaseException | None = exc
    while current is not None and current not in seen:
        seen.append(current)
        current = current.__cause__ or current.__context__
    return seen


def _failure(
    exc: BaseException,
    *,
    api: str | None = None,
    credentials_hint: str | None = None,
    forbidden_warns: bool = False,
) -> tuple[str, str | None, CheckStatus]:
    """Describe a failed request without quoting the response or the exception text.

    Args:
        exc: The exception raised by the client.
        api: The OpenAPI API whose spec a ``FileNotFoundError`` means is missing.
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
        hint = (
            spec_download_hint(api)
            if api
            else "Run: nf config download-schema; see docs/getting-started/configuration.md."
        )
        return "spec file missing", hint, CheckStatus.SKIPPED
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
    api: str,
    credentials_hint: str | None = None,
    forbidden_warns: bool = False,
) -> CheckResult:
    """Build the result row of a failed request."""
    detail, hint, status = _failure(
        exc, api=api, credentials_hint=credentials_hint, forbidden_warns=forbidden_warns
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
                    api="ontap",
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
                    api="aiqum",
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
    authenticated but may lack the Assets read scope. A second row,
    ``live.dii.<name>.rw``, reports the optional read-write key with the same ``GET``.
    """
    tenants: list[str | None] = list(_in_scope(config, "cloudinsights", scope))
    if not tenants and scope is None and "general" in config.settings.get("diiapi", {}):
        tenants = [None]
    results: list[CheckResult] = []
    for tenant in tenants:
        shown = tenant or "general"
        subject = f"live.dii.{shown}"
        ro_exc: BaseException | None = None
        try:
            factory = client_factory
            if factory is None:
                from pynetappfoundry.clients.dii.api import DIIAPIClient

                factory = DIIAPIClient
            client = factory(config, tenant)
            client.call_endpoint("/assets/storages/count")
        except Exception as e:
            ro_exc = e
            hint = (
                "Store the token with: nf config set-credential --type cloudinsights "
                f"--name {tenant} --user token"
                if tenant
                else "Set the token in <config>/apis/dii/diiapi.toml."
            )
            results.append(
                _failed_row(
                    subject, shown, e, api="dii", credentials_hint=hint, forbidden_warns=True
                )
            )
        else:
            results.append(CheckResult(subject, CheckStatus.OK, f"{shown}: connected"))
        rw_row = _check_dii_rw(config, tenant, shown, client_factory, ro_exc)
        if rw_row is not None:
            results.append(rw_row)
    return results


_DII_SET_RW = "nf config set-credential --setting diiapi.api_rw_token"


def _check_dii_rw(
    config: Config,
    tenant: str | None,
    shown: str,
    client_factory: Callable[..., Any] | None,
    ro_exc: BaseException | None,
) -> CheckResult | None:
    """Report the optional DII read-write key with one ``GET``; ``None`` when there is no row.

    The row is skipped when the read-only attempt failed with anything but an
    HTTP error: that failure is already on the read-only row. An absent key is
    ``SKIPPED`` (it is optional), a 401 is an error, and a 403 is a warning,
    because a read-write key may be scoped to write categories only.
    """
    if ro_exc is not None and not isinstance(ro_exc, requests.HTTPError):
        return None
    try:
        settings = config.get_dii_api_settings(tenant) if tenant else config.get_dii_api_settings()
    except Exception:
        return None
    label = f"{shown} read-write key"
    subject = f"live.dii.{shown}.rw"
    if settings.api_rw_token is None:
        hint = (
            "Optional, needed only for DII writes. A tenant uses the diiapi.toml [general] "
            "api_rw_token only when it has no key of its own."
            if tenant
            else f"Optional, needed only for DII writes. Set it with: {_DII_SET_RW}"
        )
        return CheckResult(subject, CheckStatus.SKIPPED, f"{label}: not set", hint=hint)
    try:
        factory = client_factory
        if factory is None:
            from pynetappfoundry.clients.dii.api import DIIAPIClient

            factory = DIIAPIClient
        factory(config, tenant, read_write=True).call_endpoint("/assets/storages/count")
    except Exception as e:
        return _failed_row(
            subject,
            label,
            e,
            api="dii",
            credentials_hint=f"Set it with: {_DII_SET_RW}",
            forbidden_warns=True,
        )
    return CheckResult(subject, CheckStatus.OK, f"{label}: connected")


PROBE_QUERY = "query DoctorProbe { volumes(pageSize: 1) { cursor } }"
"""The one Digital Advisor document doctor sends: it needs a valid token, no filters, and
fetches no customer field."""

_DA_SET_REFRESH = "nf config set-credential --setting digitaladvisorapi.refresh_token"
_DA_SET_PAT = "nf config set-credential --setting digitaladvisorapi.personal_access_token"


class _RecordingProvider:
    """Wraps a token provider to learn whether and when it refreshed, and whether that failed."""

    def __init__(self, inner: Any, persisted: list[BaseException | None]) -> None:
        self._inner = inner
        self._persisted = persisted
        self.refreshable: bool = inner.refreshable
        self.calls = 0
        self.refreshed_on_call: list[int] = []
        self.refresh_failed = False
        self.first_refresh_call: int | None = None

    def __getattr__(self, name: str) -> Any:
        """Delegate other attributes (``credential``, ``fell_back``) to the wrapped provider."""
        if name.startswith("_"):
            raise AttributeError(name)
        return getattr(self._inner, name)

    def get_token(self) -> str:
        self.calls += 1
        before = len(self._persisted)
        try:
            token: str = self._inner.get_token()
        except Exception:
            self.refresh_failed = True
            raise
        if self.first_refresh_call is None and getattr(self._inner, "credential", None) == (
            "refresh_token"
        ):
            self.first_refresh_call = self.calls
        if len(self._persisted) > before:
            self.refreshed_on_call.append(self.calls)
        return token

    def invalidate(self, token: str) -> None:
        self._inner.invalidate(token)


def _digitaladvisor_failure(
    exc: BaseException, *, refresh_mode: bool, refresh_failed: bool, fell_back: bool = False
) -> tuple[str, str | None, CheckStatus]:
    """Describe a failed Digital Advisor probe without quoting a response message."""
    from pynetappfoundry.clients.digitaladvisor import (
        DigitalAdvisorAuthError,
        DigitalAdvisorError,
        DigitalAdvisorQueryError,
    )

    if isinstance(exc, DigitalAdvisorAuthError):
        if refresh_failed:
            return "token refresh failed", str(exc), CheckStatus.ERROR
        if fell_back:
            return (
                "token rejected (UNAUTHENTICATED)",
                "The personal access token was rejected, and so was the access token doctor "
                "got by refreshing. Log in to the Digital Advisor portal, then store a fresh "
                f"refresh token with: {_DA_SET_REFRESH}; also store a new personal access "
                f"token with: {_DA_SET_PAT}",
                CheckStatus.ERROR,
            )
        if refresh_mode:
            return (
                "token rejected (UNAUTHENTICATED)",
                "The access token was rejected, and so was the one doctor got by refreshing. "
                "Log in to the Digital Advisor portal, then store a fresh refresh token with: "
                f"{_DA_SET_REFRESH}",
                CheckStatus.ERROR,
            )
        return (
            "token rejected (UNAUTHENTICATED)",
            "The personal access token is probably expired (valid 1-90 days). Store a new "
            f"one with: {_DA_SET_PAT}",
            CheckStatus.ERROR,
        )
    if isinstance(exc, DigitalAdvisorQueryError):
        codes = ", ".join(exc.codes) or "no code"
        return (
            f"query rejected ({codes})",
            "Re-run with --debug for the traceback.",
            CheckStatus.ERROR,
        )
    if isinstance(exc, DigitalAdvisorError):
        for item in _chain(exc):
            if isinstance(item, (requests.ConnectionError, requests.Timeout)):
                return (
                    f"unreachable ({type(item).__name__})",
                    "Check the address, the network path and any proxy.",
                    CheckStatus.ERROR,
                )
        logger.debug("Digital Advisor live check failed", exc_info=exc)
        return (
            f"failed ({type(exc).__name__})",
            "Check the service state and re-run with --debug.",
            CheckStatus.ERROR,
        )
    return _failure(exc)


def check_digitaladvisor(
    config: Config,
    scope: str | None,
    *,
    client_factory: Callable[..., Any] | None = None,
    session: requests.Session | None = None,
) -> list[CheckResult]:
    """Send one read-only GraphQL query to Digital Advisor to prove the stored token.

    A personal access token is only probed. With both credentials the PAT is probed
    first; a rejected PAT falls back to the refresh pair under the rules below and the
    result is a WARNING with a PAT renewal hint (ADR-0035 §10 applies on that path).
    A refresh-token pair is probed with the
    stored access token; the client refreshes, and writes the rotated tokens back, only
    when that token is missing, expired or rejected (ADR-0035). Retries are off, so a
    failure costs one request. Without ``[general]`` settings, or with ``scope``, there
    are no rows.
    """
    if scope is not None or "general" not in config.settings.get("digitaladvisorapi", {}):
        return []
    subject = "live.digitaladvisor"
    name = "Digital Advisor"
    from pynetappfoundry.clients.digitaladvisor.api import (
        DigitalAdvisorAPIClient,
        build_token_provider,
        make_token_persister,
    )
    from pynetappfoundry.core.models import RetryConfig

    shared = session if session is not None else requests.Session()
    persisted: list[BaseException | None] = []
    recorder: _RecordingProvider | None = None
    refresh_mode = False
    try:
        settings = config.get_digital_advisor_api_settings()
        refresh_mode = settings.personal_access_token is None
        persist: Callable[[str, str], None] | None = None
        if settings.refresh_token is not None:
            real_persist = make_token_persister(config)

            def persist(access: str, refresh: str) -> None:
                persisted.append(None)
                try:
                    real_persist(access, refresh)
                except Exception as e:
                    persisted[-1] = e
                    raise

        provider = build_token_provider(settings, persist=persist, session=shared)
        recorder = _RecordingProvider(provider, persisted)
        factory = client_factory or DigitalAdvisorAPIClient
        client = factory(
            config,
            token_provider=recorder,
            session=shared,
            retry_config=RetryConfig(enabled=False),
        )
        client.query(PROBE_QUERY)
    except Exception as e:
        detail, hint, status = _digitaladvisor_failure(
            e,
            refresh_mode=refresh_mode,
            refresh_failed=recorder is not None and recorder.refresh_failed,
            fell_back=recorder is not None and bool(getattr(recorder, "fell_back", False)),
        )
        label = f"{name}: {detail}"
        errors = (label,) if status is CheckStatus.ERROR else ()
        return [CheckResult(subject, status, label, errors, hint)]

    assert recorder is not None
    fell_back = bool(getattr(recorder, "fell_back", False))
    if not refresh_mode and not fell_back:
        return [
            CheckResult(subject, CheckStatus.OK, f"{name}: token works (personal access token)")
        ]
    status = CheckStatus.WARNING if fell_back else CheckStatus.OK
    pat_hint = (
        "The personal access token was rejected; renew it before the refresh token's 90-day "
        f"login window ends: {_DA_SET_PAT}"
    )
    prefix = f"{name}: token works via the refresh_token fallback" if fell_back else ""
    if not persisted:
        label = (
            f"{prefix} (stored access token; no refresh)"
            if fell_back
            else f"{name}: token works (stored access token; no refresh)"
        )
        return [CheckResult(subject, status, label, hint=pat_hint if fell_back else None)]
    why = (
        "the access token was missing or expired"
        if recorder.refreshed_on_call == [recorder.first_refresh_call]
        else "the server rejected the stored access token"
    )
    failure = persisted[-1]
    if failure is not None:
        label = (
            f"{name}: token works, but the rotated tokens could not be written back "
            f"({type(failure).__name__})"
        )
        hint = (
            "The stored refresh token may now be stale. Log in to the portal and run: "
            f"{_DA_SET_REFRESH}"
        )
        if fell_back:
            hint += f". {pat_hint}"
        return [CheckResult(subject, CheckStatus.WARNING, label, hint=hint)]
    if fell_back:
        label = (
            f"{prefix}; {why}, so doctor refreshed it and wrote the rotated tokens to "
            "digitaladvisorapi.toml"
        )
        return [CheckResult(subject, status, label, hint=pat_hint)]
    return [
        CheckResult(
            subject,
            CheckStatus.OK,
            f"{name}: token works; {why}, so doctor refreshed it and wrote the rotated "
            "tokens to digitaladvisorapi.toml",
        )
    ]


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
                    api="console",
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
                results.append(
                    _failed_row(f"{subject}.{org.id}", f"{shown}/{org_name}", e, api="console")
                )
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
                    results.append(_failed_row(agent_subject, label, e, api="console"))
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
    if "digitaladvisor" in apis:
        sections.append(
            CheckSection(
                "Digital Advisor",
                tuple(check_digitaladvisor(config, scope, client_factory=f.digitaladvisor)),
            )
        )
    return [section for section in sections if section.results]
