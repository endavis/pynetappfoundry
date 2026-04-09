"""On-demand fetching for realtime fields.

Provides functions to fetch, poll, and compare fields with
``cache_strategy="realtime"`` that are excluded from bulk cache collection.

Phase 3d of issue #495 (ADR-0012) routes all four public functions
through the unified :class:`DataSource` accessor. The dict output shape
is preserved for backwards compatibility and will be replaced with
Pydantic model instances in Phase 4.

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

from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.core.config import Config
from pynetappfoundry.data.source import DataSource
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


def _attr_to_api_path(
    mapping: TypeMapping,
    attr: str,
) -> str:
    """Translate a model attribute name to an API field path.

    Iterates TypeMapping.fields looking for a FieldMapping whose
    ``cache_attr`` matches *attr*.  Returns the corresponding
    ``api_path`` if found, otherwise returns *attr* unchanged.

    Used by :func:`fetch_realtime_collection` to translate ``**filters``
    kwargs into the dotted-key filter dict that :class:`DataSource.query`
    understands.

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


def _model_to_dotted_dict(
    instance: BaseModel | None,
    rt_fields: tuple[FieldMapping, ...],
) -> dict[str, Any]:
    """Project a Pydantic model instance into a ``cache_attr``-keyed dict.

    Walks each ``rt_field`` and reads the corresponding attribute from
    *instance* via :func:`getattr`, falling back to ``field.default`` when
    the attribute is missing. Returns an empty dict when *instance* is
    ``None``.

    Args:
        instance: Model instance produced by ``parse_api_response`` or
            ``None`` when the backend returned no record.
        rt_fields: Tuple of realtime :class:`FieldMapping` instances to
            project.

    Returns:
        Flat dict keyed by ``cache_attr``.
    """
    if instance is None:
        return {}
    # ``cache_attr`` may be a dotted path (e.g. ``"metric.iops.read"``);
    # ``parse_api_response`` restructures dotted keys into nested model
    # fields, so we walk the dumped dict to resolve them back.
    instance_dict = instance.model_dump() if isinstance(instance, BaseModel) else {}
    result: dict[str, Any] = {}
    for field in rt_fields:
        try:
            result[field.cache_attr] = get_nested_value(instance_dict, field.cache_attr)
        except PathNotFoundError:
            result[field.cache_attr] = field.default
    return result


def _fetch_realtime_via_data_source(
    data_source: DataSource,
    model_class: type[Any],
    cluster: str,
    uuid: str,
    rt_fields: tuple[FieldMapping, ...],
) -> dict[str, Any]:
    """Single-resource realtime fetch routed through :meth:`DataSource.get`.

    Args:
        data_source: The :class:`DataSource` to route through.
        model_class: Pydantic model class with registered TypeMapping.
        cluster: Name of the cluster to fetch from.
        uuid: Resource UUID.
        rt_fields: Tuple of realtime :class:`FieldMapping` instances.

    Returns:
        Dict mapping ``cache_attr`` to current value. Empty dict if no
        record was returned.
    """
    instance = data_source.get(
        model_class,
        cluster=cluster,
        id=uuid,
        source="live",
        fields=[f.cache_attr for f in rt_fields],
    )
    return _model_to_dotted_dict(instance, rt_fields)


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


def fetch_realtime(
    model_class: type[Any],
    config: Config,
    cluster: str,
    uuid: str,
    fields: list[str] | None = None,
) -> dict[str, Any]:
    """Fetch current realtime metrics for a single resource by UUID.

    Routes through :class:`DataSource` with ``source="live"``.

    Args:
        model_class: Pydantic model class with registered TypeMapping.
        config: :class:`Config` used to construct the backend.
        cluster: Name of the cluster to fetch from.
        uuid: Resource UUID.
        fields: Optional list of ``cache_attr`` names to restrict to.

    Returns:
        Dict mapping ``cache_attr`` to current value.

    Raises:
        ValueError: If no TypeMapping is registered for the model class.
    """
    _mapping, rt_fields = _resolve_realtime(model_class, fields)

    if not rt_fields:
        return {}

    data_source = DataSource(config)
    return _fetch_realtime_via_data_source(data_source, model_class, cluster, uuid, rt_fields)


