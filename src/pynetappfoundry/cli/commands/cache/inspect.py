"""Cache inspect command for troubleshooting field mappings."""

from __future__ import annotations

import contextlib
import json
import logging
from pathlib import Path
from typing import Any

import click
from rich.console import Console
from rich.tree import Tree

from pynetappfoundry.cache import ClusterMetadataDB
from pynetappfoundry.cache.cloud.metadata.mapping import CLOUD_METADATA_MAPPING
from pynetappfoundry.cache.cluster.licensing.mapping import LICENSE_PACKAGE_MAPPING
from pynetappfoundry.cache.cluster.nodes.mapping import NODE_MAPPING
from pynetappfoundry.cache.cluster.peers.mapping import CLUSTER_PEER_MAPPING
from pynetappfoundry.cache.field_mapping import TypeMapping
from pynetappfoundry.cache.network.ethernet.broadcast_domains.mapping import (
    BROADCAST_DOMAIN_MAPPING,
)
from pynetappfoundry.cache.network.ip.interfaces.mapping import NETWORK_LIF_MAPPING
from pynetappfoundry.cache.storage.aggregates.mapping import AGGREGATE_MAPPING
from pynetappfoundry.cache.storage.volumes.mapping import VOLUME_MAPPING
from pynetappfoundry.cache.svm.mapping import SVM_MAPPING
from pynetappfoundry.cli.utils import (
    format_value_markup,
    print_error,
    print_exception,
    print_warning,
)
from pynetappfoundry.clients.ontap import ONTAPCLI, ONTAPAPIClient
from pynetappfoundry.core.config import Config

logger = logging.getLogger(__name__)
console = Console()

# Registry of supported object types for inspection.
# Maps type name to (TypeMapping, cache_path) where cache_path is the
# dot-path to the list of objects in CachedClusterMetadata.
INSPECT_TYPES: dict[str, tuple[TypeMapping, str]] = {
    "aggregate": (AGGREGATE_MAPPING, "storage.aggregates"),
    "broadcast_domain": (BROADCAST_DOMAIN_MAPPING, "network.broadcast_domains"),
    "cloud_metadata": (CLOUD_METADATA_MAPPING, "cloud"),
    "cluster_peer": (CLUSTER_PEER_MAPPING, "relationships.cluster_peers"),
    "license": (LICENSE_PACKAGE_MAPPING, "license_packages"),
    "node": (NODE_MAPPING, "nodes"),
    "svm": (SVM_MAPPING, "storage.svms"),
    "network_lif": (NETWORK_LIF_MAPPING, "network.lifs"),
    "volume": (VOLUME_MAPPING, "storage.volumes"),
}


def _resolve_cache_list(
    metadata: Any,
    cache_path: str,
) -> list[Any]:
    """Walk dotted cache_path on a metadata object to get the list.

    Args:
        metadata: CachedClusterMetadata instance.
        cache_path: Dot-separated attribute path (e.g. "storage.volumes").

    Returns:
        The list at the end of the path, or empty list on error.
    """
    obj = metadata
    for attr in cache_path.split("."):
        obj = getattr(obj, attr, None)
        if obj is None:
            return []
    return obj if isinstance(obj, list) else []


def _format_value(value: object) -> str:
    """Format a value for tree display.

    Args:
        value: Value to format.

    Returns:
        Rich-formatted string.
    """
    result = format_value_markup(value)
    if result is not None:
        return result
    if isinstance(value, list):
        if not value:
            return "[dim](empty list)[/dim]"
        return f"[cyan]{len(value)} items[/cyan]"
    return str(value)


def _build_cache_tree(obj: Any) -> Tree:
    """Build a Rich tree from a Pydantic model or dict.

    Args:
        obj: Model instance or dict to display.

    Returns:
        Populated Rich Tree.
    """
    tree = Tree("[bold]CACHE[/bold]")
    data = obj.model_dump() if hasattr(obj, "model_dump") else dict(obj)
    for key, value in data.items():
        if isinstance(value, list):
            branch = tree.add(f"[cyan]{key}[/cyan]: {_format_value(value)}")
            for item in value:
                branch.add(f"[green]{item}[/green]")
        else:
            tree.add(f"[cyan]{key}[/cyan]: {_format_value(value)}")
    return tree


