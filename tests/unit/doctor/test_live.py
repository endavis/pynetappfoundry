"""Tests for the live checks of ``nf doctor`` (#1113). No test makes a network call."""

from __future__ import annotations

import shutil
import time
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import requests

from pynetappfoundry.clients.console.agent import ConsoleAgentClient
from pynetappfoundry.clients.console.api import ConsoleAPIClient
from pynetappfoundry.clients.console.auth import ConsoleAuthError
from pynetappfoundry.clients.digitaladvisor.api import ensure_read_only
from pynetappfoundry.clients.digitaladvisor.auth import TokenPersistError
from pynetappfoundry.clients.trust import HostIdentityChangedError
from pynetappfoundry.core.config import Config
from pynetappfoundry.core.config_checks import CheckResult, CheckStatus
from pynetappfoundry.doctor.live import (
    PROBE_QUERY,
    Factories,
    check_aiqum,
    check_console,
    check_digitaladvisor,
    check_dii,
    check_ontap,
    run_live_checks,
)
from pynetappfoundry.models.console_types import ConsoleAgentInfo
from tests.unit.clients.digitaladvisor.helpers import (
    gql,
    make_jwt,
    response,
    session_with,
    unauthenticated,
)

SENTINEL = "SENTINEL-response-body"
CIPHERTEXT = "SOPS[placeholder-ciphertext]"
DATA = '[settings]\ntype = "data"\n\n'
REPO = Path(__file__).resolve().parents[3]


@pytest.fixture(autouse=True)
def _isolate(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)


def _config(tmp_path: Path, files: dict[str, str]) -> Config:
    config_dir = tmp_path / "cfg"
    config_dir.mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        path = config_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return Config(config_dir=str(config_dir), script_name="test")


def _http_error(status: int) -> requests.HTTPError:
    response = requests.Response()
    response.status_code = status
    response._content = SENTINEL.encode()
    return requests.HTTPError(f"{status} Error: {SENTINEL}", response=response)


def _rendered(results: list[CheckResult]) -> str:
    return "\n".join(f"{r.label}|{r.errors}|{r.hint}" for r in results)


def _ontap_factory(*, response: Any = None, error: Exception | None = None) -> MagicMock:
    client = MagicMock()
    if error is not None:
        client.call_endpoint.side_effect = error
    else:
        client.call_endpoint.return_value = response
    return MagicMock(return_value=client)


CLUSTERS = {"c1": {"ip": "192.0.2.1"}}

# --- ONTAP ---


def test_ontap_ok() -> None:
    factory = _ontap_factory(response={"name": "c1"})

    results = check_ontap(MagicMock(), CLUSTERS, client_factory=factory)

    assert [(r.subject, r.status) for r in results] == [("live.ontap.c1", CheckStatus.OK)]
    factory.return_value.call_endpoint.assert_called_once_with("/cluster")


def test_ontap_name_mismatch_is_warning() -> None:
    results = check_ontap(
        MagicMock(), CLUSTERS, client_factory=_ontap_factory(response={"name": "other"})
    )

    assert results[0].status is CheckStatus.WARNING
    assert "does not match cluster name other" in results[0].label
    assert results[0].hint == "Rename the [clusters] key or check its ip."


def test_ontap_http_401_is_error_with_credential_hint() -> None:
    results = check_ontap(
        MagicMock(), CLUSTERS, client_factory=_ontap_factory(error=_http_error(401))
    )

    assert results[0].status is CheckStatus.ERROR
    assert results[0].label == "c1: HTTP 401"
    assert results[0].errors == ("c1: HTTP 401",)
    assert results[0].hint is not None
    assert "nf config set-credential --cluster c1" in results[0].hint
    assert SENTINEL not in _rendered(results)


def test_ontap_connection_error_is_error() -> None:
    results = check_ontap(
        MagicMock(),
        CLUSTERS,
        client_factory=_ontap_factory(error=requests.ConnectionError(SENTINEL)),
    )

    assert results[0].status is CheckStatus.ERROR
    assert results[0].label == "c1: unreachable (ConnectionError)"
    assert SENTINEL not in _rendered(results)


