"""On-demand fetching for realtime fields.

Provides functions to fetch, poll, and compare fields with
``cache_strategy="realtime"`` that are excluded from bulk cache collection.

Functions:
    fetch_realtime: Fetch current realtime metrics for a single resource.
    fetch_realtime_collection: Fetch realtime metrics for multiple resources.
    watch_realtime: Poll realtime metrics at intervals via generator.
    compare_realtime: Compare current metrics against a baseline dict.
"""

from __future__ import annotations

import time
from collections.abc import Generator
from datetime import UTC, datetime
from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.utils.dict_path import PathNotFoundError, get_nested_value

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _resolve_realtime(
    model_class: type[Any],
    fields: list[str] | None = None,
) -> tuple[TypeMapping, tuple[FieldMapping, ...]]:
    """Resolve TypeMapping and return filtered realtime fields.

    Args:
        model_class: Pydantic model class registered in the model registry.
        fields: Optional list of ``cache_attr`` names to restrict to.

    Returns:
        Tuple of ``(mapping, realtime_fields)``.

    Raises:
        ValueError: If no TypeMapping is registered for the model class.
    """
    mapping = model_registry.get_mapping(model_class.__name__)
    if mapping is None:
        msg = (
            f"No TypeMapping registered for '{model_class.__name__}'. "
            f"Ensure the model's mapping module has been imported."
        )
        raise ValueError(msg)

    rt_fields = mapping.realtime_fields()

    if fields is not None:
        field_set = set(fields)
        rt_fields = tuple(f for f in rt_fields if f.cache_attr in field_set)

    return mapping, rt_fields


def _parse_realtime_record(
    record: dict[str, Any],
    realtime_fields: tuple[FieldMapping, ...],
) -> dict[str, Any]:
    """Extract realtime field values from an API response record.

    For each field: uses ``transform(record)`` if set, else
    ``get_nested_value(record, api_path)``, falling back to ``default``.

    Args:
        record: API response record dict.
        realtime_fields: Tuple of realtime FieldMapping instances.

    Returns:
        Dict mapping ``cache_attr`` to extracted value.
    """
    result: dict[str, Any] = {}
    for field in realtime_fields:
        if field.transform is not None:
            try:
                result[field.cache_attr] = field.transform(record)
            except Exception:
                result[field.cache_attr] = field.default
        elif field.api_path is not None:
            try:
                result[field.cache_attr] = get_nested_value(record, field.api_path)
            except PathNotFoundError:
                result[field.cache_attr] = field.default
        else:
            result[field.cache_attr] = field.default
    return result


def _realtime_api_fields(
    realtime_fields: tuple[FieldMapping, ...],
) -> list[str]:
    """Deduplicate top-level API field names from realtime fields.

    Takes the first segment (before ``.``) of each ``api_path``.

    Args:
        realtime_fields: Tuple of realtime FieldMapping instances.

    Returns:
        Sorted list of unique top-level API field names.
    """
    keys: set[str] = set()
    for field in realtime_fields:
        if field.api_path is not None:
            first_segment = field.api_path.split(".")[0].split("[")[0]
            keys.add(first_segment)
    return sorted(keys)


def _attr_to_api_path(
    mapping: TypeMapping,
    attr: str,
) -> str:
    """Translate a model attribute name to an API field path.

    Iterates TypeMapping.fields looking for a FieldMapping whose
    ``cache_attr`` matches *attr*.  Returns the corresponding
    ``api_path`` if found, otherwise returns *attr* unchanged.

    Args:
        mapping: TypeMapping for the model.
        attr: Model attribute name.

    Returns:
        API field path string.
    """
    for field in mapping.fields:
        if field.cache_attr == attr and field.api_path is not None:
            return field.api_path
    return attr


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


def fetch_realtime(
    model_class: type[Any],
    client: Any,
    uuid: str,
    fields: list[str] | None = None,
) -> dict[str, Any]:
    """Fetch current realtime metrics for a single resource by UUID.

    Args:
        model_class: Pydantic model class with registered TypeMapping.
        client: API client with ``call_endpoint`` method.
        uuid: Resource UUID.
        fields: Optional list of ``cache_attr`` names to restrict to.

    Returns:
        Dict mapping ``cache_attr`` to current value.

    Raises:
        ValueError: If no TypeMapping is registered for the model class.
    """
    mapping, rt_fields = _resolve_realtime(model_class, fields)

    if not rt_fields:
        return {}

    collection_path = mapping.collection_endpoint.split("?", 1)[0]
    api_fields = _realtime_api_fields(rt_fields)
    url = f"{collection_path}/{uuid}?fields={','.join(api_fields)}"

    response = client.call_endpoint(url)
    return _parse_realtime_record(response, rt_fields)