def _build_api_endpoint(mapping: TypeMapping, object_name: str) -> str:
    """Build the full API endpoint with name filter.

    Args:
        mapping: TypeMapping for the object type.
        object_name: Name of the object to look up.

    Returns:
        Full endpoint string.
    """
    base_endpoint = mapping.api_endpoint
    separator = "&" if "?" in base_endpoint else "?"
    return f"{base_endpoint}{separator}name={object_name}"


def _build_cli_command(mapping: TypeMapping, object_name: str) -> str:
    """Build the full CLI command string.

    The CLI client wraps the command with ``set d -confirmations off;
    set -showallfields true;set -showseparator ",";`` before execution.

    Args:
        mapping: TypeMapping for the object type.
        object_name: Name of the object to look up.

    Returns:
        CLI command string as sent to the cluster.
    """
    return f"{mapping.cli_command} {object_name}"


def _fetch_api_filtered(
    api_client: ONTAPAPIClient,
    endpoint: str,
) -> dict[str, Any] | None:
    """Fetch a single object from the REST API using a name filter.

    Args:
        api_client: Initialised ONTAP API client.
        endpoint: Full API endpoint with name= filter.

    Returns:
        The first matching record dict, or None.
    """
    response = api_client.call_endpoint(endpoint)
    records: list[dict[str, Any]] = response.get("records", []) if response else []
    if records:
        return records[0]
    return None


def _fetch_api_all(
    api_client: ONTAPAPIClient,
    endpoint: str,
    object_name: str,
) -> dict[str, Any] | None:
    """Fetch all objects then search client-side (same as cache refresh).

    Args:
        api_client: Initialised ONTAP API client.
        endpoint: Base API endpoint without name filter.
        object_name: Name of the object to find in results.

    Returns:
        The matching record dict, or None.
    """
    response = api_client.call_endpoint(endpoint)
    records: list[dict[str, Any]] = response.get("records", []) if response else []
    for record in records:
        if record.get("name") == object_name:
            return record
    return None


def _fetch_cli_data(
    cli_client: ONTAPCLI,
    mapping: TypeMapping,
    object_name: str,
) -> tuple[dict[str, str] | None, dict[str, str]]:
    """Fetch a single object from the CLI by name.

    Args:
        cli_client: Initialised ONTAP SSH client.
        mapping: TypeMapping for the object type.
        object_name: Name of the object to look up.

    Returns:
        Tuple of (first data record or None, field descriptions dict).
    """
    records, descriptions = cli_client.run_a_show_command_and_parse_seperator(
        mapping.cli_command,
        arguments=object_name,
    )
    if records:
        return records[0], descriptions
    return None, descriptions


