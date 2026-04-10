"""Generate HTML reports with hierarchical tree view.

This module generates an interactive HTML report with:

- Hierarchical tree structure (Division > BU > App > Environment > Cloud > Region)
- Expand/collapse functionality using <details>/<summary> elements
- "Go to Active Cluster(s)" buttons for quick navigation
- Hyperlinks to cluster management interfaces, Azure portal, AIQUM, Connectors
- Rich cluster data including nodes, SVMs, interfaces, and CIFS/SMB configuration
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, cast

import click
from yattag import Doc, indent

import pynetappfoundry.cache.ontap.cluster.mapping
import pynetappfoundry.cache.ontap.cluster.nodes.mapping
import pynetappfoundry.cache.ontap.network.ip.interfaces.mapping
import pynetappfoundry.cache.ontap.protocols.cifs.services.mapping
import pynetappfoundry.cache.ontap.svm.svms.mapping  # noqa: F401
from pynetappfoundry.cache.field_mapping import parse_api_record
from pynetappfoundry.cache.ontap.cluster.mapping import CLUSTER_MAPPING
from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import print_debug, print_error, print_info, print_success
from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
from pynetappfoundry.core.models import ClusterConfig
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse
from pynetappfoundry.models.ontap.protocols.cifs.services.model import OntapCifsService
from pynetappfoundry.models.ontap.svm.svms.model import OntapSvm
from pynetappfoundry.query import QuerySet
from pynetappfoundry.utils.cloud import (
    build_azure_id,
    build_azure_portal_link,
    build_azure_vm_name,
    get_cloud_account_name,
)

if TYPE_CHECKING:
    from pynetappfoundry.core.cluster_entry import ClusterEntry
    from pynetappfoundry.core.config import Config
    from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata

# CSS for tree view styling
CSS_STYLES = """
.tree {
  --spacing: 1.5rem;
  --radius: 10px;
}

.tree li {
  display: block;
  position: relative;
  padding-left: calc(2 * var(--spacing) - var(--radius) - 2px);
  padding-top: 3px;
  padding-bottom: 3px;
}

.tree ul {
  margin-left: calc(var(--radius) - var(--spacing));
  padding-left: 0;
}

.tree ul li {
  border-left: 2px solid #ddd;
}

.tree ul li:last-child {
  border-color: transparent;
}

.tree ul li::before {
  content: '';
  display: block;
  position: absolute;
  top: calc(var(--spacing) / -2);
  left: -2px;
  width: calc(var(--spacing) + 2px);
  height: calc(var(--spacing) + 1px);
  border: solid #ddd;
  border-width: 0 0 2px 2px;
}

.tree summary {
  display: block;
  cursor: pointer;
  width: max-content;
  padding-right: 2em;
}

.tree summary::marker,
.tree summary::-webkit-details-marker {
  display: none;
}

.tree summary:focus {
  outline: none;
}

.tree summary:focus-visible {
  outline: 1px dotted #000;
}

.tree li::after,
.tree summary::before {
  content: '';
  display: block;
  position: absolute;
  top: calc(var(--spacing) / 2 - var(--radius));
  left: calc(var(--spacing) - var(--radius) - 1px);
  width: calc(2 * var(--radius));
  height: calc(2 * var(--radius));
  border-radius: 50%;
  background: #ddd;
}

.tree summary::before {
  z-index: 1;
  background: rgb(86, 48, 253) url('data:image/svg+xml;utf8,\
<svg xmlns="http://www.w3.org/2000/svg" width="40" height="20">\
<g fill="%23fff"><path d="m5 9h4v-4h2v4h4v2h-4v4h-2v-4h-4z"/>\
<path d="m25 9h10v2h-10z"/></g></svg>') 0 0;
}

.tree summary.prod::before {
  z-index: 1;
  background: green url('data:image/svg+xml;utf8,\
<svg xmlns="http://www.w3.org/2000/svg" width="40" height="20">\
<g fill="%23fff"><path d="m5 9h4v-4h2v4h4v2h-4v4h-2v-4h-4z"/>\
<path d="m25 9h10v2h-10z"/></g></svg>') 0 0;
}

.tree details[open] > summary::before {
  background-position: calc(-2 * var(--radius)) 0;
}

.custom-table td {
  padding: 2px;
  padding-right: 1em;
  padding-left: 1em;
  border: 1px solid black;
}

.custom-table th {
  padding: 2px;
  padding-right: 1em;
  padding-left: 1em;
  border: 2px solid black;
  background-color: rgb(17, 239, 247);
}

.noborder-table td {
  padding-top: 0;
  padding-bottom: 0;
  padding-right: .5em;
  padding-left: .5em;
  border: none;
  margin: 0;
}

.noborder-table tr {
  border: none;
}

table {
  border: none;
  border-collapse: collapse;
}

.error {
  background-color: red;
}

.active {
  background-color: green;
  color: white;
  padding-left: 2em;
  padding-right: 2em;
}

table.custom-table {
  border-collapse: collapse;
}

