"""Tests for APIWrapper class."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import requests

from pynetappfoundry.clients.openapi import APIWrapper


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
