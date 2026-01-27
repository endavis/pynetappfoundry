"""Check clusters for licensing issues."""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

import click
from netapp_ontap import HostConnection
from netapp_ontap.resources import LicensePackage, Node

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import print_error, print_info, print_warning
from pynetappfoundry.core.config import Config
from pynetappfoundry.utils.email import send_email


@click.command()
@click.option(
    "--filter",
    "-f",
    "filter",
    help='JSON filter: \'{"bu":"Business", "env":"Prod"}\'',
)
@click.option(
    "--send-email/--no-send-email",
    default=True,
    help="Send email notification (default: True).",
)
@with_config("License check failed")
def check(
    config: Config,
    clusters: dict[str, dict[str, Any]],
    send_email_flag: bool = True,
) -> None:
    """Check clusters for licensing issues.

    Examines all clusters for license expiration and missing licenses,
    optionally sending email notifications.
    """
    license_issues: list[dict[str, Any]] = []

    for name, details in clusters.items():
        print_info(f"Checking {name}...")
        issues = _check_cluster_licenses(name, details, config)
        license_issues.extend(issues)

    if license_issues:
        print_warning(f"Found {len(license_issues)} licensing issues:")
        for issue in license_issues:
            _print_issue(issue)
        if send_email_flag:
            _send_license_email(config, license_issues)
    else:
        print_info("No licensing issues found.")


def _check_cluster_licenses(
    name: str,
    details: dict[str, Any],
    config: Config,
) -> list[dict[str, Any]]:
    """Check a single cluster for license issues."""
    issues: list[dict[str, Any]] = []
    days_to_check = 30
    current_time = datetime.now(UTC)

    user, enc = config.get_user("clusters", name)
    try:
        with HostConnection(
            details["ip"],
            username=user,
            password=enc,
            verify=False,
        ):
            licenses_data: list[dict[str, Any]] = []
            for lic in LicensePackage.get_collection(fields="*"):
                licenses_data.append(lic.to_dict())

            nodes_data: dict[str, dict[str, Any]] = {}
            for node in Node.get_collection(fields="*"):
                nodes_data[node["name"]] = node.to_dict()
                nodes_data[node["name"]]["has_license"] = False

            if not licenses_data:
                issues.append(
                    {
                        "cluster": name,
                        "owner": "",
                        "error": "Could not get licenses",
                        "days_checked": -1,
                        "serial_number": -1,
                        "expires": -1,
                        "license_type": -1,
                    }
                )
                return issues

            for lic in licenses_data:
                for item in lic.get("licenses", []):
                    serial_number = item.get("serial_number", "")
                    license_type = "ONTAP BYOL"
                    days_check = days_to_check

                    # Determine license type and check period
                    if serial_number.startswith("9092"):
                        days_check = 13
                        license_type = "ONTAP Cloud Capacity"
                    elif serial_number.startswith("2265"):
                        days_check = 13
                        license_type = "Data Tiering"
                    elif serial_number.startswith("3200"):
                        license_type = "ONTAP Select"

                    owner = item.get("owner", "none")
                    if owner in nodes_data:
                        nodes_data[owner]["has_license"] = True
                        nodes_data[owner]["license_type"] = license_type

                    if "expiry_time" in item and owner != "none":
                        expiry_time = datetime.fromisoformat(item["expiry_time"])
                        delta = expiry_time - current_time
                        days_difference = delta.days

                        if days_difference < days_check:
                            issues.append(
                                {
                                    "cluster": name,
                                    "owner": owner,
                                    "error": "Expiring license",
                                    "days_checked": days_difference,
                                    "serial_number": serial_number,
                                    "expires": expiry_time,
                                    "license_type": license_type,
                                }
                            )

            # Check for nodes without licenses
            for node_name, node_data in nodes_data.items():
                if not node_data.get("has_license", False):
                    issues.append(
                        {
                            "cluster": name,
                            "node": node_name,
                            "error": "No License",
                            "days_checked": -1,
                            "serial_number": node_data.get("serial_number", "Unknown"),
                            "expires": -1,
                            "license_type": "None",
                        }
                    )

    except Exception as e:
        logging.error(f"Could not retrieve licenses for {name}: {e}")
        issues.append(
            {
                "cluster": name,
                "error": str(e),
            }
        )

    return issues


def _print_issue(issue: dict[str, Any]) -> None:
    """Print a license issue."""
    days = issue.get("days_checked", "Unknown")
    if isinstance(days, (int, float)) and days < 0:
        print_error(
            f"  {issue['cluster']} - {issue.get('owner', 'Unknown')} - "
            f"{issue.get('serial_number', 'Unknown')} has expired!"
        )
    else:
        print_warning(
            f"  {issue['cluster']} - {issue.get('owner', 'Unknown')} - expires in {days} days"
        )


def _send_license_email(
    config: Config,
    issues: list[dict[str, Any]],
) -> None:
    """Send email about license issues."""
    mailfrom = config.settings.get("settings", {}).get("licensing", {}).get("mailfrom")
    mailto = config.settings.get("settings", {}).get("licensing", {}).get("mailto")

    if not mailfrom or not mailto:
        logging.warning("Email settings not configured, skipping notification")
        return

    html_body = ["<html><body>"]
    html_body.append("<p>The following licenses should be checked:</p>")
    for issue in issues:
        days = issue.get("days_checked", "Unknown")
        html_body.append(f"<p>{issue['cluster']} - {issue.get('error', 'Unknown error')}")
        if days != "Unknown":
            html_body.append(f" - {days} days</p>")
        else:
            html_body.append("</p>")
    html_body.append("</body></html>")

    send_email(
        config,
        subject=f"{datetime.now().date()} : Licensing issues found",
        body="\n".join(html_body),
        body_type="html",
        mailfrom=mailfrom,
        mailto=mailto,
        high_priority=True,
    )
