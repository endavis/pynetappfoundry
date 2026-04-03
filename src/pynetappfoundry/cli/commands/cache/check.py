"""Cache check command for ad-hoc cache queries with filtering.

Exposes the SQL query engine via the CLI, allowing users to filter
cached model data with expressive ``--where`` expressions and project
specific fields.

Exit codes follow grep conventions:
- 0: no matches found
- 1: matches found
- 2: error
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any

import click
from rich.console import Console
from rich.table import Table

from pynetappfoundry.cache import ClusterMetadataDB
from pynetappfoundry.cache.query_engine import parse_filter
from pynetappfoundry.cli.utils import print_error, print_exception, print_warning
from pynetappfoundry.core.config import Config
from pynetappfoundry.utils.dict_path import get_nested_value

console = Console()


def _extract_where_fields(where_exprs: tuple[str, ...]) -> list[str]:
    """Extract field paths referenced in --where expressions.

    Args:
        where_exprs: Tuple of filter expression strings.

    Returns:
        List of unique field paths from the expressions.
    """
    fields: list[str] = []
    for expr in where_exprs:
        try:
            parsed = parse_filter(expr)
            if parsed.field_path not in fields:
                fields.append(parsed.field_path)
        except ValueError:
            # Skip malformed expressions; they'll be caught later
            pass
    return fields


def _resolve_default_fields(
    where_exprs: tuple[str, ...],
    sample_data: dict[str, Any],
) -> list[str]:
    """Determine default fields when --fields is not specified.

    Includes ``name`` and ``uuid`` if present on the model, plus
    any field paths referenced in ``--where`` expressions.

    Args:
        where_exprs: Filter expression strings.
        sample_data: A sample model dumped to dict for field detection.

    Returns:
        Ordered list of field names.
    """
    fields: list[str] = []
    for key in ("name", "uuid"):
        if key in sample_data:
            fields.append(key)

    for wf in _extract_where_fields(where_exprs):
        if wf not in fields:
            fields.append(wf)

    return fields


def _project_row(data: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    """Project specific fields from a model dict.

    Args:
        data: Model dumped to dict.
        fields: Dot-separated field paths.

    Returns:
        Dict with only the requested fields.
    """
    row: dict[str, Any] = {}
    for field in fields:
        try:
            row[field] = get_nested_value(data, field)
        except Exception:
            row[field] = None
    return row


def _format_csv_value(value: Any) -> str:
    """Format a value for CSV output.

    Args:
        value: Value to format.

    Returns:
        String suitable for CSV.
    """
    if value is None:
        return ""
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return str(value)


def _output_csv(
    all_rows: dict[str, list[dict[str, Any]]],
    fields: list[str],
) -> str:
    """Format results as CSV.

    Args:
        all_rows: Cluster name -> list of projected row dicts.
        fields: Column names.

    Returns:
        CSV string.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["cluster", *fields])

    for cluster_name, rows in all_rows.items():
        for row in rows:
            csv_row = [cluster_name]
            for field in fields:
                csv_row.append(_format_csv_value(row.get(field)))
            writer.writerow(csv_row)

    return output.getvalue().rstrip("\r\n")


def _output_json(
    all_rows: dict[str, list[dict[str, Any]]],
) -> str:
    """Format results as JSON.

    Args:
        all_rows: Cluster name -> list of projected row dicts.

    Returns:
        JSON string.
    """
    return json.dumps(all_rows, default=str)


def _output_table(
    all_rows: dict[str, list[dict[str, Any]]],
    fields: list[str],
) -> Table:
    """Build a Rich Table from results.

    Args:
        all_rows: Cluster name -> list of projected row dicts.
        fields: Column names.

    Returns:
        Rich Table instance.
    """
    table = Table(title="Cache Check Results")
    table.add_column("Cluster", style="bold")
    for field in fields:
        table.add_column(field, style="cyan")

    for cluster_name, rows in all_rows.items():
        for row in rows:
            values = [_format_display(row.get(field)) for field in fields]
            table.add_row(cluster_name, *values)

    return table


def _format_display(value: Any) -> str:
    """Format a value for table display.

    Args:
        value: Value to format.

    Returns:
        String representation.
    """
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (dict, list)):
        return json.dumps(value, default=str)
    return str(value)


