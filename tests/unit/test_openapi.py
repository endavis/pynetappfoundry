"""Tests for APIWrapper class."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import requests
from tenacity import RetryError

from pynetappfoundry.clients.openapi import (
    APIWrapper,
    ResponseValidationError,
    ontap_next_page_extractor,
)
from pynetappfoundry.core.models import PaginationConfig, RetryConfig, ValidationConfig


@pytest.fixture
def sample_openapi_spec() -> dict[str, Any]:
    """Sample OpenAPI specification for testing."""
    return {
        "swagger": "2.0",
        "basePath": "/api/v1",
        "paths": {
            "/users": {
                "get": {
                    "summary": "List users",
                    "description": "Get a list of all users",
                    "parameters": [
                        {
                            "name": "limit",
                            "in": "query",
                            "type": "integer",
                            "required": False,
                            "description": "Maximum number of results",
                        },
                        {
                            "name": "status",
                            "in": "query",
                            "type": "string",
                            "required": False,
                            "schema": {"type": "string", "enum": ["active", "inactive"]},
                        },
                    ],
                },
                "post": {
                    "summary": "Create user",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["name"],
                                    "properties": {
                                        "name": {"type": "string", "description": "User name"},
                                        "email": {"type": "string", "description": "User email"},
                                        "age": {"type": "integer"},
                                        "active": {"type": "boolean"},
                                    },
                                }
                            }
                        }
                    },
                },
            },
            "/users/{id}": {
                "get": {
                    "summary": "Get user by ID",
                    "parameters": [
                        {"name": "id", "in": "path", "type": "string", "required": True}
                    ],
                },
                "delete": {"summary": "Delete user"},
            },
            "/items": {
                "get": {
                    "summary": "List items",
                },
            },
        },
        "definitions": {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                },
            },
            "ItemList": {
                "type": "array",
                "items": {"$ref": "#/definitions/Item"},
            },
            "Item": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "value": {"type": "number"},
                },
            },
        },
    }


@pytest.fixture
def spec_file(tmp_path: Path, sample_openapi_spec: dict[str, Any]) -> Path:
    """Create a temporary spec file."""
    spec_path = tmp_path / "api_spec.json"
    spec_path.write_text(json.dumps(sample_openapi_spec))
    return spec_path


@pytest.fixture
def api_wrapper(spec_file: Path) -> APIWrapper:
    """Create an APIWrapper instance."""
    return APIWrapper(
        api_json_file=str(spec_file),
        base_url="https://api.example.com",
        timeout=10.0,
    )


class TestAPIWrapperInit:
    """Tests for APIWrapper initialization."""

    def test_loads_spec(self, api_wrapper: APIWrapper) -> None:
        """Test that the spec is loaded correctly."""
        assert "paths" in api_wrapper.api_spec
        assert "/users" in api_wrapper.api_spec["paths"]

    def test_log_prefix_with_name(self, spec_file: Path) -> None:
        """Test log_prefix format when name is provided."""
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            name="cluster1",
        )
        assert wrapper.log_prefix == "[cluster1:api]"
        assert wrapper.name == "cluster1"

    def test_log_prefix_without_name(self, api_wrapper: APIWrapper) -> None:
        """Test log_prefix format when name is not provided."""
        assert api_wrapper.log_prefix == "[api]"
        assert api_wrapper.name == ""

    def test_log_prefix_with_special_characters(self, spec_file: Path) -> None:
        """Test log_prefix with special characters in name."""
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            name="cluster-prod-01",
        )
        assert wrapper.log_prefix == "[cluster-prod-01:api]"

    def test_uses_base_path_from_spec(self, api_wrapper: APIWrapper) -> None:
        """Test that basePath is extracted from spec."""
        assert api_wrapper.base_api_path == "/api/v1"

    def test_custom_base_path_overrides_spec(self, spec_file: Path) -> None:
        """Test that custom base_api_path overrides spec."""
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            base_api_path="/custom/path",
        )
        assert wrapper.base_api_path == "/custom/path"

    def test_default_headers(self, api_wrapper: APIWrapper) -> None:
        """Test that default headers are set."""
        assert api_wrapper.session.headers["Content-Type"] == "application/json"

    def test_auth_header(self, spec_file: Path) -> None:
        """Test that auth headers are included."""
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            auth_header={"Authorization": "Bearer token123"},
        )
        assert wrapper.session.headers["Authorization"] == "Bearer token123"

    def test_connection_pool_configured(self, api_wrapper: APIWrapper) -> None:
        """Test that connection pool is configured for parallel requests."""
        # Get the adapter mounted for https://
        adapter = api_wrapper.session.get_adapter("https://example.com")
        # Verify pool is configured with increased size (stored as private attrs)
        assert adapter._pool_connections == 20  # type: ignore[union-attr]
        assert adapter._pool_maxsize == 20  # type: ignore[union-attr]


class TestReferenceResolution:
    """Tests for $ref resolution."""

    def test_resolve_simple_ref(self, api_wrapper: APIWrapper) -> None:
        """Test resolving a simple $ref."""
        resolved = api_wrapper._resolve_ref("#/definitions/User")
        assert resolved["type"] == "object"
        assert "id" in resolved["properties"]
        assert "name" in resolved["properties"]

    def test_resolve_nested_ref(self, api_wrapper: APIWrapper) -> None:
        """Test resolving nested $refs."""
        schema = {"items": {"$ref": "#/definitions/User"}}
        resolved = api_wrapper._resolve_refs(schema)
        assert resolved["items"]["type"] == "object"

    def test_resolve_array_with_refs(self, api_wrapper: APIWrapper) -> None:
        """Test resolving refs in arrays."""
        schema = [{"$ref": "#/definitions/User"}, {"$ref": "#/definitions/Item"}]
        resolved = api_wrapper._resolve_refs(schema)
        assert len(resolved) == 2
        assert resolved[0]["type"] == "object"
        assert "id" in resolved[0]["properties"]

    def test_resolve_non_ref_passthrough(self, api_wrapper: APIWrapper) -> None:
        """Test that non-ref schemas pass through unchanged."""
        schema = {"type": "string", "maxLength": 100}
        resolved = api_wrapper._resolve_refs(schema)
        assert resolved == schema

    def test_resolve_invalid_ref_returns_empty(self, api_wrapper: APIWrapper) -> None:
        """Test that invalid ref format returns empty dict."""
        resolved = api_wrapper._resolve_ref("definitions/User")  # Missing #
        assert resolved == {}


class TestPathFormatting:
    """Tests for path formatting."""

    def test_format_path_with_params(self, api_wrapper: APIWrapper) -> None:
        """Test path formatting with path parameters."""
        path = api_wrapper._format_path("/users/{id}", {"id": "123"})
        assert path == "/api/v1/users/123"

    def test_format_path_multiple_params(self, api_wrapper: APIWrapper) -> None:
        """Test path formatting with multiple parameters."""
        # Manually test with a template that has multiple params
        path = api_wrapper._format_path("/orgs/{org}/users/{id}", {"org": "acme", "id": "456"})
        assert path == "/api/v1/orgs/acme/users/456"

    def test_format_path_no_params(self, api_wrapper: APIWrapper) -> None:
        """Test path formatting without parameters."""
        path = api_wrapper._format_path("/users", None)
        assert path == "/api/v1/users"

    def test_format_path_double_braces(self, api_wrapper: APIWrapper) -> None:
        """Test path formatting handles double braces.

        The code first replaces {key} then {{key}}.
        So {{user_id}} becomes {789} (inner braces replaced), not 789.
        This documents the existing behavior - double braces are partially handled.
        """
        path = api_wrapper._format_path("/users/{{user_id}}", {"user_id": "789"})
        # The replacement produces {789} because it replaces inner {user_id} first
        assert path == "/api/v1/users/{789}"


class TestParameterExtraction:
    """Tests for parameter extraction."""

    def test_extract_query_params(self, api_wrapper: APIWrapper) -> None:
        """Test extracting query parameters."""
        path_params, query_params = api_wrapper._extract_parameters("/users", "GET")
        assert len(path_params) == 0
        assert len(query_params) == 2
        assert any(p["name"] == "limit" for p in query_params)
        assert any(p["name"] == "status" for p in query_params)

    def test_extract_path_params(self, api_wrapper: APIWrapper) -> None:
        """Test extracting path parameters."""
        path_params, _ = api_wrapper._extract_parameters("/users/{id}", "GET")
        assert len(path_params) == 1
        assert path_params[0]["name"] == "id"


class TestBodyValidation:
    """Tests for request body validation."""

    def test_validate_body_valid(self, api_wrapper: APIWrapper) -> None:
        """Test validation passes for valid body."""
        result = api_wrapper.validate_body(
            "/users", "POST", {"name": "John", "email": "john@example.com"}
        )
        assert result is True

    def test_validate_body_missing_required(self, api_wrapper: APIWrapper) -> None:
        """Test validation fails for missing required field."""
        result = api_wrapper.validate_body(
            "/users",
            "POST",
            {"email": "john@example.com"},  # Missing 'name'
        )
        assert result is False

    def test_validate_body_none_returns_true(self, api_wrapper: APIWrapper) -> None:
        """Test validation returns True when body is None."""
        result = api_wrapper.validate_body("/users", "GET", None)
        assert result is True

    def test_validate_body_no_schema_returns_true(self, api_wrapper: APIWrapper) -> None:
        """Test validation returns True when no schema exists."""
        result = api_wrapper.validate_body("/items", "GET", {"any": "data"})
        assert result is True


class TestListEndpoints:
    """Tests for endpoint listing."""

    def test_list_endpoints_returns_all(self, api_wrapper: APIWrapper) -> None:
        """Test listing all endpoints."""
        endpoints = api_wrapper.list_endpoints()
        paths = [e[0] for e in endpoints]
        assert "/users" in paths
        assert "/users/{id}" in paths
        assert "/items" in paths

    def test_list_endpoints_includes_methods(self, api_wrapper: APIWrapper) -> None:
        """Test that methods are included."""
        endpoints = api_wrapper.list_endpoints()
        user_endpoints = [e for e in endpoints if e[0] == "/users"]
        methods = [e[1] for e in user_endpoints]
        assert "GET" in methods
        assert "POST" in methods

    def test_list_endpoints_includes_summary(self, api_wrapper: APIWrapper) -> None:
        """Test that summaries are included."""
        endpoints = api_wrapper.list_endpoints()
        get_users = next(e for e in endpoints if e[0] == "/users" and e[1] == "GET")
        assert get_users[2] == "List users"


class TestSuggestParameters:
    """Tests for parameter suggestion."""

    def test_suggest_parameters_structure(self, api_wrapper: APIWrapper) -> None:
        """Test suggest_parameters returns expected structure."""
        suggestion = api_wrapper.suggest_parameters("/users", "GET")
        assert "path" in suggestion
        assert "method" in suggestion
        assert "summary" in suggestion
        assert "path_params" in suggestion
        assert "query_params" in suggestion
        assert "headers" in suggestion
        assert "body_sample" in suggestion

    def test_suggest_parameters_query_details(self, api_wrapper: APIWrapper) -> None:
        """Test query parameter details."""
        suggestion = api_wrapper.suggest_parameters("/users", "GET")
        query_params = suggestion["query_params"]
        limit_param = next(p for p in query_params if p["name"] == "limit")
        assert limit_param["in"] == "query"
        assert limit_param["required"] is False


class TestBuildSampleFromSchema:
    """Tests for sample generation."""

    def test_build_sample_object(self, api_wrapper: APIWrapper) -> None:
        """Test building sample from object schema."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "count": {"type": "integer"},
            },
        }
        sample = api_wrapper._build_sample_from_schema(schema)
        assert sample["name"] == "<name>"
        assert sample["count"] == 0

    def test_build_sample_with_enum(self, api_wrapper: APIWrapper) -> None:
        """Test building sample uses first enum value."""
        schema = {
            "type": "object",
            "properties": {"status": {"type": "string", "enum": ["active", "inactive"]}},
        }
        sample = api_wrapper._build_sample_from_schema(schema)
        assert sample["status"] == "active"

    def test_build_sample_array(self, api_wrapper: APIWrapper) -> None:
        """Test building sample from array schema."""
        schema = {"type": "array", "items": {"type": "string"}}
        sample = api_wrapper._build_sample_from_schema(schema)
        assert isinstance(sample, list)
        assert sample[0] == "<string>"