def test_ontap_identity_changed_uses_reset_hint() -> None:
    error = HostIdentityChangedError("192.0.2.1", Path("known"), "run the reset step")

    results = check_ontap(MagicMock(), CLUSTERS, client_factory=_ontap_factory(error=error))

    assert results[0].status is CheckStatus.ERROR
    assert results[0].label == "c1: identity changed"
    assert results[0].hint == "run the reset step"


def test_ontap_other_exception_shows_class_only() -> None:
    results = check_ontap(
        MagicMock(), CLUSTERS, client_factory=_ontap_factory(error=RuntimeError(SENTINEL))
    )

    assert results[0].label == "c1: failed (RuntimeError)"
    assert SENTINEL not in _rendered(results)


# --- AIQUM ---

AIQUM_FILES = {
    "inv.toml": DATA + '[aiqums.a1]\nip = "192.0.2.3"\n',
    "Org1/scope.toml": "",
    "Org1/inv.toml": DATA + '[aiqums.a2]\nip = "192.0.2.4"\n',
}


def test_aiqum_call_and_scope(tmp_path: Path) -> None:
    config = _config(tmp_path, AIQUM_FILES)
    client = MagicMock()
    factory = MagicMock(return_value=client)

    results = check_aiqum(config, None, client_factory=factory)

    assert [r.subject for r in results] == ["live.aiqum.a1", "live.aiqum.a2"]
    client.call_endpoint.assert_called_with(
        "/datacenter/cluster/clusters", query_params={"max_records": 1}
    )
    assert [r.subject for r in check_aiqum(config, "Org1", client_factory=factory)] == [
        "live.aiqum.a2"
    ]


def test_aiqum_401_has_set_credential_hint(tmp_path: Path) -> None:
    config = _config(tmp_path, AIQUM_FILES)
    client = MagicMock()
    client.call_endpoint.side_effect = _http_error(401)

    results = check_aiqum(config, "Org1", client_factory=MagicMock(return_value=client))

    assert results[0].status is CheckStatus.ERROR
    assert (
        results[0].hint
        == "Set them with: nf config set-credential --type aiqums --name a2 --user USER"
    )


def test_aiqum_missing_spec_is_skipped(tmp_path: Path) -> None:
    config = _config(tmp_path, AIQUM_FILES)

    results = check_aiqum(config, "Org1", client_factory=MagicMock(side_effect=FileNotFoundError))

    assert results[0].status is CheckStatus.SKIPPED
    assert results[0].label == "a2: spec file missing"


# --- DII ---

DII_FILES = {"inv.toml": DATA + '[cloudinsights.t1]\nbase_url = "https://t1.invalid"\n'}


def _dii_client(error: Exception | None = None) -> MagicMock:
    client = MagicMock()
    if error is not None:
        client.call_endpoint.side_effect = error
    return client


def test_dii_probe_and_statuses(tmp_path: Path) -> None:
    config = _config(tmp_path, DII_FILES)
    client = _dii_client()
    results = check_dii(config, None, client_factory=MagicMock(return_value=client))
    assert results[0].status is CheckStatus.OK
    client.call_endpoint.assert_called_once_with("/assets/storages/count")

    forbidden = check_dii(
        config, None, client_factory=MagicMock(return_value=_dii_client(_http_error(403)))
    )
    assert forbidden[0].status is CheckStatus.WARNING
    assert forbidden[0].errors == ()
    assert forbidden[0].label == "t1: HTTP 403"

    unauthorized = check_dii(
        config, None, client_factory=MagicMock(return_value=_dii_client(_http_error(401)))
    )
    assert unauthorized[0].status is CheckStatus.ERROR
    assert unauthorized[0].hint is not None
    assert "--type cloudinsights --name t1" in unauthorized[0].hint
    assert SENTINEL not in _rendered(forbidden + unauthorized)


def test_dii_general_only_probes_without_a_name(tmp_path: Path) -> None:
    config = _config(tmp_path, {"diiapi.toml": '[general]\napi_ro_token = "placeholder"\n'})
    factory = MagicMock(return_value=_dii_client())

    results = check_dii(config, None, client_factory=factory)

    factory.assert_called_once_with(config, None)
    assert results[0].subject == "live.dii.general"
    assert check_dii(config, "Org1", client_factory=factory) == []


