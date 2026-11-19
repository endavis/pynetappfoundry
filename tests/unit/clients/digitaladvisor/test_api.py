"""Tests for the Digital Advisor GraphQL client (#1051)."""

from __future__ import annotations

import logging
import time
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import requests

from pynetappfoundry.clients.digitaladvisor import api
from pynetappfoundry.clients.digitaladvisor.api import (
    INTROSPECTION_QUERY,
    SYSTEM_FIELDS,
    VOLUME_FIELDS,
    DigitalAdvisorAPIClient,
    RateLimiter,
    build_token_provider,
    ensure_read_only,
    fetch_schema,
)
from pynetappfoundry.clients.digitaladvisor.auth import (
    DigitalAdvisorAuthError,
    DigitalAdvisorError,
    DigitalAdvisorQueryError,
    FallbackTokenProvider,
    RefreshingTokenProvider,
    StaticTokenProvider,
)
from pynetappfoundry.core.models import DigitalAdvisorAPISettings, RetryConfig
from tests.unit.clients.digitaladvisor.helpers import (
    FakeClock,
    gql,
    make_jwt,
    response,
    session_with,
    unauthenticated,
)

PAT = "placeholder-pat"
RETRY = RetryConfig(max_attempts=3, initial_wait=2.0, max_wait=60.0)


def _settings(**kw: Any) -> DigitalAdvisorAPISettings:
    base: dict[str, Any] = {"personal_access_token": PAT}
    base.update(kw)
    return DigitalAdvisorAPISettings.model_validate(base)


def _client(
    session: MagicMock, clock: FakeClock | None = None, **kw: Any
) -> DigitalAdvisorAPIClient:
    clock = clock or FakeClock()
    kw.setdefault("settings", _settings())
    kw.setdefault("token_provider", StaticTokenProvider(PAT))
    return DigitalAdvisorAPIClient(
        session=session,
        retry_config=RETRY,
        rate_limiter=RateLimiter(1000, 1.0, clock, clock.sleep),
        sleep=clock.sleep,
        **kw,
    )


# -- ensure_read_only ---------------------------------------------------------


@pytest.mark.parametrize(
    "doc",
    [
        "query X { a }",
        "{ a }",
        "query X($a: [T!]!) { a(x: $a) { ...F } } fragment F on T { b }",
        INTROSPECTION_QUERY,
        "# mutation { x }\nquery { a }",
        "query { mutationType { name } }",
        'query { a(s: "mutation { x }") }',
    ],
)
def test_read_only_documents_pass(doc: str) -> None:
    ensure_read_only(doc)


@pytest.mark.parametrize(
    "doc",
    [
        "mutation { x }",
        "subscription { x }",
        "query { a } mutation M { x }",
        "",
        "# only a comment",
    ],
)
def test_other_documents_are_rejected(doc: str) -> None:
    with pytest.raises(DigitalAdvisorQueryError):
        ensure_read_only(doc)


def test_query_rejects_mutation_before_any_session_call() -> None:
    session = session_with()
    with pytest.raises(DigitalAdvisorQueryError):
        _client(session).query("mutation { x }")
    session.post.assert_not_called()


# -- query --------------------------------------------------------------------


def test_query_sends_bearer_and_body_and_returns_data() -> None:
    session = session_with(gql({"a": 1}))
    result = _client(session).query("query { a }", {"v": 1})

    assert result == {"a": 1}
    call = session.post.call_args
    assert call.args[0] == "https://gql.aiq.netapp.com/graphql"
    assert call.kwargs["json"] == {"query": "query { a }", "variables": {"v": 1}}
    assert call.kwargs["headers"] == {"Authorization": f"Bearer {PAT}"}
    assert call.kwargs["verify"] is True


def test_unknown_id_null_is_returned() -> None:
    assert _client(session_with(gql({"cluster": None}))).query("query { cluster }") == {
        "cluster": None
    }


def test_validation_failure_raises_query_error_with_code() -> None:
    body = {
        "errors": [{"message": "bad field", "extensions": {"code": "GRAPHQL_VALIDATION_FAILED"}}]
    }
    with pytest.raises(DigitalAdvisorQueryError) as exc:
        _client(session_with(response(400, body))).query("query { a }")
    assert exc.value.codes == ("GRAPHQL_VALIDATION_FAILED",)
    assert exc.value.messages == ("bad field",)
    session = session_with(response(400, body))
    with pytest.raises(DigitalAdvisorQueryError):
        _client(session).query("query { a }")
    assert session.post.call_count == 1  # 400 is not retried


