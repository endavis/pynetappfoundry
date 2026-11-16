"""Tests for the preferred-subscriptions operation and client method (#1034)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import SecretStr

from pynetappfoundry.clients.console.api import ConsoleAPIClient
from pynetappfoundry.clients.console.generated import ConsoleTenancyOps
from pynetappfoundry.core.models import ConsoleAPISettings
from pynetappfoundry.models.console_types import AccountSubscription

_TEMPLATE = "/license/account/{accountId}/subscriptions/preferred"


def _client(monkeypatch: pytest.MonkeyPatch, **settings: Any) -> tuple[ConsoleAPIClient, list[Any]]:
    wrappers: list[Any] = []

    def make(**kw: Any) -> MagicMock:
        wrapper = MagicMock(name=kw["name"])
        wrapper.call_endpoint.return_value = [{"subscriptionId": "sub-1", "endDate": 7}]
        wrappers.append(wrapper)
        return wrapper

    monkeypatch.setattr("pynetappfoundry.clients.console.api.APIWrapper", make)
    values: dict[str, Any] = {"base_url": "https://console.example.com", "base_api_path": "/"}
    values.update(settings)
    config = MagicMock()
    config.get_console_api_settings.return_value = ConsoleAPISettings(**values)
    config.get_schema_location.return_value = Path("unused")
    return ConsoleAPIClient(config), wrappers


def test_op_dispatches_untagged_with_query() -> None:
    dispatch = MagicMock(return_value=[])
    result = ConsoleTenancyOps(dispatch).list_preferred_subscriptions(
        "account-1", cloud_provider="aws"
    )
    assert result == []
    assert dispatch.call_args.args == (None,)
    assert dispatch.call_args.kwargs == {
        "method": "GET",
        "path_template": _TEMPLATE,
        "path_params": {"accountId": "account-1"},
        "query_params": {"cloudProvider": "aws"},
    }


def test_op_omits_query_without_cloud_provider() -> None:
    dispatch = MagicMock(return_value=[])
    ConsoleTenancyOps(dispatch).list_preferred_subscriptions("account-1")
    assert "query_params" not in dispatch.call_args.kwargs


def test_op_encodes_account_id() -> None:
    dispatch = MagicMock(return_value=[])
    ConsoleTenancyOps(dispatch).list_preferred_subscriptions("a/b")
    assert dispatch.call_args.kwargs["path_params"] == {"accountId": "a%2Fb"}


def test_op_non_list_response_raises() -> None:
    ops = ConsoleTenancyOps(MagicMock(return_value={"subscriptionId": "s"}))
    with pytest.raises(TypeError):
        ops.list_preferred_subscriptions("account-1")


def test_client_returns_account_subscriptions_with_user_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client, (wrapper,) = _client(monkeypatch, user_token=SecretStr("usr"))
    result = client.list_preferred_subscriptions("account-1")
    assert result == [AccountSubscription.model_validate({"subscriptionId": "sub-1", "endDate": 7})]
    assert wrapper.call_endpoint.called


def test_client_routes_to_service_wrapper_with_only_service_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client, (wrapper,) = _client(monkeypatch, service_token=SecretStr("svc"))
    result = client.list_preferred_subscriptions("account-1", cloud_provider="aws")
    assert [s.subscription_id for s in result] == ["sub-1"]
    assert wrapper.call_endpoint.called


def test_client_empty_array_gives_empty_list(monkeypatch: pytest.MonkeyPatch) -> None:
    client, (wrapper,) = _client(monkeypatch, user_token=SecretStr("usr"))
    wrapper.call_endpoint.return_value = []
    assert client.list_preferred_subscriptions("account-1") == []
