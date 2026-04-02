"""Tests for reports space-usage command."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cli.commands.reports.space_usage import SpaceUsageReport
from pynetappfoundry.models.ontap.cluster.nodes.model import (
    OntapNodeResponse,
    OntapNodeResponseHa,
)
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume, OntapVolumeSpace


def _make_volume(
    *,
    name: str = "vol1",
    size: int = 1099511627776,  # 1 TiB in bytes
    space_used: int = 549755813888,  # 0.5 TiB
    state: str = "online",
    type_: str = "rw",
) -> OntapVolume:
    """Create a test volume model."""
    return OntapVolume(
        name=name,
        size=size,
        space=OntapVolumeSpace(used=space_used),
        state=state,
        type_=type_,
    )


def _make_node(*, name: str = "node1", ha_enabled: bool = False) -> OntapNodeResponse:
    """Create a test node model."""
    return OntapNodeResponse(name=name, ha=OntapNodeResponseHa(enabled=ha_enabled))


@pytest.fixture
def mock_config(tmp_path: Path) -> MagicMock:
    """Create a mock Config with output_dir."""
    config = MagicMock()
    config.output_dir = tmp_path
    config.get_user.return_value = ("admin", "password")
    config.get_ontap_api_settings.return_value = MagicMock(
        base_api_path="/api",
        timeout=30.0,
    )
    config.get_schema_location.return_value = Path("/tmp/schema")
    return config


@pytest.fixture
def sample_clusters() -> dict[str, dict[str, Any]]:
    """Sample cluster details."""
    return {
        "cluster1": {
            "name": "cluster1",
            "ip": "10.0.0.1",
            "div": "IT",
            "bu": "Platform",
            "app": "Storage",
            "env": "Prod",
            "subapp": "",
            "cloud": "Azure",
            "region": "eastus",
            "tags": ["prod", "azure"],
        }
    }


def _mock_queryset(nodes: list[Any], volumes: list[Any]) -> Any:
    """Create a side_effect for QuerySet that returns nodes then volumes."""
    call_count = 0

    def side_effect(*args: Any, **kwargs: Any) -> MagicMock:
        nonlocal call_count
        call_count += 1
        qs = MagicMock()
        if call_count % 2 == 1:  # odd calls are nodes
            qs.all.return_value = nodes
        else:  # even calls are volumes
            qs.filter.return_value.all.return_value = volumes
        return qs

    return side_effect


class TestGatherData:
    """Tests for SpaceUsageReport.gather_data()."""

    @patch("pynetappfoundry.cli.commands.reports.space_usage.QuerySet")
    @patch("pynetappfoundry.cli.commands.reports.space_usage.ONTAPAPIClient")
    def test_cvo_ha_detection(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_clusters: dict[str, dict[str, Any]],
    ) -> None:
        """Test CVO HA detected with 2+ nodes and HA enabled."""
        nodes = [_make_node(name="n1", ha_enabled=True), _make_node(name="n2", ha_enabled=True)]
        mock_qs_cls.side_effect = _mock_queryset(nodes, [_make_volume()])

        report = SpaceUsageReport(mock_config, sample_clusters)
        report.gather_data()

        assert len(report.volume_data) == 1
        assert report.volume_data[0][8] == "CVO HA"

    @patch("pynetappfoundry.cli.commands.reports.space_usage.QuerySet")
    @patch("pynetappfoundry.cli.commands.reports.space_usage.ONTAPAPIClient")
    def test_cvo_detection(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_clusters: dict[str, dict[str, Any]],
    ) -> None:
        """Test CVO detected with single node."""
        mock_qs_cls.side_effect = _mock_queryset([_make_node()], [_make_volume()])

        report = SpaceUsageReport(mock_config, sample_clusters)
        report.gather_data()

        assert len(report.volume_data) == 1
        assert report.volume_data[0][8] == "CVO"

    @patch("pynetappfoundry.cli.commands.reports.space_usage.QuerySet")
    @patch("pynetappfoundry.cli.commands.reports.space_usage.ONTAPAPIClient")
    def test_volume_fields(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_clusters: dict[str, dict[str, Any]],
    ) -> None:
        """Test volume data row has correct field values."""
        mock_qs_cls.side_effect = _mock_queryset(
            [_make_node()],
            [_make_volume(name="testvol", type_="rw", state="online")],
        )

        report = SpaceUsageReport(mock_config, sample_clusters)
        report.gather_data()

        row = report.volume_data[0]
        assert row[10] == "testvol"  # volume name
        assert row[9] == "RW"  # data_type (uppercased)
        assert row[11] == "online"  # state

    @patch("pynetappfoundry.cli.commands.reports.space_usage.QuerySet")
    @patch("pynetappfoundry.cli.commands.reports.space_usage.ONTAPAPIClient")
    def test_offline_volume_zero_used(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_clusters: dict[str, dict[str, Any]],
    ) -> None:
        """Test offline volume has used_tib=0."""
        mock_qs_cls.side_effect = _mock_queryset(
            [_make_node()],
            [_make_volume(state="offline", space_used=999999)],
        )

        report = SpaceUsageReport(mock_config, sample_clusters)
        report.gather_data()

        assert report.volume_data[0][14] == 0.0  # used_tib

    @patch("pynetappfoundry.cli.commands.reports.space_usage.print_error")
    @patch("pynetappfoundry.cli.commands.reports.space_usage.ONTAPAPIClient")
    def test_error_handling(
        self,
        mock_client_cls: MagicMock,
        mock_print_error: MagicMock,
        mock_config: MagicMock,
        sample_clusters: dict[str, dict[str, Any]],
    ) -> None:
        """Test connection failure is handled gracefully."""
        mock_client_cls.side_effect = Exception("Connection refused")

        report = SpaceUsageReport(mock_config, sample_clusters)
        report.gather_data()

        assert len(report.volume_data) == 0
        mock_print_error.assert_called_once()