def test_response_without_data_raises() -> None:
    with pytest.raises(DigitalAdvisorError, match="no data"):
        _client(session_with(response(200, {}))).query("query { a }")


def _refresh_client(
    session: MagicMock, clock: FakeClock
) -> tuple[DigitalAdvisorAPIClient, MagicMock]:
    token_session = session_with(
        response(
            200, {"access_token": make_jwt(clock.now + 3600), "refresh_token": "placeholder-r1"}
        ),
    )
    provider = RefreshingTokenProvider(
        refresh_token="placeholder-r0",
        access_token=make_jwt(clock.now + 3600, {"sub": "placeholder-old"}),
        token_url="https://token.example.test/t",
        timeout=5.0,
        session=token_session,
        clock=clock,
    )
    return _client(session, clock, token_provider=provider), token_session


def test_unauthenticated_in_refresh_mode_refreshes_once_and_retries() -> None:
    clock = FakeClock()
    session = session_with(unauthenticated(), gql({"a": 1}))
    client, token_session = _refresh_client(session, clock)

    assert client.query("query { a }") == {"a": 1}
    assert token_session.post.call_count == 1
    first, second = (c.kwargs["headers"]["Authorization"] for c in session.post.call_args_list)
    assert first != second


def test_two_unauthenticated_in_a_row_raise() -> None:
    clock = FakeClock()
    client, token_session = _refresh_client(
        session_with(unauthenticated(), unauthenticated()), clock
    )
    with pytest.raises(DigitalAdvisorAuthError):
        client.query("query { a }")
    assert token_session.post.call_count == 1


def test_unauthenticated_in_pat_mode_explains_validity_without_refresh() -> None:
    session = session_with(unauthenticated())
    with pytest.raises(DigitalAdvisorAuthError, match="1-90 days"):
        _client(session).query("query { a }")
    assert session.post.call_count == 1


def test_variables_headers_and_tokens_never_logged_or_raised(
    caplog: pytest.LogCaptureFixture,
) -> None:
    secret_var = "placeholder-secret-variable"
    body = {"errors": [{"message": "bad", "extensions": {"code": "X"}}]}
    session = session_with(response(503), response(400, body))
    with caplog.at_level(logging.DEBUG), pytest.raises(DigitalAdvisorQueryError) as exc:
        _client(session).query("query { a }", {"v": secret_var})
    for text in (caplog.text, str(exc.value)):
        assert secret_var not in text
        assert PAT not in text
        assert "Authorization" not in text


# -- retry --------------------------------------------------------------------


def test_429_then_200_sleeps_once() -> None:
    clock = FakeClock()
    session = session_with(response(429, {}), gql({"a": 1}))
    assert _client(session, clock).query("query { a }") == {"a": 1}
    assert clock.sleeps == [2.0]


def test_persistent_429_stops_after_max_attempts() -> None:
    clock = FakeClock()
    session = session_with(*[response(429, {}) for _ in range(3)])
    with pytest.raises(DigitalAdvisorError, match="429"):
        _client(session, clock).query("query { a }")
    assert session.post.call_count == 3
    assert clock.sleeps == [2.0, 4.0]


def test_retry_after_header_is_honoured() -> None:
    clock = FakeClock()
    session = session_with(response(429, {}, {"Retry-After": "7"}), gql({}))
    _client(session, clock).query("query { a }")
    assert clock.sleeps == [7.0]


@pytest.mark.parametrize("first", [response(503, {}), requests.ConnectionError("x")])
def test_503_and_connection_errors_are_retried(first: Any) -> None:
    clock = FakeClock()
    session = session_with(first, gql({"a": 1}))
    assert _client(session, clock).query("query { a }") == {"a": 1}
    assert len(clock.sleeps) == 1


def test_connection_error_surviving_retries_names_the_type() -> None:
    session = session_with(*[requests.ConnectionError("placeholder-pat") for _ in range(3)])
    with pytest.raises(DigitalAdvisorError) as exc:
        _client(session).query("query { a }")
    assert "ConnectionError" in str(exc.value)
    assert PAT not in str(exc.value)


