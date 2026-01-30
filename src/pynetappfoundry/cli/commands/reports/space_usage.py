"""Generate space usage reports.

Creates Excel workbooks with 3 worksheets:
- Totals: Summary by cloud x cluster type x data type
- Usage Breakdown: Hierarchical breakdown with SUMIFS formulas
- Volumes: Per-volume data with conditional formatting
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import click
import xlsxwriter

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import print_error, print_info, print_success
from pynetappfoundry.core.config import Config

# Constants for TiB conversion
BYTES_PER_TIB = 1024**4


@dataclass
class VolumeData:
    """Data for a single volume."""

    cluster_name: str
    volume_name: str
    div: str
    bu: str
    app: str
    env: str
    subapp: str
    cloud: str
    region: str
    cluster_type: str  # "CVO" or "CVO HA"
    data_type: str  # "RW" or "DP"
    size_tib: float
    used_tib: float
    available_tib: float
    percent_used: float


@dataclass
class SpaceUsageCollector:
    """Collects and organizes space usage data from clusters."""

    volumes: list[VolumeData] = field(default_factory=list)
    # Track unique combinations for Usage Breakdown
    hierarchy_keys: set[tuple[str, ...]] = field(default_factory=set)

    def add_volume(self, volume: VolumeData) -> None:
        """Add a volume and track its hierarchy."""
        self.volumes.append(volume)
        # Track hierarchy for Usage Breakdown
        self.hierarchy_keys.add(
            (
                volume.div,
                volume.bu,
                volume.app,
                volume.env,
                volume.subapp,
                volume.cloud,
                volume.region,
                volume.cluster_type,
                volume.data_type,
            )
        )


def bytes_to_tib(size_bytes: int) -> float:
    """Convert bytes to TiB with 7 decimal places precision."""
    return round(size_bytes / BYTES_PER_TIB, 7)


def detect_cluster_type(nodes: list[dict[str, Any]]) -> str:
    """Detect if cluster is HA or single-node CVO.

    Args:
        nodes: List of node dictionaries from Node.get_collection

    Returns:
        "CVO HA" if HA cluster, "CVO" otherwise
    """
    if len(nodes) > 1:
        # Check HA enabled on first node
        first_node = nodes[0]
        ha_info = first_node.get("ha", {})
        if ha_info.get("enabled", False):
            return "CVO HA"
    return "CVO"


class ExcelReportBuilder:
    """Builds Excel report with xlsxwriter."""

    def __init__(self, filename: str) -> None:
        """Initialize workbook and formats."""
        self.workbook = xlsxwriter.Workbook(filename)
        self._setup_formats()

    def _setup_formats(self) -> None:
        """Set up cell formats for the workbook."""
        # Header format
        self.header_format = self.workbook.add_format(
            {
                "bold": True,
                "bg_color": "#4472C4",
                "font_color": "white",
                "border": 1,
            }
        )

        # TiB number format (7 decimal places)
        self.tib_format = self.workbook.add_format({"num_format": "0.0000000"})

        # Percentage format
        self.percent_format = self.workbook.add_format({"num_format": "0.00%"})

        # Red background for high usage (>=90%)
        self.high_usage_format = self.workbook.add_format(
            {"bg_color": "#FF6B6B", "num_format": "0.00%"}
        )

        # Total row format
        self.total_format = self.workbook.add_format(
            {
                "bold": True,
                "top": 2,
                "num_format": "0.0000000",
            }
        )

    def create_totals_sheet(self, collector: SpaceUsageCollector) -> None:
        """Create the Totals worksheet with summary by cloud/type/datatype."""
        sheet = self.workbook.add_worksheet("Totals")

        # Headers
        headers = [
            "Cloud",
            "Cluster Type",
            "Data Type",
            "Total Size (TiB)",
            "Used (TiB)",
            "Available (TiB)",
            "Volume Count",
        ]
        for col, header in enumerate(headers):
            sheet.write(0, col, header, self.header_format)

        # Aggregate data by cloud/cluster_type/data_type
        aggregates: dict[tuple[str, str, str], dict[str, float]] = {}
        for vol in collector.volumes:
            key = (vol.cloud.upper(), vol.cluster_type, vol.data_type)
            if key not in aggregates:
                aggregates[key] = {
                    "size": 0.0,
                    "used": 0.0,
                    "available": 0.0,
                    "count": 0,
                }
            aggregates[key]["size"] += vol.size_tib
            aggregates[key]["used"] += vol.used_tib
            aggregates[key]["available"] += vol.available_tib
            aggregates[key]["count"] += 1

        # Write data rows
        row = 1
        for (cloud, cluster_type, data_type), values in sorted(aggregates.items()):
            sheet.write(row, 0, cloud)
            sheet.write(row, 1, cluster_type)
            sheet.write(row, 2, data_type)
            sheet.write(row, 3, values["size"], self.tib_format)
            sheet.write(row, 4, values["used"], self.tib_format)
            sheet.write(row, 5, values["available"], self.tib_format)
            sheet.write(row, 6, int(values["count"]))
            row += 1

        # Add table formatting
        if row > 1:
            sheet.add_table(
                0,
                0,
                row - 1,
                len(headers) - 1,
                {
                    "name": "TotalsTable",
                    "style": "Table Style Medium 9",
                    "columns": [{"header": h} for h in headers],
                },
            )

        # Auto-fit columns
        sheet.set_column(0, 2, 15)
        sheet.set_column(3, 5, 18)
        sheet.set_column(6, 6, 12)

    def create_usage_breakdown_sheet(self, collector: SpaceUsageCollector) -> None:
        """Create the Usage Breakdown worksheet with hierarchical view."""
        sheet = self.workbook.add_worksheet("Usage Breakdown")

        # Headers
        headers = [
            "Division",
            "BU",
            "App",
            "Environment",
            "SubApp",
            "Cloud",
            "Region",
            "Cluster Type",
            "Data Type",
            "Total Size (TiB)",
            "Used (TiB)",
            "Available (TiB)",
            "Volume Count",
        ]
        for col, header in enumerate(headers):
            sheet.write(0, col, header, self.header_format)

        # Build aggregated data by hierarchy
        # Key: (div, bu, app, env, subapp, cloud, region, cluster_type, data_type)
        aggregates: dict[tuple[str, str, str, str, str, str, str, str, str], dict[str, float]] = {}
        for vol in collector.volumes:
            key = (
                vol.div,
                vol.bu,
                vol.app,
                vol.env,
                vol.subapp,
                vol.cloud.upper(),
                vol.region,
                vol.cluster_type,
                vol.data_type,
            )
            if key not in aggregates:
                aggregates[key] = {
                    "size": 0.0,
                    "used": 0.0,
                    "available": 0.0,
                    "count": 0,
                }
            aggregates[key]["size"] += vol.size_tib
            aggregates[key]["used"] += vol.used_tib
            aggregates[key]["available"] += vol.available_tib
            aggregates[key]["count"] += 1

        # Write data rows, sorted by hierarchy
        row = 1
        for key, values in sorted(aggregates.items()):
            for col, val in enumerate(key):
                sheet.write(row, col, val)
            sheet.write(row, 9, values["size"], self.tib_format)
            sheet.write(row, 10, values["used"], self.tib_format)
            sheet.write(row, 11, values["available"], self.tib_format)
            sheet.write(row, 12, int(values["count"]))
            row += 1

        # Add table with totals row
        if row > 1:
            sheet.add_table(
                0,
                0,
                row - 1,
                len(headers) - 1,
                {
                    "name": "UsageBreakdownTable",
                    "style": "Table Style Medium 9",
                    "columns": [{"header": h} for h in headers],
                    "total_row": True,
                },
            )
            # SUMIFS-style totals are built into the table's total_row feature
            # Write SUBTOTAL formulas for numeric columns
            sheet.write_formula(row, 9, f"=SUBTOTAL(109,J2:J{row})", self.total_format)
            sheet.write_formula(row, 10, f"=SUBTOTAL(109,K2:K{row})", self.total_format)
            sheet.write_formula(row, 11, f"=SUBTOTAL(109,L2:L{row})", self.total_format)
            sheet.write_formula(row, 12, f"=SUBTOTAL(109,M2:M{row})", self.total_format)

        # Auto-fit columns
        sheet.set_column(0, 4, 12)  # Hierarchy columns
        sheet.set_column(5, 8, 12)  # Cloud/region/type columns
        sheet.set_column(9, 11, 18)  # TiB columns
        sheet.set_column(12, 12, 12)  # Count column

    def create_volumes_sheet(self, collector: SpaceUsageCollector) -> None:
        """Create the Volumes worksheet with per-volume data."""
        sheet = self.workbook.add_worksheet("Volumes")

        # Headers
        headers = [
            "Cluster",
            "Volume",
            "Division",
            "BU",
            "App",
            "Environment",
            "SubApp",
            "Cloud",
            "Region",
            "Cluster Type",
            "Data Type",
            "Size (TiB)",
            "Used (TiB)",
            "Available (TiB)",
            "% Used",
        ]
        for col, header in enumerate(headers):
            sheet.write(0, col, header, self.header_format)

        # Write volume data
        row = 1
        for vol in sorted(collector.volumes, key=lambda v: (v.cluster_name, v.volume_name)):
            sheet.write(row, 0, vol.cluster_name)
            sheet.write(row, 1, vol.volume_name)
            sheet.write(row, 2, vol.div)
            sheet.write(row, 3, vol.bu)
            sheet.write(row, 4, vol.app)
            sheet.write(row, 5, vol.env)
            sheet.write(row, 6, vol.subapp)
            sheet.write(row, 7, vol.cloud.upper())
            sheet.write(row, 8, vol.region)
            sheet.write(row, 9, vol.cluster_type)
            sheet.write(row, 10, vol.data_type)
            sheet.write(row, 11, vol.size_tib, self.tib_format)
            sheet.write(row, 12, vol.used_tib, self.tib_format)
            sheet.write(row, 13, vol.available_tib, self.tib_format)
            # Percent as decimal for Excel (0.9 = 90%)
            sheet.write(row, 14, vol.percent_used / 100, self.percent_format)
            row += 1

        # Add conditional formatting for high usage (>=90%)
        if row > 1:
            sheet.conditional_format(
                1,
                14,
                row - 1,
                14,
                {
                    "type": "cell",
                    "criteria": ">=",
                    "value": 0.9,
                    "format": self.high_usage_format,
                },
            )

            # Add table formatting
            sheet.add_table(
                0,
                0,
                row - 1,
                len(headers) - 1,
                {
                    "name": "VolumesTable",
                    "style": "Table Style Medium 9",
                    "columns": [{"header": h} for h in headers],
                },
            )

        # Auto-fit columns
        sheet.set_column(0, 1, 25)  # Cluster/volume
        sheet.set_column(2, 6, 12)  # Hierarchy
        sheet.set_column(7, 10, 12)  # Cloud/type
        sheet.set_column(11, 13, 18)  # TiB columns
        sheet.set_column(14, 14, 10)  # Percent

    def close(self) -> None:
        """Close the workbook."""
        self.workbook.close()


@click.command("space-usage")
@click.option(
    "--filter",
    "-f",
    "filter",
    help='JSON filter: \'{"bu":"Business", "env":"Prod"}\'',
)
@with_config("Space usage report failed")
def space_usage(
    config: Config,
    clusters: dict[str, dict[str, Any]],
) -> None:
    """Generate space usage reports.

    Creates an Excel workbook with 3 worksheets:
    - Totals: Summary by cloud provider, cluster type, and data type
    - Usage Breakdown: Hierarchical breakdown by div/BU/app/env/subapp
    - Volumes: Per-volume data with conditional formatting for high usage
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = config.output_dir / f"space_usage_{timestamp}.xlsx"

    collector = SpaceUsageCollector()

    for name, details in clusters.items():
        print_info(f"Gathering space data for {name}...")
        _gather_cluster_data(name, details, config, collector)

    if not collector.volumes:
        print_error("No volume data collected. Check cluster connectivity.")
        return

    # Build Excel report
    builder = ExcelReportBuilder(str(filename))
    builder.create_totals_sheet(collector)
    builder.create_usage_breakdown_sheet(collector)
    builder.create_volumes_sheet(collector)
    builder.close()

    print_success(f"Report saved to {filename}")
    print_info(f"Total volumes: {len(collector.volumes)}")


