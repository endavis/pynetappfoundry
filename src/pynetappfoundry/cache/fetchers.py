"""Generic fetch dispatcher driven by TypeMapping metadata.

This module implements the pure-fetch layer described in
`ADR-0013 <../../../docs/decisions/0013-datasource-as-a-thin-facade-over-the-collector.md>`_
(§1, §2, §5). A single module-level :func:`fetch` function takes a Pydantic
model class, resolves its :class:`TypeMapping` via
:meth:`ModelRegistry.get_mapping_by_model_class`, and dispatches entirely
on declared metadata:

- ``mapping.cli_command`` non-empty → CLI path (raises
  :class:`NotImplementedError` pointing at #532 until Phase 4+).
- ``mapping.parent_mapping`` non-None → parameterized endpoint; parent
  objects are themselves fetched via a recursive :func:`fetch` call and
  each parent's ``parent_id_field`` is substituted into the endpoint URL.
- ``mapping.response_shape == "singleton"`` → ``call_endpoint`` (no
  pagination) + :func:`parse_api_record`.
- Otherwise → ``get_all_records`` + :func:`parse_api_response`.

Post-collection hooks declared on :class:`FieldMapping` with
``cache_strategy="derived"`` are invoked against the fetched instances
before return. The only cross-model hook dependency hardcoded here is
``compute_is_ha``: when the resolved mapping is ``CLUSTER_MAPPING`` and
no ``results_cache`` is supplied, this module recursively fetches
:class:`OntapNodeResponse` to populate ``results["nodes"]``. A general
``FieldMapping.depends_on=[...]`` mechanism is deferred (see ADR-0013 §5)
until a second derived field with cross-model dependencies appears.
"""

from __future__ import annotations

import logging
from functools import partial
from typing import TYPE_CHECKING, Any, cast