# -- paginate -----------------------------------------------------------------


def _page(records: list[Any], cursor: str | None, total: int | None = None) -> Any:
    conn: dict[str, Any] = {"cursor": cursor, "items": records}
    if total is not None:
        conn["totalCount"] = total
    return gql({"things": conn})


def _sent_variables(session: MagicMock) -> list[dict[str, Any]]:
    return [c.kwargs["json"]["variables"] for c in session.post.call_args_list]


def test_paginate_follows_cursor_across_three_pages() -> None:
    session = session_with(_page([1], "c1"), _page([2], "c2"), _page([3], "c3"), _page([], "c4"))
    records = _client(session).paginate("query { things }", {"f": 1}, "things", "items", 7)

    assert records == [1, 2, 3]
    sent = _sent_variables(session)
    assert [v.get("after") for v in sent] == [None, "c1", "c2", "c3"]
    assert all(v["pageSize"] == 7 and v["f"] == 1 for v in sent)


def test_paginate_uses_settings_page_size() -> None:
    session = session_with(_page([], None))
    _client(session, settings=_settings(page_size=25)).paginate(
        "query { x }", None, "things", "items"
    )
    assert _sent_variables(session)[0]["pageSize"] == 25


def test_paginate_stops_at_total_count() -> None:
    session = session_with(_page([1, 2], "c1", total=3), _page([3], "c2", total=3))
    assert _client(session).paginate("query { x }", None, "things", "items") == [1, 2, 3]
    assert session.post.call_count == 2


def test_paginate_stops_on_empty_page_without_total() -> None:
    session = session_with(_page([1], "c1"), _page([], "c2"))
    assert _client(session).paginate("query { x }", None, "things", "items") == [1]


def test_paginate_stops_on_repeated_cursor() -> None:
    session = session_with(_page([1], "c1"), _page([2], "c1"))
    assert _client(session).paginate("query { x }", None, "things", "items") == [1, 2]
    assert session.post.call_count == 2


def test_paginate_logs_error_at_page_cap(caplog: pytest.LogCaptureFixture) -> None:
    session = session_with(*[_page([n], f"c{n}") for n in range(5)])
    with patch.object(api, "DIGITAL_ADVISOR_MAX_PAGES", 2), caplog.at_level(logging.ERROR):
        records = _client(session).paginate("query { x }", None, "things", "items")
    assert records == [0, 1]
    assert "stopped after 2 pages" in caplog.text


# -- typed methods -------------------------------------------------------------

SYSTEMS_ARGS: dict[str, Any] = {
    "product_types": ["PT"],
    "system_states": ["SS"],
    "include_all_states": True,
    "include_storage_grid_nodes": False,
}


def _doc(session: MagicMock) -> str:
    doc: str = session.post.call_args_list[0].kwargs["json"]["query"]
    return doc


def test_list_systems_default_document_and_variables() -> None:
    session = session_with(
        gql({"systems": {"cursor": "c", "totalCount": 1, "systems": [{"a": 1}]}})
    )
    assert _client(session).list_systems(**SYSTEMS_ARGS) == [{"a": 1}]

    doc = _doc(session)
    ensure_read_only(doc)
    assert f"systems {{ {' '.join(SYSTEM_FIELDS)} }}" in doc
    assert "$productTypes: [ProductType!]!" in doc
    assert "$systemStates: [SystemState!]!" in doc
    variables = _sent_variables(session)[0]
    assert variables["productTypes"] == ["PT"]
    assert variables["systemStates"] == ["SS"]
    assert variables["includeAllStates"] is True
    assert variables["includeStorageGridNodes"] is False


def test_list_systems_fields_override_and_filters() -> None:
    session = session_with(gql({"systems": {"cursor": None, "systems": []}}))
    _client(session).list_systems(
        **SYSTEMS_ARGS, fields=["systemId"], filters={"clusterIds": ["x"]}
    )
    doc = _doc(session)
    assert "systems { systemId }" in doc
    assert "$clusterIds: [String!]" in doc
    assert "clusterIds: $clusterIds" in doc
    assert _sent_variables(session)[0]["clusterIds"] == ["x"]