def _gather_cluster_data(
    name: str,
    details: dict[str, Any],
    config: Config,
    collector: SpaceUsageCollector,
) -> None:
    """Gather space usage data from a single cluster."""
    from netapp_ontap.host_connection import HostConnection
    from netapp_ontap.resources import Node, Volume

    user, password = config.get_user("clusters", name)

    try:
        with HostConnection(
            details["ip"],
            username=user,
            password=password,
            verify=False,
        ):
            # Detect cluster type (HA vs single node)
            nodes = list(Node.get_collection(fields="ha"))
            node_dicts = [n.to_dict() for n in nodes]
            cluster_type = detect_cluster_type(node_dicts)

            # Get metadata from cluster details
            div = details.get("div", "")
            bu = details.get("bu", "")
            app = details.get("app", "")
            env = details.get("env", "")
            subapp = details.get("subapp", "")
            cloud = details.get("cloud", "")
            region = details.get("region", "")

            # Get volumes
            for vol in Volume.get_collection(fields="name,type,space"):
                vol_dict = vol.to_dict()

                # Skip system volumes
                vol_name = vol_dict.get("name", "")
                if vol_name.startswith("vol0") or vol_name.endswith("_root"):
                    continue

                space = vol_dict.get("space", {})
                size_bytes = space.get("size", 0)
                used_bytes = space.get("used", 0)
                available_bytes = space.get("available", 0)

                # Skip volumes with no size
                if size_bytes == 0:
                    continue

                # Calculate percent used
                percent_used = (used_bytes / size_bytes * 100) if size_bytes > 0 else 0.0

                # Volume type is "rw" or "dp"
                data_type = vol_dict.get("type", "rw").upper()

                volume_data = VolumeData(
                    cluster_name=name,
                    volume_name=vol_name,
                    div=div,
                    bu=bu,
                    app=app,
                    env=env,
                    subapp=subapp,
                    cloud=cloud,
                    region=region,
                    cluster_type=cluster_type,
                    data_type=data_type,
                    size_tib=bytes_to_tib(size_bytes),
                    used_tib=bytes_to_tib(used_bytes),
                    available_tib=bytes_to_tib(available_bytes),
                    percent_used=percent_used,
                )
                collector.add_volume(volume_data)

    except Exception as e:
        print_error(f"Could not gather space data for {name}: {e}")
