"""Tests for the Console UI link builders."""

from __future__ import annotations

import pytest

from pynetappfoundry.utils.console_links import (
    CONSOLE_UI_BASE_URL,
    CVO_PREFIX,
    ONPREM_PREFIX,
    build_console_agent_edit_link,
    build_console_agents_link,
    build_console_aggregates_link,
    build_console_svm_link,
    build_console_volumes_link,
    build_console_working_environment_link,
    is_cvo_public_id,
)

ONPREM_ID = "OnPremWorkingEnvironment-XXXXXXXX"
CVO_ID = "VsaWorkingEnvironment-XXXXXXXX"
BASE = "https://console.netapp.com"


class TestWorkingEnvironment:
    def test_default_base_url(self) -> None:
        assert CONSOLE_UI_BASE_URL == BASE

    def test_onprem(self) -> None:
        assert (
            build_console_working_environment_link(ONPREM_ID)
            == f"{BASE}/storage/on-prem/{ONPREM_ID}"
        )

    def test_cvo(self) -> None:
        assert (
            build_console_working_environment_link(CVO_ID)
            == f"{BASE}/storage/cloud-volumes-ontap/{CVO_ID}"
        )

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            build_console_working_environment_link("")

    def test_unknown_prefix_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown"):
            build_console_working_environment_link("SomethingElse-XXXXXXXX")

    @pytest.mark.parametrize("base", ["https://ui.example.test", "https://ui.example.test/"])
    def test_custom_base_url_no_double_slash(self, base: str) -> None:
        url = build_console_working_environment_link(CVO_ID, base_url=base)
        assert url == f"https://ui.example.test/storage/cloud-volumes-ontap/{CVO_ID}"

    def test_id_is_quoted(self) -> None:
        url = build_console_working_environment_link(f"{CVO_PREFIX}a/b c")
        assert url.endswith(f"{CVO_PREFIX}a%2Fb%20c")


class TestVolumesSvmAggregates:
    @pytest.mark.parametrize("public_id", [ONPREM_ID, CVO_ID])
    def test_volumes_link(self, public_id: str) -> None:
        url = build_console_volumes_link(public_id)
        assert url == f"{build_console_working_environment_link(public_id)}/volumes"

    def test_svm_link_is_working_environment_link(self) -> None:
        assert build_console_svm_link(CVO_ID) == build_console_working_environment_link(CVO_ID)

    def test_cvo_aggregates(self) -> None:
        assert build_console_aggregates_link(CVO_ID).endswith(f"/{CVO_ID}/aggregates")

    def test_onprem_aggregates_raises(self) -> None:
        with pytest.raises(ValueError, match="CVO"):
            build_console_aggregates_link(ONPREM_ID)

    def test_aggregates_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            build_console_aggregates_link("")

    def test_aggregates_unknown_prefix_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown"):
            build_console_aggregates_link("Other-XXXXXXXX")

    def test_volumes_custom_base(self) -> None:
        url = build_console_volumes_link(CVO_ID, base_url="https://ui.example.test/")
        assert url.startswith("https://ui.example.test/storage/")


class TestAgents:
    def test_agents_list(self) -> None:
        assert build_console_agents_link() == f"{BASE}/agents-mgmt"

    def test_agent_edit(self) -> None:
        assert build_console_agent_edit_link("agentXXXX") == f"{BASE}/agents-mgmt/agentXXXX/edit"

    def test_agent_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="agent_id"):
            build_console_agent_edit_link("")

    def test_agent_id_quoted(self) -> None:
        assert "a%2Fb" in build_console_agent_edit_link("a/b")

    def test_agents_custom_base_trailing_slash(self) -> None:
        assert (
            build_console_agents_link(base_url="https://ui.example.test/")
            == "https://ui.example.test/agents-mgmt"
        )


class TestIsCvo:
    def test_cvo_true(self) -> None:
        assert is_cvo_public_id(CVO_ID) is True

    def test_onprem_false(self) -> None:
        assert is_cvo_public_id(ONPREM_ID) is False
        assert ONPREM_ID.startswith(ONPREM_PREFIX)

    def test_empty_false(self) -> None:
        assert is_cvo_public_id("") is False