class TestCallEndpoint:
    """Tests for HTTP request making."""

    def test_call_endpoint_builds_url(self, api_wrapper: APIWrapper) -> None:
        """Test that call_endpoint builds correct URL."""
        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"data": []}
            mock_request.return_value = mock_response

            api_wrapper.call_endpoint("/users", "GET")

            call_args = mock_request.call_args
            assert call_args[0][0] == "GET"
            assert call_args[0][1] == "https://api.example.com/api/v1/users"

    def test_call_endpoint_with_query_params(self, api_wrapper: APIWrapper) -> None:
        """Test that query params are appended to URL."""
        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"data": []}
            mock_request.return_value = mock_response

            api_wrapper.call_endpoint("/users", "GET", query_params={"limit": 10})

            call_args = mock_request.call_args
            assert "limit=10" in call_args[0][1]

    def test_call_endpoint_with_path_params(self, api_wrapper: APIWrapper) -> None:
        """Test that path params are substituted."""
        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"id": "123"}
            mock_request.return_value = mock_response

            api_wrapper.call_endpoint("/users/{id}", "GET", path_params={"id": "123"})

            call_args = mock_request.call_args
            assert "/users/123" in call_args[0][1]

    def test_call_endpoint_with_body(self, api_wrapper: APIWrapper) -> None:
        """Test that body is sent correctly."""
        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.json.return_value = {"id": "new"}
            mock_request.return_value = mock_response

            body = {"name": "John"}
            api_wrapper.call_endpoint("/users", "POST", body=body)

            call_args = mock_request.call_args
            assert call_args[1]["json"] == body

    def test_call_endpoint_invalid_body_raises(self, api_wrapper: APIWrapper) -> None:
        """Test that invalid body raises ValueError."""
        with pytest.raises(ValueError, match="validation failed"):
            api_wrapper.call_endpoint("/users", "POST", body={"invalid": "data"})

    def test_call_endpoint_returns_json(self, api_wrapper: APIWrapper) -> None:
        """Test that JSON response is returned."""
        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"users": []}
            mock_request.return_value = mock_response

            result = api_wrapper.call_endpoint("/users", "GET")

            assert result == {"users": []}

    def test_call_endpoint_returns_text_on_json_error(self, api_wrapper: APIWrapper) -> None:
        """Test that text is returned when JSON parsing fails."""
        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = "plain text response"
            mock_response.json.side_effect = ValueError("No JSON")
            mock_request.return_value = mock_response

            result = api_wrapper.call_endpoint("/users", "GET")

            assert result == "plain text response"

    def test_call_endpoint_raises_on_http_error(self, api_wrapper: APIWrapper) -> None:
        """Test that HTTP errors are raised."""
        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_response.raise_for_status.side_effect = requests.HTTPError("Not Found")
            mock_request.return_value = mock_response

            with pytest.raises(requests.HTTPError):
                api_wrapper.call_endpoint("/users/{id}", "GET", path_params={"id": "999"})

    def test_call_endpoint_uses_verify_ssl_default(self, api_wrapper: APIWrapper) -> None:
        """Test that SSL verification is enabled by default."""
        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_request.return_value = mock_response

            api_wrapper.call_endpoint("/users", "GET")

            call_args = mock_request.call_args
            # SSL verification is now enabled by default for security
            assert call_args[1]["verify"] is True

    def test_call_endpoint_verify_ssl_configurable(self, spec_file: Path) -> None:
        """Test that SSL verification can be disabled when needed."""
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            verify_ssl=False,
        )
        with patch.object(wrapper.session, "request") as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_request.return_value = mock_response

            wrapper.call_endpoint("/items", "GET")

            call_args = mock_request.call_args
            assert call_args[1]["verify"] is False

    def test_call_endpoint_uses_timeout(self, api_wrapper: APIWrapper) -> None:
        """Test that timeout is used."""
        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_request.return_value = mock_response

            api_wrapper.call_endpoint("/users", "GET")

            call_args = mock_request.call_args
            assert call_args[1]["timeout"] == 10.0  # from fixture


