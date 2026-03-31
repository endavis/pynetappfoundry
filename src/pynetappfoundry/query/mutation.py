"""Write operations (POST/PATCH/DELETE) for ONTAP models.

Provides :class:`Mutation`, a high-level interface for creating, updating,
and deleting ONTAP resources using existing
:class:`~pynetappfoundry.cache.field_mapping.TypeMapping` metadata.
"""

from __future__ import annotations

import logging
from typing import Any, TypeVar

from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import TypeMapping, parse_api_record
from pynetappfoundry.clients.openapi import APIWrapper
from pynetappfoundry.core.models import RetryConfig

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def _set_nested(d: dict[str, Any], path: str, value: Any) -> None:
    """Set a value in a nested dict using a dot-separated path.

    Merges with existing keys so that sibling paths like ``svm.name``
    and ``svm.uuid`` produce ``{"svm": {"name": ..., "uuid": ...}}``.

    Args:
        d: Target dictionary (modified in place).
        path: Dot-separated key path (e.g. ``"svm.name"``).
        value: Value to set at the leaf.
    """
    keys = path.split(".")
    current = d
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value


class Mutation:
    """Write interface for ONTAP models.

    Translates model attribute names to nested API JSON and dispatches
    POST, PATCH, and DELETE requests via the API client.

    Example::

        m = Mutation(OntapVolume, client)
        vol = m.create(name="vol1", svm_name="vs1")
        m.update("uuid-123", state="offline")
        m.delete("uuid-123")
    """

    def __init__(
        self,
        model_class: type[T],
        client: APIWrapper,
    ) -> None:
        self._model_class = model_class
        self._client = client
        self._mapping = self._resolve_mapping(model_class)

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

    def create(
        self,
        *,
        poll: bool = False,
        poll_interval: float = 5,
        poll_timeout: float = 300,
        **kwargs: Any,
    ) -> Any:
        """Create a new resource via POST.

        Translates keyword arguments from model attribute names to nested
        API JSON.  Disables retry (POST is non-idempotent).

        Args:
            poll: If True and the response contains a job, block until
                the job completes and return the final
                :class:`~pynetappfoundry.models.ontap.cluster.jobs.model.OntapJob`.
            poll_interval: Seconds between poll requests (default 5).
            poll_timeout: Maximum seconds to wait (default 300).
            **kwargs: Model attribute name/value pairs.

        Returns:
            Parsed model instance, or :class:`OntapJob` when *poll* is True.
        """
        from pynetappfoundry.query.job import JobTracker

        body = self._build_body(kwargs)
        path = self._collection_path()
        logger.debug("Mutation.create %s: POST %s body=%s", self._mapping.name, path, body)
        response = self._client.call_endpoint(
            path,
            method="POST",
            body=body,
            retry_config=RetryConfig(enabled=False),
        )
        if poll and isinstance(response, dict) and "job" in response:
            tracker = JobTracker.from_response(
                response,
                self._client,
                poll_interval=poll_interval,
                poll_timeout=poll_timeout,
            )
            return tracker.wait()
        return self._parse_response(response)

    def update(
        self,
        uuid: str,
        *,
        poll: bool = False,
        poll_interval: float = 5,
        poll_timeout: float = 300,
        **kwargs: Any,
    ) -> Any:
        """Update an existing resource via PATCH.

        Args:
            uuid: Resource UUID.
            poll: If True and the response contains a job, block until
                the job completes and return the final
                :class:`~pynetappfoundry.models.ontap.cluster.jobs.model.OntapJob`.
            poll_interval: Seconds between poll requests (default 5).
            poll_timeout: Maximum seconds to wait (default 300).
            **kwargs: Model attribute name/value pairs to update.

        Returns:
            Parsed model instance, or :class:`OntapJob` when *poll* is True.
        """
        from pynetappfoundry.query.job import JobTracker

        body = self._build_body(kwargs)
        path = f"{self._collection_path()}/{uuid}"
        logger.debug("Mutation.update %s: PATCH %s body=%s", self._mapping.name, path, body)
        response = self._client.call_endpoint(
            path,
            method="PATCH",
            body=body,
        )
        if poll and isinstance(response, dict) and "job" in response:
            tracker = JobTracker.from_response(
                response,
                self._client,
                poll_interval=poll_interval,
                poll_timeout=poll_timeout,
            )
            return tracker.wait()
        return self._parse_response(response)

    def delete(self, uuid: str, **kwargs: Any) -> Any:
        """Delete a resource via DELETE.

        Args:
            uuid: Resource UUID.
            **kwargs: Optional body parameters (e.g. force flags).

        Returns:
            Raw API response.
        """
        path = f"{self._collection_path()}/{uuid}"
        body = self._build_body(kwargs) if kwargs else None
        logger.debug("Mutation.delete %s: DELETE %s body=%s", self._mapping.name, path, body)
        return self._client.call_endpoint(
            path,
            method="DELETE",
            body=body,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _collection_path(self) -> str:
        """Return the collection endpoint path without query parameters."""
        return self._mapping.collection_endpoint.split("?", 1)[0]

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

    def _build_body(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        """Translate flat model attrs to nested API JSON.

        Each key is translated via ``_attr_to_api_path``, then the
        dot-separated path is expanded into nested dicts.
        """
        body: dict[str, Any] = {}
        for attr, value in kwargs.items():
            api_path = self._attr_to_api_path(attr)
            _set_nested(body, api_path, value)
        return body

    def _parse_response(self, response: Any) -> Any:
        """Parse an API response into a model instance if possible.

        Returns raw response for 202 async jobs (None/empty), or when
        the response is not a dict containing record fields.
        """
        if not isinstance(response, dict):
            return response

        # Check if response looks like a record (has fields from the mapping)
        mapping_api_paths = {
            f.api_path.split(".")[0] for f in self._mapping.fields if f.api_path is not None
        }
        response_keys = set(response.keys())
        if mapping_api_paths & response_keys:
            return parse_api_record(
                self._mapping,
                response,
                f"Mutation<{self._mapping.name}>",
            )

        return response
