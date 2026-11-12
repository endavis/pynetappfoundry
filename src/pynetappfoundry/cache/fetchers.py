"""Generic fetch dispatcher driven by TypeMapping metadata.

This module implements the pure-fetch layer described in
`ADR-0013 <../../../docs/decisions/0013-datasource-as-a-thin-facade-over-the-collector.md>`_
(§1, §2, §5). A single module-level :func:`fetch` function takes a Pydantic
model class, resolves its :class:`TypeMapping` via
:meth:`ModelRegistry.get_mapping_by_model_class`, and dispatches entirely
on declared metadata:

- ``mapping.cli_command`` non-empty → CLI path via :func:`_fetch_cli`.
  The CLI client executes the command, raw output is parsed into dicts
  by :func:`parse_vm_instance_output`, and records are fed through
  :func:`parse_cli_records`.
- ``mapping.parent_mapping`` non-None → parameterized endpoint; parent
  objects come from ``results_cache`` or are fetched on demand via a
  recursive :func:`fetch` call (:func:`fetch_parents`, #975) and
  each parent's ``parent_id_field`` is substituted into the endpoint URL.
- ``mapping.response_shape == "computed"`` → no request; an empty model
  instance is built and filled by the derived-field hooks (ADR-0024).
- ``mapping.response_shape == "singleton"`` → ``call_endpoint`` (no
  pagination) + :func:`parse_api_record`.
- Otherwise → ``get_all_records`` + :func:`parse_api_response`.

Post-collection hooks declared on :class:`FieldMapping` with
``cache_strategy="derived"`` are invoked against the fetched instances
before return. Cross-model dependencies are declared via
``FieldMapping.depends_on=(<ModelClass>, ...)``: this module iterates
every derived field's ``depends_on`` tuple and, for each dependency
missing from the shared ``results_cache``, recursively calls
:func:`fetch` to populate it. Results are keyed by the dependency's
``__name__`` so callers that pre-populate the cache (e.g. the
``MetadataCollector``) short-circuit the recursive fetch. See ADR-0013
§5 for the full design.
"""

from __future__ import annotations

import logging
import re
from functools import partial
from typing import TYPE_CHECKING, Any, cast

from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import (
    TypeMapping,
    parse_cli_records,
)
from pynetappfoundry.cache.field_mapping import (
    parse_api_record as _parse_api_record_raw,
)
from pynetappfoundry.cache.field_mapping import (
    parse_api_response as _parse_api_response_raw,
)

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence

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


def _resolve_parent_ids(
    mapping: TypeMapping, parent: BaseModel
) -> tuple[tuple[str, ...] | None, str | None]:
    """Resolve every parent field that fills the child's path placeholders.

    Args:
        mapping: Child TypeMapping (``effective_parent_id_fields()`` non-empty).
        parent: Parent model instance.

    Returns:
        ``(values, None)`` when every field has a value, else
        ``(None, field)`` naming the first field with no value. Only
        ``None`` and the empty string count as missing; ``0`` and other
        falsy but valid identifiers are substituted as ``str(value)``.
    """
    values: list[str] = []
    for field in mapping.effective_parent_id_fields():
        value = _resolve_dotted_attr(parent, field)
        if value is None or value == "":
            return None, field
        values.append(str(value))
    return tuple(values), None


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


def normalize_cli_key(key: str) -> str:
    """Normalize a CLI output key to snake_case.

    Converts spaces and hyphens to underscores, lowercases the string,
    and strips non-alphanumeric characters (except underscores).

    This is extracted from ``MetadataCollector._normalize_cli_key``
    so both the collector and :func:`_fetch_cli` share the same logic.

    Args:
        key: Original key from CLI output.

    Returns:
        Normalized key name.
    """
    normalized = key.lower().replace(" ", "_").replace("-", "_")
    normalized = re.sub(r"[^a-z0-9_]", "", normalized)
    return normalized


def parse_vm_instance_output(output: list[str]) -> list[dict[str, str]]:
    """Parse ``virtual-machine instance show`` CLI output into raw records.

    The CLI output contains key-value pairs (``Key: Value``) for each
    node, separated by new ``Node:`` entries.  Each node's data becomes
    one dict with :func:`normalize_cli_key`-normalised keys.

    This is extracted from ``MetadataCollector._parse_vm_instance_output``
    so both the collector and :func:`_fetch_cli` share the same logic.

    Args:
        output: Lines of CLI output.

    Returns:
        List of raw record dicts (one per node) with normalized keys.
    """
    results: list[dict[str, str]] = []
    current_data: dict[str, str] = {}
    current_node: str = ""

    for line in output:
        line = line.strip()
        if not line:
            continue

        if ":" not in line:
            continue

        parts = line.split(":", 1)
        if len(parts) != 2:
            continue

        key = parts[0].strip()
        value = parts[1].strip()
        key_normalized = normalize_cli_key(key)

        if key_normalized == "node":
            if current_node and current_data:
                current_data["node"] = current_node
                results.append(current_data)
            current_node = value
            current_data = {}
        else:
            current_data[key_normalized] = value

    if current_node and current_data:
        current_data["node"] = current_node
        results.append(current_data)

    if not results and current_data:
        current_data["node"] = ""
        results.append(current_data)

    return results