def fetch_realtime_collection(
    model_class: type[Any],
    client: Any,
    fields: list[str] | None = None,
    **filters: Any,
) -> list[dict[str, Any]]:
    """Fetch realtime metrics for multiple resources with optional filtering.

    Always includes ``uuid`` and ``name`` in the response for identification.

    Args:
        model_class: Pydantic model class with registered TypeMapping.
        client: API client with ``get_all_records`` method.
        fields: Optional list of ``cache_attr`` names to restrict to.
        **filters: Filter kwargs using model attribute names.

    Returns:
        List of dicts, each with ``uuid``, ``name``, and realtime field values.

    Raises:
        ValueError: If no TypeMapping is registered for the model class.
    """
    mapping, rt_fields = _resolve_realtime(model_class, fields)

    api_fields = _realtime_api_fields(rt_fields)
    # Always include uuid and name for identification
    for ident_field in ("uuid", "name"):
        if ident_field not in api_fields:
            api_fields.append(ident_field)
    api_fields.sort()

    collection_path = mapping.collection_endpoint.split("?", 1)[0]

    # Build query params
    params_parts = [f"fields={','.join(api_fields)}"]
    for attr, value in filters.items():
        api_path = _attr_to_api_path(mapping, attr)
        params_parts.append(f"{api_path}={value}")

    url = f"{collection_path}?{'&'.join(params_parts)}"

    response = client.get_all_records(url)
    records: list[dict[str, Any]] = []
    raw_records = response.get("records", []) if isinstance(response, dict) else []

    for raw in raw_records:
        parsed = _parse_realtime_record(raw, rt_fields)
        parsed["uuid"] = raw.get("uuid", "")
        parsed["name"] = raw.get("name", "")
        records.append(parsed)

    return records


def watch_realtime(
    model_class: type[Any],
    client: Any,
    uuid: str,
    fields: list[str] | None = None,
    interval: float = 5,
    count: int | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Poll realtime metrics at intervals, yielding snapshots.

    Generator that calls :func:`fetch_realtime` in a loop, adding a
    ``_timestamp`` key (ISO format UTC) to each yielded dict.

    Args:
        model_class: Pydantic model class with registered TypeMapping.
        client: API client with ``call_endpoint`` method.
        uuid: Resource UUID.
        fields: Optional list of ``cache_attr`` names to restrict to.
        interval: Seconds between polls (default 5).
        count: Stop after N iterations; ``None`` for infinite.

    Yields:
        Dict with realtime field values and ``_timestamp``.
    """
    iteration = 0
    while True:
        snapshot = fetch_realtime(model_class, client, uuid, fields)
        snapshot["_timestamp"] = datetime.now(tz=UTC).isoformat()
        yield snapshot

        iteration += 1
        if count is not None and iteration >= count:
            return

        time.sleep(interval)


def compare_realtime(
    model_class: type[Any],
    client: Any,
    uuid: str,
    baseline: dict[str, Any],
    fields: list[str] | None = None,
) -> dict[str, dict[str, Any]]:
    """Compare current realtime metrics against a baseline dict.

    For numeric values (int/float), includes ``baseline``, ``current``,
    and ``delta`` (current - baseline).  For non-numeric values, includes
    ``baseline`` and ``current`` only.  Fields in current but not in
    baseline include ``current`` only.

    Args:
        model_class: Pydantic model class with registered TypeMapping.
        client: API client with ``call_endpoint`` method.
        uuid: Resource UUID.
        baseline: Dict of ``cache_attr`` to baseline values.
        fields: Optional list of ``cache_attr`` names to restrict to.

    Returns:
        Dict mapping ``cache_attr`` to comparison dict.
    """
    current = fetch_realtime(model_class, client, uuid, fields)

    result: dict[str, dict[str, Any]] = {}
    for attr, current_val in current.items():
        if attr in baseline:
            baseline_val = baseline[attr]
            comparison: dict[str, Any] = {
                "baseline": baseline_val,
                "current": current_val,
            }
            if isinstance(current_val, (int, float)) and isinstance(baseline_val, (int, float)):
                comparison["delta"] = current_val - baseline_val
            result[attr] = comparison
        else:
            result[attr] = {"current": current_val}

    return result
