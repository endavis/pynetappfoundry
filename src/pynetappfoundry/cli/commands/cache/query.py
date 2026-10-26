"""Cache query command for querying specific fields from cached metadata."""

from __future__ import annotations

import csv
import io
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import click
from rich.console import Console

from pynetappfoundry.cache import ClusterMetadataDB
from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cli.utils import (
    format_value_markup,
    print_error,
    print_exception,
    print_warning,
)
from pynetappfoundry.core.config import Config
from pynetappfoundry.data.source import DataSource
from pynetappfoundry.utils.dict_path import (
    DEFAULT_IDENTIFIER_KEYS,
    PathNotFoundError,
    get_nested_value,
    get_nested_value_with_identifiers,
)

console = Console()

# Matches a wildcard array-access segment like "nodes[*]"
_WILDCARD_SEGMENT = re.compile(r"\[\*\]")

# Matches a filter predicate segment like nodes["name=vol1"] or nodes['name=vol1']
_FILTER_SEGMENT = re.compile(r"""\[["'].+?["']\]""")


def _is_wildcard_path(field: str) -> bool:
    """Return True if *field* contains a wildcard [*] or filter predicate segment.

    Args:
        field: Dot-notation field path.

    Returns:
        True if the path should be resolved with identifiers (via
        ``get_nested_value_with_identifiers``) rather than plain
        ``get_nested_value``.
    """
    return bool(_WILDCARD_SEGMENT.search(field) or _FILTER_SEGMENT.search(field))


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


def _get_field_value_with_identifiers(
    data: dict[str, Any],
    field: str,
    identifier_keys: tuple[str, ...],
) -> tuple[list[dict[str, Any]] | None, str | None]:
    """Get a wildcard/filter field's results labelled by identifier.

    Args:
        data: Dictionary to query.
        field: Dot-notation path containing a wildcard or filter segment.
        identifier_keys: Dot-notation key paths tried, in order, to label
            each array item.

    Returns:
        Tuple of (records, error_message). ``records`` is a list of
        ``{"key": identifier, "value": value}`` dicts. If successful,
        error_message is None.
    """
    try:
        pairs = get_nested_value_with_identifiers(data, field, identifier_keys)
    except PathNotFoundError as e:
        return None, str(e)
    return [{"key": key, "value": value} for key, value in pairs], None


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


def _format_display_value(value: Any) -> str:
    """Format a value for default display output with Rich markup.

    Uses shared ``format_value_markup`` for scalar types and adds
    indented JSON formatting for dicts/lists.

    Args:
        value: Value to format.

    Returns:
        String with Rich markup for colored display.
    """
    result = format_value_markup(value)
    if result is not None:
        return result
    if isinstance(value, (dict, list)):
        return json.dumps(value, indent=2, default=str)
    return str(value)


def _format_csv_value(value: Any) -> str:
    """Format a value for CSV output.

    Args:
        value: Value to format.

    Returns:
        String representation suitable for CSV.
    """
    if value is None:
        return ""
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, dict):
        return json.dumps(value)
    return str(value)