class TestGetRequestSchemaForEndpoint:
    """Tests for schema retrieval."""

    def test_get_schema_human_readable(self, api_wrapper: APIWrapper) -> None:
        """Test human-readable schema format."""
        result = api_wrapper.get_request_schema_for_endpoint("/users", "POST")
        assert result is not None
        assert isinstance(result, dict)
        assert "fields" in result
        assert "sample" in result
        fields = result["fields"]
        assert isinstance(fields, dict)
        assert "name" in fields

    def test_get_schema_raw(self, api_wrapper: APIWrapper) -> None:
        """Test raw schema format."""
        result = api_wrapper.get_request_schema_for_endpoint("/users", "POST", human_readable=False)
        assert result is not None
        assert "properties" in result

    def test_get_schema_none_when_no_body(self, api_wrapper: APIWrapper) -> None:
        """Test None returned when no request body."""
        result = api_wrapper.get_request_schema_for_endpoint("/users", "GET")
        assert result is None


class TestRetryConfig:
    """Tests for RetryConfig model."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = RetryConfig()
        assert config.enabled is True
        assert config.max_attempts == 3
        assert config.initial_wait == 1.0
        assert config.max_wait == 60.0
        assert config.exponential_base == 2
        assert config.retryable_status_codes == [429, 500, 502, 503, 504]
        assert config.retry_on_connection_error is True

    def test_custom_values(self) -> None:
        """Test custom configuration values."""
        config = RetryConfig(
            enabled=False,
            max_attempts=5,
            initial_wait=0.5,
            max_wait=30.0,
            exponential_base=3,
            retryable_status_codes=[500, 503],
            retry_on_connection_error=False,
        )
        assert config.enabled is False
        assert config.max_attempts == 5
        assert config.initial_wait == 0.5
        assert config.max_wait == 30.0
        assert config.exponential_base == 3
        assert config.retryable_status_codes == [500, 503]
        assert config.retry_on_connection_error is False

    def test_max_attempts_bounds(self) -> None:
        """Test max_attempts validation bounds."""
        with pytest.raises(ValueError):
            RetryConfig(max_attempts=0)  # below minimum
        with pytest.raises(ValueError):
            RetryConfig(max_attempts=11)  # above maximum

    def test_initial_wait_minimum(self) -> None:
        """Test initial_wait validation minimum."""
        with pytest.raises(ValueError):
            RetryConfig(initial_wait=0.05)  # below 0.1

    def test_max_wait_minimum(self) -> None:
        """Test max_wait validation minimum."""
        with pytest.raises(ValueError):
            RetryConfig(max_wait=0.5)  # below 1.0

    def test_exponential_base_minimum(self) -> None:
        """Test exponential_base validation minimum."""
        with pytest.raises(ValueError):
            RetryConfig(exponential_base=1)  # below 2


class TestValidationConfig:
    """Tests for ValidationConfig model."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = ValidationConfig()
        assert config.enabled is False
        assert config.strict is False
        assert config.validate_success_only is True

    def test_custom_values(self) -> None:
        """Test custom configuration values."""
        config = ValidationConfig(
            enabled=True,
            strict=True,
            validate_success_only=False,
        )
        assert config.enabled is True
        assert config.strict is True
        assert config.validate_success_only is False


