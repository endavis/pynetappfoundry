"""Integration tests for ONTAP API client.

These tests demonstrate how to test ONTAP API interactions using mocked
HTTP responses. They serve as examples for testing patterns that can be
applied to actual integration testing.

Example usage:
    # Run all integration tests
    uv run pytest tests/integration/ -v

    # Run only ONTAP client tests
    uv run pytest tests/integration/test_ontap_client.py -v
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import requests

from pynetappfoundry.clients.openapi import APIWrapper
from pynetappfoundry.core.config import Config
from pynetappfoundry.core.models import RetryConfig, ValidationConfig


class TestAPIWrapperIntegration:
    """Integration tests for APIWrapper with realistic scenarios."""

    @pytest.fixture
    def api_wrapper(self, mock_ontap_spec: Path) -> APIWrapper:
        """Create an APIWrapper instance with mock ONTAP spec."""
        return APIWrapper(
            api_json_file=str(mock_ontap_spec / "all.json"),
            base_url="https://test-cluster.example.com",
            auth_header={"Authorization": "Basic YWRtaW46YWRtaW4="},
            base_api_path="/api",
        )

    def test_list_available_endpoints(self, api_wrapper: APIWrapper) -> None:
        """Test listing all available API endpoints."""
        endpoints = api_wrapper.list_endpoints()

        # Should have our mock endpoints
        assert len(endpoints) >= 3
        paths = [ep[0] for ep in endpoints]
        assert "/cluster" in paths
        assert "/storage/volumes" in paths
        assert "/storage/aggregates" in paths

    def test_get_endpoint_parameters(self, api_wrapper: APIWrapper) -> None:
        """Test getting parameter suggestions for an endpoint."""
        params = api_wrapper.suggest_parameters("/storage/volumes", "GET")

        assert params["path"] == "/storage/volumes"
        assert params["method"] == "GET"
        assert "query_params" in params

        # Check query parameters are extracted
        query_param_names = [p["name"] for p in params["query_params"]]
        assert "svm.name" in query_param_names
        assert "fields" in query_param_names

    def test_call_endpoint_with_mocked_response(
        self, api_wrapper: APIWrapper, sample_volume_response: dict[str, Any]
    ) -> None:
        """Test calling an endpoint with a mocked HTTP response."""
        with patch.object(api_wrapper.session, "request") as mock_request:
            # Setup mock response
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_volume_response
            mock_response.text = '{"records": []}'
            mock_request.return_value = mock_response

            # Call the endpoint
            result = api_wrapper.call_endpoint(
                "/storage/volumes",
                "GET",
                query_params={"fields": "name,size,space"},
            )

            # Verify the call was made correctly
            mock_request.assert_called_once()
            call_args = mock_request.call_args

            # Check URL construction (URL is second positional arg after method)
            url = call_args[0][1] if len(call_args[0]) > 1 else call_args.kwargs.get("url", "")
            assert "https://test-cluster.example.com/api/storage/volumes" in url
            assert "fields=" in url

            # Verify response
            assert result["num_records"] == 2
            assert len(result["records"]) == 2

    def test_call_endpoint_with_path_parameters(
        self, api_wrapper: APIWrapper, sample_cluster_response: dict[str, Any]
    ) -> None:
        """Test calling an endpoint that requires path parameters."""
        with patch.object(api_wrapper.session, "request") as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_cluster_response
            mock_response.text = "{}"
            mock_request.return_value = mock_response

            result = api_wrapper.call_endpoint("/cluster", "GET")

            assert result["name"] == "test-cluster"
            assert result["version"]["generation"] == 9


class TestRetryBehavior:
    """Tests demonstrating retry behavior with transient failures."""

    @pytest.fixture
    def api_wrapper_with_retry(self, mock_ontap_spec: Path) -> APIWrapper:
        """Create an APIWrapper with retry enabled."""
        return APIWrapper(
            api_json_file=str(mock_ontap_spec / "all.json"),
            base_url="https://test-cluster.example.com",
            base_api_path="/api",
            retry_config=RetryConfig(
                enabled=True,
                max_attempts=3,
                initial_wait=0.1,
                max_wait=1.0,
            ),
        )

    def test_retry_on_transient_failure(
        self,
        api_wrapper_with_retry: APIWrapper,
        sample_cluster_response: dict[str, Any],
    ) -> None:
        """Test that transient 503 errors trigger retries."""
        with patch.object(api_wrapper_with_retry.session, "request") as mock_request:
            # First call fails with 503, second succeeds
            mock_503 = MagicMock()
            mock_503.status_code = 503

            mock_200 = MagicMock()
            mock_200.status_code = 200
            mock_200.json.return_value = sample_cluster_response
            mock_200.text = "{}"

            mock_request.side_effect = [mock_503, mock_200]

            result = api_wrapper_with_retry.call_endpoint("/cluster", "GET")

            # Should have retried and succeeded
            assert mock_request.call_count == 2
            assert result["name"] == "test-cluster"

    def test_no_retry_on_client_error(self, api_wrapper_with_retry: APIWrapper) -> None:
        """Test that 4xx errors do not trigger retries."""
        with patch.object(api_wrapper_with_retry.session, "request") as mock_request:
            mock_404 = MagicMock()
            mock_404.status_code = 404
            mock_404.raise_for_status.side_effect = requests.HTTPError("Not Found")

            mock_request.return_value = mock_404

            with pytest.raises(requests.HTTPError):
                api_wrapper_with_retry.call_endpoint("/cluster", "GET")

            # Should not have retried
            assert mock_request.call_count == 1


class TestResponseValidation:
    """Tests demonstrating response validation features."""

    @pytest.fixture
    def api_wrapper_with_validation(self, mock_ontap_spec: Path) -> APIWrapper:
        """Create an APIWrapper with validation enabled."""
        return APIWrapper(
            api_json_file=str(mock_ontap_spec / "all.json"),
            base_url="https://test-cluster.example.com",
            base_api_path="/api",
            retry_config=RetryConfig(enabled=False),
            validation_config=ValidationConfig(enabled=True, strict=False),
        )

    def test_valid_response_passes_validation(
        self,
        api_wrapper_with_validation: APIWrapper,
        sample_cluster_response: dict[str, Any],
    ) -> None:
        """Test that valid responses pass schema validation."""
        with patch.object(api_wrapper_with_validation.session, "request") as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_cluster_response
            mock_response.text = "{}"
            mock_request.return_value = mock_response

            # Should not raise any validation errors
            result = api_wrapper_with_validation.call_endpoint("/cluster", "GET")
            assert result["name"] == "test-cluster"


class TestConfigIntegration:
    """Tests demonstrating Config integration with API clients."""

    def test_config_loads_cluster_data(self, mock_config_dir: Path, tmp_path: Path) -> None:
        """Test that Config correctly loads cluster configuration."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)

            config = Config(
                config_dir=str(mock_config_dir),
                output_dir=str(output_dir),
                script_name="test",
            )

            # Search for clusters
            clusters = config.search("clusters", {"env": "Dev"})
            assert "test-cluster" in clusters
            assert clusters["test-cluster"]["ip"] == "192.168.1.100"
        finally:
            os.chdir(original_cwd)

    def test_config_search_with_tags(self, mock_config_dir: Path, tmp_path: Path) -> None:
        """Test searching clusters by tags."""
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)

            config = Config(
                config_dir=str(mock_config_dir),
                output_dir=str(output_dir),
                script_name="test",
            )

            # Search by tag
            clusters = config.search("clusters", {"tags": "test"})
            assert "test-cluster" in clusters
        finally:
            os.chdir(original_cwd)