# --- Console ---


def _console_config(tmp_path: Path) -> Config:
    return _config(
        tmp_path,
        {
            "consoleapi.toml": '[general]\nuser_token = "placeholder-token"\n',
            "Org1/scope.toml": "",
            "Org1/consoleapi.toml": '[general]\nuser_token = "placeholder-token"\n',
        },
    )


def _org(org_id: str = "org-1") -> MagicMock:
    org = MagicMock()
    org.id = org_id
    org.name = "Org Name"
    return org


def _agent(agent_id: str, status: str) -> ConsoleAgentInfo:
    return ConsoleAgentInfo(agentId=agent_id, name=f"name-{agent_id}", status=status)


def _api_client(agents: list[ConsoleAgentInfo]) -> MagicMock:
    client = MagicMock(spec=ConsoleAPIClient)
    client.list_organizations.return_value = [_org()]
    client.list_agents.return_value = agents
    client.user_token_provider = None
    client.service_token_provider = MagicMock()
    return client


def test_console_active_agent_ok_and_inactive_warns(tmp_path: Path) -> None:
    config = _config(tmp_path, {"consoleapi.toml": '[general]\nuser_token = "placeholder-token"\n'})
    api = _api_client([_agent("a-active", "active"), _agent("a-off", "inactive")])
    agent = MagicMock(spec=ConsoleAgentClient)
    agent_factory = MagicMock(return_value=agent)

    results = check_console(
        config,
        None,
        api_client_factory=MagicMock(return_value=api),
        agent_client_factory=agent_factory,
    )

    by_status = {r.subject: r.status for r in results}
    assert by_status["live.console.root"] is CheckStatus.OK
    assert by_status["live.console.root.org-1.a-active"] is CheckStatus.OK
    assert by_status["live.console.root.org-1.a-off"] is CheckStatus.WARNING
    assert "not probed" in next(r.label for r in results if r.subject.endswith("a-off"))
    agent_factory.assert_called_once()
    assert agent_factory.call_args.args[1] == "a-active"
    assert agent_factory.call_args.kwargs["token_provider"] is api.service_token_provider
    agent.about.assert_called_once_with()
    # Only the read-only calls were made.
    assert {c[0] for c in api.method_calls} <= {"list_organizations", "list_agents"}
    assert {c[0] for c in agent.method_calls} == {"about"}


def test_console_auth_error_at_construction_is_error(tmp_path: Path) -> None:
    config = _console_config(tmp_path)
    factory = MagicMock(side_effect=ConsoleAuthError("token endpoint answered HTTP 401"))

    results = check_console(config, None, api_client_factory=factory)

    assert len(results) == 2
    assert all(r.status is CheckStatus.ERROR for r in results)
    assert "token endpoint answered HTTP 401" in results[0].label


def test_console_scope_limits_accounts(tmp_path: Path) -> None:
    config = _console_config(tmp_path)
    factory = MagicMock(return_value=_api_client([]))

    results = check_console(config, "Org1", api_client_factory=factory)

    assert [r.subject for r in results] == ["live.console.Org1"]
    factory.assert_called_once_with(config, scope="Org1")


def test_console_without_account_is_skipped(tmp_path: Path) -> None:
    config = _config(tmp_path, {})

    results = check_console(config, None)

    assert [(r.status, r.label) for r in results] == [
        (CheckStatus.SKIPPED, "No Console account configured")
    ]


def test_console_agent_failure_is_error(tmp_path: Path) -> None:
    config = _console_config(tmp_path)
    agent = MagicMock(spec=ConsoleAgentClient)
    agent.about.side_effect = _http_error(502)

    results = check_console(
        config,
        "Org1",
        api_client_factory=MagicMock(return_value=_api_client([_agent("a1", "active")])),
        agent_client_factory=MagicMock(return_value=agent),
    )

    failed = next(r for r in results if r.subject.endswith("a1"))
    assert failed.status is CheckStatus.ERROR
    assert failed.label.endswith("HTTP 502")
    assert SENTINEL not in _rendered(results)


