"""Write operations (POST/PATCH/PUT/DELETE) for ONTAP and DII models.

Provides :class:`Mutation`, a high-level interface for creating, updating,
and deleting ONTAP and Data Infrastructure Insights (DII) resources using
existing :class:`~pynetappfoundry.cache.field_mapping.TypeMapping` metadata.

DII writes need a read-write client, ``DIIAPIClient(config, read_write=True)``.
Request and response bodies of writes are not logged; only the top-level body
keys are.
"""

from __future__ import annotations

import logging
import re
from typing import Any, TypeVar

from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import TypeMapping, parse_api_record
from pynetappfoundry.clients.openapi import APIWrapper
from pynetappfoundry.core.models import RetryConfig
from pynetappfoundry.utils.dict_path import set_nested_value as _set_nested

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class Mutation:
    """Write interface for ONTAP and DII models.

    Translates model attribute names to nested API JSON and dispatches
    POST, PATCH/PUT, and DELETE requests via the API client.

    For ONTAP, items live at ``<collection>/<uuid>`` and updates use PATCH.
    For DII, the item path template (``<collection>/{id}`` or
    ``<collection>/{dataSourceId}``) and the update method (PATCH if the spec
    declares it, else PUT) come from the client's OpenAPI spec. A DII PUT
    replaces the whole object. DII has no job polling, and the client must be
    a read-write client (``DIIAPIClient(config, read_write=True)``).

    Example::

        m = Mutation(OntapVolume, client)
        vol = m.create(name="vol1", svm_name="vs1")
        m.update("uuid-123", state="offline")
        m.delete("uuid-123")

        dii = Mutation(DiiAssetsAnnotation, DIIAPIClient(config, read_write=True))
        dii.create(name="owner", type_="TEXT")
        dii.delete("42")
    """

    def __init__(
        self,
        model_class: type[T],
        client: APIWrapper,
    ) -> None:
        self._model_class = model_class
        self._client = client
        self._mapping = self._resolve_mapping(model_class)
        if self._is_dii() and getattr(client, "read_write", False) is not True:
            from pynetappfoundry.clients.dii.api import DIIWriteTokenMissingError

            raise DIIWriteTokenMissingError(
                f"DII writes for '{model_class.__name__}' need a read-write client: "
                "build it with DIIAPIClient(config, read_write=True)."
            )

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
                f"Mappings are auto-registered; verify a mapping.py module "
                f"exists under cache/<api>/ for this model."
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

        if poll and self._is_dii():
            raise ValueError("DII writes have no job polling; do not pass poll=True.")
        body = self._build_body(kwargs)
        path = self._collection_path()
        logger.debug(
            "Mutation.create %s: POST %s body keys=%s", self._mapping.name, path, sorted(body)
        )
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
        """Update an existing resource via PATCH (DII: PATCH, else PUT).

        Args:
            uuid: Resource UUID; for DII the ``id`` / ``dataSourceId``.
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

        if poll and self._is_dii():
            raise ValueError("DII writes have no job polling; do not pass poll=True.")
        body = self._build_body(kwargs)
        method = self._update_method() if self._is_dii() else "PATCH"
        logger.debug(
            "Mutation.update %s: %s %s body keys=%s",
            self._mapping.name,
            method,
            uuid,
            sorted(body),
        )
        response = self._item_call(uuid, method, body)
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
            uuid: Resource UUID; for DII the ``id`` / ``dataSourceId``.
            **kwargs: Optional body parameters (e.g. force flags).

        Returns:
            Raw API response.
        """
        body = self._build_body(kwargs) if kwargs else None
        logger.debug(
            "Mutation.delete %s: DELETE %s body keys=%s",
            self._mapping.name,
            uuid,
            sorted(body) if body else [],
        )
        return self._item_call(uuid, "DELETE", body)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _is_dii(self) -> bool:
        """Return True when the mapping belongs to the DII API."""
        return self._mapping.api_type == "dii"

    def _item_template(self) -> tuple[str, str]:
        """Return the DII item path template and its placeholder name.

        Looks for ``<collection>/{<placeholder>}`` in the client's spec paths.

        Raises:
            ValueError: If the spec declares no such item path.
        """
        collection = self._collection_path()
        pattern = re.compile(rf"^{re.escape(collection)}/\{{([^}}/]+)\}}$")
        for candidate in self._client.api_spec.get("paths", {}):
            match = pattern.match(candidate)
            if match:
                return candidate, match.group(1)
        raise ValueError(f"The API spec declares no item path under '{collection}'.")

    def _update_method(self) -> str:
        """Return PATCH if the DII item path declares it, else PUT.

        Raises:
            ValueError: If the item path declares neither.
        """
        template, _ = self._item_template()
        operations = {m.upper() for m in self._client.api_spec["paths"][template]}
        for method in ("PATCH", "PUT"):
            if method in operations:
                return method
        raise ValueError(f"The API spec declares neither PATCH nor PUT for '{template}'.")

    def _item_call(self, item_id: str, method: str, body: dict[str, Any] | None) -> Any:
        """Call the item endpoint for *item_id* with *method*."""
        if self._is_dii():
            template, placeholder = self._item_template()
            return self._client.call_endpoint(
                template,
                method=method,
                path_params={placeholder: item_id},
                body=body,
            )
        return self._client.call_endpoint(
            f"{self._collection_path()}/{item_id}",
            method=method,
            body=body,
        )

    def _collection_path(self) -> str:
        """Return the collection endpoint path without query parameters."""
        return self._mapping.collection_endpoint.split("?", 1)[0]

    def _attr_to_api_path(self, attr: str) -> str:
        """Translate a model attribute name to an API field path.

        Supports three lookup strategies (in order):

        1. Exact ``cache_attr`` match (e.g. ``"name"`` → ``"name"``).
        2. Dunder-separated kwargs: ``"ip__address"`` is normalised to
           ``"ip.address"`` and matched against ``cache_attr`` values.
        3. Pass-through: if no match, return *attr* unchanged (allows
           raw API field names).
        """
        # Direct match on cache_attr
        for field in self._mapping.fields:
            if field.cache_attr == attr and field.api_path is not None:
                return field.api_path

        # Dunder → dot translation for Python kwargs compatibility
        if "__" in attr:
            dot_attr = attr.replace("__", ".")
            for field in self._mapping.fields:
                if field.cache_attr == dot_attr and field.api_path is not None:
                    return field.api_path
            return dot_attr

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
