"""Cache query command for querying specific fields from cached metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import click
from rich.console import Console

from pynetappfoundry.cache import ClusterMetadataDB
from pynetappfoundry.cli.utils import print_error, print_exception, print_warning
from pynetappfoundry.core.config import Config
from pynetappfoundry.utils.dict_path import PathNotFoundError, get_nested_value

console = Console()


def _get_field_value(data: dict[str, Any], field: str) -> tuple[Any, str | None]:
    """Get a field value from data, returning value and error message if any.

    Args:
        data: Dictionary to query.
        field: Dot-notation path to the field.

    Returns:
        Tuple of (value, error_message). If successful, error_message is None.
    """
    try:
        return get_nested_value(data, field), None
    except PathNotFoundError as e:
        return None, str(e)


def _format_value(value: Any) -> str:
    """Format a value for display.

    Args:
        value: Value to format.

    Returns:
        String representation of the value.
    """
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return str(value)


@click.command()
@click.argument("cluster", required=False)
@click.argument("fields", nargs=-1)
@click.option(
    "--filter",
    "-f",
    "filter_str",
    help='JSON filter for cluster selection: \'{"bu":"Business", "env":"Prod"}\'',
)
@click.option(
    "--all",
    "query_all",
    is_flag=True,
    help="Query all cached clusters.",
)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output as JSON.",
)
@click.option(
    "--raw",
    is_flag=True,
    help="Output values only, no field names (single cluster only).",
)
@click.pass_context
def query(
    ctx: click.Context,
    cluster: str | None,
    fields: tuple[str, ...],
    filter_str: str | None,
    query_all: bool,
    output_json: bool,
    raw: bool,
) -> None:
    """Query specific fields from cached cluster metadata.

    Use dot notation to access nested fields (e.g., cloud.instance_type).
    Use bracket notation for array access (e.g., nodes[0].name).

    \b
    Examples:
        # Single cluster, single field
        nf cache query cluster1 cloud.instance_type

        # Single cluster, multiple fields
        nf cache query cluster1 cloud.instance_type cluster.ontap_version

        # All cached clusters
        nf cache query --all cloud.instance_type

        # Filtered clusters
        nf cache query -f '{"bu":"Business"}' cloud.provider cloud.region

        # JSON output
        nf cache query cluster1 cloud.instance_type --json

        # Raw output (single cluster only, for scripting)
        nf cache query cluster1 cluster.ontap_version --raw

        # Array access
        nf cache query cluster1 nodes[0].name
    """
    config_dir = ctx.obj.get("config_dir", "config")

    # Check if config directory exists
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(1)

    # When --all or --filter is used, Click still parses the first positional arg as 'cluster'.
    # We need to treat it as a field in that case and combine with any additional fields.
    effective_fields: tuple[str, ...]
    effective_cluster: str | None

    if query_all or filter_str:
        # Treat cluster as first field if provided
        effective_fields = (cluster, *fields) if cluster else fields
        effective_cluster = None
    else:
        effective_fields = fields
        effective_cluster = cluster

    # Validate arguments
    if not effective_cluster and not query_all and not filter_str:
        print_error("Must specify CLUSTER, --all, or --filter/-f")
        ctx.exit(1)

    if not effective_fields:
        print_error("Must specify at least one FIELD to query")
        ctx.exit(1)

    # Raw output only valid with single cluster
    if raw and (query_all or filter_str):
        print_error("--raw is only valid when querying a single cluster")
        ctx.exit(1)

    try:
        config = Config(config_dir=config_dir, script_name="cache-query")
    except Exception as e:
        print_exception(f"Failed to load configuration: {e}", e)
        ctx.exit(1)

    db = ClusterMetadataDB(config=config)

    # Determine which clusters to query
    cluster_names: list[str] = []
    if effective_cluster:
        cluster_names = [effective_cluster]
    elif query_all:
        cached = db.list_clusters()
        cluster_names = [c["cluster_name"] for c in cached]
        if not cluster_names:
            print_warning("No cached clusters found. Use 'nf cache refresh' to populate.")
            db.close()
            ctx.exit(0)
    elif filter_str:
        try:
            filter_dict = json.loads(filter_str)
        except json.JSONDecodeError as e:
            print_error(f"Invalid filter JSON: {e}")
            db.close()
            ctx.exit(1)

        filtered = config.get_clusters(filter_dict)
        if not filtered:
            print_warning("No clusters match the filter criteria.")
            db.close()
            ctx.exit(0)
        cluster_names = list(filtered.keys())

    # Query each cluster
    results: dict[str, dict[str, Any]] = {}
    errors: list[str] = []

    for name in cluster_names:
        metadata = db.get(name)
        if not metadata:
            print_warning(f"No cached data for cluster '{name}', skipping.")
            continue

        data = metadata.model_dump()
        cluster_results: dict[str, Any] = {}

        for field in effective_fields:
            value, error = _get_field_value(data, field)
            if error:
                errors.append(f"{name}: {error}")
            else:
                cluster_results[field] = value

        if cluster_results:
            results[name] = cluster_results

    db.close()

    # Handle errors
    if errors and not results:
        for err in errors:
            print_error(err)
        ctx.exit(1)

    if not results:
        print_error("No results found.")
        ctx.exit(1)

    # Print warnings for any errors that occurred but we still have some results
    for err in errors:
        print_warning(err)

    # Output results
    if output_json:
        console.print(json.dumps(results, default=str))
    elif raw:
        # Raw output: only values, one per line
        # Only valid for single cluster (already validated above)
        cluster_result = next(iter(results.values()))
        for field in effective_fields:
            if field in cluster_result:
                console.print(_format_value(cluster_result[field]))
    else:
        # Default output: grouped by cluster
        for name, cluster_result in results.items():
            console.print(f"[bold]{name}:[/bold]")
            for field in effective_fields:
                if field in cluster_result:
                    console.print(f"  {field}: {_format_value(cluster_result[field])}")