class TestResponseValidation:
    """Tests for response validation."""

    @pytest.fixture
    def spec_with_response_schema(self, tmp_path: Path) -> Path:
        """Create a spec with response schemas."""
        spec = {
            "swagger": "2.0",
            "basePath": "/api/v1",
            "paths": {
                "/users": {
                    "get": {
                        "summary": "List users",
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "required": ["users"],
                                            "properties": {
                                                "users": {
                                                    "type": "array",
                                                    "items": {"type": "object"},
                                                },
                                                "count": {"type": "integer"},
                                            },
                                        }
                                    }
                                }
                            },
                            "default": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {"error": {"type": "string"}},
                                        }
                                    }
                                }
                            },
                        },
                    },
                },
            },
        }
        spec_path = tmp_path / "spec_with_response.json"
        spec_path.write_text(json.dumps(spec))
        return spec_path

    @pytest.fixture
    def wrapper_with_response_schema(self, spec_with_response_schema: Path) -> APIWrapper:
        """Create wrapper with response schema spec."""
        return APIWrapper(
            api_json_file=str(spec_with_response_schema),
            base_url="https://api.example.com",
            validation_config=ValidationConfig(enabled=True),
        )

    def test_validate_response_valid_data(self, wrapper_with_response_schema: APIWrapper) -> None:
        """Test validation passes for valid response data."""
        result = wrapper_with_response_schema.validate_response(
            "/users", "GET", 200, {"users": [], "count": 0}
        )
        assert result is True

    def test_validate_response_invalid_data_warning(
        self, wrapper_with_response_schema: APIWrapper
    ) -> None:
        """Test validation fails with warning for invalid data (non-strict)."""
        result = wrapper_with_response_schema.validate_response(
            "/users",
            "GET",
            200,
            {"invalid": "data"},  # missing required 'users'
        )
        assert result is False

    def test_validate_response_invalid_data_strict(self, spec_with_response_schema: Path) -> None:
        """Test validation raises exception for invalid data in strict mode."""
        wrapper = APIWrapper(
            api_json_file=str(spec_with_response_schema),
            base_url="https://api.example.com",
            validation_config=ValidationConfig(enabled=True, strict=True),
        )
        with pytest.raises(ResponseValidationError) as exc_info:
            wrapper.validate_response("/users", "GET", 200, {"invalid": "data"})
        assert exc_info.value.status_code == 200
        assert exc_info.value.method == "GET"
        assert exc_info.value.path_template == "/users"

    def test_validate_response_disabled(self, spec_with_response_schema: Path) -> None:
        """Test validation skipped when disabled."""
        wrapper = APIWrapper(
            api_json_file=str(spec_with_response_schema),
            base_url="https://api.example.com",
            validation_config=ValidationConfig(enabled=False),
        )
        result = wrapper.validate_response("/users", "GET", 200, {"invalid": "data"})
        assert result is True  # Skipped, returns True

    def test_validate_response_success_only(self, wrapper_with_response_schema: APIWrapper) -> None:
        """Test validation skips non-2xx when validate_success_only is True."""
        # 404 response should not be validated with validate_success_only=True (default)
        result = wrapper_with_response_schema.validate_response(
            "/users", "GET", 404, {"any": "data"}
        )
        assert result is True

    def test_validate_response_all_status_codes(self, spec_with_response_schema: Path) -> None:
        """Test validation applies to all status codes when validate_success_only=False."""
        wrapper = APIWrapper(
            api_json_file=str(spec_with_response_schema),
            base_url="https://api.example.com",
            validation_config=ValidationConfig(enabled=True, validate_success_only=False),
        )
        # Uses "default" schema for non-200 responses
        result = wrapper.validate_response("/users", "GET", 404, {"error": "not found"})
        assert result is True

    def test_validate_response_no_schema(self, api_wrapper: APIWrapper) -> None:
        """Test validation passes when no schema defined."""
        result = api_wrapper.validate_response("/items", "GET", 200, {"any": "data"})
        assert result is True

    def test_get_response_schema_exact_status(
        self, wrapper_with_response_schema: APIWrapper
    ) -> None:
        """Test getting response schema by exact status code."""
        schema = wrapper_with_response_schema._get_response_schema("/users", "GET", 200)
        assert schema is not None
        assert "properties" in schema
        assert "users" in schema["properties"]

    def test_get_response_schema_default(self, wrapper_with_response_schema: APIWrapper) -> None:
        """Test getting default response schema."""
        schema = wrapper_with_response_schema._get_response_schema("/users", "GET", 500)
        assert schema is not None
        assert "properties" in schema
        assert "error" in schema["properties"]


