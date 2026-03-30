"""Fluent query interface for ONTAP models.

Provides :class:`QuerySet`, a lazy, chainable query builder that translates
model attribute filters into ONTAP REST API queries using the existing
:class:`~pynetappfoundry.cache.field_mapping.TypeMapping` metadata.
"""

from __future__ import annotations

import copy
import logging
from typing import Any, TypeVar
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import TypeMapping, parse_api_response
from pynetappfoundry.clients.openapi import APIWrapper
from pynetappfoundry.query.exceptions import MultipleResultsError, NotFoundError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def _log_missing_fields(
    record: dict[str, Any],
    expected: list[str],
    type_name: str,
    record_id: str,
) -> None:
    """Log missing fields at debug level.

    Simple callback satisfying the ``log_missing_fn`` signature required
    by :func:`~pynetappfoundry.cache.field_mapping.parse_api_response`.
    """
    missing = [f for f in expected if f not in record]
    if missing:
        logger.debug(
            "QuerySet %s[%s]: missing fields %s",
            type_name,
            record_id,
            missing,
        )


class QuerySet:
    """Lazy, chainable query builder for ONTAP models.

    Uses :class:`~pynetappfoundry.cache.field_mapping.TypeMapping` metadata
    to translate model attribute names to API field paths and build correct
    REST API URLs.

    Type Parameters:
        T: The model class (a :class:`~pydantic.BaseModel` subclass).

    Example::

        vols = QuerySet(OntapVolume, client).filter(svm_name="vs1").all()
        vol = QuerySet(OntapVolume, client).get(uuid="abc-123")
    """

    def __init__(
        self,
        model_class: type[T],
        client: APIWrapper,
    ) -> None:
        self._model_class = model_class
        self._client = client
        self._mapping = self._resolve_mapping(model_class)
        self._filters: dict[str, Any] = {}
        self._fields_list: list[str] = []
        self._order_by_list: list[str] = []
        self._max_records: int | None = None

    @staticmethod
    def _resolve_mapping(model_class: type[T]) -> TypeMapping:
        """Look up TypeMapping from the model registry.

        Raises:
            ValueError: If no mapping is registered for the model class.
        """
        mapping = model_registry.get_mapping(model_class.__name__)
        if mapping is None:
            msg = (
                f"No TypeMapping registered for '{model_class.__name__}'. "
                f"Ensure the model's mapping module has been imported."
            )
            raise ValueError(msg)
        return mapping

    # ------------------------------------------------------------------
    # Chaining methods
    # ------------------------------------------------------------------

    def filter(self, **kwargs: Any) -> QuerySet:
        """Return a new QuerySet with additional API-side filters.

        Keys are model attribute names (e.g. ``svm_name``), which are
        translated to API field paths (e.g. ``svm.name``) via the
        TypeMapping.  Unknown attributes are passed through as-is,
        allowing raw API field names.
        """
        clone = self._clone()
        for attr, value in kwargs.items():
            api_path = self._attr_to_api_path(attr)
            clone._filters[api_path] = value
        return clone

    def fields(self, *names: str) -> QuerySet:
        """Return a new QuerySet with explicit field projection.

        Overrides the default ``fields=*`` from the endpoint.  Field
        names are model attribute names, translated to API paths.
        """
        clone = self._clone()
        clone._fields_list = [self._attr_to_api_path(n) for n in names]
        return clone

    def order_by(self, *field_specs: str) -> QuerySet:
        """Return a new QuerySet with ordering.

        Each *field_spec* is a model attribute name optionally followed
        by `` asc`` or `` desc`` (e.g. ``"name asc"``).  The attribute
        portion is translated to the API path.
        """
        clone = self._clone()
        translated: list[str] = []
        for spec in field_specs:
            parts = spec.split(None, 1)
            attr = parts[0]
            suffix = f" {parts[1]}" if len(parts) > 1 else ""
            translated.append(f"{self._attr_to_api_path(attr)}{suffix}")
        clone._order_by_list = translated
        return clone

    def limit(self, n: int) -> QuerySet:
        """Return a new QuerySet limited to *n* records."""
        clone = self._clone()
        clone._max_records = n
        return clone

    # ------------------------------------------------------------------
    # Terminal methods
    # ------------------------------------------------------------------

    def all(self) -> list[Any]:
        """Execute the query and return all matching model instances."""
        url = self._build_url()
        response = self._client.get_all_records(url)
        return parse_api_response(
            self._mapping,
            response,
            f"QuerySet<{self._mapping.name}>",
            _log_missing_fields,
        )

    def first(self) -> Any | None:
        """Execute the query and return the first result, or ``None``."""
        results = self.limit(1).all()
        return results[0] if results else None

    def get(self, **kwargs: Any) -> Any:
        """Return exactly one result matching *kwargs*.

        Raises:
            NotFoundError: If zero results are returned.
            MultipleResultsError: If more than one result is returned.
        """
        qs = self.filter(**kwargs) if kwargs else self
        results = qs.all()
        if len(results) == 0:
            merged_filters = {
                **self._filters,
                **{self._attr_to_api_path(k): v for k, v in kwargs.items()},
            }
            raise NotFoundError(self._mapping.name, merged_filters)
        if len(results) > 1:
            merged_filters = {
                **self._filters,
                **{self._attr_to_api_path(k): v for k, v in kwargs.items()},
            }
            raise MultipleResultsError(self._mapping.name, len(results), merged_filters)
        return results[0]

    def count(self) -> int:
        """Return the number of matching records without fetching them."""
        url = self._build_url(return_records=False)
        response = self._client.call_endpoint(url)
        if isinstance(response, dict):
            return int(response.get("num_records", 0))
        return 0

    def __iter__(self) -> Any:
        """Iterate over all results."""
        return iter(self.all())

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _clone(self) -> QuerySet:
        """Return a shallow copy with deep-copied mutable state."""
        clone = copy.copy(self)
        clone._filters = dict(self._filters)
        clone._fields_list = list(self._fields_list)
        clone._order_by_list = list(self._order_by_list)
        return clone

    def _attr_to_api_path(self, attr: str) -> str:
        """Translate a model attribute name to an API field path.

        Iterates TypeMapping.fields looking for a FieldMapping whose
        ``cache_attr`` matches *attr*.  Returns the corresponding
        ``api_path`` if found, otherwise returns *attr* unchanged
        (allowing raw API field names).
        """
        for field in self._mapping.fields:
            if field.cache_attr == attr and field.api_path is not None:
                return field.api_path
        return attr

    def _build_url(self, *, return_records: bool = True) -> str:
        """Build the full API URL from the TypeMapping and query state.

        Starts from ``TypeMapping.build_collection_url()``, parses it,
        then merges filters, fields, order_by, and max_records into the
        query parameters.
        """
        base_url = self._mapping.build_collection_url()
        parsed = urlparse(base_url)
        params = parse_qs(parsed.query, keep_blank_values=True)

        # Merge filters
        for key, value in self._filters.items():
            params[key] = [str(value)]

        # Override fields if explicitly set
        if self._fields_list:
            params["fields"] = [",".join(self._fields_list)]

        # Add ordering
        if self._order_by_list:
            params["order_by"] = [",".join(self._order_by_list)]

        # Add max_records
        if self._max_records is not None:
            params["max_records"] = [str(self._max_records)]

        # Add return_records=false for count queries
        if not return_records:
            params["return_records"] = ["false"]

        query_string = urlencode(params, doseq=True)
        return urlunparse(parsed._replace(query=query_string))
