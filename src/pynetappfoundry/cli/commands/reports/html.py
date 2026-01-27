"""Generate HTML reports."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import click

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import print_info, print_success
from pynetappfoundry.core.config import Config


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
    """Generate HTML reports.

    Creates an HTML page with summary information about
    all matching clusters.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = config.output_dir / f"report_{timestamp}.html"

    html_content: list[str] = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "    <title>NetApp Cluster Report</title>",
        "    <style>",
        "        body { font-family: Arial, sans-serif; margin: 20px; }",
        "        table { border-collapse: collapse; width: 100%; }",
        "        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
        "        th { background-color: #4CAF50; color: white; }",
        "        tr:nth-child(even) { background-color: #f2f2f2; }",
        "        h1 { color: #333; }",
        "        h2 { color: #666; }",
        "    </style>",
        "</head>",
        "<body>",
        f"    <h1>NetApp Cluster Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>",
    ]

    for name, details in clusters.items():
        print_info(f"Gathering data for {name}...")
        cluster_html = _gather_cluster_html(name, details, config)
        html_content.extend(cluster_html)

    html_content.extend(
        [
            "</body>",
            "</html>",
        ]
    )

    with open(filename, "w") as f:
        f.write("\n".join(html_content))

    print_success(f"Report saved to {filename}")


def _gather_cluster_html(
    name: str,
    details: dict[str, Any],
    config: Config,
) -> list[str]:
    """Gather HTML report data from a single cluster."""
    from netapp_ontap import HostConnection
    from netapp_ontap.resources import Cluster, Node, Volume

    html_parts: list[str] = [
        f"    <h2>{name}</h2>",
    ]

    user, enc = config.get_user("clusters", name)

    try:
        with HostConnection(
            details["ip"],
            username=user,
            password=enc,
            verify=False,
        ):
            # Cluster info
            cluster = Cluster()
            cluster.get()
            cluster_dict = cluster.to_dict()

            html_parts.append("    <h3>Cluster Info</h3>")
            html_parts.append("    <table>")
            html_parts.append("        <tr><th>Property</th><th>Value</th></tr>")
            html_parts.append(
                f"        <tr><td>Name</td><td>{cluster_dict.get('name', 'Unknown')}</td></tr>"
            )
            version = cluster_dict.get("version", {}).get("full", "Unknown")
            html_parts.append(f"        <tr><td>Version</td><td>{version}</td></tr>")
            html_parts.append("    </table>")

            # Nodes
            html_parts.append("    <h3>Nodes</h3>")
            html_parts.append("    <table>")
            html_parts.append(
                "        <tr><th>Name</th><th>Model</th><th>Serial</th><th>Uptime</th></tr>"
            )
            for node in Node.get_collection(fields="*"):
                node_dict = node.to_dict()
                html_parts.append(
                    f"        <tr><td>{node_dict.get('name', 'Unknown')}</td>"
                    f"<td>{node_dict.get('model', 'Unknown')}</td>"
                    f"<td>{node_dict.get('serial_number', 'Unknown')}</td>"
                    f"<td>{node_dict.get('uptime', 'Unknown')}</td></tr>"
                )
            html_parts.append("    </table>")

            # Volumes summary
            volumes = list(Volume.get_collection(fields="name,state,space"))
            html_parts.append(f"    <h3>Volumes ({len(volumes)} total)</h3>")
            html_parts.append("    <table>")
            html_parts.append("        <tr><th>Name</th><th>State</th><th>Size</th></tr>")
            for vol in volumes[:20]:  # Show first 20
                vol_dict = vol.to_dict()
                html_parts.append(
                    f"        <tr><td>{vol_dict.get('name', 'Unknown')}</td>"
                    f"<td>{vol_dict.get('state', 'Unknown')}</td>"
                    f"<td>{vol_dict.get('space', {}).get('size', 'Unknown')}</td></tr>"
                )
            if len(volumes) > 20:
                html_parts.append(
                    f"        <tr><td colspan='3'>... and {len(volumes) - 20} more</td></tr>"
                )
            html_parts.append("    </table>")

    except Exception as e:
        logging.error(f"Could not gather HTML data for {name}: {e}")
        html_parts.append(f"    <p style='color: red;'>Error: {e}</p>")

    return html_parts