class TestRetryLogic:
    """Tests for retry logic."""

    def test_retry_on_503(self, spec_file: Path) -> None:
        """Test retry on 503 status code."""
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            retry_config=RetryConfig(max_attempts=3, initial_wait=0.1, max_wait=1.0),
        )
        with patch.object(wrapper.session, "request") as mock_request:
            # First two calls return 503, third succeeds
            mock_503 = MagicMock()
            mock_503.status_code = 503

            mock_200 = MagicMock()
            mock_200.status_code = 200
            mock_200.json.return_value = {"users": []}

            mock_request.side_effect = [mock_503, mock_503, mock_200]

            result = wrapper.call_endpoint("/users", "GET")

            assert result == {"users": []}
            assert mock_request.call_count == 3

    def test_retry_exhausted(self, spec_file: Path) -> None:
        """Test that RetryError is raised when retries are exhausted."""
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            retry_config=RetryConfig(max_attempts=2, initial_wait=0.1, max_wait=1.0),
        )
        with patch.object(wrapper.session, "request") as mock_request:
            mock_503 = MagicMock()
            mock_503.status_code = 503

            mock_request.return_value = mock_503

            # tenacity raises RetryError when max attempts reached with retryable result
            with pytest.raises(RetryError):
                wrapper.call_endpoint("/users", "GET")

            # Should have tried max_attempts times
            assert mock_request.call_count == 2

    def test_retry_disabled(self, spec_file: Path) -> None:
        """Test that retry can be disabled."""
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            retry_config=RetryConfig(enabled=False),
        )
        with patch.object(wrapper.session, "request") as mock_request:
            mock_503 = MagicMock()
            mock_503.status_code = 503
            mock_503.raise_for_status.side_effect = requests.HTTPError("Service Unavailable")

            mock_request.return_value = mock_503

            with pytest.raises(requests.HTTPError):
                wrapper.call_endpoint("/users", "GET")

            # No retry, only one call
            assert mock_request.call_count == 1

    def test_retry_on_connection_error(self, spec_file: Path) -> None:
        """Test retry on connection error."""
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            retry_config=RetryConfig(
                max_attempts=3, initial_wait=0.1, max_wait=1.0, retry_on_connection_error=True
            ),
        )
        with patch.object(wrapper.session, "request") as mock_request:
            mock_200 = MagicMock()
            mock_200.status_code = 200
            mock_200.json.return_value = {"data": []}

            mock_request.side_effect = [
                requests.ConnectionError("Connection failed"),
                requests.ConnectionError("Connection failed"),
                mock_200,
            ]

            result = wrapper.call_endpoint("/users", "GET")

            assert result == {"data": []}
            assert mock_request.call_count == 3

    def test_no_retry_on_connection_error_when_disabled(self, spec_file: Path) -> None:
        """Test no retry on connection error when disabled."""
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            retry_config=RetryConfig(
                max_attempts=3, initial_wait=0.1, retry_on_connection_error=False
            ),
        )
        with patch.object(wrapper.session, "request") as mock_request:
            mock_request.side_effect = requests.ConnectionError("Connection failed")

            with pytest.raises(requests.ConnectionError):
                wrapper.call_endpoint("/users", "GET")

            # Only one call, no retry
            assert mock_request.call_count == 1

    def test_no_retry_on_success(self, spec_file: Path) -> None:
        """Test no retry on successful response."""
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            retry_config=RetryConfig(max_attempts=3),
        )
        with patch.object(wrapper.session, "request") as mock_request:
            mock_200 = MagicMock()
            mock_200.status_code = 200
            mock_200.json.return_value = {"users": []}

            mock_request.return_value = mock_200

            result = wrapper.call_endpoint("/users", "GET")

            assert result == {"users": []}
            assert mock_request.call_count == 1

    def test_no_retry_on_4xx(self, spec_file: Path) -> None:
        """Test no retry on 4xx client errors (not in default retryable list)."""
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            retry_config=RetryConfig(max_attempts=3, initial_wait=0.1),
        )
        with patch.object(wrapper.session, "request") as mock_request:
            mock_400 = MagicMock()
            mock_400.status_code = 400
            mock_400.raise_for_status.side_effect = requests.HTTPError("Bad Request")

            mock_request.return_value = mock_400

            with pytest.raises(requests.HTTPError):
                wrapper.call_endpoint("/users", "GET")

            # Only one call, no retry for 400
            assert mock_request.call_count == 1


class TestPerCallOverrides:
    """Tests for per-call configuration overrides."""

    def test_per_call_retry_config(self, spec_file: Path) -> None:
        """Test per-call retry configuration override."""
        # Instance-level: retry enabled
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            retry_config=RetryConfig(enabled=True, max_attempts=5),
        )
        with patch.object(wrapper.session, "request") as mock_request:
            mock_503 = MagicMock()
            mock_503.status_code = 503
            mock_503.raise_for_status.side_effect = requests.HTTPError("Service Unavailable")

            mock_request.return_value = mock_503

            # Per-call: disable retry
            with pytest.raises(requests.HTTPError):
                wrapper.call_endpoint("/users", "GET", retry_config=RetryConfig(enabled=False))

            # Only one call because per-call config disabled retry
            assert mock_request.call_count == 1

    def test_per_call_validation_config(self, tmp_path: Path) -> None:
        """Test per-call validation configuration override."""
        spec = {
            "swagger": "2.0",
            "basePath": "/api/v1",
            "paths": {
                "/users": {
                    "get": {
                        "summary": "List users",
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "required": ["users"],
                                            "properties": {
                                                "users": {"type": "array"},
                                            },
                                        }
                                    }
                                }
                            }
                        },
                    }
                }
            },
        }
        spec_path = tmp_path / "spec.json"
        spec_path.write_text(json.dumps(spec))

        # Instance-level: validation disabled
        wrapper = APIWrapper(
            api_json_file=str(spec_path),
            base_url="https://api.example.com",
            validation_config=ValidationConfig(enabled=False),
            retry_config=RetryConfig(enabled=False),
        )
        with patch.object(wrapper.session, "request") as mock_request:
            mock_200 = MagicMock()
            mock_200.status_code = 200
            mock_200.json.return_value = {"invalid": "data"}

            mock_request.return_value = mock_200

            # Per-call: enable strict validation
            with pytest.raises(ResponseValidationError):
                wrapper.call_endpoint(
                    "/users",
                    "GET",
                    validation_config=ValidationConfig(enabled=True, strict=True),
                )