@click.command()
@click.argument("cluster", required=False)
@click.argument("model", required=False)
@click.option(
    "--where",
    "-w",
    "where_exprs",
    multiple=True,
    help="Filter expression (repeatable, AND-joined). E.g. -w \"autosize.mode != 'grow_shrink'\"",
)
@click.option(
    "--fields",
    "-F",
    "fields_str",
    help="Comma-separated field paths for projection.",
)
@click.option(
    "--all",
    "query_all",
    is_flag=True,
    help="Query all cached clusters.",
)
@click.option(
    "--filter",
    "-f",
    "filter_str",
    help='JSON filter for cluster selection: \'{"bu":"Business", "env":"Prod"}\'',
)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output as JSON.",
)
@click.option(
    "--csv",
    "output_csv",
    is_flag=True,
    help="Output as CSV with header row.",
)
@click.option(
    "--count",
    "output_count",
    is_flag=True,
    help="Only print match count per cluster.",
)
@click.pass_context
def check(
    ctx: click.Context,
    cluster: str | None,
    model: str | None,
    where_exprs: tuple[str, ...],
    fields_str: str | None,
    query_all: bool,
    filter_str: str | None,
    output_json: bool,
    output_csv: bool,
    output_count: bool,
) -> None:
    """Query cached model data with filtering.

    Filter cached cluster metadata using expressive --where expressions
    and project specific fields. Useful for ad-hoc checks and CI scripts.

    Exit codes follow grep conventions: 0 = no matches, 1 = matches found,
    2 = error.

    \b
    Examples:
        # Find volumes where autosize mode is not grow_shrink
        nf cache check cluster1 storage.volumes \\
            -w "autosize.mode != 'grow_shrink'" \\
            -F name,svm.name,autosize.mode

        # Check all clusters
        nf cache check --all storage.volumes \\
            -w "autosize.mode != 'grow_shrink'"

        # Filtered cluster selection + data filter
        nf cache check -f '{"env":"Prod"}' storage.volumes \\
            -w "autosize.mode != 'grow_shrink'" \\
            -F name,svm.name,autosize.mode

        # Count matches only
        nf cache check --all storage.volumes \\
            -w "size > 1073741824" --count

        # JSON output for scripting
        nf cache check --all nodes -w "model = 'FAS8200'" --json

        # CSV output
        nf cache check --all storage.volumes \\
            -w "state = 'online'" --csv
    """
    config_dir = ctx.obj.get("config_dir", "config")

    # Check if config directory exists
    config_path = Path.cwd() / config_dir
    if not config_path.exists():
        print_error(f"Configuration directory not found: {config_path}")
        ctx.exit(2)

    # When --all or --filter is used, Click parses the first positional arg
    # as 'cluster'. Treat it as the MODEL in that case.
    effective_model: str
    effective_cluster: str | None

    if query_all or filter_str:
        if cluster and model:
            # Both positional args provided with --all/--filter; cluster is the model
            effective_model = cluster
            effective_cluster = None
        elif cluster:
            # Only first positional; it's the model
            effective_model = cluster
            effective_cluster = None
        else:
            print_error("Must specify MODEL argument")
            ctx.exit(2)
    else:
        if not cluster:
            print_error("Must specify CLUSTER, --all, or --filter/-f")
            ctx.exit(2)
        if not model:
            print_error("Must specify MODEL argument")
            ctx.exit(2)
        effective_model = model
        effective_cluster = cluster

    try:
        config = Config(config_dir=config_dir, script_name="cache-check")
    except Exception as e:
        print_exception(f"Failed to load configuration: {e}", e)
        ctx.exit(2)

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
            ctx.exit(2)

        filtered = config.get_clusters(filter_dict)
        if not filtered:
            print_warning("No clusters match the filter criteria.")
            db.close()
            ctx.exit(0)
        cluster_names = list(filtered.keys())

    # Parse field list
    fields: list[str] | None = None
    if fields_str:
        fields = [f.strip() for f in fields_str.split(",") if f.strip()]

    # Query each cluster
    all_rows: dict[str, list[dict[str, Any]]] = {}
    total_matches = 0

    for name in cluster_names:
        try:
            results = db.query_with_filters(name, effective_model, list(where_exprs))
        except ValueError as e:
            error_msg = str(e)
            if "Unknown model name" in error_msg:
                available = ", ".join(sorted(db._registry.keys()))
                print_error(f"{error_msg}. Available models: {available}")
            else:
                print_error(error_msg)
            db.close()
            ctx.exit(2)

        if not results:
            continue

        # Determine effective fields
        effective_fields = fields
        if effective_fields is None:
            # Default: name + uuid (if present) + where field paths
            sample = results[0].model_dump()
            effective_fields = _resolve_default_fields(where_exprs, sample)
            # If still empty (no name/uuid, no where), show all top-level keys
            if not effective_fields:
                effective_fields = list(sample.keys())

        # Project fields
        rows: list[dict[str, Any]] = []
        for result in results:
            dumped = result.model_dump()
            row = _project_row(dumped, effective_fields)
            rows.append(row)

        all_rows[name] = rows
        total_matches += len(rows)

    db.close()

    # If fields were not set yet (no results at all), set for output
    if fields is None and not all_rows:
        effective_fields_for_output: list[str] = []
    elif fields is not None:
        effective_fields_for_output = fields
    else:
        # Use the fields from the first cluster that had results
        first_rows = next(iter(all_rows.values()))
        effective_fields_for_output = list(first_rows[0].keys()) if first_rows else []

    # Output
    if output_count:
        for name in cluster_names:
            count = len(all_rows.get(name, []))
            console.print(f"{name}: {count}")
        ctx.exit(1 if total_matches > 0 else 0)

    if not all_rows:
        ctx.exit(0)

    if output_json:
        console.print(_output_json(all_rows))
    elif output_csv:
        console.print(_output_csv(all_rows, effective_fields_for_output))
    else:
        table = _output_table(all_rows, effective_fields_for_output)
        console.print(table)

    ctx.exit(1 if total_matches > 0 else 0)
