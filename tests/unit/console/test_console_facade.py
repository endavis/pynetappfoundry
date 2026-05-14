"""Tests for the org-scoped Console facade (ADR-0019 §1)."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.console import Console
from pynetappfoundry.core.models import ConsoleAPISettings
from pynetappfoundry.models.console.types import Organization


def _make_config(settings: ConsoleAPISettings, tmp_path: Any) -> MagicMock:
    config = MagicMock()
    config.get_console_api_settings.return_value = settings
    config.get_schema_location.return_value = tmp_path
    return config


@pytest.fixture
def settings_with_default_org() -> ConsoleAPISettings:
    return ConsoleAPISettings(
        user_token="user-jwt",
        base_url="https://api.bluexp.netapp.com",
        base_api_path="/",
        org_id="org-default",
    )


@pytest.fixture
def settings_without_org() -> ConsoleAPISettings:
    return ConsoleAPISettings(
        user_token="user-jwt",
        base_url="https://api.bluexp.netapp.com",
        base_api_path="/",
    )


class TestConsoleOrgBinding:
    """org_id resolution from constructor argument vs. settings default."""

    def test_constructor_arg_wins_over_settings_default(
        self,
        settings_with_default_org: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            MagicMock(),
        )
        console = Console(_make_config(settings_with_default_org, tmp_path), org_id="org-explicit")
        assert console.org_id == "org-explicit"

    def test_settings_default_used_when_no_arg(
        self,
        settings_with_default_org: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            MagicMock(),
        )
        console = Console(_make_config(settings_with_default_org, tmp_path))
        assert console.org_id == "org-default"

    def test_raises_when_no_org_id_anywhere(
        self,
        settings_without_org: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            MagicMock(),
        )
        with pytest.raises(ValueError, match="org_id"):
            Console(_make_config(settings_without_org, tmp_path))


class TestConsoleDelegatesToClient:
    """The facade thinly delegates to ConsoleAPIClient with its bound org_id."""

    def test_get_organization_delegates_with_bound_org_id(
        self,
        settings_with_default_org: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        wrapper_instance = MagicMock()
        wrapper_instance.call_endpoint.return_value = {
            "id": "org-default",
            "name": "Default Org",
            "resourceClass": "tenancyv4",
            "resourceType": "organization",
        }
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            MagicMock(return_value=wrapper_instance),
        )

        console = Console(_make_config(settings_with_default_org, tmp_path))
        org = console.get_organization()

        assert isinstance(org, Organization)
        assert org.id == "org-default"
        wrapper_instance.call_endpoint.assert_called_once_with(
            method="GET",
            path_template="/organizations/{organization_id}",
            path_params={"organization_id": "org-default"},
        )
