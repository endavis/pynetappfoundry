"""Write operations (POST/PATCH/PUT/DELETE) for ONTAP and DII models.

Provides :class:`Mutation`, a high-level interface for creating, updating,
and deleting ONTAP and Data Infrastructure Insights (DII) resources using
existing :class:`~pynetappfoundry.cache.field_mapping.TypeMapping` metadata.

DII writes need a read-write client, ``DIIAPIClient(config, read_write=True)``.
Request and response bodies of writes are not logged; only the top-level body
keys (or a list's length) are.

:meth:`Mutation.call` reaches DII operations beyond collection CRUD: action
endpoints and sub-resource writes such as annotation value assignment.
"""

from __future__ import annotations

import logging
import re
from typing import Any, TypeVar
from urllib.parse import quote

from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import TypeMapping, parse_api_record
from pynetappfoundry.clients.openapi import APIWrapper
from pynetappfoundry.core.models import RetryConfig
from pynetappfoundry.utils.dict_path import set_nested_value as _set_nested

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

_WRITE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def _describe_body(body: dict[str, Any] | list[Any] | None) -> str:
    """Describe *body* for a log line without its values."""
    if body is None:
        return "none"
    if isinstance(body, list):
        return f"list of {len(body)} item(s)"
    return f"keys={sorted(body)}"


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

    For DII, :meth:`call` sends any write operation under the model's endpoint,
    for example an action or an annotation assignment, with the same
    read-write client guard.
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

    def call(
        self,
        method: str,
        path: str | None = None,
        *,
        path_params: dict[str, str | int] | None = None,
        body: dict[str, Any] | list[Any] | None = None,
    ) -> Any:
        """Send a DII write operation at or below the model's endpoint.

        Reaches action endpoints and sub-resource writes (for example
        ``PUT /assets/volumes/{id}/annotations``) that are not collection CRUD.
        The body is validated against the OpenAPI spec by the client. POST has
        retry disabled, as in :meth:`create`.

        Args:
            method: ``POST``, ``PUT``, ``PATCH`` or ``DELETE``.
            path: Spec path template; defaults to the model's endpoint
                (for example ``/assets/volumes/{id}/annotations``).
            path_params: One entry per ``{placeholder}`` in *path*.
            body: JSON object or array, sent as-is.

        Returns:
            The raw API response, not parsed into the model.

        Raises:
            ValueError: For a non-write method, an ONTAP model, a path outside
                the model's endpoint or the spec, an undeclared method, or
                path parameters that do not match the placeholders.
        """
        verb = method.upper()
        if verb not in _WRITE_METHODS:
            raise ValueError(f"Mutation.call supports {sorted(_WRITE_METHODS)}, not '{method}'.")
        template = self._operation_path(path, verb)
        encoded = self._encode_path_params(template, path_params)
        logger.debug(
            "Mutation.call %s: %s %s body=%s",
            self._mapping.name,
            verb,
            template,
            _describe_body(body),
        )
        if verb == "POST":
            return self._client.call_endpoint(
                template,
                method=verb,
                path_params=encoded or None,
                body=body,
                retry_config=RetryConfig(enabled=False),
            )
        return self._client.call_endpoint(
            template, method=verb, path_params=encoded or None, body=body
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _is_dii(self) -> bool:
        """Return True when the mapping belongs to the DII API."""
        return self._mapping.api_type == "dii"

    def _operation_path(self, path: str | None, method: str) -> str:
        """Return the validated spec path for :meth:`call`.

        Raises:
            ValueError: If the model is not DII, *path* is outside the model's
                endpoint, is not in the spec, or does not declare *method*.
        """
        if not self._is_dii():
            raise ValueError("Mutation.call is only supported for DII models.")
        collection = self._mapping.api_endpoint.split("?", 1)[0]
        template = collection if path is None else path
        if template != collection and not template.startswith(collection + "/"):
            raise ValueError(f"Path '{template}' is outside the model endpoint '{collection}'.")
        operations = self._client.api_spec.get("paths", {}).get(template)
        if operations is None:
            raise ValueError(f"The API spec declares no path '{template}'.")
        if method not in {m.upper() for m in operations}:
            raise ValueError(f"The API spec declares no {method} for '{template}'.")
        return template

    @staticmethod
    def _encode_path_params(
        template: str, path_params: dict[str, str | int] | None
    ) -> dict[str, str]:
        """Percent-encode *path_params*, which must match the placeholders of *template*.

        Raises:
            ValueError: If the keys differ from the placeholders (names only).
        """
        placeholders = set(re.findall(r"\{([^}/]+)\}", template))
        given = set(path_params or {})
        if placeholders != given:
            raise ValueError(
                f"Path parameters {sorted(given)} do not match placeholders {sorted(placeholders)}."
            )
        return {k: quote(str(v), safe="") for k, v in (path_params or {}).items()}

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