.env-button {
  border: none;
  color: black;
  text-align: center;
  text-decoration: underline;
  display: inline-block;
  cursor: pointer;
}
"""

# JavaScript for tree navigation
JS_SCRIPT = """
const envButtons = document.querySelectorAll('.env-button');
document.addEventListener('DOMContentLoaded', function() {
    openDetailsToButtons();
}, false);

envButtons.forEach(button => {
    button.addEventListener('click', function() {
        openActiveTrees(this.id);
    });
});

function openDetailsToButtons() {
    const activeElements = document.querySelectorAll('.button-stop');
    activeElements.forEach(element => {
        let open_flag = true;
        let parent = element.closest('details');
        parent = parent.parentElement.closest('details');
        while (parent) {
            parent.open = true;
            parent = parent.parentElement.closest('details');
        }
    });
}

function openActiveTrees(buttonid) {
    active_class = '.' + buttonid.replace('button', 'active');
    stop_class = 'button-stop';
    const activeElements = document.querySelectorAll(active_class);
    activeElements.forEach(element => {
        open_flag = !element.open;
        let parent = element.closest('details');

        while (parent) {
            if (!open_flag && parent.classList.contains(stop_class)) {
                parent.open = true;
                break;
            } else {
                parent.open = open_flag;
            }
            parent = parent.parentElement.closest('details');
        }
        if (parent) {
            parent.open = open_flag;
        }
    });
}
"""


class HTMLReportBuilder:
    """Main HTML report builder that manages hierarchy and generates output.

    This class builds a hierarchical tree view of NetApp clusters organized by:
    Division -> Business Unit -> App -> Environment -> SubApp -> Cloud -> Region -> Clusters

    Attributes:
        name: Name of the report.
        config: Configuration object with cluster data and settings.
        cluster_details: Dictionary of cluster configurations.
        clusterdata: Dictionary of ClusterData objects keyed by cluster name.
        divisions: Hierarchical structure of divisions containing the tree.
        counts: Statistics about clusters (HA pairs, single nodes, etc.).
        button_ids: List of element IDs that have "Go to Active" buttons.
    """

    def __init__(
        self,
        name: str,
        clusters: dict[str, dict[str, Any]],
        config: Config,
    ) -> None:
        """Initialize the HTML report builder.

        Args:
            name: Name for the report.
            clusters: Dictionary of cluster configurations.
            config: Configuration object with settings and utilities.
        """
        self.config = config
        self.name = name
        self.cluster_details = clusters
        self.clusterdata: dict[str, ClusterData] = {}
        self.divisions: dict[str, dict[str, Any]] = {}
        self.counts: dict[str, int] = {"ha": 0, "sn": 0, "aiqums": 0, "connectors": 0}
        self.button_ids: list[str] = []

        self.doc, self.tag, self.text = Doc().tagtext()
        self._build_hierarchy()

    def _build_hierarchy(self) -> None:
        """Build the hierarchical structure from cluster data."""
        self.counts["aiqums"] = self.config.count("aiqums", "ip")
        self.counts["connectors"] = self.config.count("connectors", "ip")

        for item in self.cluster_details:
            entry = self.cluster_details[item]
            self.clusterdata[item] = ClusterData(
                item,
                self,
                cluster_entry=entry,  # type: ignore[arg-type]
                **entry,
            )
            cluster = self.clusterdata[item]

            # Count HA vs single-node clusters
            if len(cluster.nodes) > 1:
                self.counts["ha"] += 1
            else:
                self.counts["sn"] += 1

            # Build hierarchy: div -> bu -> app -> env -> subapp -> cloud -> region
            div_name = getattr(cluster, "div", "")
            if div_name not in self.divisions:
                self.divisions[div_name] = {}
            div = self.divisions[div_name]

            bu_name = getattr(cluster, "bu", "")
            if bu_name not in div:
                div[bu_name] = {}
            bu = div[bu_name]

            app_name = getattr(cluster, "app", "")
            if app_name not in bu:
                bu[app_name] = {}
            app = bu[app_name]

            env_name = getattr(cluster, "env", "")
            if env_name not in app:
                app[env_name] = {}
            env = app[env_name]

            subapp_name = getattr(cluster, "subapp", "")
            if subapp_name not in env:
                env[subapp_name] = {}
            subapp_dict = env[subapp_name]

            cloud_name = getattr(cluster, "cloud", "")
            if cloud_name not in subapp_dict:
                subapp_dict[cloud_name] = {}
            cloud = subapp_dict[cloud_name]

            region_name = getattr(cluster, "region", "")
            if region_name not in cloud:
                cloud[region_name] = {}
            region = cloud[region_name]

            region[cluster.name] = cluster
            if cluster.ele_class:
                self.button_ids.append(cluster.ele_class)

    def format_azure_info(self, azure_info: dict[str, Any]) -> None:
        """Format Azure cloud information into table rows.

        Args:
            azure_info: Azure configuration dictionary with location, resource_group, etc.
        """
        self.format_table_row_text("Azure Subscription Name", azure_info["location"])
        azure_data = self.config.data.get("azure", {}).get(azure_info["location"], {})
        sub_id = azure_data.get("id", "")
        self.format_table_row_text("Azure Subscription ID", sub_id)

        resource_group_id = build_azure_id(sub_id, azure_info["resource_group"])
        resource_group_url = build_azure_portal_link(resource_group_id)
        self.format_table_row_link("Azure Resource Group", resource_group_id, resource_group_url)

        if "vmname" in azure_info:
            self.format_table_row_text("Azure VM Name", azure_info["vmname"])
            vmlink_id = build_azure_id(
                sub_id, azure_info["resource_group"], resource_name=azure_info["vmname"]
            )
            vmlink_url = build_azure_portal_link(vmlink_id)
            self.format_table_row_link("Azure VM", vmlink_id, vmlink_url)

    def format_table_row_text(
        self,
        *args: str,
        header: bool = False,
        error: bool = False,
    ) -> None:
        """Format a table row with text cells.

        Args:
            *args: Cell values to display.
            header: If True, use <th> tags instead of <td>.
            error: If True, apply error styling.
        """
        kwargs: dict[str, str] = {}
        if error:
            kwargs = {"klass": "error"}
        with self.tag("tr"):
            for item in args:
                with self.tag("th" if header else "td", **kwargs):
                    self.text(str(item))

    def format_table_row_link(self, col1: str, col2: str, link: str | None = None) -> None:
        """Format a table row with a link in the second column.

        Args:
            col1: Text for first column.
            col2: Text for link.
            link: URL for the link.
        """
        with self.tag("tr"):
            with self.tag("td"):
                self.text(col1)
            with self.tag("td"):
                if link:
                    with self.tag("a", ("href", link)):
                        self.text(col2)
                else:
                    self.text(col2)

    def format_generic_cloud_item(self, item_type: str, item: dict[str, Any]) -> None:
        """Format a generic cloud utility item (AIQUM, Connector, etc.).

        Args:
            item_type: Type of item (e.g., "AIQUM", "Connector").
            item: Item configuration with ip and optional azure info.
        """
        with self.tag("li"):
            with self.tag("details"):
                with self.tag("summary"):
                    with self.tag("a", ("href", f"https://{item['ip']}")):
                        self.text(item_type)
                with self.tag("ul"):
                    with self.tag("li"):
                        with self.tag("table", ("class", "custom-table")):
                            self.format_table_row_text("IP", item["ip"])
                            self.format_table_row_link(
                                "Application", "Link", f"https://{item['ip']}"
                            )
                            if "azure" in item:
                                self.format_azure_info(item["azure"])

    def format_ci(self, ci: dict[str, Any]) -> None:
        """Format Cloud Insights link.

        Args:
            ci: Cloud Insights configuration with url.
        """
        with self.tag("li"):
            with self.tag("a", ("href", ci["url"])):
                self.text("Cloud Insights")

    def format_utilities(self, search_terms: dict[str, str]) -> None:
        """Format utilities section (Cloud Insights, AIQUM, Connectors).

        Args:
            search_terms: Search terms to find the closest matching utilities.
        """
        ci = self.config.find_closest("cloudinsights", search_terms)
        if ci:
            self.format_ci(ci)
        aiqum = self.config.find_closest("aiqums", search_terms)
        if aiqum:
            self.format_generic_cloud_item("AIQUM", aiqum)
        connector = self.config.find_closest("connectors", search_terms)
        if connector:
            self.format_generic_cloud_item("Connector", connector)

    def generate_html(self) -> str:
        """Generate the complete HTML document.

        Returns:
            Formatted HTML string.
        """
        self.doc.asis("<!DOCTYPE html>")
        with self.tag("html", ("lang", "en")):
            with self.tag("head"):
                self.doc.asis('<meta charset="utf-8">')
                self.doc.asis(
                    '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
                )
                with self.tag("title"):
                    self.text("NetApp Cluster Report")
                with self.tag("base", ("target", "_blank"), ("rel", "noopener noreferrer")):
                    pass
                with self.tag("style"):
                    self.doc.asis(CSS_STYLES)
            with self.tag("body"):
                with self.tag("ul", ("class", "tree")):
                    self._format_divisions()
                with self.tag("script"):
                    self.doc.asis(JS_SCRIPT)

        result: str = indent(self.doc.getvalue())
        print_debug(f"Processed {self.counts['ha'] + self.counts['sn']} clusters")
        print_debug(f"   Single Node : {self.counts['sn']}")
        print_debug(f"   HA          : {self.counts['ha']}")
        return result

    def _format_divisions(self) -> None:
        """Format all divisions at the top level of the tree."""
        divisions = sorted(self.divisions.keys())
        for division in divisions:
            search_terms = {"div": division}
            with self.tag("li"):
                with self.tag("details", ("open", "")):
                    with self.tag("summary"):
                        self.text(division)
                    with self.tag("ul"):
                        self._format_business_units(
                            division, self.divisions[division], search_terms
                        )

    def _format_business_units(
        self,
        where: str,
        business_units: dict[str, Any],
        search_terms: dict[str, str],
    ) -> None:
        """Format business units within a division.

        Args:
            where: Path identifier for navigation.
            business_units: Dictionary of business units.
            search_terms: Current search terms for utilities lookup.
        """
        for business_unit in sorted(business_units.keys()):
            new_search_terms = search_terms.copy()
            new_search_terms["bu"] = business_unit
            new_where = f"{where}-{business_unit}"
            with self.tag("li"):
                with self.tag("details"):
                    with self.tag("summary"):
                        with self.tag("table", ("class", "noborder-table")):
                            with self.tag("tr"):
                                with self.tag("td"):
                                    self.text(business_unit)
                    with self.tag("ul"):
                        self._format_apps(
                            new_where, business_units[business_unit], new_search_terms
                        )

    def _format_buttons(self, where: str) -> None:
        """Format the "Go to Active Cluster(s)" button.

        Args:
            where: Element ID prefix for the button.
        """
        with self.tag("td"):
            with self.tag("button", ("class", "env-button"), ("id", f"{where}-active")):
                self.text("Go to Active Cluster(s)")

    def _format_apps(
        self,
        where: str,
        apps: dict[str, Any],
        search_terms: dict[str, str],
    ) -> None:
        """Format applications within a business unit.

        Args:
            where: Path identifier for navigation.
            apps: Dictionary of applications.
            search_terms: Current search terms for utilities lookup.
        """
        if len(apps.keys()) == 1 and "" in apps:
            new_where = f"{where}-"
            new_search_terms = search_terms.copy()
            new_search_terms["app"] = ""
            self._format_environments(new_where, apps[""], new_search_terms)
        else:
            for app in sorted(apps.keys()):
                new_where = f"{where}-{app}"
                det_class = "button-stop" if new_where in self.button_ids else ""
                new_search_terms = search_terms.copy()
                new_search_terms["app"] = app
                with self.tag("li"):
                    details_attrs: list[tuple[str, str]] = []
                    if det_class:
                        details_attrs.append(("class", det_class))
                    with self.tag("details", *details_attrs):
                        with self.tag("summary"):
                            with self.tag("table", ("class", "noborder-table")):
                                with self.tag("tr"):
                                    with self.tag("td"):
                                        self.text(app)
                                    if det_class:
                                        self._format_buttons(new_where)
                        with self.tag("ul"):
                            self._format_environments(new_where, apps[app], new_search_terms)

    def _format_environments(
        self,
        where: str,
        environments: dict[str, Any],
        search_terms: dict[str, str],
    ) -> None:
        """Format environments within an application.

        Args:
            where: Path identifier for navigation.
            environments: Dictionary of environments.
            search_terms: Current search terms for utilities lookup.
        """
        for environment in sorted(environments.keys()):
            new_where = f"{where}-{environment}".replace("/", "").replace("&", "")
            det_class = "button-stop" if new_where in self.button_ids else ""
            new_search_terms = search_terms.copy()
            new_search_terms["env"] = environment
            with self.tag("li"):
                details_attrs: list[tuple[str, str]] = []
                if det_class:
                    details_attrs.append(("class", det_class))
                with self.tag("details", *details_attrs):
                    with self.tag("summary"):
                        with self.tag("table", ("class", "noborder-table")):
                            with self.tag("tr"):
                                with self.tag("td"):
                                    self.text(environment)
                                if det_class:
                                    self._format_buttons(new_where)
                    with self.tag("ul"):
                        self._format_subapps(new_where, environments[environment], new_search_terms)

    def _format_subapps(
        self,
        where: str,
        subapps: dict[str, Any],
        search_terms: dict[str, str],
    ) -> None:
        """Format sub-applications within an environment.

        Args:
            where: Path identifier for navigation.
            subapps: Dictionary of sub-applications.
            search_terms: Current search terms for utilities lookup.
        """
        if len(subapps.keys()) == 1 and "" in subapps:
            new_search_terms = search_terms.copy()
            new_search_terms["subapp"] = ""
            self._format_clouds(subapps[""], new_search_terms)
        else:
            for subapp in sorted(subapps.keys()):
                new_where = f"{where}-{subapp}"
                det_class = "button-stop" if new_where in self.button_ids else ""
                new_search_terms = search_terms.copy()
                new_search_terms["subapp"] = subapp
                with self.tag("li"):
                    details_attrs: list[tuple[str, str]] = []
                    if det_class:
                        details_attrs.append(("class", det_class))
                    with self.tag("details", *details_attrs):
                        with self.tag("summary"):
                            with self.tag("table", ("class", "noborder-table")):
                                with self.tag("tr"):
                                    with self.tag("td"):
                                        self.text(subapp)
                                    if det_class:
                                        self._format_buttons(new_where)
                        with self.tag("ul"):
                            self._format_clouds(subapps[subapp], new_search_terms)

    def _format_clouds(
        self,
        clouds: dict[str, Any],
        search_terms: dict[str, str],
    ) -> None:
        """Format cloud providers within a sub-application.

        Args:
            clouds: Dictionary of cloud providers.
            search_terms: Current search terms for utilities lookup.
        """
        for cloud in sorted(clouds.keys()):
            new_search_terms = search_terms.copy()
            new_search_terms["cloud"] = cloud
            with self.tag("li"):
                with self.tag("details"):
                    with self.tag("summary"):
                        self.text(cloud.upper() if cloud else "On-Premises")
                    with self.tag("ul"):
                        self._format_regions(clouds[cloud], new_search_terms)

    def _format_regions(
        self,
        regions: dict[str, Any],
        search_terms: dict[str, str],
    ) -> None:
        """Format regions within a cloud provider.

        Args:
            regions: Dictionary of regions.
            search_terms: Current search terms for utilities lookup.
        """
        for region in sorted(regions.keys()):
            region_data = regions[region]
            new_search_terms = search_terms.copy()
            new_search_terms["region"] = region
            with self.tag("li"):
                with self.tag("details"):
                    with self.tag("summary"):
                        self.text(region if region else "Default")
                    with self.tag("ul"):
                        self.format_utilities(new_search_terms)
                        self._format_netapps(region_data)

    def _format_netapps(self, netapps: dict[str, ClusterData]) -> None:
        """Format NetApp clusters within a region.

        Args:
            netapps: Dictionary of ClusterData objects.
        """
        for netapp_name in netapps:
            netapps[netapp_name].format()


class ClusterData:
    """Data container for a single NetApp cluster.

    Gathers and formats cluster information including:
    - Cluster configuration (version, management IPs)
    - Nodes (serial numbers, management IPs)
    - SVMs/vservers (interfaces, DNS, CIFS/SMB)
    - Cloud provider information (Azure resource groups, VMs)

    Attributes:
        name: Cluster name.
        cluster_info: ClusterInfo from the /cluster endpoint.
        nodes: List of OntapNodeResponse objects.
        svms: List of OntapSvm objects.
        cifs_services: List of OntapCifsService objects.
        management_ip: Cluster management IP address.
        app_instance: Reference to the parent HTMLReportBuilder.
        ele_class: CSS class for active cluster highlighting.
    """

    def __init__(
        self,
        clustername: str,
        app_instance: HTMLReportBuilder,
        cluster_entry: ClusterEntry | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize cluster data and gather information from the cluster.

        Args:
            clustername: Name of the cluster.
            app_instance: Parent HTMLReportBuilder instance.
            cluster_entry: ClusterEntry wrapper with lazy cache accessors.
            **kwargs: Cluster configuration from TOML.
        """
        self.name = clustername
        self.cluster_type = ""
        self._cluster_entry = cluster_entry
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.cluster_info: ClusterInfo | None = None
        self.nodes: list[OntapNodeResponse] = []
        self.svms: list[OntapSvm] = []
        self.cifs_services: list[OntapCifsService] = []
        self.management_ip: str = ""
        self.cloud_metadata: list[CloudMetadata] = []
        self.cloud_metadata_by_node: dict[str, CloudMetadata] = {}
        self.cloud_provider: str = ""
        self.cloud_account_id: str = ""
        self.cloud_resource_group_name: str = ""
        self.cloud_region: str = ""
        self.cloud_resource_group_link: str = ""
        self.app_instance = app_instance

        # Build element class for active cluster navigation
        self.ele_class = ""
        if hasattr(self, "tags") and "active" in getattr(self, "tags", []):
            div = getattr(self, "div", "")
            bu = getattr(self, "bu", "")
            app = getattr(self, "app", "")
            env = getattr(self, "env", "")
            subapp = getattr(self, "subapp", "")
            ele_class = f"{div}-{bu}-{app}-{env}{f'-{subapp}' if subapp else ''}"
            self.ele_class = ele_class.replace("&", "").replace("/", "")

        self._gather_data()

    def _build_cloud_info(self) -> None:
        """Build cloud-specific information from cached metadata.

        Stores the full list of CloudMetadata and a lookup dict keyed by node name.
        Extracts cluster-level fields (provider, account, region, resource group)
        from the first entry. Per-node fields (instance_id, instance_type, etc.)
        are accessed via cloud_metadata_by_node in _format_netapp_node().
        """
        if not self._cluster_entry:
            return

        ontap = self._cluster_entry.ontap
        if not ontap or not ontap.cloud:
            return

        self.cloud_metadata = ontap.cloud
        self.cloud_metadata_by_node = {cm.node: cm for cm in ontap.cloud}

        first_cloud = ontap.cloud[0]
        self.cloud_provider = first_cloud.provider
        self.cloud_account_id = first_cloud.account_id
        self.cloud_resource_group_name = first_cloud.resource_group_name
        self.cloud_region = first_cloud.region
        self.cloud_resource_group_link = first_cloud.resource_group_link

    def _gather_data(self) -> None:
        """Gather data from the cluster via ONTAP REST API."""
        print_debug(f"Gathering data for {self.name}")
        self._build_cloud_info()

        ip = getattr(self, "ip", None)
        if not ip:
            print_error(f"No IP address for cluster {self.name}")
            return

        try:
            cluster_config = ClusterConfig(name=self.name, ip=ip)
            client = ONTAPAPIClient(cluster=cluster_config, config=self.app_instance.config)
        except Exception as e:
            print_error(f"Could not get credentials for {self.name}: {e}")
            return

        try:
            # ClusterInfo singleton — /cluster returns flat dict, not records
            response = client.call_endpoint(CLUSTER_MAPPING.build_collection_url())
            if response:
                self.cluster_info = cast(
                    ClusterInfo,
                    parse_api_record(CLUSTER_MAPPING, response, f"[{self.name}]"),
                )

            self.management_ip = ip
            config = self.app_instance.config
            self.nodes = QuerySet(OntapNodeResponse, client, config=config).all()
            self.svms = QuerySet(OntapSvm, client, config=config).all()
            self.cifs_services = QuerySet(OntapCifsService, client, config=config).all()
        except Exception as e:
            print_error(f"Could not gather data from {self.name}: {e}")

    def format(self) -> None:
        """Format the cluster data as HTML."""
        print_debug(f"Formatting cluster: {self.name}")
        is_active = hasattr(self, "tags") and "active" in getattr(self, "tags", [])

        tag = self.app_instance.tag
        text = self.app_instance.text

        with tag("li"):
            details_attrs: list[tuple[str, str]] = []
            if self.ele_class:
                details_attrs.append(("class", f"{self.ele_class}-active"))
            with tag("details", *details_attrs):
                with tag("summary"):
                    with tag("table"):
                        with tag("tr"):
                            with tag("td"):
                                text(self.name)
                            if is_active:
                                with tag("td", ("class", "active")):
                                    text("Active")
                with tag("ul"):
                    self._format_netapp_cloud_info()
                    self._format_netapp_cluster_info()
                    self._format_netapp_vservers_info()
                    self._format_netapp_nodes()

    def _format_netapp_cloud_info(self) -> None:
        """Format cluster-level cloud provider information.

        Shows provider, account/subscription ID, resource group, and region.
        Per-node fields (instance_id, instance_type, etc.) are rendered
        in _format_netapp_node() instead.
        """
        tag = self.app_instance.tag
        text = self.app_instance.text
        fmt = self.app_instance.format_table_row_text
        fmt_link = self.app_instance.format_table_row_link

        if not self.cloud_provider:
            return

        provider_lower = self.cloud_provider.lower()
        account_label = get_cloud_account_name(provider_lower).title() + " ID"

        with tag("li"):
            with tag("details"):
                with tag("summary"):
                    text(f"Cloud - {self.cloud_provider}")
                with tag("ul"):
                    with tag("li"):
                        with tag("table", ("class", "custom-table")):
                            fmt("Provider", self.cloud_provider)
                            if self.cloud_account_id:
                                fmt(account_label, self.cloud_account_id)
                            if self.cloud_resource_group_name:
                                if self.cloud_resource_group_link:
                                    fmt_link(
                                        "Resource Group",
                                        self.cloud_resource_group_name,
                                        self.cloud_resource_group_link,
                                    )
                                else:
                                    fmt("Resource Group", self.cloud_resource_group_name)
                            if self.cloud_region:
                                fmt("Region", self.cloud_region)

    def _format_netapp_cluster_info(self) -> None:
        """Format cluster-level information (version, management IPs, DNS, NTP)."""
        if self.cluster_info is None:
            return

        tag = self.app_instance.tag
        text = self.app_instance.text

        management_link = f"https://{self.management_ip}" if self.management_ip else ""

        with tag("li"):
            with tag("details"):
                with tag("summary"):
                    if management_link:
                        with tag("a", ("href", management_link)):
                            text("Cluster")
                    else:
                        text("Cluster")
                with tag("ul"):
                    with tag("li"):
                        with tag("table", ("class", "custom-table")):
                            version = self.cluster_info.ontap_version or "Unknown"
                            self.app_instance.format_table_row_text("Version", version)

                            if self.management_ip:
                                self.app_instance.format_table_row_text(
                                    "Cluster Management IP", self.management_ip
                                )
                            if management_link:
                                self.app_instance.format_table_row_link(
                                    "System Manager", "Link", management_link
                                )
                                self.app_instance.format_table_row_link(
                                    "SPI", "Link", f"{management_link}/spi"
                                )

                    # DNS information
                    with tag("li"):
                        with tag("details"):
                            with tag("summary"):
                                text("DNS")
                            with tag("ul"):
                                with tag("li"):
                                    with tag("table", ("class", "custom-table")):
                                        domains = self.cluster_info.dns_domains
                                        self.app_instance.format_table_row_text(
                                            "Domains", ", ".join(domains) if domains else "None"
                                        )
                                        for i, name_server in enumerate(
                                            self.cluster_info.name_servers
                                        ):
                                            self.app_instance.format_table_row_text(
                                                f"Server {i + 1}", name_server
                                            )

                    # NTP information
                    with tag("li"):
                        with tag("details"):
                            with tag("summary"):
                                text("NTP")
                            with tag("ul"):
                                with tag("li"):
                                    with tag("table", ("class", "custom-table")):
                                        ntp_servers = self.cluster_info.ntp_servers
                                        if ntp_servers:
                                            for i, name_server in enumerate(ntp_servers):
                                                self.app_instance.format_table_row_text(
                                                    f"Server {i + 1}", name_server
                                                )
                                        else:
                                            self.app_instance.format_table_row_text(
                                                "None", error=True
                                            )

    def _format_netapp_vservers_info(self) -> None:
        """Format SVM/vserver information."""
        if not self.svms:
            return

        tag = self.app_instance.tag
        text = self.app_instance.text

        for svm in sorted(self.svms, key=lambda s: s.name):
            print_debug(f"  SVM: {svm.name}")

            state_text = " - State: Stopped" if svm.state == "stopped" else ""

            with tag("li"):
                with tag("details"):
                    with tag("summary"):
                        text(f"vserver {svm.name}{state_text}")
                    with tag("ul"):
                        self._format_netapp_vserver_interfaces_info(svm)
                        self._format_netapp_vserver_dns_info(svm)
                        self._format_netapp_vserver_smb_server_info(svm)

    def _format_netapp_vserver_interfaces_info(self, svm: OntapSvm) -> None:
        """Format SVM network interface information.

        Args:
            svm: OntapSvm model instance.
        """
        if not svm.ip_interfaces:
            return

        tag = self.app_instance.tag
        text = self.app_instance.text

        with tag("li"):
            with tag("details"):
                with tag("summary"):
                    text("Interfaces")
                with tag("ul"):
                    with tag("li"):
                        with tag("table", ("class", "custom-table")):
                            self.app_instance.format_table_row_text(
                                "LIF name", "LIF IP", "Home Node", header=True
                            )
                            for iface in svm.ip_interfaces:
                                ip_addr = iface.ip.address or "Unknown"
                                netmask = iface.ip.netmask
                                home_node = iface.location.home_node.name or "Unknown"
                                self.app_instance.format_table_row_text(
                                    iface.name,
                                    f"{ip_addr}/{netmask}" if netmask else ip_addr,
                                    home_node,
                                )

    def _format_netapp_vserver_dns_info(self, svm: OntapSvm) -> None:
        """Format SVM DNS configuration.

        Args:
            svm: OntapSvm model instance.
        """
        tag = self.app_instance.tag
        text = self.app_instance.text

        with tag("li"):
            with tag("details"):
                with tag("summary"):
                    text("DNS")
                with tag("ul"):
                    with tag("li"):
                        with tag("table", ("class", "custom-table")):
                            domains = svm.dns.domains
                            self.app_instance.format_table_row_text(
                                "Domains", ", ".join(domains) if domains else "None"
                            )
                            for i, name_server in enumerate(svm.dns.servers):
                                self.app_instance.format_table_row_text(
                                    f"Server {i + 1}", name_server
                                )

    def _format_netapp_vserver_smb_server_info(self, svm: OntapSvm) -> None:
        """Format SVM CIFS/SMB server configuration.

        Args:
            svm: OntapSvm model instance.
        """
        if not svm.cifs.name:
            return

        # Find matching CIFS service by name
        cifs: OntapCifsService | None = None
        for cs in self.cifs_services:
            if cs.name == svm.cifs.name:
                cifs = cs
                break

        if cifs is None:
            return

        tag = self.app_instance.tag
        text = self.app_instance.text

        with tag("li"):
            with tag("details"):
                with tag("summary"):
                    text("SMB Server")
                with tag("ul"):
                    with tag("li"):
                        with tag("table", ("class", "custom-table")):
                            self.app_instance.format_table_row_text("Enabled", str(cifs.enabled))
                            self.app_instance.format_table_row_text("Name", cifs.name)
                            self.app_instance.format_table_row_text("Domain", cifs.ad_domain.fqdn)
                            self.app_instance.format_table_row_text(
                                "Organizational Unit", cifs.ad_domain.organizational_unit
                            )

                    # Security settings
                    with tag("li"):
                        with tag("details"):
                            with tag("summary"):
                                text("Security")
                            with tag("ul"):
                                with tag("li"):
                                    with tag("table", ("class", "custom-table")):
                                        items: list[tuple[str, str, Any]] = [
                                            (
                                                "Is Signing Required",
                                                "security.smb_signing",
                                                cifs.security.smb_signing,
                                            ),
                                            (
                                                "Use start_tls for AD LDAP connection",
                                                "security.use_start_tls",
                                                cifs.security.use_start_tls,
                                            ),
                                            (
                                                "LM Compatibility Level",
                                                "security.lm_compatibility_level",
                                                cifs.security.lm_compatibility_level,
                                            ),
                                            (
                                                "Is SMB Encryption Required",
                                                "security.smb_encryption",
                                                cifs.security.smb_encryption,
                                            ),
                                            (
                                                "Client Session Security",
                                                "security.session_security",
                                                cifs.security.session_security,
                                            ),
                                            (
                                                "LDAP Referral Enabled For AD LDAP connections",
                                                "security.ldap_referral_enabled",
                                                cifs.security.ldap_referral_enabled,
                                            ),
                                            (
                                                "Use LDAPS for AD LDAP connection",
                                                "security.use_ldaps",
                                                cifs.security.use_ldaps,
                                            ),
                                            (
                                                "Encryption is required for DC Connections",
                                                "security.encrypt_dc_connection",
                                                cifs.security.encrypt_dc_connection,
                                            ),
                                            (
                                                "AES session key enabled for NetLogon channel",
                                                "security.aes_netlogon_enabled",
                                                cifs.security.aes_netlogon_enabled,
                                            ),
                                            (
                                                "Try Channel Binding For AD LDAP Connections",
                                                "security.try_ldap_channel_binding",
                                                cifs.security.try_ldap_channel_binding,
                                            ),
                                            (
                                                "Encryption Types Advertised to Kerberos",
                                                "security.advertised_kdc_encryptions",
                                                cifs.security.advertised_kdc_encryptions,
                                            ),
                                        ]
                                        for header, _attr, value in items:
                                            if isinstance(value, list):
                                                self.app_instance.format_table_row_text(
                                                    header, ", ".join(str(v) for v in value)
                                                )
                                            else:
                                                self.app_instance.format_table_row_text(
                                                    header, str(value)
                                                )

    def _format_netapp_nodes(self) -> None:
        """Format cluster node information."""
        if not self.nodes:
            return

        for node in sorted(self.nodes, key=lambda n: n.name):
            self._format_netapp_node(node)

    def _format_netapp_node(self, node: OntapNodeResponse) -> None:
        """Format a single node's information.

        Args:
            node: OntapNodeResponse model instance.
        """
        tag = self.app_instance.tag
        text = self.app_instance.text
        fmt = self.app_instance.format_table_row_text
        fmt_link = self.app_instance.format_table_row_link

        mgmt_ip = node.management_interface.ip.address
        management_link = f"https://{mgmt_ip}" if mgmt_ip else ""

        with tag("li"):
            with tag("details"):
                with tag("summary"):
                    if management_link:
                        with tag("a", ("href", management_link)):
                            text(node.name or "Unknown")
                    else:
                        text(node.name or "Unknown")
                with tag("ul"):
                    with tag("li"):
                        with tag("table", ("class", "custom-table")):
                            if mgmt_ip:
                                fmt("Node Management IP", mgmt_ip)
                            serial = node.serial_number or "Unknown"
                            fmt("Serial Number", serial)
                            if management_link:
                                fmt_link("System Manager", "Link", management_link)
                                fmt_link("SPI", "Link", f"{management_link}/spi")

                    # Per-node cloud section
                    cloud_meta = self.cloud_metadata_by_node.get(node.name)
                    if cloud_meta:
                        self._format_node_cloud_section(node, cloud_meta)

    def _format_node_cloud_section(
        self,
        node: OntapNodeResponse,
        cloud_meta: CloudMetadata,
    ) -> None:
        """Format per-node cloud provider information.

        Shows VM name, instance ID, instance type, availability zone,
        and cloud console links for the given node.

        Args:
            node: OntapNodeResponse model instance.
            cloud_meta: CloudMetadata for this node.
        """
        tag = self.app_instance.tag
        text = self.app_instance.text
        fmt = self.app_instance.format_table_row_text
        fmt_link = self.app_instance.format_table_row_link

        provider = cloud_meta.provider
        provider_lower = provider.lower()

        # Derive VM name
        if provider_lower == "azure":
            vm_name = build_azure_vm_name(self.name, node.name, is_ha=len(self.nodes) > 1)
        else:
            vm_name = node.name

        with tag("li"):
            with tag("details"):
                with tag("summary"):
                    text(f"Cloud - {provider}")
                with tag("ul"):
                    with tag("li"):
                        with tag("table", ("class", "custom-table")):
                            if vm_name:
                                fmt("VM Name", vm_name)
                            if cloud_meta.instance_id:
                                fmt("Instance ID", cloud_meta.instance_id)
                            if cloud_meta.instance_type:
                                fmt("Instance Type", cloud_meta.instance_type)
                            if cloud_meta.availability_zone:
                                fmt("Availability Zone", cloud_meta.availability_zone)
                            if cloud_meta.instance_link:
                                fmt_link("Cloud Console", "Link", cloud_meta.instance_link)
                            if cloud_meta.instance_sso_link:
                                fmt_link(
                                    "Cloud Console (SSO)",
                                    "Link",
                                    cloud_meta.instance_sso_link,
                                )