# --- Digital Advisor ---

PAT = "PLACEHOLDER-pat-token"
OLD_REFRESH = "PLACEHOLDER-old-refresh"
NEW_REFRESH = "PLACEHOLDER-new-refresh"
NEW_ACCESS = make_jwt(time.time() + 7200, {"tag": "new"})
OK_BODY = {"volumes": {"cursor": None}}
PERSIST = "pynetappfoundry.clients.digitaladvisor.api.make_token_persister"


def _da_config(tmp_path: Path, *, pat: bool = False, access: str | None = None) -> Config:
    lines = ["[general]"]
    if pat:
        lines.append(f'personal_access_token = "{PAT}"')
    else:
        lines.append(f'refresh_token = "{OLD_REFRESH}"')
        if access is not None:
            lines.append(f'access_token = "{access}"')
    return _config(tmp_path, {"digitaladvisorapi.toml": "\n".join(lines) + "\n"})


def _token_ok() -> requests.Response:
    return response(200, {"access_token": NEW_ACCESS, "refresh_token": NEW_REFRESH})


def _no_token_in(results: list[CheckResult], *tokens: str) -> None:
    text = _rendered(results)
    for token in (PAT, OLD_REFRESH, NEW_REFRESH, NEW_ACCESS, *tokens):
        assert token not in text


def _posted_urls(session: MagicMock) -> list[str]:
    return [c.args[0] for c in session.post.call_args_list]


def test_da_pat_probes_once_and_never_refreshes(tmp_path: Path) -> None:
    config = _da_config(tmp_path, pat=True)
    session = session_with(gql(OK_BODY))

    results = check_digitaladvisor(config, None, session=session)

    assert [(r.subject, r.status) for r in results] == [("live.digitaladvisor", CheckStatus.OK)]
    assert "personal access token" in results[0].label
    assert _posted_urls(session) == [config.get_digital_advisor_api_settings().graphql_url]
    _no_token_in(results)


def test_da_unexpired_access_token_is_sent_without_refresh_or_write(tmp_path: Path) -> None:
    access = make_jwt(time.time() + 3600, {"tag": "stored"})
    config = _da_config(tmp_path, access=access)
    session = session_with(gql(OK_BODY))

    with patch(PERSIST) as persister:
        results = check_digitaladvisor(config, None, session=session)

    assert results[0].status is CheckStatus.OK
    assert "no refresh" in results[0].label
    assert session.post.call_count == 1
    assert session.post.call_args.kwargs["headers"]["Authorization"].endswith(access)
    persister.return_value.assert_not_called()
    _no_token_in(results, access)


@pytest.mark.parametrize("access", [None, make_jwt(1.0)])
def test_da_missing_or_expired_token_refreshes_and_writes_back(
    tmp_path: Path, access: str | None
) -> None:
    config = _da_config(tmp_path, access=access)
    settings = config.get_digital_advisor_api_settings()
    session = session_with(_token_ok(), gql(OK_BODY))

    results = check_digitaladvisor(config, None, session=session)

    assert results[0].status is CheckStatus.OK
    assert "missing or expired" in results[0].label
    assert "digitaladvisorapi.toml" in results[0].label
    assert _posted_urls(session) == [settings.token_url, settings.graphql_url]
    written = (tmp_path / "cfg" / "digitaladvisorapi.toml").read_text()
    assert NEW_REFRESH in written
    assert NEW_ACCESS in written
    assert OLD_REFRESH not in written
    _no_token_in(results, *([access] if access else []))


def test_da_write_back_failure_is_a_warning(tmp_path: Path) -> None:
    config = _da_config(tmp_path)
    session = session_with(_token_ok(), gql(OK_BODY))

    with patch(PERSIST, return_value=MagicMock(side_effect=TokenPersistError("path SECRET"))):
        results = check_digitaladvisor(config, None, session=session)

    assert results[0].status is CheckStatus.WARNING
    assert "TokenPersistError" in results[0].label
    assert "set-credential --setting digitaladvisorapi.refresh_token" in (results[0].hint or "")
    assert "SECRET" not in _rendered(results)
    _no_token_in(results)


