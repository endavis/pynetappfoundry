"""Check clusters for licensing issues."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import click

import pynetappfoundry.cache.ontap.cluster.licensing.licenses.mapping
import pynetappfoundry.cache.ontap.cluster.nodes.mapping  # noqa: F401 - register TypeMapping
from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import print_error, print_info, print_warning
from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
from pynetappfoundry.core.config import Config
from pynetappfoundry.core.models import ClusterConfig
from pynetappfoundry.models.ontap.cluster.licensing.licenses import (
    OntapLicensePackageResponse,
)
from pynetappfoundry.models.ontap.cluster.nodes import OntapNodeResponse
from pynetappfoundry.query import QuerySet
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
    "send_email_flag",
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
        if send_email_flag:
            _send_no_issues_email(config)


def _check_cluster_licenses(
    name: str,
    details: dict[str, Any],
    config: Config,
) -> list[dict[str, Any]]:
    """Check a single cluster for license issues."""
    issues: list[dict[str, Any]] = []
    days_to_check = 30
    current_time = datetime.now(UTC)

    try:
        cluster_config = ClusterConfig(**details)
        client = ONTAPAPIClient(cluster=cluster_config, config=config)

        packages: list[OntapLicensePackageResponse] = QuerySet(
            OntapLicensePackageResponse, client
        ).all()

        nodes_response: list[OntapNodeResponse] = QuerySet(OntapNodeResponse, client).all()

        nodes_data: dict[str, dict[str, Any]] = {}
        for node in nodes_response:
            nodes_data[node.name] = {
                "serial_number": node.serial_number,
                "has_license": False,
            }

        if not packages:
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

        for pkg in packages:
            for lic in pkg.licenses:
                serial_number = lic.serial_number
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

                owner = lic.owner or "none"
                if owner in nodes_data:
                    nodes_data[owner]["has_license"] = True
                    nodes_data[owner]["license_type"] = license_type

                if lic.expiry_time and owner != "none":
                    expiry_time = datetime.fromisoformat(lic.expiry_time)
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
        print_error(f"Could not retrieve licenses for {name}: {e}")
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


def _build_styled_html(issues: list[dict[str, Any]]) -> str:
    """Build styled HTML email body for license issues.

    Args:
        issues: List of license issue dicts.

    Returns:
        Styled HTML string.
    """
    html_parts: list[str] = [
        "<html>",
        "<head>",
        "    <style>",
        "    .red-white {",
        "        background-color: red;",
        "        color: white;",
        "        padding: 5px;",
        "        font-weight: bold;",
        "    }",
        "    .yellow-black {",
        "        background-color: yellow;",
        "        color: black;",
        "        padding: 5px;",
        "        font-weight: bold;",
        "    }",
        "    </style>",
        "</head>",
        "<body>",
        "    <p>The following licenses should be checked</p>",
    ]

    for issue in issues:
        cluster = issue.get("cluster", "Unknown")
        owner = issue.get("owner", "Unknown")
        serial = issue.get("serial_number", "Unknown")
        license_type = issue.get("license_type", "Unknown")
        days = issue.get("days_checked", "Unknown")
        expires = issue.get("expires", "Unknown")

        if isinstance(expires, datetime):
            expires_str = expires.strftime("%Y-%m-%d")
        else:
            expires_str = str(expires)

        if isinstance(days, (int, float)) and days < 0:
            abs_days = abs(days)
            html_parts.append(
                f"    <p class='red-white'>"
                f"{cluster} - {owner} - {serial} - {license_type} "
                f"has expired {abs_days} days ago on {expires_str}!</p>"
            )
        else:
            html_parts.append(
                f"    <p class='yellow-black'>"
                f"{cluster} - {owner} - {serial} - {license_type} "
                f"expires in {days} days on {expires_str}.</p>"
            )

    html_parts.extend(["</body>", "</html>"])

    return "\n".join(html_parts)


def _send_license_email(
    config: Config,
    issues: list[dict[str, Any]],
) -> None:
    """Send email about license issues."""
    licensing_settings = config.get_licensing_settings()

    if not licensing_settings:
        print_warning("Email settings not configured, skipping notification")
        return

    html_body = _build_styled_html(issues)

    send_email(
        config,
        subject=f"{datetime.now().date()} : Licensing issues found",
        body=html_body,
        body_type="html",
        mailfrom=licensing_settings.mailfrom,
        mailto=licensing_settings.mailto,
        high_priority=True,
    )


def _send_no_issues_email(config: Config) -> None:
    """Send email when no licensing issues are found."""
    licensing_settings = config.get_licensing_settings()

    if not licensing_settings:
        print_warning("Email settings not configured, skipping notification")
        return

    send_email(
        config,
        subject=f"{datetime.now().date()} : No licensing issues found",
        body="No licensing issues",
        body_type="html",
        mailfrom=licensing_settings.mailfrom,
        mailto=licensing_settings.mailto,
    )