@click.command()
@click.argument("cluster")
@click.argument("object_name")
@click.option(
    "--type",
    "-t",
    "object_type",
    type=click.Choice(sorted(INSPECT_TYPES.keys()), case_sensitive=False),
    default="volume",
    show_default=True,
    help="Object type to inspect.",
)
@click.pass_context
def inspect(ctx: click.Context, cluster: str, object_name: str, object_type: str) -> None:
    """Inspect cache, CLI, and API data for a single object.

    Displays three sections so you can compare what is stored in the
    local cache versus the live API and CLI responses from the cluster.

    \b
    Examples:
        nf cache inspect PRODCL1 PRODVOL1
        nf cache inspect PRODCL1 PRODVOL1 --type volume
    """
    config_dir = ctx.obj.get("config_dir", "config")

    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(1)

    try:
        config = Config(config_dir=config_dir, script_name="cache-inspect")
    except Exception as e:
        print_exception(f"Failed to load configuration: {e}", e)
        ctx.exit(1)

    if cluster not in config.data.get("clusters", {}):
        print_error(f"Cluster '{cluster}' not found in configuration.")
        available = list(config.data.get("clusters", {}).keys())
        if available:
            console.print(f"Available clusters: {', '.join(available)}")
        ctx.exit(1)

    mapping, cache_path = INSPECT_TYPES[object_type.lower()]

    # ── CACHE section ──────────────────────────────────────────────
    console.print()
    console.rule("[bold] CACHE [/bold]")
    db = ClusterMetadataDB(config=config)
    metadata = db.get(cluster)
    db.close()

    if metadata:
        items = _resolve_cache_list(metadata, cache_path)
        match = next((i for i in items if getattr(i, "name", None) == object_name), None)
        if match:
            console.print(_build_cache_tree(match))
        else:
            print_warning(
                f"Object '{object_name}' not found in cache section '{cache_path}'. "
                "Try 'nf cache refresh' first."
            )
    else:
        print_warning(f"No cached data for cluster '{cluster}'. Run 'nf cache refresh' first.")

    # Build the exact commands that will be executed.
    cli_command = _build_cli_command(mapping, object_name)
    api_endpoint = _build_api_endpoint(mapping, object_name)

    # ── CLI section ────────────────────────────────────────────────
    console.print()
    console.rule("[bold] CLI [/bold]")
    console.print(f"[dim]Command: {cli_command}[/dim]")

    cluster_data = config.data["clusters"][cluster]
    user, password = config.get_user("clusters", cluster)

    cli_client: ONTAPCLI | None = None
    try:
        cli_client = ONTAPCLI(
            name=cluster,
            host_or_ip=cluster_data.get("ip", ""),
            username=user,
            password=password,
        )
        cli_record, cli_descriptions = _fetch_cli_data(cli_client, mapping, object_name)
        if cli_record:
            tree = Tree("[bold]CLI[/bold]")
            for key, value in cli_record.items():
                desc = cli_descriptions.get(key, "")
                label = f"[dim]{desc}[/dim] " if desc else ""
                tree.add(f"[cyan]{key}[/cyan]: {label}[green]{value}[/green]")
            console.print(tree)
        else:
            print_warning(f"CLI returned no data for '{object_name}'.")
    except Exception as e:
        print_exception(f"CLI query failed: {e}", e)
    finally:
        if cli_client:
            with contextlib.suppress(Exception):
                cli_client.disconnect()

    # ── API (filtered) section ────────────────────────────────────
    console.print()
    console.rule("[bold] API (filtered) [/bold]")
    console.print(f"[dim]Endpoint: {api_endpoint}[/dim]")

    class _ClusterObj:
        def __init__(self, name: str, ip: str) -> None:
            self.name = name
            self.ip = ip

    api_client: ONTAPAPIClient | None = None
    try:
        api_client = ONTAPAPIClient(
            cluster=_ClusterObj(cluster, cluster_data.get("ip", "")),
            config=config,
        )
        api_record = _fetch_api_filtered(api_client, api_endpoint)
        if api_record:
            console.print_json(json.dumps(api_record, default=str))
        else:
            print_warning(f"API returned no data for '{object_name}'.")
    except Exception as e:
        print_exception(f"API query failed: {e}", e)

    # ── API (all) section ──────────────────────────────────────
    base_endpoint = mapping.api_endpoint
    console.print()
    console.rule("[bold] API (all) [/bold]")
    console.print(f"[dim]Endpoint: {base_endpoint}[/dim]")

    try:
        if not api_client:
            api_client = ONTAPAPIClient(
                cluster=_ClusterObj(cluster, cluster_data.get("ip", "")),
                config=config,
            )
        api_record_all = _fetch_api_all(api_client, base_endpoint, object_name)
        if api_record_all:
            console.print_json(json.dumps(api_record_all, default=str))
        else:
            print_warning(f"API returned no data for '{object_name}'.")
    except Exception as e:
        print_exception(f"API query failed: {e}", e)

    console.print()