class TestAPIWrapperWithConfigs:
    """Tests for APIWrapper initialization with configs."""

    def test_default_retry_config(self, spec_file: Path) -> None:
        """Test default retry config is enabled."""
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
        )
        assert wrapper.retry_config.enabled is True
        assert wrapper.retry_config.max_attempts == 3

    def test_default_validation_config(self, spec_file: Path) -> None:
        """Test default validation config is disabled."""
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
        )
        assert wrapper.validation_config.enabled is False

    def test_custom_retry_config(self, spec_file: Path) -> None:
        """Test custom retry config."""
        config = RetryConfig(enabled=False, max_attempts=5)
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            retry_config=config,
        )
        assert wrapper.retry_config.enabled is False
        assert wrapper.retry_config.max_attempts == 5

    def test_custom_validation_config(self, spec_file: Path) -> None:
        """Test custom validation config."""
        config = ValidationConfig(enabled=True, strict=True)
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            validation_config=config,
        )
        assert wrapper.validation_config.enabled is True
        assert wrapper.validation_config.strict is True


class TestPaginationConfig:
    """Tests for PaginationConfig model."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = PaginationConfig()
        assert config.enabled is True
        assert config.max_pages == 100
        assert config.records_key == "records"

    def test_custom_values(self) -> None:
        """Test custom configuration values."""
        config = PaginationConfig(
            enabled=False,
            max_pages=50,
            records_key="items",
        )
        assert config.enabled is False
        assert config.max_pages == 50
        assert config.records_key == "items"

    def test_max_pages_minimum(self) -> None:
        """Test max_pages validation rejects 0."""
        with pytest.raises(ValueError):
            PaginationConfig(max_pages=0)

    def test_max_pages_maximum(self) -> None:
        """Test max_pages validation rejects values above 10000."""
        with pytest.raises(ValueError):
            PaginationConfig(max_pages=10001)

    def test_extra_fields_forbidden(self) -> None:
        """Test that extra fields are rejected."""
        with pytest.raises(ValueError):
            PaginationConfig(unknown_field="value")  # type: ignore[call-arg]


class TestOntapNextPageExtractor:
    """Tests for ontap_next_page_extractor function."""

    def test_extracts_next_href(self) -> None:
        """Test extraction of next href from _links.next.href."""
        response = {
            "records": [],
            "_links": {
                "self": {"href": "/api/storage/aggregates"},
                "next": {"href": "/api/storage/aggregates?start.name=aggr5&max_records=25"},
            },
        }
        result = ontap_next_page_extractor(response)
        assert result == "/api/storage/aggregates?start.name=aggr5&max_records=25"

    def test_returns_none_when_no_links(self) -> None:
        """Test returns None when _links key is missing."""
        response: dict[str, Any] = {"records": []}
        assert ontap_next_page_extractor(response) is None

    def test_returns_none_when_no_next(self) -> None:
        """Test returns None when _links has self but no next."""
        response: dict[str, Any] = {
            "records": [],
            "_links": {"self": {"href": "/api/storage/aggregates"}},
        }
        assert ontap_next_page_extractor(response) is None

    def test_returns_none_when_links_is_none(self) -> None:
        """Test returns None when _links value is None."""
        response: dict[str, Any] = {"records": [], "_links": None}
        assert ontap_next_page_extractor(response) is None

    def test_returns_none_for_empty_dict(self) -> None:
        """Test returns None for empty response dict."""
        assert ontap_next_page_extractor({}) is None

    def test_returns_none_when_next_has_no_href(self) -> None:
        """Test returns None when _links.next exists but has no href."""
        response: dict[str, Any] = {
            "records": [],
            "_links": {"next": {"self": "/api/storage/aggregates"}},
        }
        assert ontap_next_page_extractor(response) is None


class TestGetAllRecords:
    """Tests for APIWrapper.get_all_records method."""

    def _make_response(
        self,
        data: dict[str, Any],
        status_code: int = 200,
    ) -> MagicMock:
        """Helper to create a mock HTTP response."""
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.json.return_value = data
        mock_resp.raise_for_status.return_value = None
        return mock_resp

    def test_single_page_no_pagination_links(self, api_wrapper: APIWrapper) -> None:
        """Test single page response without pagination links returns as-is."""
        page_data = {
            "records": [{"name": "vol1"}, {"name": "vol2"}],
            "num_records": 2,
        }
        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.return_value = self._make_response(page_data)

            result = api_wrapper.get_all_records("/users", "GET")

            assert result["records"] == [{"name": "vol1"}, {"name": "vol2"}]
            assert result["num_records"] == 2
            assert mock_request.call_count == 1

    def test_two_pages(self, api_wrapper: APIWrapper) -> None:
        """Test following one next link and merging records."""
        page1 = {
            "records": [{"name": "vol1"}],
            "num_records": 1,
            "_links": {"next": {"href": "/api/v1/users?start=2&max_records=1"}},
        }
        page2 = {
            "records": [{"name": "vol2"}],
            "num_records": 1,
        }
        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.side_effect = [
                self._make_response(page1),
                self._make_response(page2),
            ]

            result = api_wrapper.get_all_records("/users", "GET")

            assert result["records"] == [{"name": "vol1"}, {"name": "vol2"}]
            assert result["num_records"] == 2
            assert "_links" not in result
            assert mock_request.call_count == 2

    def test_three_pages(self, api_wrapper: APIWrapper) -> None:
        """Test following two next links with correct total."""
        page1 = {
            "records": [{"name": "a"}],
            "num_records": 1,
            "_links": {"next": {"href": "/api/v1/users?start=2"}},
        }
        page2 = {
            "records": [{"name": "b"}],
            "num_records": 1,
            "_links": {"next": {"href": "/api/v1/users?start=3"}},
        }
        page3 = {
            "records": [{"name": "c"}],
            "num_records": 1,
        }
        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.side_effect = [
                self._make_response(page1),
                self._make_response(page2),
                self._make_response(page3),
            ]

            result = api_wrapper.get_all_records("/users", "GET")

            assert len(result["records"]) == 3
            assert result["num_records"] == 3
            assert mock_request.call_count == 3

    def test_subsequent_page_url_construction(self, api_wrapper: APIWrapper) -> None:
        """Test that subsequent page URLs use base_url + href (no duplicate /api)."""
        page1 = {
            "records": [{"name": "vol1"}],
            "_links": {"next": {"href": "/api/v1/users?start=2"}},
        }
        page2 = {"records": [{"name": "vol2"}]}

        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.side_effect = [
                self._make_response(page1),
                self._make_response(page2),
            ]

            api_wrapper.get_all_records("/users", "GET")

            # Second call should use base_url + href directly
            second_call = mock_request.call_args_list[1]
            assert second_call[0][1] == "https://api.example.com/api/v1/users?start=2"

    def test_absolute_url_in_next_link(self, api_wrapper: APIWrapper) -> None:
        """Test that absolute URLs in next links are used as-is."""
        page1 = {
            "records": [{"name": "vol1"}],
            "_links": {"next": {"href": "https://other.example.com/api/v1/users?start=2"}},
        }
        page2 = {"records": [{"name": "vol2"}]}

        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.side_effect = [
                self._make_response(page1),
                self._make_response(page2),
            ]

            api_wrapper.get_all_records("/users", "GET")

            second_call = mock_request.call_args_list[1]
            assert second_call[0][1] == "https://other.example.com/api/v1/users?start=2"

    def test_pagination_disabled(self, api_wrapper: APIWrapper) -> None:
        """Test that disabled pagination returns first page as-is with _links preserved."""
        page_data = {
            "records": [{"name": "vol1"}],
            "_links": {"next": {"href": "/api/v1/users?start=2"}},
        }
        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.return_value = self._make_response(page_data)

            result = api_wrapper.get_all_records(
                "/users",
                "GET",
                pagination_config=PaginationConfig(enabled=False),
            )

            assert "_links" in result
            assert mock_request.call_count == 1

    def test_max_pages_limit(self, api_wrapper: APIWrapper) -> None:
        """Test that pagination stops at max_pages and returns collected records."""

        def make_page(n: int) -> dict[str, Any]:
            return {
                "records": [{"name": f"vol{n}"}],
                "_links": {"next": {"href": f"/api/v1/users?start={n + 1}"}},
            }

        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.side_effect = [self._make_response(make_page(i)) for i in range(1, 5)]

            result = api_wrapper.get_all_records(
                "/users",
                "GET",
                pagination_config=PaginationConfig(max_pages=3),
            )

            assert len(result["records"]) == 3
            assert mock_request.call_count == 3

    def test_custom_records_key(self, api_wrapper: APIWrapper) -> None:
        """Test pagination with custom records_key."""
        page1 = {
            "items": [{"name": "vol1"}],
            "_links": {"next": {"href": "/api/v1/users?start=2"}},
        }
        page2 = {"items": [{"name": "vol2"}]}

        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.side_effect = [
                self._make_response(page1),
                self._make_response(page2),
            ]

            result = api_wrapper.get_all_records(
                "/users",
                "GET",
                pagination_config=PaginationConfig(records_key="items"),
            )

            assert result["items"] == [{"name": "vol1"}, {"name": "vol2"}]

    def test_non_dict_response_raises_type_error(self, api_wrapper: APIWrapper) -> None:
        """Test that non-dict response raises TypeError."""
        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.text = "plain text"
            mock_resp.json.side_effect = ValueError("No JSON")
            mock_resp.raise_for_status.return_value = None
            mock_request.return_value = mock_resp

            with pytest.raises(TypeError, match="Expected dict response"):
                api_wrapper.get_all_records("/users", "GET")

    def test_page2_json_parse_failure(self, api_wrapper: APIWrapper) -> None:
        """Test that page 2 JSON parse failure raises TypeError."""
        page1 = {
            "records": [{"name": "vol1"}],
            "_links": {"next": {"href": "/api/v1/users?start=2"}},
        }
        mock_page2 = MagicMock()
        mock_page2.status_code = 200
        mock_page2.json.side_effect = ValueError("No JSON")
        mock_page2.raise_for_status.return_value = None

        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.side_effect = [
                self._make_response(page1),
                mock_page2,
            ]

            with pytest.raises(TypeError, match="failed to parse JSON"):
                api_wrapper.get_all_records("/users", "GET")

    def test_page2_http_error(self, api_wrapper: APIWrapper) -> None:
        """Test that page 2 HTTP 500 raises HTTPError immediately."""
        page1 = {
            "records": [{"name": "vol1"}],
            "_links": {"next": {"href": "/api/v1/users?start=2"}},
        }
        mock_page2 = MagicMock()
        mock_page2.status_code = 500
        mock_page2.raise_for_status.side_effect = requests.HTTPError("Server Error")

        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.side_effect = [
                self._make_response(page1),
                mock_page2,
            ]

            with pytest.raises(requests.HTTPError, match="Server Error"):
                api_wrapper.get_all_records(
                    "/users",
                    "GET",
                    retry_config=RetryConfig(enabled=False),
                )

    def test_custom_next_page_extractor(self, api_wrapper: APIWrapper) -> None:
        """Test pagination with a custom next_page_extractor."""

        def custom_extractor(response: dict[str, Any]) -> str | None:
            return response.get("next_url")

        page1 = {
            "records": [{"name": "vol1"}],
            "next_url": "/api/v1/users?page=2",
        }
        page2 = {"records": [{"name": "vol2"}]}

        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.side_effect = [
                self._make_response(page1),
                self._make_response(page2),
            ]

            result = api_wrapper.get_all_records(
                "/users",
                "GET",
                next_page_extractor=custom_extractor,
            )

            assert result["records"] == [{"name": "vol1"}, {"name": "vol2"}]

    def test_headers_include_additional_headers(self, api_wrapper: APIWrapper) -> None:
        """Test that page 2 requests include additional_headers."""
        page1 = {
            "records": [{"name": "vol1"}],
            "_links": {"next": {"href": "/api/v1/users?start=2"}},
        }
        page2 = {"records": [{"name": "vol2"}]}

        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.side_effect = [
                self._make_response(page1),
                self._make_response(page2),
            ]

            api_wrapper.get_all_records(
                "/users",
                "GET",
                additional_headers={"X-Custom": "test-value"},
            )

            # Check page 2 headers include the custom header
            second_call = mock_request.call_args_list[1]
            assert second_call[1]["headers"]["X-Custom"] == "test-value"

    def test_retry_config_applies_to_subsequent_pages(self, spec_file: Path) -> None:
        """Test that per-call retry config is used for page 2."""
        wrapper = APIWrapper(
            api_json_file=str(spec_file),
            base_url="https://api.example.com",
            retry_config=RetryConfig(enabled=False),
        )
        page1 = {
            "records": [{"name": "vol1"}],
            "_links": {"next": {"href": "/api/v1/users?start=2"}},
        }
        # Page 2: first attempt 503, second attempt succeeds
        mock_503 = MagicMock()
        mock_503.status_code = 503

        page2_data = {"records": [{"name": "vol2"}]}

        with patch.object(wrapper.session, "request") as mock_request:
            mock_request.side_effect = [
                self._make_response(page1),
                mock_503,
                self._make_response(page2_data),
            ]

            result = wrapper.get_all_records(
                "/users",
                "GET",
                retry_config=RetryConfig(
                    enabled=True,
                    max_attempts=3,
                    initial_wait=0.1,
                    max_wait=1.0,
                ),
            )

            assert result["records"] == [{"name": "vol1"}, {"name": "vol2"}]
            assert mock_request.call_count == 3

    def test_validation_applies_to_subsequent_pages(self, tmp_path: Path) -> None:
        """Test that validation is applied to subsequent pages in strict mode."""
        spec = {
            "swagger": "2.0",
            "basePath": "/api/v1",
            "paths": {
                "/users": {
                    "get": {
                        "summary": "List users",
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "required": ["records"],
                                            "properties": {
                                                "records": {"type": "array"},
                                            },
                                        }
                                    }
                                }
                            }
                        },
                    }
                }
            },
        }
        spec_path = tmp_path / "spec.json"
        spec_path.write_text(json.dumps(spec))

        wrapper = APIWrapper(
            api_json_file=str(spec_path),
            base_url="https://api.example.com",
            retry_config=RetryConfig(enabled=False),
        )

        page1 = {
            "records": [{"name": "vol1"}],
            "_links": {"next": {"href": "/api/v1/users?start=2"}},
        }
        # Page 2 has invalid data (missing required 'records')
        page2_invalid = {"invalid": "data"}

        with patch.object(wrapper.session, "request") as mock_request:
            mock_request.side_effect = [
                self._make_response(page1),
                self._make_response(page2_invalid),
            ]

            with pytest.raises(ResponseValidationError):
                wrapper.get_all_records(
                    "/users",
                    "GET",
                    validation_config=ValidationConfig(enabled=True, strict=True),
                )

    def test_validation_skipped_when_disabled(self, api_wrapper: APIWrapper) -> None:
        """Test that disabled validation does not raise on invalid data."""
        page1 = {
            "records": [{"name": "vol1"}],
            "_links": {"next": {"href": "/api/v1/users?start=2"}},
        }
        page2 = {"records": [{"name": "vol2"}]}

        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.side_effect = [
                self._make_response(page1),
                self._make_response(page2),
            ]

            # Default validation is disabled, should not raise
            result = api_wrapper.get_all_records("/users", "GET")

            assert len(result["records"]) == 2

    def test_empty_records_on_pages(self, api_wrapper: APIWrapper) -> None:
        """Test that empty pages with next links are handled correctly."""
        page1 = {
            "records": [],
            "_links": {"next": {"href": "/api/v1/users?start=2"}},
        }
        page2 = {
            "records": [],
            "_links": {"next": {"href": "/api/v1/users?start=3"}},
        }
        page3 = {"records": [{"name": "vol1"}]}

        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.side_effect = [
                self._make_response(page1),
                self._make_response(page2),
                self._make_response(page3),
            ]

            result = api_wrapper.get_all_records("/users", "GET")

            assert result["records"] == [{"name": "vol1"}]
            assert mock_request.call_count == 3

    def test_merged_response_preserves_other_keys(self, api_wrapper: APIWrapper) -> None:
        """Test that extra top-level keys from first page are preserved."""
        page1 = {
            "records": [{"name": "vol1"}],
            "extra_key": "preserved_value",
            "another_key": 42,
            "_links": {"next": {"href": "/api/v1/users?start=2"}},
        }
        page2 = {"records": [{"name": "vol2"}]}

        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.side_effect = [
                self._make_response(page1),
                self._make_response(page2),
            ]

            result = api_wrapper.get_all_records("/users", "GET")

            assert result["extra_key"] == "preserved_value"
            assert result["another_key"] == 42

    def test_num_records_not_present_in_source(self, api_wrapper: APIWrapper) -> None:
        """Test that num_records is not added if not in original response."""
        page1 = {
            "records": [{"name": "vol1"}],
            "_links": {"next": {"href": "/api/v1/users?start=2"}},
        }
        page2 = {"records": [{"name": "vol2"}]}

        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.side_effect = [
                self._make_response(page1),
                self._make_response(page2),
            ]

            result = api_wrapper.get_all_records("/users", "GET")

            assert "num_records" not in result

    def test_call_endpoint_params_forwarded(self, api_wrapper: APIWrapper) -> None:
        """Test that path_params and query_params reach page 1."""
        page_data = {"records": [{"name": "vol1"}]}

        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_request.return_value = self._make_response(page_data)

            api_wrapper.get_all_records(
                "/users/{id}",
                "GET",
                path_params={"id": "123"},
                query_params={"limit": 25},
            )

            call_args = mock_request.call_args
            url = call_args[0][1]
            assert "/users/123" in url
            assert "limit=25" in url