def _output_csv(
    results: dict[str, dict[str, Any]],
    fields: tuple[str, ...],
) -> str:
    """Format results as CSV.

    When any field is a wildcard or filter predicate path, a ``key`` column
    is added after ``cluster`` and rows are expanded by that field's
    results. If several fields are wildcard/filter paths, the ``key``
    column comes from the first one (by position in *fields*); the other
    wildcard fields are aligned to it by index.

    Fields without a wildcard/filter path keep the legacy behavior: a
    field whose value happens to be a plain list also expands rows, aligned
    by index (and drives the ``key`` column's row count too, when no field
    is a wildcard/filter path).

    Args:
        results: Query results keyed by cluster name. Wildcard/filter field
            values are lists of ``{"key", "value"}`` dicts; other field
            values are plain.
        fields: Field names in order.

    Returns:
        CSV formatted string.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    wildcard_fields = [f for f in fields if _is_wildcard_path(f)]
    include_key_column = bool(wildcard_fields)

    # Write header
    header = ["cluster"]
    if include_key_column:
        header.append("key")
    header.extend(fields)
    writer.writerow(header)

    # Write data rows
    for cluster_name, cluster_result in results.items():
        if include_key_column:
            first_field = wildcard_fields[0]
            records = cluster_result.get(first_field) or []
            row_count = len(records)

            if row_count > 0:
                for i in range(row_count):
                    row = [cluster_name, records[i]["key"]]
                    for field in fields:
                        if field in wildcard_fields:
                            field_records = cluster_result.get(field) or []
                            row.append(
                                _format_csv_value(field_records[i]["value"])
                                if i < len(field_records)
                                else ""
                            )
                        else:
                            row.append(_format_csv_value(cluster_result.get(field)))
                    writer.writerow(row)
            else:
                row = [cluster_name, ""]
                for field in fields:
                    if field in wildcard_fields:
                        row.append("")
                    else:
                        row.append(_format_csv_value(cluster_result.get(field)))
                writer.writerow(row)
            continue

        # Legacy behavior: no wildcard/filter field present. A plain list
        # value (e.g. a field group returned whole) still expands rows.
        list_length = 0
        for field in fields:
            value = cluster_result.get(field)
            if isinstance(value, list) and list_length == 0:
                list_length = len(value)
                # If lists have different lengths, use the first one found

        if list_length > 0:
            for i in range(list_length):
                row = [cluster_name]
                for field in fields:
                    value = cluster_result.get(field)
                    if isinstance(value, list):
                        row.append(_format_csv_value(value[i] if i < len(value) else None))
                    else:
                        row.append(_format_csv_value(value))
                writer.writerow(row)
        else:
            row = [cluster_name]
            for field in fields:
                value = cluster_result.get(field)
                row.append(_format_csv_value(value))
            writer.writerow(row)

    return output.getvalue().rstrip("\r\n")


def _extract_field_groups(fields: tuple[str, ...]) -> set[str]:
    """Extract the top-level field group from each field path.

    The first path segment (before ``.`` or ``[``) identifies the field
    group on ``CachedClusterMetadata``.

    Args:
        fields: Field path strings (e.g. ``"nodes[0].name"``).

    Returns:
        Set of unique top-level group names.
    """
    groups: set[str] = set()
    for field in fields:
        head = re.split(r"[.\[]", field, maxsplit=1)[0]
        groups.add(head)
    return groups


def _fetch_live_groups(
    config: Config,
    cluster: str,
    field_groups: set[str],
) -> dict[str, Any]:
    """Fetch field groups live via DataSource and assemble a dict.

    Each group is resolved via the table registry. Groups with a
    ``TypeMapping`` are fetched through ``DataSource.query(source="live")``;
    groups without one are skipped with a warning.

    Args:
        config: Application config.
        cluster: Cluster name.
        field_groups: Set of top-level field group names to fetch.

    Returns:
        Dict compatible with ``get_nested_value()`` walking (mirrors
        the shape of ``CachedClusterMetadata.model_dump()``).
    """
    from pynetappfoundry.cache.db_schema import _ensure_registry

    registry = _ensure_registry()
    ds = DataSource(config)
    data: dict[str, Any] = {
        "cluster_name": cluster,
        "cached_at": datetime.now(tz=UTC).isoformat(),
    }

    for group in field_groups:
        # Find all registry entries belonging to this group
        group_entries = [
            (path, spec)
            for path, spec in registry.items()
            if path == group or path.startswith(f"{group}.")
        ]
        if not group_entries:
            # Envelope/non-data field — skip silently
            continue

        group_data: dict[str, Any] = {}
        for path, spec in group_entries:
            mapping = model_registry.get_mapping(spec.model_class.__name__)
            if mapping is None:
                print_warning(
                    f"Field group '{path}' cannot be fetched live (no TypeMapping); skipping."
                )
                continue

            try:
                results = list(ds.query(spec.model_class, cluster=cluster, source="live"))
            except ValueError as e:
                print_warning(f"Cannot fetch '{path}' live: {e}")
                continue

            # Build nested structure under group_data
            relative = path[len(group) :].lstrip(".")
            dumped: Any
            if spec.is_list:
                dumped = [r.model_dump() for r in results]
            else:
                dumped = results[0].model_dump() if results else {}

            if relative:
                _set_nested(group_data, relative, dumped)
            else:
                group_data = dumped

        data[group] = group_data

    return data


def _set_nested(target: dict[str, Any], dotted_path: str, value: Any) -> None:
    """Set a value in a nested dict via dot-path, creating intermediate dicts."""
    parts = dotted_path.split(".")
    for part in parts[:-1]:
        target = target.setdefault(part, {})
    target[parts[-1]] = value


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
@click.option(
    "--csv",
    "output_csv",
    is_flag=True,
    help="Output as CSV with header row.",
)
@click.option(
    "--live",
    "live",
    is_flag=True,
    default=False,
    help=(
        "Bypass the cache and fetch data live from each cluster. "
        "Only the requested field groups are fetched."
    ),
)
@click.option(
    "--key",
    "identifier_key",
    default=None,
    help=(
        "Identifier field path used to label wildcard/filter results "
        "(e.g. svm.name). Overrides the default identifier order "
        "(name, svm.name, uuid, then array index) for every wildcard or "
        "filter field in the query."
    ),
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
    output_csv: bool,
    live: bool = False,
    identifier_key: str | None = None,
) -> None:
    """Query specific fields from cached cluster metadata.

    Use dot notation to access nested fields (e.g., cloud.instance_type).
    Use bracket notation for array access (e.g., nodes[0].name).
    Use wildcard [*] to access all items in an array (e.g., nodes[*].name).
    Wildcard and filter predicate results are labelled with an identifier
    for the array item they came from (name, svm.name, uuid, or the array
    index as a fallback); override with --key.

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

        # Wildcard array access (get field from all items)
        nf cache query cluster1 nodes[*].name

        # Wildcard with --raw (one key<TAB>value line per item, for scripting)
        nf cache query cluster1 nodes[*].name --raw

        # Choose the identifier field explicitly (default: name, svm.name, uuid)
        nf cache query cluster1 nodes[*].serial_number --key name

        # CSV output
        nf cache query --all cloud.provider cloud.region --csv

        # CSV with wildcards (expands to multiple rows, labelled by a key column)
        nf cache query cluster1 nodes[*].name nodes[*].serial_number --csv

        # Filter predicate (select items by field value)
        nf cache query cluster1 'volumes["name=vol1"].size'

        # OR filter (match multiple values)
        nf cache query cluster1 'volumes["name=vol1 || name=vol2"].size'

        # Single-quoted predicate (alternative syntax)
        nf cache query cluster1 "volumes['state=online'].name"
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

    # Warn if --live requests many field groups
    if live:
        field_groups = _extract_field_groups(effective_fields)
        if len(field_groups) > 3:
            print_warning(
                f"--live is fetching {len(field_groups)} field groups "
                f"({', '.join(sorted(field_groups))}); this may be slow."
            )

    identifier_keys: tuple[str, ...] = (
        (identifier_key,) if identifier_key else DEFAULT_IDENTIFIER_KEYS
    )

    # Query each cluster
    results: dict[str, dict[str, Any]] = {}
    errors: list[str] = []

    for name in cluster_names:
        if live:
            live_groups = _extract_field_groups(effective_fields)
            data = _fetch_live_groups(config, name, live_groups)
        else:
            metadata = db.get_lazy(name)
            if not metadata:
                print_warning(f"No cached data for cluster '{name}', skipping.")
                continue
            data = metadata.model_dump()

        cluster_results: dict[str, Any] = {}

        for field in effective_fields:
            if _is_wildcard_path(field):
                records, error = _get_field_value_with_identifiers(data, field, identifier_keys)
                if error:
                    errors.append(f"{name}: {error}")
                elif not records:
                    continue
                else:
                    cluster_results[field] = records
            else:
                value, error = _get_field_value(data, field)
                if error:
                    errors.append(f"{name}: {error}")
                elif isinstance(value, list) and not value:
                    continue
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
    elif output_csv:
        console.print(_output_csv(results, effective_fields))
    elif raw:
        # Raw output: only values, one per line
        # Only valid for single cluster (already validated above)
        # Wildcard/filter results print one "key<TAB>value" line per item
        cluster_result = next(iter(results.values()))
        for field in effective_fields:
            if field in cluster_result:
                value = cluster_result[field]
                if _is_wildcard_path(field):
                    # Write the tab directly: console.print() expands tabs
                    # to spaces, which would break key<TAB>value scripting.
                    for record in value:
                        console.file.write(f"{record['key']}\t{_format_value(record['value'])}\n")
                elif isinstance(value, list):
                    # Non-wildcard list results: one value per line
                    for item in value:
                        console.print(_format_value(item))
                else:
                    console.print(_format_value(value))
    else:
        # Default output: grouped by cluster
        for name, cluster_result in results.items():
            console.print(f"[bold]{name}:[/bold]")
            for field in effective_fields:
                if field in cluster_result:
                    if _is_wildcard_path(field):
                        console.print(f"  [cyan]{field}[/cyan]:")
                        for record in cluster_result[field]:
                            formatted = _format_display_value(record["value"])
                            if "\n" in formatted:
                                console.print(f"    {record['key']}:")
                                for line in formatted.split("\n"):
                                    console.print(f"      {line}")
                            else:
                                console.print(f"    {record['key']}: {formatted}")
                    else:
                        formatted = _format_display_value(cluster_result[field])
                        if "\n" in formatted:
                            console.print(f"  [cyan]{field}[/cyan]:")
                            for line in formatted.split("\n"):
                                console.print(f"    {line}")
                        else:
                            console.print(f"  [cyan]{field}[/cyan]: {formatted}")