def test_da_refresh_rejected_is_an_error_with_the_client_hint(tmp_path: Path) -> None:
    config = _da_config(tmp_path)
    session = session_with(response(401, {"message": SENTINEL}))

    results = check_digitaladvisor(config, None, session=session)

    assert results[0].status is CheckStatus.ERROR
    assert results[0].label == "Digital Advisor: token refresh failed"
    assert "Log in to the Digital Advisor portal" in (results[0].hint or "")
    assert session.post.call_count == 1
    assert SENTINEL not in _rendered(results)
    _no_token_in(results)


def test_da_rejected_unexpired_token_is_refreshed_once_and_retried(tmp_path: Path) -> None:
    access = make_jwt(time.time() + 3600, {"tag": "stored"})
    config = _da_config(tmp_path, access=access)
    settings = config.get_digital_advisor_api_settings()
    session = session_with(unauthenticated(), _token_ok(), gql(OK_BODY))

    results = check_digitaladvisor(config, None, session=session)

    assert results[0].status is CheckStatus.OK
    assert "rejected the stored access token" in results[0].label
    assert _posted_urls(session) == [
        settings.graphql_url,
        settings.token_url,
        settings.graphql_url,
    ]
    assert NEW_REFRESH in (tmp_path / "cfg" / "digitaladvisorapi.toml").read_text()
    _no_token_in(results, access)


def test_da_still_rejected_after_refresh_is_an_error(tmp_path: Path) -> None:
    access = make_jwt(time.time() + 3600, {"tag": "stored"})
    config = _da_config(tmp_path, access=access)
    session = session_with(unauthenticated(), _token_ok(), unauthenticated())

    results = check_digitaladvisor(config, None, session=session)

    assert results[0].status is CheckStatus.ERROR
    assert results[0].label == "Digital Advisor: token rejected (UNAUTHENTICATED)"
    assert "fresh refresh token" in (results[0].hint or "")
    assert "personal access token" not in (results[0].hint or "")
    assert session.post.call_count == 3
    _no_token_in(results, access)


def test_da_pat_rejected_has_the_pat_hint(tmp_path: Path) -> None:
    config = _da_config(tmp_path, pat=True)
    session = session_with(unauthenticated())

    results = check_digitaladvisor(config, None, session=session)

    assert results[0].status is CheckStatus.ERROR
    assert results[0].label == "Digital Advisor: token rejected (UNAUTHENTICATED)"
    assert "digitaladvisorapi.personal_access_token" in (results[0].hint or "")
    assert session.post.call_count == 1
    _no_token_in(results)


@pytest.mark.parametrize(
    ("outcome", "expected"),
    [
        (response(503, {"errors": [{"message": SENTINEL}]}), "failed (DigitalAdvisorError)"),
        (requests.ConnectionError(SENTINEL), "unreachable (ConnectionError)"),
        (requests.Timeout(SENTINEL), "unreachable (Timeout)"),
    ],
)
def test_da_failures_make_one_attempt(
    tmp_path: Path, outcome: requests.Response | BaseException, expected: str
) -> None:
    config = _da_config(tmp_path, pat=True)
    session = session_with(outcome, outcome)

    results = check_digitaladvisor(config, None, session=session)

    assert results[0].status is CheckStatus.ERROR
    assert expected in results[0].label
    assert session.post.call_count == 1
    assert SENTINEL not in _rendered(results)
    _no_token_in(results)


def test_da_query_error_shows_the_code_not_the_message(tmp_path: Path) -> None:
    config = _da_config(tmp_path, pat=True)
    body = {"errors": [{"message": SENTINEL, "extensions": {"code": "GRAPHQL_VALIDATION_FAILED"}}]}
    session = session_with(response(200, body))

    results = check_digitaladvisor(config, None, session=session)

    assert results[0].label == "Digital Advisor: query rejected (GRAPHQL_VALIDATION_FAILED)"
    assert SENTINEL not in _rendered(results)


def test_da_unconfigured_or_scoped_has_no_rows(tmp_path: Path) -> None:
    session = session_with()
    assert check_digitaladvisor(_config(tmp_path, {"inv.toml": DATA}), None, session=session) == []
    configured = _da_config(tmp_path, pat=True)
    assert check_digitaladvisor(configured, "Org1", session=session) == []
    session.post.assert_not_called()


