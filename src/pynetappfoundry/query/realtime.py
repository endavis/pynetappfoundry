"""On-demand fetching for realtime fields.

Provides functions to fetch, poll, and compare fields with
``cache_strategy="realtime"`` that are excluded from bulk cache collection.

All four public functions return Pydantic model instances (or lists/generators
thereof). ``compare_realtime`` returns a nested dict with per-field comparison
results.

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
            f"Mappings are auto-registered; verify a mapping.py module "
            f"exists under cache/ontap/ for this model."
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


def _fetch_realtime_via_data_source(
    data_source: DataSource,
    model_class: type[Any],
    cluster: str,
    uuid: str,
    rt_fields: tuple[FieldMapping, ...],
) -> BaseModel | None:
    """Single-resource realtime fetch routed through :meth:`DataSource.get`.

    Args:
        data_source: The :class:`DataSource` to route through.
        model_class: Pydantic model class with registered TypeMapping.
        cluster: Name of the cluster to fetch from.
        uuid: Resource UUID.
        rt_fields: Tuple of realtime :class:`FieldMapping` instances.

    Returns:
        The model instance, or ``None`` if no record was returned.
    """
    return data_source.get(
        model_class,
        cluster=cluster,
        id=uuid,
        source="live",
        fields=[f.cache_attr for f in rt_fields],
    )


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


def fetch_realtime(
    model_class: type[Any],
    config: Config,
    cluster: str,
    uuid: str,
    fields: list[str] | None = None,
) -> BaseModel | None:
    """Fetch current realtime metrics for a single resource by UUID.

    Routes through :class:`DataSource` with ``source="live"``.

    Args:
        model_class: Pydantic model class with registered TypeMapping.
        config: :class:`Config` used to construct the backend.
        cluster: Name of the cluster to fetch from.
        uuid: Resource UUID.
        fields: Optional list of ``cache_attr`` names to restrict to.

    Returns:
        The model instance with realtime fields populated, or ``None``
        when the backend returned no record. Returns ``None`` when the
        model has no realtime fields.

    Raises:
        ValueError: If no TypeMapping is registered for the model class.
    """
    _mapping, rt_fields = _resolve_realtime(model_class, fields)

    if not rt_fields:
        return None

    data_source = DataSource(config)
    return _fetch_realtime_via_data_source(data_source, model_class, cluster, uuid, rt_fields)


def fetch_realtime_collection(
    model_class: type[Any],
    config: Config,
    cluster: str,
    fields: list[str] | None = None,
    **filters: Any,
) -> list[BaseModel]:
    """Fetch realtime metrics for multiple resources with optional filtering.

    Routes through :meth:`DataSource.query` with ``source="live"``.

    Args:
        model_class: Pydantic model class with registered TypeMapping.
        config: :class:`Config` used to construct the backend.
        cluster: Name of the cluster to fetch from.
        fields: Optional list of ``cache_attr`` names to restrict to.
        **filters: Filter kwargs using model attribute names.

    Returns:
        List of model instances with realtime fields populated.

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

    return list(builder)


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
    instance (built once at the top of the call). Each snapshot is a dict
    with ``model`` (the model instance or ``None``) and ``_timestamp``
    (ISO format UTC).

    Args:
        model_class: Pydantic model class with registered TypeMapping.
        config: :class:`Config` used to construct the backend.
        cluster: Name of the cluster to fetch from.
        uuid: Resource UUID.
        fields: Optional list of ``cache_attr`` names to restrict to.
        interval: Seconds between polls (default 5).
        count: Stop after N iterations; ``None`` for infinite.

    Yields:
        Dict with ``model`` (BaseModel | None) and ``_timestamp``.
    """
    _mapping, rt_fields = _resolve_realtime(model_class, fields)

    data_source = DataSource(config)

    iteration = 0
    while True:
        if rt_fields:
            instance = _fetch_realtime_via_data_source(
                data_source, model_class, cluster, uuid, rt_fields
            )
        else:
            instance = None
        snapshot: dict[str, Any] = {
            "model": instance,
            "_timestamp": datetime.now(tz=UTC).isoformat(),
        }
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

    The model instance is fetched via :func:`fetch_realtime` and then
    each realtime field's current value is read from the model via
    attribute access.

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
    _mapping, rt_fields = _resolve_realtime(model_class, fields)

    instance = fetch_realtime(model_class, config, cluster, uuid, fields)
    if instance is None:
        return {}

    # Extract current values from the model instance.
    instance_dict = instance.model_dump() if isinstance(instance, BaseModel) else {}
    current: dict[str, Any] = {}
    for field in rt_fields:
        try:
            current[field.cache_attr] = get_nested_value(instance_dict, field.cache_attr)
        except PathNotFoundError:
            current[field.cache_attr] = field.default

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