def test_list_systems_declares_enum_list_types_for_platform_and_mode() -> None:
    session = session_with(gql({"systems": {"cursor": None, "systems": []}}))
    _client(session).list_systems(
        **SYSTEMS_ARGS, filters={"platformType": ["ONTAP"], "operatingMode": ["CLUSTER_MODE"]}
    )
    doc = _doc(session)
    assert "$platformType: [SystemPlatformType!]" in doc
    assert "$operatingMode: [SystemOperatingMode!]" in doc
    assert "platformType: $platformType" in doc
    assert "operatingMode: $operatingMode" in doc
    variables = _sent_variables(session)[0]
    assert variables["platformType"] == ["ONTAP"]
    assert variables["operatingMode"] == ["CLUSTER_MODE"]


def test_list_systems_pages_through_the_systems_connection() -> None:
    session = session_with(
        gql({"systems": {"cursor": "c1", "systems": [{"a": 1}]}}),
        gql({"systems": {"cursor": "c2", "systems": []}}),
    )
    assert _client(session).list_systems(**SYSTEMS_ARGS) == [{"a": 1}]
    assert _sent_variables(session)[1]["after"] == "c1"


def test_list_volumes_default_document_and_paging() -> None:
    session = session_with(
        gql({"volumes": {"cursor": "c1", "totalCount": 2, "volumes": [{"id": 1}]}}),
        gql({"volumes": {"cursor": "c2", "totalCount": 2, "volumes": [{"id": 2}]}}),
    )
    assert _client(session).list_volumes(filters={"isRoot": False}) == [{"id": 1}, {"id": 2}]
    doc = _doc(session)
    ensure_read_only(doc)
    assert f"volumes {{ {' '.join(VOLUME_FIELDS)} }}" in doc
    assert "$isRoot: Boolean" in doc
    assert _sent_variables(session)[1]["after"] == "c1"


@pytest.mark.parametrize("bad", ["a b", "a{", "1a", "a}) { x", ""])
def test_bad_field_name_raises_before_any_request(bad: str) -> None:
    session = session_with()
    with pytest.raises(ValueError, match=r"field name|empty"):
        _client(session).list_volumes(fields=[bad])
    with pytest.raises(ValueError):
        _client(session).list_systems(**SYSTEMS_ARGS, fields=[bad])
    session.post.assert_not_called()


def test_unknown_filter_raises() -> None:
    with pytest.raises(ValueError, match="unknown filter"):
        _client(session_with()).list_volumes(filters={"bogus": 1})
    with pytest.raises(ValueError, match="unknown filter"):
        _client(session_with()).list_systems(**SYSTEMS_ARGS, filters={"vserverId": 1})


# -- construction and schema ----------------------------------------------------


def test_client_needs_config_or_settings() -> None:
    with pytest.raises(ValueError):
        DigitalAdvisorAPIClient()


def test_client_builds_the_provider_from_settings() -> None:
    pat = DigitalAdvisorAPIClient(settings=_settings(), session=session_with())
    assert pat._tokens.refreshable is False
    refresh = DigitalAdvisorAPIClient(
        settings=DigitalAdvisorAPISettings.model_validate({"refresh_token": "placeholder-r"}),
        session=session_with(),
    )
    assert refresh._tokens.refreshable is True
    assert "placeholder" not in repr(refresh)


def test_fetch_schema_sends_no_auth_and_returns_data() -> None:
    session = session_with(response(200, {"data": {"__schema": {"types": []}}}))
    assert fetch_schema("https://gql.example.test/graphql", 5.0, session) == {
        "__schema": {"types": []}
    }
    call = session.post.call_args
    assert "headers" not in call.kwargs
    assert call.kwargs["json"]["query"] == INTROSPECTION_QUERY


@pytest.mark.parametrize(
    "resp", [response(500, {}), response(200, None), response(200, {"data": {}})]
)
def test_fetch_schema_rejects_bad_responses(resp: requests.Response) -> None:
    with pytest.raises(DigitalAdvisorError):
        fetch_schema("https://gql.example.test/graphql", 5.0, session_with(resp))


# -- both credentials (#1120) -------------------------------------------------

REFRESH0 = "placeholder-r0"


def _both_client(
    session: MagicMock,
    token_session: MagicMock,
    *,
    access: str | None,
    persist: MagicMock | None = None,
) -> DigitalAdvisorAPIClient:
    values: dict[str, Any] = {"refresh_token": REFRESH0}
    if access is not None:
        values["access_token"] = access
    settings = _settings(**values)
    provider = build_token_provider(settings, persist=persist, session=token_session)
    return _client(session, settings=settings, token_provider=provider)


