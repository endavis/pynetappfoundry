"""Generate HTML reports with hierarchical tree view.

This module generates an interactive HTML report with:

- Hierarchical tree structure (Division > BU > App > Environment > Cloud > Region)
- Expand/collapse functionality using <details>/<summary> elements
- "Go to Active Cluster(s)" buttons for quick navigation
- Hyperlinks to cluster management interfaces, Azure portal, AIQUM, Connectors
- Rich cluster data including nodes, SVMs, interfaces, and CIFS/SMB configuration
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

import click
from yattag import Doc, indent

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import print_info, print_success
from pynetappfoundry.utils.cloud import (
    build_azure_id,
    build_azure_portal_link,
)

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config

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
            self.clusterdata[item] = ClusterData(item, self, **self.cluster_details[item])
            cluster = self.clusterdata[item]

            # Count HA vs single-node clusters
            if len(list(cluster.fetched_data.get("nodes", {}).keys())) > 1:
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
        logging.info(f"Processed {self.counts['ha'] + self.counts['sn']} clusters")
        logging.info(f"   Single Node : {self.counts['sn']}")
        logging.info(f"   HA          : {self.counts['ha']}")
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
        fetched_data: Dictionary of data fetched from the cluster.
        app_instance: Reference to the parent HTMLReportBuilder.
        ele_class: CSS class for active cluster highlighting.
    """

    def __init__(
        self,
        clustername: str,
        app_instance: HTMLReportBuilder,
        **kwargs: Any,
    ) -> None:
        """Initialize cluster data and gather information from the cluster.

        Args:
            clustername: Name of the cluster.
            app_instance: Parent HTMLReportBuilder instance.
            **kwargs: Cluster configuration from TOML.
        """
        self.name = clustername
        self.cluster_type = ""
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.fetched_data: dict[str, Any] = {}
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
        """Build cloud-specific information (Azure subscription IDs, resource URLs).

        Uses cloud_* fields from cluster config (enriched from cache).
        """
        # Get cloud info from cluster config (enriched by Config._enrich_with_cache)
        cloud_provider = getattr(self, "cloud_provider", "")
        if cloud_provider.lower() == "azure":
            sub_id = getattr(self, "cloud_account_id", "")
            resource_group = getattr(self, "cloud_resource_group_name", "")
            if sub_id and resource_group:
                self.cloud_resource_group_id = build_azure_id(sub_id, resource_group)
                self.cloud_resource_group_url = build_azure_portal_link(
                    self.cloud_resource_group_id
                )

    def _gather_data(self) -> None:
        """Gather data from the cluster via ONTAP REST API."""
        from netapp_ontap import HostConnection
        from netapp_ontap.resources import CifsService, Cluster, IpInterface, Node, Svm

        logging.info(f"Gathering data for {self.name}")
        self._build_cloud_info()

        ip = getattr(self, "ip", None)
        if not ip:
            logging.error(f"No IP address for cluster {self.name}")
            return

        try:
            user, password = self.app_instance.config.get_user("clusters", self.name)
        except Exception as e:
            logging.error(f"Could not get credentials for {self.name}: {e}")
            return

        try:
            with HostConnection(ip, username=user, password=password, verify=False):
                cluster = Cluster()
                cluster.get()
                self.fetched_data["cluster"] = cluster.to_dict()

                nodes = list(Node.get_collection(fields="*"))
                self.fetched_data["nodes"] = {}
                for node in nodes:
                    self.fetched_data["nodes"][node["name"]] = node.to_dict()

                svms = list(Svm.get_collection(fields="*"))
                self.fetched_data["svms"] = {}
                for svm in svms:
                    self.fetched_data["svms"][svm["name"]] = svm.to_dict()

                ipinterfaces = list(IpInterface.get_collection(fields="*"))
                self.fetched_data["interfaces"] = {}
                for interface in ipinterfaces:
                    self.fetched_data["interfaces"][interface["name"]] = interface.to_dict()

                cifsservices = list(CifsService.get_collection(fields="*"))
                self.fetched_data["cifs"] = {}
                for cifserver in cifsservices:
                    self.fetched_data["cifs"][cifserver["name"]] = cifserver.to_dict()
        except Exception as e:
            logging.error(f"Could not gather data from {self.name}: {e}")

    def format(self) -> None:
        """Format the cluster data as HTML."""
        logging.info(f"Formatting cluster: {self.name}")
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
        """Format cloud provider information for the cluster.

        Uses cloud_* fields from cluster config (enriched from cache).
        """
        tag = self.app_instance.tag
        text = self.app_instance.text
        fmt = self.app_instance.format_table_row_text
        fmt_link = self.app_instance.format_table_row_link

        cloud_provider = getattr(self, "cloud_provider", "")
        if not cloud_provider:
            return

        with tag("li"):
            with tag("details"):
                with tag("summary"):
                    text(f"{cloud_provider} Information")
                with tag("ul"):
                    with tag("li"):
                        with tag("table", ("class", "custom-table")):
                            fmt("Provider", cloud_provider)
                            region = getattr(self, "cloud_region", "")
                            if region:
                                fmt("Region", region)
                            instance_type = getattr(self, "cloud_instance_type", "")
                            if instance_type:
                                fmt("Instance Type", instance_type)
                            instance_id = getattr(self, "cloud_instance_id", "")
                            if instance_id:
                                fmt("Instance ID", instance_id)

                            # Azure-specific fields
                            if cloud_provider.lower() == "azure":
                                account_id = getattr(self, "cloud_account_id", "")
                                if account_id:
                                    fmt("Subscription ID", account_id)
                                rg_name = getattr(self, "cloud_resource_group_name", "")
                                if rg_name:
                                    rg_url = getattr(self, "cloud_resource_group_url", "")
                                    if rg_url:
                                        fmt_link("Resource Group", rg_name, rg_url)
                                    else:
                                        fmt("Resource Group", rg_name)

    def _format_netapp_cluster_info(self) -> None:
        """Format cluster-level information (version, management IPs, DNS, NTP)."""
        if "cluster" not in self.fetched_data:
            return

        tag = self.app_instance.tag
        text = self.app_instance.text
        cluster_data = self.fetched_data["cluster"]

        mgmt_interfaces = cluster_data.get("management_interfaces", [])
        if mgmt_interfaces:
            management_ip = mgmt_interfaces[0].get("ip", {}).get("address", "")
            management_link = f"https://{management_ip}"
        else:
            management_link = ""

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
                            version = cluster_data.get("version", {}).get("full", "Unknown")
                            self.app_instance.format_table_row_text("Version", version)

                            if mgmt_interfaces:
                                mgmt_ip = mgmt_interfaces[0].get("ip", {}).get("address", "Unknown")
                                self.app_instance.format_table_row_text(
                                    "Cluster Management IP", mgmt_ip
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
                                        domains = cluster_data.get("dns_domains", [])
                                        self.app_instance.format_table_row_text(
                                            "Domains", ", ".join(domains) if domains else "None"
                                        )
                                        for i, name_server in enumerate(
                                            cluster_data.get("name_servers", [])
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
                                        ntp_servers = cluster_data.get("ntp_servers", [])
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
        if "svms" not in self.fetched_data:
            return

        tag = self.app_instance.tag
        text = self.app_instance.text

        for svm_name in sorted(self.fetched_data["svms"].keys()):
            svm_data = self.fetched_data["svms"][svm_name]
            logging.info(f"  SVM: {svm_data.get('name', svm_name)}")

            state = svm_data.get("state", "")
            state_text = " - State: Stopped" if state == "stopped" else ""

            with tag("li"):
                with tag("details"):
                    with tag("summary"):
                        text(f"vserver {svm_data.get('name', svm_name)}{state_text}")
                    with tag("ul"):
                        self._format_netapp_vserver_interfaces_info(svm_data)
                        self._format_netapp_vserver_dns_info(svm_data)
                        self._format_netapp_vserver_smb_server_info(svm_data)

    def _format_netapp_vserver_interfaces_info(self, svm_data: dict[str, Any]) -> None:
        """Format SVM network interface information.

        Args:
            svm_data: SVM data dictionary.
        """
        if "ip_interfaces" not in svm_data:
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
                            for svm_interface in svm_data["ip_interfaces"]:
                                iface_name = svm_interface.get("name", "")
                                ip_interface = self.fetched_data.get("interfaces", {}).get(
                                    iface_name, {}
                                )
                                if ip_interface:
                                    ip_info = ip_interface.get("ip", {})
                                    ip_addr = ip_info.get("address", "Unknown")
                                    netmask = ip_info.get("netmask", "")
                                    home_node = (
                                        ip_interface.get("location", {})
                                        .get("home_node", {})
                                        .get("name", "Unknown")
                                    )
                                    self.app_instance.format_table_row_text(
                                        iface_name,
                                        f"{ip_addr}/{netmask}" if netmask else ip_addr,
                                        home_node,
                                    )

    def _format_netapp_vserver_dns_info(self, svm_data: dict[str, Any]) -> None:
        """Format SVM DNS configuration.

        Args:
            svm_data: SVM data dictionary.
        """
        tag = self.app_instance.tag
        text = self.app_instance.text
        dns_data = svm_data.get("dns", {})

        with tag("li"):
            with tag("details"):
                with tag("summary"):
                    text("DNS")
                with tag("ul"):
                    with tag("li"):
                        with tag("table", ("class", "custom-table")):
                            domains = dns_data.get("domains", [])
                            self.app_instance.format_table_row_text(
                                "Domains", ", ".join(domains) if domains else "None"
                            )
                            for i, name_server in enumerate(dns_data.get("servers", [])):
                                self.app_instance.format_table_row_text(
                                    f"Server {i + 1}", name_server
                                )

    def _format_netapp_vserver_smb_server_info(self, svm_data: dict[str, Any]) -> None:
        """Format SVM CIFS/SMB server configuration.

        Args:
            svm_data: SVM data dictionary.
        """
        cifs_ref = svm_data.get("cifs", {})
        if "name" not in cifs_ref:
            return

        cifs_name = cifs_ref["name"]
        cifs_data = self.fetched_data.get("cifs", {}).get(cifs_name, {})
        if not cifs_data:
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
                            self.app_instance.format_table_row_text(
                                "Enabled", str(cifs_data.get("enabled", "Unknown"))
                            )
                            self.app_instance.format_table_row_text(
                                "Name", cifs_data.get("name", "")
                            )
                            ad_domain = cifs_data.get("ad_domain", {})
                            self.app_instance.format_table_row_text(
                                "Domain", ad_domain.get("fqdn", "")
                            )
                            self.app_instance.format_table_row_text(
                                "Organizational Unit", ad_domain.get("organizational_unit", "")
                            )

                    # Security settings
                    with tag("li"):
                        with tag("details"):
                            with tag("summary"):
                                text("Security")
                            with tag("ul"):
                                with tag("li"):
                                    with tag("table", ("class", "custom-table")):
                                        security = cifs_data.get("security", {})
                                        items = [
                                            ("Is Signing Required", "smb_signing"),
                                            (
                                                "Use start_tls for AD LDAP connection",
                                                "use_start_tls",
                                            ),
                                            ("LM Compatibility Level", "lm_compatibility_level"),
                                            ("Is SMB Encryption Required", "smb_encryption"),
                                            ("Client Session Security", "session_security"),
                                            (
                                                "LDAP Referral Enabled For AD LDAP connections",
                                                "ldap_referral_enabled",
                                            ),
                                            ("Use LDAPS for AD LDAP connection", "use_ldaps"),
                                            (
                                                "Encryption is required for DC Connections",
                                                "encrypt_dc_connection",
                                            ),
                                            (
                                                "AES session key enabled for NetLogon channel",
                                                "aes_netlogon_enabled",
                                            ),
                                            (
                                                "Try Channel Binding For AD LDAP Connections",
                                                "try_ldap_channel_binding",
                                            ),
                                            (
                                                "Encryption Types Advertised to Kerberos",
                                                "advertised_kdc_encryptions",
                                            ),
                                        ]
                                        for header, key in items:
                                            value = security.get(key, "")
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
        if "nodes" not in self.fetched_data:
            return

        for node_name in sorted(self.fetched_data["nodes"].keys()):
            node_data = self.fetched_data["nodes"][node_name]
            self._format_netapp_node(node_data)

    def _format_netapp_node(self, node_data: dict[str, Any]) -> None:
        """Format a single node's information.

        Args:
            node_data: Node data dictionary.
        """
        tag = self.app_instance.tag
        text = self.app_instance.text

        mgmt_interfaces = node_data.get("management_interfaces", [])
        if mgmt_interfaces:
            mgmt_ip = mgmt_interfaces[0].get("ip", {}).get("address", "")
            management_link = f"https://{mgmt_ip}"
        else:
            management_link = ""
            mgmt_ip = ""

        # Build VM information for cloud deployments
        vm_id = None
        vm_url = None
        vm_name = None
        vm_type = None
        cloud_provider = getattr(self, "cloud_provider", "")

        if cloud_provider.lower() == "azure":
            node_name = node_data.get("name", "")
            short_name = node_name.split("-")[0] if "-" in node_name else node_name

            try:
                node_number = int(node_name.split("-")[1]) if "-" in node_name else 1
            except (ValueError, IndexError):
                node_number = 1

            vm_type = "Azure VM"
            if len(self.fetched_data.get("nodes", {})) > 1:
                vm_name = f"{short_name}-vm{node_number}"
            else:
                vm_name = short_name

            sub_id = getattr(self, "cloud_account_id", "")
            resource_group = getattr(self, "cloud_resource_group_name", "")
            if sub_id and resource_group:
                vm_id = build_azure_id(sub_id, resource_group, resource_name=vm_name)
                vm_url = build_azure_portal_link(vm_id)

        with tag("li"):
            with tag("details"):
                with tag("summary"):
                    if management_link:
                        with tag("a", ("href", management_link)):
                            text(node_data.get("name", "Unknown"))
                    else:
                        text(node_data.get("name", "Unknown"))
                with tag("ul"):
                    with tag("li"):
                        with tag("table", ("class", "custom-table")):
                            if mgmt_ip:
                                self.app_instance.format_table_row_text(
                                    "Node Management IP", mgmt_ip
                                )
                            serial = node_data.get("serial_number", "Unknown")
                            self.app_instance.format_table_row_text("Serial Number", serial)
                            if management_link:
                                self.app_instance.format_table_row_link(
                                    "System Manager", "Link", management_link
                                )
                                self.app_instance.format_table_row_link(
                                    "SPI", "Link", f"{management_link}/spi"
                                )
                            if vm_name and vm_id and vm_url and vm_type:
                                self.app_instance.format_table_row_text(f"{vm_type} Name", vm_name)
                                self.app_instance.format_table_row_link(vm_type, vm_id, vm_url)


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