def fetch_realtime_collection(
    model_class: type[Any],
    config: Config,
    cluster: str,
    fields: list[str] | None = None,
    **filters: Any,
) -> list[dict[str, Any]]:
    """Fetch realtime metrics for multiple resources with optional filtering.

    Always includes ``uuid`` and ``name`` in the response for identification.
    Routes through :meth:`DataSource.query` with ``source="live"``.

    Args:
        model_class: Pydantic model class with registered TypeMapping.
        config: :class:`Config` used to construct the backend.
        cluster: Name of the cluster to fetch from.
        fields: Optional list of ``cache_attr`` names to restrict to.
        **filters: Filter kwargs using model attribute names.

    Returns:
        List of dicts, each with ``uuid``, ``name``, and realtime field values.

    Raises:
        ValueError: If no TypeMapping is registered for the model class.
    """
    mapping, rt_fields = _resolve_realtime(model_class, fields)

    # Translate kwarg filters (model attr names) to dotted API paths
    # that DataSource.QueryBuilder.filter() understands.
    translated_filters: dict[str, Any] = {}
    for attr, value in filters.items():
        translated_filters[_attr_to_api_path(mapping, attr)] = value

    # Always request uuid and name for identification alongside the
    # realtime cache_attrs.
    requested_attrs: list[str] = [f.cache_attr for f in rt_fields]
    for ident in ("uuid", "name"):
        if ident not in requested_attrs:
            requested_attrs.append(ident)

    data_source = DataSource(config)
    builder = (
        data_source.query(model_class, cluster=cluster, source="live")
        .filter(translated_filters)
        .fields(*requested_attrs)
    )

    records: list[dict[str, Any]] = []
    for instance in builder:
        parsed = _model_to_dotted_dict(instance, rt_fields)
        parsed["uuid"] = getattr(instance, "uuid", "")
        parsed["name"] = getattr(instance, "name", "")
        records.append(parsed)

    return records


def watch_realtime(
    model_class: type[Any],
    config: Config,
    cluster: str,
    uuid: str,
    fields: list[str] | None = None,
    interval: float = 5,
    count: int | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Poll realtime metrics at intervals, yielding snapshots.

    Generator that routes each poll through a single :class:`DataSource`
    instance (built once at the top of the call), adding a ``_timestamp``
    key (ISO format UTC) to each yielded dict.

    Args:
        model_class: Pydantic model class with registered TypeMapping.
        config: :class:`Config` used to construct the backend.
        cluster: Name of the cluster to fetch from.
        uuid: Resource UUID.
        fields: Optional list of ``cache_attr`` names to restrict to.
        interval: Seconds between polls (default 5).
        count: Stop after N iterations; ``None`` for infinite.

    Yields:
        Dict with realtime field values and ``_timestamp``.
    """
    _mapping, rt_fields = _resolve_realtime(model_class, fields)

    data_source = DataSource(config)

    iteration = 0
    while True:
        if rt_fields:
            snapshot = _fetch_realtime_via_data_source(
                data_source, model_class, cluster, uuid, rt_fields
            )
        else:
            snapshot = {}
        snapshot["_timestamp"] = datetime.now(tz=UTC).isoformat()
        yield snapshot

        iteration += 1
        if count is not None and iteration >= count:
            return

        time.sleep(interval)


def compare_realtime(
    model_class: type[Any],
    config: Config,
    cluster: str,
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
        config: :class:`Config` used to construct the backend.
        cluster: Name of the cluster to fetch from.
        uuid: Resource UUID.
        baseline: Dict of ``cache_attr`` to baseline values.
        fields: Optional list of ``cache_attr`` names to restrict to.

    Returns:
        Dict mapping ``cache_attr`` to comparison dict.
    """
    current = fetch_realtime(model_class, config, cluster, uuid, fields)

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
