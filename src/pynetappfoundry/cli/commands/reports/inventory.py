"""Generate inventory spreadsheet report.

Creates an Excel workbook with a NetApps sheet containing one row per
cluster with identity, network, cloud, node, and licensing columns.
Matches the layout of the Storage Devices inventory spreadsheet.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import click

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.options import filter_option
from pynetappfoundry.cli.utils import print_info, print_success
from pynetappfoundry.core.cluster_entry import ClusterEntry
from pynetappfoundry.core.config import Config
from pynetappfoundry.data.source import DataSource
from pynetappfoundry.utils.excel import ExcelWorkbook

if TYPE_CHECKING:
    from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata
    from pynetappfoundry.models.ontap.cluster.licensing.licenses import (
        OntapLicensePackageResponse,
    )
    from pynetappfoundry.models.ontap.cluster.model import OntapCluster
    from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse
    from pynetappfoundry.models.ontap.cluster.traits.model import ClusterTraits

# Maps cloud provider region codes to human-readable site names.
_REGION_TO_SITE: dict[str, str] = {
    # Azure
    "centralus": "Central",
    "eastus": "East 1",
    "eastus2": "East 2",
    "northcentralus": "North Central",
    "southcentralus": "South Central",
    "westus": "West 1",
    "westus2": "West 2",
    "westus3": "West 3",
    "westeurope": "West Europe",
    "northeurope": "North Europe",
    "uksouth": "UK South",
    "ukwest": "UK West",
    # AWS
    "us-east-1": "East 1",
    "us-east-2": "East 2",
    "us-west-1": "West 1",
    "us-west-2": "West 2",
    "eu-west-1": "Ireland",
    "eu-west-2": "London",
    "eu-central-1": "Frankfurt",
    "ap-southeast-1": "Singapore",
    "ap-southeast-2": "Sydney",
    "ap-northeast-1": "Tokyo",
}

_HEADERS = [
    "Name",
    "Division",
    "Application/ Business Unit",
    "Environment",
    "Contacts",
    "Notes",
    "Site",
    "Version",
    "Cloud Location",
    "Type",
    "License Expiration",
    "Subscription Name",
    "Resource Group Name",
    "Subscription ID",
    "Cluster Management IP",
    "System Manager",
    "BlueXP (NetApp Console) Connector IP",
    "BlueXP (NetApp Console) Name",
    "System ID",
    "Deployment Server",
    "New OCUM IP",
    "VM SKU Type",
    "Node-1 Name",
    "Node1 IP",
    "Node 1 Serial",
    "Node-2 Name",
    "Node2 IP",
    "Node 2 Serial",
    "Application Mapping",
    "Storage Account",
    "VM Names",
    "Load-Balancers",
    "Remark",
]

# 0-based columns whose text wraps (Contacts, Notes, and the trailing free-text columns).
_WRAP_COLS = frozenset({4, 5, 28, 29, 30, 31})

# Column widths (approximate, in character units)
_COL_WIDTHS = [
    20,
    12,
    22,
    12,
    40,
    35,
    14,
    14,
    14,
    12,
    20,
    35,
    55,
    38,
    20,
    25,
    40,
    28,
    38,
    18,
    30,
    22,
    25,
    16,
    25,
    25,
    16,
    25,
    35,
    35,
    35,
    55,
    20,
]


def _node_mgmt_ip(node: OntapNodeResponse) -> str:
    """Return the management IP for a node, falling back to management_interfaces list."""
    ip = node.management_interface.ip.address
    if not ip:
        for iface in node.management_interfaces:
            if iface.ip.address:
                return iface.ip.address
    return ip or ""


def _license_expiration(licenses: list[OntapLicensePackageResponse]) -> str:
    """Return earliest non-empty expiry date across all license packages, or blank."""
    earliest: str = ""
    for pkg in licenses:
        for lic in pkg.licenses:
            exp = lic.expiry_time
            if exp and (not earliest or exp < earliest):
                earliest = exp
    return earliest


def _short_version(ontap_version: str) -> str:
    """Extract short version like '9.16.1P3' from full ONTAP version string."""
    match = re.search(r"(\d+\.\d+\.\d+\w*)", ontap_version)
    return match.group(1) if match else ontap_version


def _cloud_type(traits: ClusterTraits) -> str:
    """Derive the cluster type string."""
    if not traits.is_cloud:
        return "OnTap Select"
    return "CVO HA" if traits.is_ha else "CVO"


class InventoryReport:
    """Builds the NetApp inventory Excel workbook."""

    def __init__(self, config: Config, clusters: dict[str, Any]) -> None:
        self.config = config
        self.clusters = clusters
        self.rows: list[list[Any]] = []

    def _collect_cloud_meta(
        self,
        entry: ClusterEntry,
        traits: ClusterTraits | None,
    ) -> list[CloudMetadata]:
        """Load cloud metadata from cache for CVO clusters only."""
        if not traits or not traits.is_cloud:
            return []
        ontap = entry.ontap
        if not ontap or not ontap.cloud:
            return []
        return list(ontap.cloud)

    def _build_row(
        self,
        name: str,
        entry: ClusterEntry,
        cluster_info: OntapCluster | None,
        nodes: list[OntapNodeResponse],
        licenses: list[OntapLicensePackageResponse],
        cloud_meta: list[CloudMetadata],
        traits: ClusterTraits | None = None,
    ) -> list[Any]:
        """Build a single data row for one cluster."""
        from pynetappfoundry.models.ontap.cluster.traits.model import ClusterTraits

        cloud_by_node: dict[str, CloudMetadata] = {cm.node: cm for cm in cloud_meta}
        first_cloud = cloud_meta[0] if cloud_meta else None

        div = entry.get("div", "")
        bu = entry.get("bu", "")
        env = entry.get("env", "")
        contacts = entry.get("contacts", "")
        cloud_cfg = entry.get("cloud", "")

        region_code = first_cloud.region if first_cloud else ""
        site = _REGION_TO_SITE.get(region_code.lower(), region_code)

        version = _short_version(cluster_info.version.full) if cluster_info else ""

        cloud_location = (
            first_cloud.provider if first_cloud else (cloud_cfg.title() if cloud_cfg else "")
        )

        ctype = _cloud_type(traits or ClusterTraits()) if cluster_info else ""

        lic_exp = _license_expiration(licenses)

        # Azure subscription info — try cloud metadata first, then TOML config
        sub_name = ""
        rg_name = ""
        rg_link = ""
        if first_cloud:
            rg_name = first_cloud.resource_group_name
            rg_link = first_cloud.resource_group_link
        if not sub_name:
            azure_cfg = entry.get("azure", {})
            if isinstance(azure_cfg, dict):
                sub_name = azure_cfg.get("location", "")
                if not rg_name:
                    rg_name = azure_cfg.get("resource_group", "")
        sub_id = first_cloud.account_id if first_cloud else ""
        rg_cell: Any = (rg_name, rg_link) if rg_name and rg_link else rg_name

        mgmt_ip = entry.get("ip", "")
        sys_mgr: Any = (f"https://{mgmt_ip}", f"https://{mgmt_ip}") if mgmt_ip else ""

        search_terms = {
            "div": div,
            "bu": bu,
            "app": entry.get("app", ""),
            "env": env,
        }
        connector = self.config.find_closest("connectors", search_terms)
        connector_ip: Any = ""
        connector_name = ""
        if connector:
            ip_raw = str(connector.get("ip", "")).strip()
            url = f"https://{ip_raw}/" if ip_raw else ""
            connector_ip = (url, url) if url else ""
            conn_azure = connector.get("azure", {})
            connector_name = conn_azure.get("vmname", "") if isinstance(conn_azure, dict) else ""

        system_id = cluster_info.uuid if cluster_info else ""

        aiqum = self.config.find_closest("aiqums", search_terms)
        aiqum_ip: Any = ""
        if aiqum:
            ip_raw = str(aiqum.get("ip", "")).strip()
            url = f"https://{ip_raw}" if ip_raw else ""
            aiqum_ip = (url, url) if url else ""

        vm_sku = first_cloud.instance_type if first_cloud else ""

        n1 = nodes[0] if len(nodes) > 0 else None
        n2 = nodes[1] if len(nodes) > 1 else None

        n1_name = n1.name if n1 else "NA"
        n1_ip = _node_mgmt_ip(n1) if n1 else "NA"
        n1_serial = n1.serial_number if n1 else "NA"
        n2_name = n2.name if n2 else "NA"
        n2_ip = _node_mgmt_ip(n2) if n2 else "NA"
        n2_serial = n2.serial_number if n2 else "N/A"

        vm_names_parts: list[str] = []
        for node in nodes:
            cm = cloud_by_node.get(node.name)
            if cm and cm.vm_name:
                vm_names_parts.append(cm.vm_name)
        vm_names = ", ".join(vm_names_parts)

        return [
            name,  # Name
            div,  # Division
            bu,  # Application/BU
            env,  # Environment
            contacts,  # Contacts
            "",  # Notes (blank for now)
            site,  # Site
            version,  # Version
            cloud_location,  # Cloud Location
            ctype,  # Type
            lic_exp,  # License Expiration
            sub_name,  # Subscription Name
            rg_cell,  # Resource Group Name (link)
            sub_id,  # Subscription ID
            mgmt_ip,  # Cluster Management IP
            sys_mgr,  # System Manager (link)
            connector_ip,  # BlueXP Connector IP (link)
            connector_name,  # BlueXP Connector Name
            system_id,  # System ID
            "NA",  # Deployment Server
            aiqum_ip,  # New OCUM IP (link)
            vm_sku,  # VM SKU Type
            n1_name,  # Node-1 Name
            n1_ip,  # Node1 IP
            n1_serial,  # Node 1 Serial
            n2_name,  # Node-2 Name
            n2_ip,  # Node2 IP
            n2_serial,  # Node 2 Serial
            "",  # Application Mapping (blank for now)
            "",  # Storage Account (blank for now)
            vm_names,  # VM Names
            "",  # Load-Balancers (blank for now)
            "",  # Remark
        ]

    def build(self) -> None:
        """Collect one data row per cluster."""
        from pynetappfoundry.models.ontap.cluster.licensing.licenses import (
            OntapLicensePackageResponse,
        )
        from pynetappfoundry.models.ontap.cluster.model import OntapCluster
        from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse
        from pynetappfoundry.models.ontap.cluster.traits.model import ClusterTraits

        ds = DataSource(self.config)
        self.rows = []
        for name, entry in self.clusters.items():
            cluster_info = ds.query(OntapCluster, cluster=name, source="auto").first()
            nodes = list(ds.query(OntapNodeResponse, cluster=name, source="auto"))
            licenses = list(ds.query(OntapLicensePackageResponse, cluster=name, source="auto"))
            traits = ds.query(ClusterTraits, cluster=name, source="auto").first()
            cloud_meta = self._collect_cloud_meta(entry, traits)
            self.rows.append(
                self._build_row(name, entry, cluster_info, nodes, licenses, cloud_meta, traits)
            )

    def save(self, path: str | Path) -> None:
        """Write the collected rows to an Excel file."""
        wb = ExcelWorkbook(path)
        sheet = wb.add_sheet("NetApps")
        ws = sheet.worksheet

        base = {"font_name": "Calibri", "valign": "top"}
        header_fmt = wb.add_format(
            {
                **base,
                "font_size": 11,
                "bold": True,
                "font_color": "#FFFFFF",
                "bg_color": "#1F4E79",
                "pattern": 1,
            }
        )
        body_fmt = wb.add_format({**base, "font_size": 10})
        body_wrap = wb.add_format({**base, "font_size": 10, "text_wrap": True})
        link_props = {**base, "font_size": 10, "font_color": "#0563C1", "underline": 1}
        link_fmt = wb.add_format(link_props)
        link_wrap = wb.add_format({**link_props, "text_wrap": True})

        sheet.append(_HEADERS, header_fmt)
        ws.set_row(0, 30)
        ws.freeze_panes(1, 0)
        ws.autofilter(0, 0, 0, len(_HEADERS) - 1)
        for col, width in enumerate(_COL_WIDTHS):
            ws.set_column(col, col, width)

        for row_idx, row_data in enumerate(self.rows, start=1):
            for col, value in enumerate(row_data):
                wrap = col in _WRAP_COLS
                if isinstance(value, tuple):
                    display, url = value
                    if url:
                        ws.write_url(
                            row_idx, col, url, link_wrap if wrap else link_fmt, string=display
                        )
                        continue
                    value = display
                ws.write(row_idx, col, value, body_wrap if wrap else body_fmt)
        wb.close()


@click.command()
@filter_option()
@with_config("Inventory report generation failed")
def inventory(
    config: Config,
    clusters: dict[str, Any],
) -> None:
    """Generate inventory spreadsheet of all NetApp clusters.

    Creates an Excel workbook (NetApps sheet) with one row per cluster
    containing identity, network, cloud, node, and licensing columns.
    Matches the Storage Devices inventory spreadsheet layout.
    """
    if not clusters:
        raise click.ClickException("No clusters found matching the filter criteria")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = config.output_dir / f"inventory_{timestamp}.xlsx"

    print_info(f"Building inventory report for {len(clusters)} cluster(s)...")

    report = InventoryReport(config, clusters)
    report.build()
    report.save(filename)

    print_success(f"Report saved to {filename}")