def _fetch_cli(
    mapping: TypeMapping,
    cli_client: ONTAPCLI,
    log_prefix: str,
) -> list[BaseModel]:
    """Fetch records via CLI command execution and parsing.

    Runs the mapping's ``cli_command`` through *cli_client*, parses
    the raw text output into dict records via
    :func:`parse_vm_instance_output`, and feeds them through
    :func:`parse_cli_records`.

    Args:
        mapping: TypeMapping with a non-empty ``cli_command``.
        cli_client: SSH/CLI client to run the command on.
        log_prefix: Prefix for log messages.

    Returns:
        List of parsed model instances.
    """
    logger.debug("%s CLI command: %s", log_prefix, mapping.cli_command)
    output = cli_client.run_command(mapping.cli_command)
    logger.debug("%s CLI response: %d lines", log_prefix, len(output))
    records = parse_vm_instance_output(output)
    return parse_cli_records(mapping, records, log_prefix, _noop_log_missing)


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
    if not mapping.effective_parent_id_fields():
        raise ValueError(
            f"{mapping.name}: parent_id_field must be set for parameterized collection"
        )

    aggregated: list[BaseModel] = []
    for parent, url in iter_parent_urls(mapping, parent_objects, log_prefix):
        try:
            if mapping.response_shape == "singleton":
                record = api_client.call_endpoint(url, method="GET")
                if record:
                    aggregated.append(_parse_api_record(mapping, record, log_prefix))
            else:
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


def iter_parent_urls(
    mapping: TypeMapping,
    parent_objects: Sequence[BaseModel],
    log_prefix: str,
) -> Iterator[tuple[BaseModel, str]]:
    """Yield ``(parent, resolved_url)`` for each parent that fills the placeholders.

    A parent with no value for one of ``mapping``'s parent id fields is
    skipped with a ``SKIP_PARENT`` warning.

    Args:
        mapping: Child TypeMapping with ``parent_id_field(s)`` set.
        parent_objects: Parent model instances.
        log_prefix: Prefix for log messages.

    Yields:
        Each usable parent and the child endpoint URL resolved for it.
    """
    for parent in parent_objects:
        values, missing = _resolve_parent_ids(mapping, parent)
        if values is None:
            parent_name = getattr(parent, "name", repr(parent))
            logger.warning(
                "%s SKIP_PARENT: %s - parent %s has no '%s'",
                log_prefix,
                mapping.name,
                parent_name,
                missing,
            )
            continue
        yield parent, mapping.build_parameterized_url(values[0] if len(values) == 1 else values)


def _validate_parent_chain(mapping: TypeMapping) -> None:
    """Raise ``ValueError`` if the parent chain has an unregistered link or a cycle."""
    seen = [mapping.name]
    current = mapping
    while current.parent_mapping:
        parent = model_registry.get_mapping(current.parent_mapping)
        if parent is None:
            raise ValueError(
                f"{current.name}: parent mapping {current.parent_mapping!r} is not registered"
            )
        if parent.name in seen:
            raise ValueError(
                f"{mapping.name}: parent_mapping cycle: {' -> '.join([*seen, parent.name])}"
            )
        seen.append(parent.name)
        current = parent