def _unexpired(label: str) -> str:
    return make_jwt(time.time() + 3600, {"sub": label})


def _new_tokens() -> requests.Response:
    return response(
        200, {"access_token": _unexpired("placeholder-new"), "refresh_token": "placeholder-r1"}
    )


def _bearers(session: MagicMock) -> list[str]:
    return [c.kwargs["headers"]["Authorization"] for c in session.post.call_args_list]


def test_both_working_pat_makes_no_token_request_or_write() -> None:
    session, token_session, persist = session_with(gql({"a": 1})), session_with(), MagicMock()
    client = _both_client(session, token_session, access=None, persist=persist)
    assert client.query("query { a }") == {"a": 1}
    assert session.post.call_count == 1
    token_session.post.assert_not_called()
    persist.assert_not_called()


def test_both_rejected_pat_falls_back_to_the_stored_access_token() -> None:
    access = _unexpired("placeholder-stored")
    session = session_with(unauthenticated(), gql({"a": 1}))
    token_session, persist = session_with(), MagicMock()
    client = _both_client(session, token_session, access=access, persist=persist)
    assert client.query("query { a }") == {"a": 1}
    assert _bearers(session) == [f"Bearer {PAT}", f"Bearer {access}"]
    token_session.post.assert_not_called()
    persist.assert_not_called()


def test_both_stored_access_token_rejected_refreshes_then_succeeds() -> None:
    access = _unexpired("placeholder-stored")
    session = session_with(unauthenticated(), unauthenticated(), gql({"a": 1}))
    token_session, persist = session_with(_new_tokens()), MagicMock()
    client = _both_client(session, token_session, access=access, persist=persist)
    assert client.query("query { a }") == {"a": 1}
    assert session.post.call_count == 3
    assert token_session.post.call_count == 1
    persist.assert_called_once()


def test_both_rejected_everywhere_names_both_renewal_steps(
    caplog: pytest.LogCaptureFixture,
) -> None:
    access = _unexpired("placeholder-stored")
    session = session_with(unauthenticated(), unauthenticated(), unauthenticated())
    token_session = session_with(_new_tokens())
    client = _both_client(session, token_session, access=access)
    with caplog.at_level(logging.DEBUG), pytest.raises(DigitalAdvisorAuthError) as exc:
        client.query("query { a }")
    assert session.post.call_count == 3
    message = str(exc.value)
    assert "digitaladvisorapi.refresh_token" in message
    assert "digitaladvisorapi.personal_access_token" in message
    for text in (message, caplog.text):
        for secret in (PAT, REFRESH0, access, "placeholder-r1"):
            assert secret not in text


def test_both_pat_rejected_and_refresh_endpoint_401_names_both_steps() -> None:
    session = session_with(unauthenticated())
    client = _both_client(session, session_with(response(401)), access=None)
    with pytest.raises(DigitalAdvisorAuthError) as exc:
        client.query("query { a }")
    assert "digitaladvisorapi.refresh_token" in str(exc.value)
    assert "digitaladvisorapi.personal_access_token" in str(exc.value)
    assert PAT not in str(exc.value)
    assert REFRESH0 not in str(exc.value)


def test_both_503_on_the_pat_request_does_not_switch() -> None:
    session = session_with(response(503), gql({"a": 1}))
    token_session = session_with()
    client = _both_client(session, token_session, access=None)
    assert client.query("query { a }") == {"a": 1}
    assert _bearers(session) == [f"Bearer {PAT}", f"Bearer {PAT}"]
    token_session.post.assert_not_called()


def test_build_token_provider_picks_the_provider_by_credentials() -> None:
    def build(**values: Any) -> object:
        settings = DigitalAdvisorAPISettings.model_validate(values)
        return build_token_provider(settings, persist=None, session=session_with())

    assert isinstance(build(personal_access_token=PAT), StaticTokenProvider)
    assert isinstance(build(refresh_token=REFRESH0), RefreshingTokenProvider)
    assert isinstance(
        build(personal_access_token=PAT, refresh_token=REFRESH0), FallbackTokenProvider
    )
