"""Declarative field mapping framework for API data collection.

Provides dataclasses and generic parsers that map API and CLI responses
to cache model objects using declarative field definitions.

Example:
    >>> from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
    >>> mapping = FieldMapping(cache_attr="name", api_path="name", cli_field="volume")
    >>> mapping.cache_attr
    'name'
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from pynetappfoundry.utils.dict_path import PathNotFoundError, get_nested_value

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class FieldMapping:
    """Maps a single field between API response, CLI output, and cache model attribute.

    Attributes:
        cache_attr: Model attribute name on the target dataclass.
        api_path: Dot-path for API extraction (e.g. ``"svm.name"``).
        cli_field: Hyphenated CLI field name (e.g. ``"vserver"``).
        default: Default value when the field is missing.
        transform: Custom API extraction function receiving the full record dict.
            Overrides ``api_path`` when set.
        cli_transform: Custom CLI extraction function receiving the full record dict.
            Overrides ``cli_field`` when set.
    """

    cache_attr: str
    api_path: str | None = None
    cli_field: str | None = None
    default: Any = ""
    transform: Callable[[dict[str, Any]], Any] | None = None
    cli_transform: Callable[[dict[str, Any]], Any] | None = None


@dataclass(frozen=True)
class TypeMapping:
    """Declarative mapping definition for an API object type.

    Attributes:
        name: Human-readable type name (e.g. ``"Volume"``).
        model_class: Pydantic model class for the cache object.
        api_endpoint: REST API endpoint including query params.
        cli_command: CLI show command name. Empty string if not applicable.
        fields: Tuple of field mapping definitions.
        id_field: Field used for log identification.
        records_path: Dot-notation path to the records list in the API response
            envelope (e.g. ``"records"`` for ONTAP, ``"_embedded.items"`` for
            other APIs). Default: ``"records"``.
        api_type: Tag identifying which API client/unit registry to use
            (e.g. ``"ontap"``, ``"aiqum"``). Default: ``"ontap"``.
    """

    name: str
    model_class: type[BaseModel]
    api_endpoint: str
    cli_command: str = ""
    fields: tuple[FieldMapping, ...] = ()
    id_field: str = "name"
    records_path: str = "records"
    api_type: str = "ontap"

    def api_expected_fields(self) -> list[str]:
        """Derive top-level API keys expected in a response record.

        Extracts the first segment of each ``api_path`` (before any dot or
        bracket), deduplicates, and sorts alphabetically.

        Returns:
            Sorted list of unique top-level API field names.
        """
        keys: set[str] = set()
        for field in self.fields:
            if field.api_path is not None:
                first_segment = field.api_path.split(".")[0].split("[")[0]
                keys.add(first_segment)
        return sorted(keys)

    def cli_expected_fields(self) -> list[str]:
        """Derive CLI field names expected in a CLI record.

        Returns:
            Sorted list of unique CLI field names (excludes transform-only fields).
        """
        keys: set[str] = set()
        for field in self.fields:
            if field.cli_field is not None:
                keys.add(field.cli_field)
        return sorted(keys)


def _coerce_cli_value(value: str, default: Any) -> Any:
    """Coerce a CLI string value to match the default's type.

    ONTAP CLI conventions handled:
    - ``"-"`` means missing/N/A → returns default
    - ``"%"`` suffix on thresholds → stripped before int conversion
    - ``"true"``/``"false"``/``"on"``/``"off"`` for booleans

    Args:
        value: Raw CLI string value.
        default: Default value whose type guides coercion.

    Returns:
        Coerced value matching the default's type.
    """
    value = value.strip()
    if value in ("-", ""):
        return default
    if isinstance(default, bool):
        return value.lower() in ("true", "yes", "1", "on")
    if isinstance(default, int):
        cleaned = value.rstrip("%")
        try:
            return int(cleaned)
        except (ValueError, TypeError):
            return default
    return value


def parse_api_record(
    mapping: TypeMapping,
    record: dict[str, Any],
    log_prefix: str,
) -> BaseModel:
    """Parse a single API response record into a model instance.

    For each field: uses ``transform(record)`` if set, otherwise extracts
    via ``get_nested_value(record, api_path)``. Falls back to default on
    ``PathNotFoundError``. Transform exceptions propagate (logged as
    ``TRANSFORM_FAILURE``).

    Args:
        mapping: Type mapping definition.
        record: Single API response record dict.
        log_prefix: Prefix for log messages.

    Returns:
        Populated model instance.
    """
    kwargs: dict[str, Any] = {}
    for field in mapping.fields:
        if field.transform is not None:
            try:
                kwargs[field.cache_attr] = field.transform(record)
            except Exception:
                logger.error(
                    "%s TRANSFORM_FAILURE: %s '%s' - transform error for field '%s'",
                    log_prefix,
                    mapping.name,
                    record.get(mapping.id_field, record.get("uuid", "unknown")),
                    field.cache_attr,
                )
                raise
        elif field.api_path is not None:
            try:
                kwargs[field.cache_attr] = get_nested_value(record, field.api_path)
            except PathNotFoundError:
                kwargs[field.cache_attr] = field.default
        else:
            kwargs[field.cache_attr] = field.default
    return mapping.model_class(**kwargs)


def parse_cli_record(
    mapping: TypeMapping,
    record: dict[str, Any],
    log_prefix: str,
) -> BaseModel:
    """Parse a single CLI output record into a model instance.

    For each field: uses ``cli_transform(record)`` if set, otherwise looks
    up ``record.get(cli_field)`` with type coercion via ``_coerce_cli_value``.

    Args:
        mapping: Type mapping definition.
        record: Single CLI output record dict.
        log_prefix: Prefix for log messages.

    Returns:
        Populated model instance.
    """
    kwargs: dict[str, Any] = {}
    for field in mapping.fields:
        if field.cli_transform is not None:
            try:
                kwargs[field.cache_attr] = field.cli_transform(record)
            except Exception:
                logger.error(
                    "%s TRANSFORM_FAILURE: %s - cli_transform error for field '%s'",
                    log_prefix,
                    mapping.name,
                    field.cache_attr,
                )
                raise
        elif field.cli_field is not None:
            raw = record.get(field.cli_field)
            if raw is None:
                kwargs[field.cache_attr] = field.default
            elif isinstance(raw, str):
                kwargs[field.cache_attr] = _coerce_cli_value(raw, field.default)
            else:
                kwargs[field.cache_attr] = raw
        else:
            kwargs[field.cache_attr] = field.default
    return mapping.model_class(**kwargs)


def parse_api_response(
    mapping: TypeMapping,
    response: Any,
    log_prefix: str,
    log_missing_fn: Callable[
        [dict[str, Any], list[str], str, str],
        None,
    ],
) -> list[BaseModel]:
    """Parse a full API response into a list of model instances.

    Extracts the records list from the response using ``mapping.records_path``
    (supports dot-notation for nested envelopes), logs missing fields via the
    provided callback, and delegates each record to ``parse_api_record``.

    Args:
        mapping: Type mapping definition.
        response: Full API response dict or None.
        log_prefix: Prefix for log messages.
        log_missing_fn: Callback for logging missing fields.

    Returns:
        List of populated model instances.
    """
    if not response:
        return []

    try:
        records = get_nested_value(response, mapping.records_path)
    except PathNotFoundError:
        records = []
    logger.debug("%s API response: %d %ss", log_prefix, len(records), mapping.name.lower())

    expected = mapping.api_expected_fields()
    results: list[BaseModel] = []
    for record in records:
        record_id = record.get(mapping.id_field, record.get("uuid", "unknown"))
        log_missing_fn(record, expected, mapping.name, record_id)
        results.append(parse_api_record(mapping, record, log_prefix))
    return results


def parse_cli_records(
    mapping: TypeMapping,
    records: list[dict[str, Any]],
    log_prefix: str,
    log_missing_fn: Callable[
        [dict[str, Any], list[str], str, str],
        None,
    ],
) -> list[BaseModel]:
    """Parse CLI output records into a list of model instances.

    Args:
        mapping: Type mapping definition.
        records: List of CLI output record dicts.
        log_prefix: Prefix for log messages.
        log_missing_fn: Callback for logging missing fields.

    Returns:
        List of populated model instances.
    """
    if not records:
        return []

    logger.debug("%s CLI response: %d %ss", log_prefix, len(records), mapping.name.lower())

    expected = mapping.cli_expected_fields()
    results: list[BaseModel] = []
    for record in records:
        id_field_mapping = next(
            (f for f in mapping.fields if f.cache_attr == mapping.id_field),
            None,
        )
        cli_id_key: str = mapping.id_field
        if id_field_mapping and id_field_mapping.cli_field:
            cli_id_key = id_field_mapping.cli_field
        record_id = record.get(cli_id_key, "unknown")
        log_missing_fn(record, expected, f"{mapping.name}(CLI)", record_id)
        results.append(parse_cli_record(mapping, record, log_prefix))
    return results
