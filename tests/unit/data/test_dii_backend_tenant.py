"""Tenant routing in DiiBackend._get_api_client (#1053)."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

from pynetappfoundry.data.dii_backend import DiiBackend

_PATCH = "pynetappfoundry.clients.dii.api.DIIAPIClient"


def _backend(data: Any) -> DiiBackend:
    config = MagicMock()
    config.data = data
    return DiiBackend(config)


class TestDiiTenantRouting:
    def test_named_tenant_passes_name(self) -> None:
        backend = _backend({"cloudinsights": {"t1": {"base_url": "https://a"}}})
        with patch(_PATCH) as client_cls:
            client = backend._get_api_client("t1")
        client_cls.assert_called_once_with(config=backend._config, name="t1")
        assert client is client_cls.return_value

    def test_unknown_name_uses_default_tenant(self) -> None:
        backend = _backend({"cloudinsights": {"t1": {}}})
        with patch(_PATCH) as client_cls:
            backend._get_api_client("tenant1")
        client_cls.assert_called_once_with(config=backend._config)

    def test_no_inventory_uses_default_tenant(self) -> None:
        backend = _backend({})
        with patch(_PATCH) as client_cls:
            backend._get_api_client("t1")
        client_cls.assert_called_once_with(config=backend._config)

    def test_non_dict_inventory_uses_default_tenant(self) -> None:
        backend = _backend({"cloudinsights": ["t1"]})
        with patch(_PATCH) as client_cls:
            backend._get_api_client("t1")
        client_cls.assert_called_once_with(config=backend._config)

    def test_two_tenants_get_distinct_clients(self) -> None:
        backend = _backend({"cloudinsights": {"t1": {}, "t2": {}}})
        with patch(_PATCH, side_effect=lambda **_: MagicMock()) as client_cls:
            first = backend._get_api_client("t1")
            second = backend._get_api_client("t2")
        assert first is not second
        names = [call.kwargs["name"] for call in client_cls.call_args_list]
        assert names == ["t1", "t2"]

    def test_same_tenant_is_cached(self) -> None:
        backend = _backend({"cloudinsights": {"t1": {}}})
        with patch(_PATCH) as client_cls:
            first = backend._get_api_client("t1")
            second = backend._get_api_client("t1")
        assert first is second
        assert client_cls.call_count == 1
