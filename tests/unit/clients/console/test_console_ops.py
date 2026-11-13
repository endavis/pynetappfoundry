"""Tests for the generated Console operation classes and their dispatch (#735)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import SecretStr

from pynetappfoundry.clients.console._ops_support import (
    csv_param,
    drop_none,
    expect_list,
    expect_object,
)
from pynetappfoundry.clients.console.agent import ConsoleAgentClient
from pynetappfoundry.clients.console.api import (
    ConsoleAPIClient,
    ConsoleServiceTokenMissingError,
    ConsoleUserTokenMissingError,
)
from pynetappfoundry.clients.console.generated import ConsoleAgentOps, ConsoleTenancyOps
from pynetappfoundry.core.models import ConsoleAPISettings
from pynetappfoundry.models.console.cvo import post_onprem_working_environments as post_models

CALL = {"method": "GET", "path_template": "/x"}


def _config(**settings: Any) -> MagicMock:
    values: dict[str, Any] = {"base_url": "https://console.example.com", "base_api_path": "/"}
    values.update(settings)
    config = MagicMock()
    config.get_console_api_settings.return_value = ConsoleAPISettings(**values)
    config.get_schema_location.return_value = Path("unused")
    return config


def _client(monkeypatch: pytest.MonkeyPatch, **settings: Any) -> tuple[ConsoleAPIClient, list[Any]]:
    wrappers: list[Any] = []

    def make(**kw: Any) -> MagicMock:
        wrapper = MagicMock(name=kw["name"])
        wrapper.call_endpoint.return_value = {"ok": True}
        wrappers.append(wrapper)
        return wrapper

    monkeypatch.setattr("pynetappfoundry.clients.console.api.APIWrapper", make)
    return ConsoleAPIClient(_config(**settings)), wrappers


def test_user_dispatch_with_only_service_token_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    client, _ = _client(monkeypatch, service_token=SecretStr("svc"))
    with pytest.raises(ConsoleUserTokenMissingError):
        client._dispatch("user", **CALL)


def test_service_dispatch_with_only_user_token_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    client, _ = _client(monkeypatch, user_token=SecretStr("usr"))
    with pytest.raises(ConsoleServiceTokenMissingError):
        client._dispatch("service", **CALL)


def test_user_and_service_dispatch_pick_their_wrapper(monkeypatch: pytest.MonkeyPatch) -> None:
    client, (user, service) = _client(
        monkeypatch, user_token=SecretStr("usr"), service_token=SecretStr("svc")
    )
    client._dispatch("service", **CALL)
    client._dispatch("user", **CALL)
    service.call_endpoint.assert_called_once_with(**CALL)
    user.call_endpoint.assert_called_once_with(**CALL)


def test_untagged_dispatch_prefers_user_then_service(monkeypatch: pytest.MonkeyPatch) -> None:
    client, (user, service) = _client(
        monkeypatch, user_token=SecretStr("usr"), service_token=SecretStr("svc")
    )
    client._dispatch(None, **CALL)
    user.call_endpoint.assert_called_once()
    service.call_endpoint.assert_not_called()

    only_service, (wrapper,) = _client(monkeypatch, service_token=SecretStr("svc"))
    only_service._dispatch(None, **CALL)
    wrapper.call_endpoint.assert_called_once()


def test_dispatch_uses_provider_token_per_call(monkeypatch: pytest.MonkeyPatch) -> None:
    client, (user,) = _client(monkeypatch, user_token=SecretStr("usr"))
    provider = MagicMock()
    provider.get_token.return_value = "tok"
    client._user_provider = provider

    client._dispatch("user", **CALL)

    user.call_endpoint.assert_called_once_with(
        **CALL, additional_headers={"Authorization": "Bearer tok"}
    )


def test_ops_namespace_on_both_clients(monkeypatch: pytest.MonkeyPatch) -> None:
    client, _ = _client(monkeypatch, user_token=SecretStr("usr"))
    assert isinstance(client.ops, ConsoleTenancyOps)

    monkeypatch.setattr("pynetappfoundry.clients.console.agent.APIWrapper", MagicMock())
    agent = ConsoleAgentClient(_config(user_token=SecretStr("usr")), "agent-placeholder")
    assert isinstance(agent.ops, ConsoleAgentOps)


def test_tenancy_op_encodes_path_param(monkeypatch: pytest.MonkeyPatch) -> None:
    client, (wrapper,) = _client(monkeypatch, user_token=SecretStr("usr"))
    client.ops.get_folder("a/b")
    assert wrapper.call_endpoint.call_args.kwargs["path_params"] == {"folder_id": "a%2Fb"}


def test_tenancy_op_sends_query_only_when_given(monkeypatch: pytest.MonkeyPatch) -> None:
    client, (wrapper,) = _client(monkeypatch, user_token=SecretStr("usr"))
    client.ops.list_organizations(limit="5", continue_="cursor-placeholder")
    assert wrapper.call_endpoint.call_args.kwargs["query_params"] == {
        "limit": "5",
        "continue": "cursor-placeholder",
    }


def test_agent_create_op_sends_dump_without_retry() -> None:
    dispatch = MagicMock(return_value={})
    ops = ConsoleAgentOps(dispatch)
    body = post_models.RequestBody(
        tenantId="ws-placeholder",
        clusterAddress="cluster.example.com",
        clusterUserName="admin-placeholder",
        clusterPassword="pw-placeholder",
        location="ON_PREM",
    )

    ops.create_onprem_working_environment(body)

    (token_type,), kwargs = dispatch.call_args
    assert token_type is None
    assert kwargs["method"] == "POST"
    assert kwargs["body"] == body.model_dump(exclude_none=True)
    assert kwargs["retry_config"].enabled is False


def test_agent_get_op_keeps_wrapper_retry() -> None:
    dispatch = MagicMock(return_value=[])
    ConsoleAgentOps(dispatch).list_onprem_working_environments(fields=["a", "b"])
    kwargs = dispatch.call_args.kwargs
    assert "retry_config" not in kwargs
    assert kwargs["query_params"] == {"fields": "a,b"}


def test_helpers() -> None:
    assert csv_param(None) is None
    assert csv_param("a,b") == "a,b"
    assert csv_param(["a", "b"]) == "a,b"
    assert drop_none({"a": 1, "b": None}) == {"a": 1}
    assert expect_object({"a": 1}, "op") == {"a": 1}
    assert expect_list([1], "op") == [1]


def test_expect_errors_name_operation_and_type_not_content() -> None:
    with pytest.raises(TypeError, match=r"op.*list") as exc_info:
        expect_object(["content-marker"], "op")
    assert "content-marker" not in str(exc_info.value)
    with pytest.raises(TypeError, match=r"op.*dict") as exc_info:
        expect_list({"k": "content-marker"}, "op")
    assert "content-marker" not in str(exc_info.value)


# --- typed tenancy results (#1027) ------------------------------------------


def test_tenancy_ops_return_generated_models() -> None:
    from pynetappfoundry.models.console.tenancyv4 import get_folders_, get_organizations

    ops = ConsoleTenancyOps(MagicMock(return_value={"id": "f-1", "name": "n"}))
    assert isinstance(ops.get_folder("f-1"), get_folders_.Response200Body)

    listing = {"items": [{"id": "o-1", "name": "n"}], "count": 1, "continue": "cursor-placeholder"}
    result = ConsoleTenancyOps(MagicMock(return_value=listing)).list_organizations()
    assert isinstance(result, get_organizations.Response200Body)
    assert result.continue_ == "cursor-placeholder"
    assert result.items is not None
    assert isinstance(result.items[0], get_organizations.Resource10GetResponseBody)


def test_tenancy_op_accepts_payload_without_type_or_version() -> None:
    result = ConsoleTenancyOps(MagicMock(return_value={"id": "o-1"})).get_organization("o-1")
    assert result.type is None
    assert result.version is None


def test_wrapper_still_requires_compact_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    from pydantic import ValidationError

    client, (wrapper,) = _client(monkeypatch, user_token=SecretStr("usr"))
    wrapper.call_endpoint.return_value = {"name": "n", "resourceClass": "ORG"}  # no id
    with pytest.raises(ValidationError):
        client.get_organization("o-1")


def test_wrapper_list_organizations_null_items(monkeypatch: pytest.MonkeyPatch) -> None:
    client, (wrapper,) = _client(monkeypatch, user_token=SecretStr("usr"))
    wrapper.call_endpoint.return_value = {"items": None}
    assert client.list_organizations() == []