from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import (
    TypeMapping,
)
from pynetappfoundry.cache.field_mapping import (
    parse_api_record as _parse_api_record_raw,
)
from pynetappfoundry.cache.field_mapping import (
    parse_api_response as _parse_api_response_raw,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
    from pynetappfoundry.clients.ontap.cli import ONTAPCLI

logger = logging.getLogger(__name__)

# Cache-collector style: skip realtime fields when parsing bulk fetches so
# volatile metrics are not persisted into the cache snapshot.
_parse_api_record = partial(_parse_api_record_raw, skip_realtime=True)
_parse_api_response = partial(_parse_api_response_raw, skip_realtime=True)


def _noop_log_missing(
    _record: dict[str, Any],
    _expected_fields: list[str],
    _record_type: str,
    _record_id: str,
) -> None:
    """Default missing-field logger used when no callback is supplied."""
    return None


def _resolve_dotted_attr(obj: object, dotted_path: str) -> Any:
    """Resolve a dotted attribute path on an object.

    Returns ``None`` if any intermediate attribute is missing or ``None``.
    """
    current: Any = obj
    for part in dotted_path.split("."):
        current = getattr(current, part, None)
        if current is None:
            return None
    return current


def _run_post_collection_hooks(
    mapping: TypeMapping,
    items: list[BaseModel],
    results_cache: dict[str, Any],
    log_prefix: str,
) -> list[BaseModel]:
    """Run every ``post_collection`` callable on each fetched instance.

    Args:
        mapping: The TypeMapping whose derived fields should be evaluated.
        items: Fetched instances (possibly empty).
        results_cache: Cross-model results dict passed to each hook.
        log_prefix: Prefix for log messages.

    Returns:
        Updated list (same length) with hook-computed fields populated.
    """
    derived = mapping.derived_fields()
    if not derived or not items:
        return items
    for field in derived:
        if field.post_collection is None:
            continue
        try:
            items = [field.post_collection(item, results_cache) for item in items]
        except Exception:
            logger.error(
                "%s DERIVED_FIELD_FAILURE: %s.%s - post_collection error",
                log_prefix,
                mapping.name,
                field.cache_attr,
            )
            raise
    return items


def _fetch_flat(
    mapping: TypeMapping,
    api_client: ONTAPAPIClient,
    log_prefix: str,
) -> list[BaseModel]:
    """Fetch a flat (non-parameterized) endpoint via the ONTAP API client.

    Dispatches on ``mapping.response_shape``:

    - ``"singleton"`` → ``call_endpoint`` (paginate=False), then
      :func:`parse_api_record` on the raw dict.
    - ``"envelope"`` → ``get_all_records``, then :func:`parse_api_response`
      over the records list.

    Args:
        mapping: TypeMapping for the target model.
        api_client: ONTAP API client.
        log_prefix: Prefix for log messages.

    Returns:
        List of parsed model instances. Singleton responses are wrapped
        in a single-element list so callers can treat all shapes uniformly.
    """
    url = mapping.build_collection_url()
    if mapping.response_shape == "singleton":
        logger.debug("%s API call (singleton): GET %s", log_prefix, url)
        response = api_client.call_endpoint(url, method="GET")
        if not response:
            return []
        record_id = response.get(mapping.id_field, response.get("uuid", "unknown"))
        logger.debug("%s API response: %s=%s", log_prefix, mapping.name, record_id)
        return [_parse_api_record(mapping, response, log_prefix)]

    logger.debug("%s API call: GET %s", log_prefix, url)
    response = api_client.get_all_records(url, method="GET")
    if not response:
        return []
    return _parse_api_response(mapping, response, log_prefix, _noop_log_missing)


def _fetch_parameterized(
    mapping: TypeMapping,
    parent_objects: Sequence[BaseModel],
    api_client: ONTAPAPIClient,
    log_prefix: str,
) -> list[BaseModel]:
    """Fetch child records from a parameterized endpoint by iterating parents.

    For each parent object, substitutes the parent's identifier into the
    URL placeholder, fetches child records, and aggregates them. API
    failures on individual parents are logged as warnings and skipped
    (matching the original collector semantics).

    Args:
        mapping: Child TypeMapping (must have parent_mapping and
            parent_id_field set).
        parent_objects: Already-collected parent model instances.
        api_client: ONTAP API client.
        log_prefix: Prefix for log messages.

    Returns:
        Aggregated list of child model instances across all parents.

    Raises:
        ValueError: If ``mapping.parent_mapping`` or
            ``mapping.parent_id_field`` is not set.
    """
    if not mapping.parent_mapping:
        raise ValueError(f"{mapping.name}: parent_mapping must be set for parameterized collection")
    if not mapping.parent_id_field:
        raise ValueError(
            f"{mapping.name}: parent_id_field must be set for parameterized collection"
        )

    aggregated: list[BaseModel] = []
    for parent in parent_objects:
        parent_id = _resolve_dotted_attr(parent, mapping.parent_id_field)
        if not parent_id:
            parent_name = getattr(parent, "name", repr(parent))
            logger.warning(
                "%s SKIP_PARENT: %s - parent %s has no '%s'",
                log_prefix,
                mapping.name,
                parent_name,
                mapping.parent_id_field,
            )
            continue

        url = mapping.build_parameterized_url(str(parent_id))
        try:
            response = api_client.get_all_records(url, method="GET")
            children = _parse_api_response(mapping, response, log_prefix, _noop_log_missing)
            aggregated.extend(children)
        except Exception as e:
            parent_name = getattr(parent, "name", repr(parent))
            logger.warning(
                "%s CHILD_FETCH_FAILED: %s for parent %s - %s: %s",
                log_prefix,
                mapping.name,
                parent_name,
                type(e).__name__,
                e,
            )

    return aggregated


def fetch[T: BaseModel](
    model_class: type[T],
    cluster: str,
    config: Any,
    api_client: ONTAPAPIClient,
    *,
    cli_client: ONTAPCLI | None = None,
    results_cache: dict[str, Any] | None = None,
    log_prefix: str = "",
) -> list[T] | T:
    """Generic fetch dispatcher driven by TypeMapping metadata.

    Resolves the :class:`TypeMapping` for ``model_class`` and dispatches
    on ``cli_command`` / ``parent_mapping`` / ``response_shape``. See the
    module docstring for the full dispatch rules.

    Args:
        model_class: Pydantic model class registered on a TypeMapping.
        cluster: Cluster name (used for log context only in this phase).
        config: Global ``Config`` instance. Currently unused by the fetch
            path; accepted to match ADR-0013's planned signature so that
            Phase 3 (``OntapBackend`` rewrite) does not need to change the
            call sites again.
        api_client: ONTAP REST API client.
        cli_client: Optional SSH/CLI client. Only consulted when the
            mapping declares ``cli_command`` (deferred to #532).
        results_cache: Optional shared results dict. When supplied it is
            passed to every ``post_collection`` hook (so ``compute_is_ha``
            can short-circuit to already-fetched nodes). When omitted and
            the resolved mapping's derived fields depend on nodes, this
            function recursively fetches :class:`OntapNodeResponse` to
            populate ``results_cache["nodes"]``.
        log_prefix: Prefix for log messages.

    Returns:
        For singleton mappings, a single model instance. For all other
        mappings, a list of model instances.

    Raises:
        NotImplementedError: If the mapping's ``cli_command`` is set
            (CLI dispatch is deferred to #532).
        ValueError: If no TypeMapping is registered for ``model_class``.
    """
    del cluster  # reserved for logging / future use
    del config
    del cli_client  # reserved for CLI dispatch (#532)

    mapping = model_registry.get_mapping_by_model_class(model_class)
    if mapping is None:
        raise ValueError(
            f"fetch(): no TypeMapping registered for model class "
            f"{model_class.__module__}.{model_class.__name__}"
        )

    if mapping.cli_command:
        raise NotImplementedError(
            f"fetch(): CLI dispatch for {mapping.name} (cli_command="
            f"{mapping.cli_command!r}) is not yet supported; tracked in "
            f"https://github.com/endavis/pynetappfoundry/issues/532"
        )

    # Prepare results_cache used by post-collection hooks.
    local_cache: dict[str, Any] = results_cache if results_cache is not None else {}

    # Hardcoded cross-model dependency: compute_is_ha needs results["nodes"].
    # See ADR-0013 §5 amendment — a general FieldMapping.depends_on=[...]
    # mechanism will be added when a second derived field needs one.
    if results_cache is None and "nodes" not in local_cache and _needs_nodes_dependency(mapping):
        # Avoid a circular dependency: only import the node mapping's model
        # class lazily when the hook actually needs it.
        from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse

        nodes_result = fetch(
            OntapNodeResponse,
            cluster="",
            config=None,
            api_client=api_client,
            log_prefix=log_prefix,
        )
        local_cache["nodes"] = nodes_result if isinstance(nodes_result, list) else [nodes_result]

    # Fetch instances.
    if mapping.parent_mapping:
        # Parent objects must already be in results_cache. The collector
        # threads this via `_collect_svm_top_metrics_users` and composite
        # assembly; tests may pass a synthetic results_cache.
        parent_key = _results_key_for_parent(mapping.parent_mapping)
        parents: Sequence[BaseModel] = local_cache.get(parent_key, [])
        items = _fetch_parameterized(mapping, parents, api_client, log_prefix)
    else:
        items = _fetch_flat(mapping, api_client, log_prefix)

    # Run post-collection hooks against the fetched instances.
    items = _run_post_collection_hooks(mapping, items, local_cache, log_prefix)

    if mapping.response_shape == "singleton":
        if not items:
            # Singleton endpoint returned nothing — fall back to an empty
            # model instance, matching the original collector behavior.
            return cast(T, mapping.model_class())
        return cast(T, items[0])
    return cast("list[T]", items)


def _needs_nodes_dependency(mapping: TypeMapping) -> bool:
    """Return True if any derived-field hook on ``mapping`` needs ``results['nodes']``.

    Phase 2 only recognizes ``compute_is_ha`` from
    ``pynetappfoundry.cache.ontap.cluster.mapping``. A general mechanism
    is deferred (ADR-0013 §5).
    """
    for field in mapping.derived_fields():
        hook = field.post_collection
        if hook is None:
            continue
        if getattr(hook, "__name__", "") == "compute_is_ha":
            return True
    return False


def _results_key_for_parent(parent_mapping_name: str) -> str:
    """Map a parent mapping name to its ``results_cache`` key.

    The convention is simple: callers store parents under the parent
    mapping's registry name (e.g. ``"OntapSvm"`` → ``results_cache["OntapSvm"]``).
    This avoids fragile snake_case heuristics. Phase 3 (DataSource
    rewrite) will codify this as the public contract; the collector's
    existing parameterized path bypasses this helper entirely by
    calling :func:`_fetch_parameterized` directly with explicit parents.
    """
    return parent_mapping_name


__all__ = ["fetch"]