def test_da_invalid_settings_use_the_configuration_error_path(tmp_path: Path) -> None:
    config = _config(tmp_path, {"digitaladvisorapi.toml": "[general]\ntimeout = 5\n"})

    results = check_digitaladvisor(config, None, session=session_with())

    assert results[0].status is CheckStatus.ERROR
    assert results[0].subject == "live.digitaladvisor"


def test_da_sends_only_read_only_queries(tmp_path: Path) -> None:
    config = _da_config(tmp_path)
    settings = config.get_digital_advisor_api_settings()
    session = session_with(_token_ok(), gql(OK_BODY))

    check_digitaladvisor(config, None, session=session)

    assert {c[0] for c in session.method_calls} == {"post"}
    graphql = [c for c in session.post.call_args_list if c.args[0] == settings.graphql_url]
    assert len(graphql) == 1
    for call in graphql:
        document = call.kwargs["json"]
        ensure_read_only(document["query"])
        assert document["query"] == PROBE_QUERY
    assert _posted_urls(session).count(settings.token_url) == 1


def test_run_live_checks_puts_digitaladvisor_last(tmp_path: Path) -> None:
    config = _da_config(tmp_path, pat=True)
    client = MagicMock()
    client.query.return_value = OK_BODY
    factory = MagicMock(return_value=client)

    sections = run_live_checks(
        config,
        apis=("digitaladvisor",),
        scope=None,
        clusters={},
        factories=Factories(digitaladvisor=factory),
    )

    assert [s.title for s in sections] == ["Digital Advisor"]
    factory.assert_called_once()
    client.query.assert_called_once_with(PROBE_QUERY)
    unconfigured = run_live_checks(
        _config(tmp_path / "x", {"inv.toml": DATA}),
        apis=("digitaladvisor",),
        scope=None,
        clusters={},
    )
    assert unconfigured == []


# --- run_live_checks ---


def test_run_live_checks_sections_follow_apis(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": AIQUM_FILES["inv.toml"]})
    factories = Factories(aiqum=MagicMock(return_value=MagicMock()))

    sections = run_live_checks(
        config, apis=("aiqum", "ontap"), scope=None, clusters={}, factories=factories
    )

    assert [s.title for s in sections] == ["AIQUM"]


# --- GET at the wire ---


def test_every_request_is_a_get(tmp_path: Path) -> None:
    files = {
        "users.toml": (
            '[clusters]\nuser = "u"\nenc = "placeholder"\n\n'
            '[aiqums]\nuser = "u"\nenc = "placeholder"\n'
        ),
        "ontapapi.toml": '[general]\nbase_api_path = "/api"\n',
        "aiqumapi.toml": '[general]\nbase_api_path = "/api"\n',
        "diiapi.toml": '[general]\napi_ro_token = "placeholder"\nbase_url = "https://t.invalid"\n',
        "inv.toml": DATA + '[clusters.c1]\nip = "192.0.2.1"\n\n[aiqums.a1]\nip = "192.0.2.3"\n',
    }
    config = _config(tmp_path, files)
    for api in ("ontap", "aiqum", "dii"):
        target = tmp_path / "cfg" / "apis" / api
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO / "docs" / "example-config" / "apis" / api / "all.json", target)
    methods: list[str] = []

    def fake_execute(self: Any, method: str, url: str, **kwargs: Any) -> requests.Response:
        methods.append(method)
        response = requests.Response()
        response.status_code = 200
        response._content = b'{"name": "c1"}'
        return response

    with patch(
        "pynetappfoundry.clients.openapi.APIWrapper._execute_request_with_retry", fake_execute
    ):
        sections = run_live_checks(
            config,
            apis=("ontap", "aiqum", "dii"),
            scope=None,
            clusters=config.get_clusters({}),
        )

    assert methods
    assert set(methods) == {"GET"}
    assert [s.title for s in sections] == ["ONTAP", "AIQUM", "DII"]
    assert all(r.status is CheckStatus.OK for s in sections for r in s.results), sections
