"""Wrapper for OpenAPI-based APIs."""

from __future__ import annotations

import contextlib
import json
import logging
from collections.abc import Callable
from typing import Any
from urllib.parse import urlencode

import requests
from jsonschema import ValidationError, validate
from requests.adapters import HTTPAdapter
from tenacity import (
    RetryCallState,
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    wait_exponential,
)

from pynetappfoundry.core.models import PaginationConfig, RetryConfig, ValidationConfig

NextPageExtractor = Callable[[dict[str, Any]], str | None]
"""Callable that receives a JSON response dict and returns the next page URL or None."""


def ontap_next_page_extractor(response: dict[str, Any]) -> str | None:
    """Extract next page URL from ONTAP/AIQUM HAL _links.next.href.

    Args:
        response: The JSON response dictionary.

    Returns:
        The next page URL string, or None if no next page.
    """
    try:
        href: str = response["_links"]["next"]["href"]
    except (KeyError, TypeError):
        return None
    return href


class ResponseValidationError(Exception):
    """Raised when API response fails schema validation in strict mode."""

    def __init__(
        self,
        message: str,
        path_template: str,
        method: str,
        status_code: int,
        validation_error: str,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message.
            path_template: The API path template.
            method: HTTP method.
            status_code: Response status code.
            validation_error: The underlying validation error message.
        """
        super().__init__(message)
        self.path_template = path_template
        self.method = method
        self.status_code = status_code
        self.validation_error = validation_error


class APIWrapper:
    """Tiny OpenAPI wrapper client for path/param discovery + calling endpoints."""

    def __init__(
        self,
        api_json_file: str,
        base_url: str,
        auth_header: dict[str, str] | None = None,
        timeout: float = 30.0,
        session: requests.Session | None = None,
        base_api_path: str = "",
        verify_ssl: bool = True,
        retry_config: RetryConfig | None = None,
        validation_config: ValidationConfig | None = None,
        name: str = "",
    ) -> None:
        """Initialize the API wrapper.

        Args:
            api_json_file: Path to the OpenAPI JSON specification file.
            base_url: Base URL for the API.
            auth_header: Authentication headers to include.
            timeout: Request timeout in seconds.
            session: Existing requests session to use.
            base_api_path: Base path prefix for all API paths.
            verify_ssl: Whether to verify SSL certificates. Default True for security.
            retry_config: Configuration for retry behavior. Defaults to enabled.
            validation_config: Configuration for response validation. Defaults to disabled.
            name: Name for log prefix (e.g., cluster name). Used in [name:api] format.
        """
        self.name = name
        self.log_prefix = f"[{name}:api]" if name else "[api]"
        self.verify_ssl = verify_ssl
        # Load the API spec
        with open(api_json_file, encoding="utf-8") as f:
            self.api_spec: dict[str, Any] = json.load(f)

        self.base_api_path = base_api_path
        if not base_api_path:
            with contextlib.suppress(KeyError):
                self.base_api_path = self.api_spec["basePath"]

        if not base_api_path:
            logging.warning(f"{self.log_prefix} No base api path found for base_url: {base_url}")

        if not auth_header:
            auth_header = {}

        # Networking defaults
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()

        # Configure connection pool to handle parallel API calls
        # Default pool size (10) is insufficient when using ThreadPoolExecutor
        adapter = HTTPAdapter(pool_connections=20, pool_maxsize=20)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        # Default headers (can be extended per request)
        default_headers = {
            "Content-Type": "application/json",
        }

        self.session.headers.update(default_headers)
        self.session.headers.update(auth_header)

        # Retry and validation configuration
        self.retry_config = retry_config if retry_config is not None else RetryConfig()
        self.validation_config = (
            validation_config if validation_config is not None else ValidationConfig()
        )

    def _get_operation(self, api_path: str, method: str) -> dict[str, Any]:
        """Get the operation for an API path.

        Args:
            api_path: The API path (e.g., /storage/assets).
            method: HTTP method (get, put, etc).

        Returns:
            Operation specification from the API spec.
        """
        method = method.lower()
        path: dict[str, Any] = self.api_spec["paths"].get(api_path, {})
        if not path:
            logging.error(f"{self.log_prefix} _get_operation: did not find {api_path}")
        operation: dict[str, Any] = path.get(method, {})
        if not operation:
            logging.error(
                f"{self.log_prefix} _get_operation: could not find {operation} for {api_path}"
            )
        return operation

    def _resolve_ref(self, ref: str) -> Any:
        """Resolve refs like '#/components/schemas/SomeSchema' against the api_spec."""
        if not ref.startswith("#"):
            return {}

        keys = ref.split("/")
        del keys[0]  # delete the #

        new_ref: Any = self.api_spec
        for key in keys:
            new_ref = new_ref[key]
        return new_ref

    def _resolve_refs(self, schema: Any) -> Any:
        """Deep-resolve $ref in the provided schema dict/list/primitive."""
        if isinstance(schema, dict):
            if "$ref" in schema:
                target = self._resolve_ref(schema["$ref"])
                return self._resolve_refs(target)
            return {k: self._resolve_refs(v) for k, v in schema.items()}
        if isinstance(schema, list):
            return [self._resolve_refs(item) for item in schema]
        return schema

    def _format_path(self, path_template: str, path_params: dict[str, Any] | None) -> str:
        """Replace placeholders like {id} in the path template with provided values.

        Also tolerates {{id}} just in case.
        """
        path = f"{self.base_api_path}{path_template}"
        if path_params:
            for k, v in path_params.items():
                path = path.replace(f"{{{k}}}", str(v))  # OpenAPI style
                path = path.replace(f"{{{{{k}}}}}", str(v))  # tolerate double braces
        return path

    def _extract_parameters(
        self, path_template: str, method: str
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Return (path_params, query_params) lists from the spec entry."""
        op = self._get_operation(path_template, method)
        params = op.get("parameters", []) or []
        path_params = [p for p in params if p.get("in") == "path"]
        query_params = [p for p in params if p.get("in") == "query"]
        return path_params, query_params

    def _get_request_schema(self, path_template: str, method: str) -> dict[str, Any] | None:
        """Return the resolved JSON Schema dict for the request body if present.

        Only supports application/json for simplicity.
        """
        op = self._get_operation(path_template, method)

        content = op.get("requestBody", {}).get("content", {}).get("application/json", {})

        if not content:
            logging.error(
                f"{self.log_prefix} _get_request_schema: no content for {path_template}:{method}"
            )

        schema = content.get("schema")

        if not schema:
            return None
        resolved: dict[str, Any] = self._resolve_refs(schema)
        return resolved

    def _build_sample_from_schema(self, schema: dict[str, Any]) -> Any:
        """Heuristic sample generator for a JSON Schema object.

        Produces a minimal readable skeleton with placeholder values.
        """
        t = schema.get("type")
        if not t and "oneOf" in schema:
            return self._build_sample_from_schema(schema["oneOf"][0])
        if t == "object" or ("properties" in schema):
            props = schema.get("properties", {})
            required = set(schema.get("required", []))
            sample: dict[str, Any] = {}
            for name, sub in props.items():
                sub = self._resolve_refs(sub)
                subtype = sub.get("type")
                enum = sub.get("enum")
                if enum:
                    value: Any = enum[0]
                elif subtype == "string" or subtype is None:
                    value = f"<{name}>"
                elif subtype == "integer":
                    value = 0
                elif subtype == "number":
                    value = 0.0
                elif subtype == "boolean":
                    value = False
                elif subtype == "array":
                    value = [self._build_sample_from_schema(sub.get("items", {}))]
                elif subtype == "object":
                    value = self._build_sample_from_schema(sub)
                else:
                    value = None
                sample[name] = value
                # If description present, tack on a pseudo-comment key (human readable)
                if "description" in sub:
                    sample[f"__desc__{name}"] = sub["description"]
                if name in required:
                    sample[f"__required__{name}"] = True
            return sample
        if t == "array":
            return [self._build_sample_from_schema(schema.get("items", {}))]
        if t == "string":
            return "<string>"
        if t == "integer":
            return 0
        if t == "number":
            return 0.0
        if t == "boolean":
            return False
        # Default fallback:
        return {}

    def list_endpoints(self) -> list[tuple[str, str, str | None]]:
        """Return list of (path, METHOD, summary) triples for quick discovery."""
        items: list[tuple[str, str, str | None]] = []
        for path in self.api_spec["paths"]:
            methods = self.api_spec["paths"].get(path, {})

            for m in methods:
                if "summary" in methods[m]:
                    summary = methods[m].get("summary")
                    items.append((path, m.upper(), summary))
                elif "description" in methods[m]:
                    summary = methods[m].get("description")
                    if "." in summary:
                        summary = summary.split(".")[0]
                    items.append((path, m.upper(), summary))

        return items

    def get_request_schema_for_endpoint(
        self, path_template: str, method: str = "GET", human_readable: bool = True
    ) -> dict[str, Any] | str | None:
        """Return the requestBody schema for the given endpoint.

        If human_readable=True, return a compact dict describing fields
        (type/required/enum/description), plus a 'sample' field with a minimal example body.
        """
        resolved = self._get_request_schema(path_template, method)

        if not resolved:
            return None

        if not human_readable:
            return resolved

        def describe(schema: dict[str, Any]) -> dict[str, Any]:
            info: dict[str, Any] = {"type": schema.get("type", "object")}
            props = schema.get("properties", {})
            required = set(schema.get("required", []))
            fields: dict[str, Any] = {}
            for name, sub in props.items():
                sub = self._resolve_refs(sub)
                fields[name] = {
                    "type": sub.get("type", "object" if "properties" in sub else "unknown"),
                    "required": name in required,
                    "description": sub.get("description"),
                }
                if "enum" in sub:
                    fields[name]["enum"] = list(sub["enum"])
            info["fields"] = fields
            info["sample"] = self._build_sample_from_schema(schema)
            return info

        return describe(resolved)

    def validate_body(
        self,
        path_template: str,
        method: str = "GET",
        body: dict[str, Any] | None = None,
    ) -> bool:
        """Validate 'body' against the endpoint's resolved schema (if any).

        If no body or no schema is present, returns True.
        """
        if body is None:
            return True
        schema = self._get_request_schema(path_template, method)
        if not schema:
            return True
        try:
            validate(instance=body, schema=schema)
            return True
        except ValidationError as e:
            logging.error(f"{self.log_prefix} Request body validation error: {e.message}")
            return False

    def suggest_parameters(self, path_template: str, method: str = "GET") -> dict[str, Any]:
        """Return a human-readable structure with parameter info.

        Returns dict with:
        - path_params: name, type, required, description
        - query_params: name, type, required, description
        - headers: default headers this client will send
        - body: sample JSON body (if any)
        - summary: brief endpoint summary from spec
        """
        method = method.upper()
        op = self._get_operation(path_template, method)
        path_params, query_params = self._extract_parameters(path_template, method)

        def simplify(param: dict[str, Any]) -> dict[str, Any]:
            sch = param.get("schema", {})
            return {
                "name": param.get("name"),
                "in": param.get("in"),
                "type": sch.get("type"),
                "required": param.get("required", False),
                "description": param.get("description"),
                "enum": sch.get("enum"),
                "format": sch.get("format"),
            }

        path_list = [simplify(p) for p in path_params]
        query_list = [simplify(p) for p in query_params]

        schema = self._get_request_schema(path_template, method)
        body_sample = self._build_sample_from_schema(schema) if schema else None

        return {
            "path": path_template,
            "method": method,
            "summary": op.get("summary"),
            "path_params": path_list,
            "query_params": query_list,
            "headers": dict(self.session.headers),
            "body_sample": body_sample,
        }

    def _get_response_schema(
        self, path_template: str, method: str, status_code: int
    ) -> dict[str, Any] | None:
        """Extract response schema from the OpenAPI spec for a given status code.

        Args:
            path_template: The API path template.
            method: HTTP method.
            status_code: The response status code to get schema for.

        Returns:
            Resolved JSON Schema dict for the response, or None if not found.
        """
        op = self._get_operation(path_template, method)
        responses = op.get("responses", {})

        # Try exact status code first, then wildcard (e.g., "2XX"), then "default"
        status_str = str(status_code)
        response_spec = responses.get(status_str)

        if not response_spec:
            # Try wildcard like "2XX"
            wildcard = f"{status_str[0]}XX"
            response_spec = responses.get(wildcard)

        if not response_spec:
            response_spec = responses.get("default")

        if not response_spec:
            return None

        # OpenAPI 3.x style
        content = response_spec.get("content", {}).get("application/json", {})
        schema = content.get("schema")

        if schema:
            resolved: dict[str, Any] = self._resolve_refs(schema)
            return resolved

        return None

    def validate_response(
        self,
        path_template: str,
        method: str,
        status_code: int,
        response_data: Any,
        validation_config: ValidationConfig | None = None,
    ) -> bool:
        """Validate response data against the OpenAPI schema.

        Args:
            path_template: The API path template.
            method: HTTP method.
            status_code: The response status code.
            response_data: The response data to validate.
            validation_config: Optional override for validation config.

        Returns:
            True if validation passes or is disabled, False otherwise.

        Raises:
            ResponseValidationError: If strict mode is enabled and validation fails.
        """
        config = validation_config if validation_config is not None else self.validation_config

        if not config.enabled:
            return True

        # Only validate success responses if configured
        if config.validate_success_only and not (200 <= status_code < 300):
            return True

        schema = self._get_response_schema(path_template, method, status_code)
        if not schema:
            logging.debug(
                f"{self.log_prefix} No response schema found for "
                f"{method} {path_template} status {status_code}"
            )
            return True

        try:
            validate(instance=response_data, schema=schema)
            return True
        except ValidationError as e:
            error_msg = (
                f"{self.log_prefix} Response validation failed for {method} {path_template} "
                f"status {status_code}: {e.message}"
            )
            if config.strict:
                raise ResponseValidationError(
                    message=error_msg,
                    path_template=path_template,
                    method=method,
                    status_code=status_code,
                    validation_error=e.message,
                ) from e
            logging.warning(error_msg)
            return False

    def _should_retry_response(
        self, response: requests.Response, retry_config: RetryConfig
    ) -> bool:
        """Determine if a response should trigger a retry.

        Args:
            response: The HTTP response.
            retry_config: Retry configuration.

        Returns:
            True if the response status code is in the retryable list.
        """
        return response.status_code in retry_config.retryable_status_codes

    def _create_retry_callback(self, retry_config: RetryConfig) -> Any:
        """Create a callback for logging retry attempts.

        Args:
            retry_config: Retry configuration.

        Returns:
            A callback function for tenacity.
        """

        def log_retry(retry_state: RetryCallState) -> None:
            if retry_state.attempt_number > 1:
                outcome = retry_state.outcome
                if outcome is not None:
                    exception = outcome.exception()
                    result = outcome.result() if exception is None else None
                    if exception:
                        logging.warning(
                            f"{self.log_prefix} Retry attempt {retry_state.attempt_number} "
                            f"after exception: {exception}"
                        )
                    elif result is not None and hasattr(result, "status_code"):
                        logging.warning(
                            f"{self.log_prefix} Retry attempt {retry_state.attempt_number} "
                            f"after status code: {result.status_code}"
                        )

        return log_retry

    def _execute_request_with_retry(
        self,
        method: str,
        url: str,
        body: dict[str, Any] | None,
        headers: dict[str, str | bytes],
        retry_config: RetryConfig | None = None,
    ) -> requests.Response:
        """Execute an HTTP request with retry logic.

        Args:
            method: HTTP method.
            url: Full URL to request.
            body: Request body (JSON).
            headers: Request headers.
            retry_config: Optional override for retry config.

        Returns:
            The HTTP response.

        Raises:
            requests.RequestException: If all retries are exhausted.
        """
        config = retry_config if retry_config is not None else self.retry_config

        if not config.enabled:
            return self.session.request(
                method,
                url,
                json=body,
                headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
            )

        # Build retry conditions
        def should_retry_result(response: requests.Response) -> bool:
            return self._should_retry_response(response, config)

        retry_conditions: Any = retry_if_result(should_retry_result)

        if config.retry_on_connection_error:
            retry_conditions = retry_conditions | retry_if_exception_type(
                (requests.ConnectionError, requests.Timeout)
            )

        # Create the retry decorator dynamically
        @retry(
            stop=stop_after_attempt(config.max_attempts),
            wait=wait_exponential(
                multiplier=config.initial_wait,
                max=config.max_wait,
                exp_base=config.exponential_base,
            ),
            retry=retry_conditions,
            before_sleep=self._create_retry_callback(config),
            reraise=True,
        )
        def make_request() -> requests.Response:
            return self.session.request(
                method,
                url,
                json=body,
                headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
            )

        return make_request()

    def call_endpoint(
        self,
        path_template: str,
        method: str = "GET",
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        additional_headers: dict[str, str] | None = None,
        retry_config: RetryConfig | None = None,
        validation_config: ValidationConfig | None = None,
    ) -> Any:
        """Make the HTTP call.

        Validates body (if schema exists), applies retry logic, validates response,
        and raises for HTTP errors.

        Args:
            path_template: API path template.
            method: HTTP method.
            path_params: Values for path placeholders.
            query_params: Query string parameters.
            body: Request body (JSON).
            additional_headers: Extra headers to include.
            retry_config: Optional per-call retry configuration override.
            validation_config: Optional per-call validation configuration override.

        Returns:
            Response JSON or text.

        Raises:
            ValueError: If request body validation fails.
            requests.HTTPError: If the request fails.
            ResponseValidationError: If response validation fails in strict mode.
        """
        method = method.upper()

        # Validate body against the schema for the *template* path
        if not self.validate_body(path_template, method, body):
            raise ValueError("Request body validation failed.")

        # Build URL (formatting path placeholders)
        path = self._format_path(path_template, path_params)
        logging.debug(f"{self.log_prefix} API Path: {path}")
        url = f"{self.base_url}{path}"
        logging.debug(f"{self.log_prefix} API URL: {url}")

        # Encode query params
        if query_params:
            url += "?" + urlencode(query_params, doseq=True)

        # Merge headers
        headers = dict(self.session.headers)
        if additional_headers:
            headers.update(additional_headers)

        logging.debug(f"{self.log_prefix} Calling {method} {url} {headers}")

        # Execute request with retry logic
        resp = self._execute_request_with_retry(
            method=method,
            url=url,
            body=body,
            headers=headers,
            retry_config=retry_config,
        )

        logging.debug(f"{self.log_prefix} {path} Response Status Code: {resp.status_code}")
        resp.raise_for_status()

        # Try JSON, else return text
        try:
            logging.debug(f"{self.log_prefix} {path} Response Text: {resp.text}")
            response_data = resp.json()
        except ValueError:
            response_data = resp.text

        # Validate response if enabled
        self.validate_response(
            path_template=path_template,
            method=method,
            status_code=resp.status_code,
            response_data=response_data,
            validation_config=validation_config,
        )

        return response_data

    def get_all_records(
        self,
        path_template: str,
        method: str = "GET",
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        additional_headers: dict[str, str] | None = None,
        retry_config: RetryConfig | None = None,
        validation_config: ValidationConfig | None = None,
        pagination_config: PaginationConfig | None = None,
        next_page_extractor: NextPageExtractor | None = None,
    ) -> dict[str, Any]:
        """Fetch all pages of a paginated API response and merge records.

        Makes the initial request via call_endpoint(), then follows pagination
        links using the next_page_extractor to collect all records across pages.

        Args:
            path_template: API path template.
            method: HTTP method.
            path_params: Values for path placeholders.
            query_params: Query string parameters.
            body: Request body (JSON).
            additional_headers: Extra headers to include.
            retry_config: Optional per-call retry configuration override.
            validation_config: Optional per-call validation configuration override.
            pagination_config: Configuration for pagination behavior.
            next_page_extractor: Callable to extract next page URL from response.
                Defaults to ontap_next_page_extractor.

        Returns:
            Merged response dict with all records combined, _links removed,
            and num_records updated if present in original response.

        Raises:
            TypeError: If the response is not a dict.
            ValueError: If request body validation fails.
            requests.HTTPError: If any request fails.
            ResponseValidationError: If response validation fails in strict mode.
        """
        config = pagination_config if pagination_config is not None else PaginationConfig()
        extractor = (
            next_page_extractor if next_page_extractor is not None else ontap_next_page_extractor
        )

        # Fetch first page via call_endpoint (full validation, URL building, retry)
        first_response = self.call_endpoint(
            path_template=path_template,
            method=method,
            path_params=path_params,
            query_params=query_params,
            body=body,
            additional_headers=additional_headers,
            retry_config=retry_config,
            validation_config=validation_config,
        )

        if not isinstance(first_response, dict):
            msg = f"Expected dict response for pagination, got {type(first_response).__name__}"
            raise TypeError(msg)

        if not config.enabled:
            logging.debug(f"{self.log_prefix} Pagination disabled, returning first page")
            return first_response

        # Collect records from first page
        all_records: list[Any] = list(first_response.get(config.records_key, []))
        page_count = 1

        logging.debug(
            f"{self.log_prefix} Page {page_count}: {len(all_records)} records "
            f"(total: {len(all_records)})"
        )

        # Pre-compute headers for subsequent pages
        headers: dict[str, str | bytes] = dict(self.session.headers)
        if additional_headers:
            headers.update(additional_headers)

        # Effective configs for subsequent pages
        effective_retry = retry_config if retry_config is not None else self.retry_config
        effective_validation = (
            validation_config if validation_config is not None else self.validation_config
        )

        # Follow pagination links
        current_response = first_response
        while page_count < config.max_pages:
            next_url = extractor(current_response)
            if next_url is None:
                break

            page_count += 1

            # Build full URL
            if next_url.startswith(("http://", "https://")):
                full_url = next_url
            else:
                full_url = f"{self.base_url}{next_url}"

            logging.debug(f"{self.log_prefix} Fetching page {page_count}: {full_url}")

            resp = self._execute_request_with_retry(
                method=method.upper(),
                url=full_url,
                body=None,
                headers=headers,
                retry_config=effective_retry,
            )

            resp.raise_for_status()

            try:
                page_data = resp.json()
            except ValueError as e:
                logging.error(f"{self.log_prefix} Page {page_count}: failed to parse JSON response")
                msg = f"Page {page_count}: failed to parse JSON response"
                raise TypeError(msg) from e

            # Validate subsequent page if enabled
            if effective_validation.enabled:
                self.validate_response(
                    path_template=path_template,
                    method=method,
                    status_code=resp.status_code,
                    response_data=page_data,
                    validation_config=effective_validation,
                )

            page_records = page_data.get(config.records_key, [])
            all_records.extend(page_records)
            current_response = page_data

            logging.debug(
                f"{self.log_prefix} Page {page_count}: {len(page_records)} records "
                f"(total: {len(all_records)})"
            )
        else:
            if extractor(current_response) is not None:
                logging.warning(
                    f"{self.log_prefix} Pagination stopped at max_pages limit "
                    f"({config.max_pages}). Some records may not have been fetched."
                )

        logging.info(
            f"{self.log_prefix} Fetched {len(all_records)} total records across {page_count} pages"
        )

        # Build merged response
        merged = dict(first_response)
        merged[config.records_key] = all_records
        merged.pop("_links", None)

        if "num_records" in first_response:
            merged["num_records"] = len(all_records)

        return merged