def fetch_parents(
    mapping: TypeMapping,
    api_client: ONTAPAPIClient,
    results_cache: dict[str, Any],
    log_prefix: str = "",
) -> list[BaseModel]:
    """Return the parent instances of a child *mapping*, fetching them if absent.

    ``results_cache[parent_mapping]`` is used when present (an empty list
    counts as present). Otherwise the parent model is fetched through
    :func:`fetch` with the same cache, so multi-level chains recurse, and
    stored under that key.

    Raises:
        ValueError: If a parent mapping in the chain is not registered, or the
            chain has a cycle. Raised before any request is made.
    """
    parent_key = _results_key_for_parent(mapping.parent_mapping or "")
    if parent_key in results_cache:
        return list(results_cache[parent_key])
    _validate_parent_chain(mapping)
    parent_map = model_registry.get_mapping(parent_key)
    if parent_map is None:  # pragma: no cover - guarded by _validate_parent_chain
        raise ValueError(f"{mapping.name}: parent mapping {parent_key!r} is not registered")
    result = fetch(
        parent_map.model_class,
        cluster="",
        config=None,
        api_client=api_client,
        results_cache=results_cache,
        log_prefix=log_prefix,
    )
    parents: list[BaseModel] = list(result) if isinstance(result, list) else [result]
    results_cache[parent_key] = parents
    return parents


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
            passed to every ``post_collection`` hook so derived-field
            hooks can short-circuit to already-fetched dependencies.
            When omitted (or when a dependency declared via
            ``FieldMapping.depends_on`` is absent from the dict), this
            function recursively fetches the dependency and stores it
            under ``results_cache[dep_class.__name__]``.
        log_prefix: Prefix for log messages.

    Returns:
        For singleton and computed mappings, a single model instance. For all other
        mappings, a list of model instances.

    Raises:
        ValueError: If no TypeMapping is registered for ``model_class``,
            or if a CLI-only mapping is invoked without a ``cli_client``.
    """
    del cluster  # reserved for logging / future use
    del config

    mapping = model_registry.get_mapping_by_model_class(model_class)
    if mapping is None:
        raise ValueError(
            f"fetch(): no TypeMapping registered for model class "
            f"{model_class.__module__}.{model_class.__name__}. "
            f"Mappings are auto-registered; verify a mapping.py module "
            f"exists under cache/ontap/ for this model."
        )

    # Prepare results_cache used by post-collection hooks.
    local_cache: dict[str, Any] = results_cache if results_cache is not None else {}

    # Generic cross-model dependency resolution driven by
    # ``FieldMapping.depends_on``. For each derived-field hook, ensure
    # every declared dependency is populated in ``local_cache`` under the
    # dependency's ``__name__`` key before the hook runs. Callers that
    # pre-populate the cache (e.g. ``MetadataCollector``) short-circuit
    # this fan-out via the cache-hit check below. See ADR-0013 §5.
    for field in mapping.derived_fields():
        if field.post_collection is None or not field.depends_on:
            continue
        for dep_class in field.depends_on:
            dep_key = dep_class.__name__
            if dep_key in local_cache:
                continue
            dep_result = fetch(
                dep_class,
                cluster="",
                config=None,
                api_client=api_client,
                log_prefix=log_prefix,
            )
            local_cache[dep_key] = dep_result if isinstance(dep_result, list) else [dep_result]

    # Fetch instances — dispatch on CLI vs API path.
    if mapping.is_computed:
        # No endpoint: start from an empty model; the derived-field hooks
        # fill it from the dependencies resolved above (ADR-0024).
        items = [mapping.model_class()]
    elif mapping.cli_command:
        if cli_client is None:
            raise ValueError(
                f"fetch(): {mapping.name} requires cli_client (cli_command={mapping.cli_command!r})"
            )
        items = _fetch_cli(mapping, cli_client, log_prefix)
    elif mapping.parent_mapping:
        # Parents come from results_cache (the collector pre-populates it);
        # when absent they are fetched on demand, recursively (#975).
        parents = fetch_parents(mapping, api_client, local_cache, log_prefix)
        items = _fetch_parameterized(mapping, parents, api_client, log_prefix)
    else:
        items = _fetch_flat(mapping, api_client, log_prefix)

    # Run post-collection hooks against the fetched instances.
    items = _run_post_collection_hooks(mapping, items, local_cache, log_prefix)

    if mapping.parent_mapping is None and mapping.response_shape in ("singleton", "computed"):
        if not items:
            # Singleton endpoint returned nothing — fall back to an empty
            # model instance, matching the original collector behavior.
            return cast(T, mapping.model_class())
        return cast(T, items[0])
    return cast("list[T]", items)


def _results_key_for_parent(parent_mapping_name: str) -> str:
    """Map a parent mapping name to its ``results_cache`` key.

    The convention is simple: callers store parents under the parent
    mapping's registry name (e.g. ``"OntapSvm"`` → ``results_cache["OntapSvm"]``).
    This avoids fragile snake_case heuristics. Phase 3 (DataSource
    rewrite) will codify this as the public contract. :func:`fetch_parents`
    reads and fills this key; the collector's existing parameterized path
    bypasses it by calling :func:`_fetch_parameterized` directly with
    explicit parents.
    """
    return parent_mapping_name


__all__ = [
    "fetch",
    "fetch_parents",
    "iter_parent_urls",
    "normalize_cli_key",
    "parse_vm_instance_output",
]