@click.command()
@click.option(
    "--filter",
    "-f",
    "filter",
    help='JSON filter: \'{"bu":"Business", "env":"Prod"}\'',
)
@with_config("HTML report generation failed")
def html(
    config: Config,
    clusters: dict[str, dict[str, Any]],
) -> None:
    """Generate HTML reports with hierarchical tree view.

    Creates an interactive HTML page with a tree structure showing
    all matching clusters organized by Division, Business Unit,
    Application, Environment, Sub-Application, Cloud, and Region.

    Features:
    - Expand/collapse tree nodes
    - "Go to Active Cluster(s)" buttons for quick navigation
    - Links to cluster management interfaces
    - Azure portal links for cloud deployments
    - Cluster, node, and SVM configuration details
    """
    if not clusters:
        raise click.ClickException("No clusters found matching the filter criteria")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = config.output_dir / f"report_{timestamp}.html"

    print_info(f"Building HTML report for {len(clusters)} cluster(s)...")

    builder = HTMLReportBuilder("NetApp Report", clusters, config)
    html_content = builder.generate_html()

    with open(filename, "w") as f:
        f.write(html_content)

    print_success(f"Report saved to {filename}")
    print_info(f"   HA Clusters    : {builder.counts['ha']}")
    print_info(f"   Single-Node    : {builder.counts['sn']}")
