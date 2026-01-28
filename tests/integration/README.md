# Integration Tests

This directory contains integration tests that verify the interaction between
pynetappfoundry components and (mocked) external systems.

## Purpose

Integration tests differ from unit tests in that they:
- Test multiple components working together
- Verify realistic usage patterns
- Use mocked external services to simulate real-world scenarios
- Demonstrate how to test against ONTAP/DII APIs

## Running Tests

```bash
# Run all integration tests
uv run pytest tests/integration/ -v

# Run with coverage
uv run pytest tests/integration/ --cov=pynetappfoundry -v

# Run specific test file
uv run pytest tests/integration/test_ontap_client.py -v
```

## Test Structure

### Fixtures (`conftest.py`)

Common fixtures for integration tests:

- `mock_cluster` - A mock cluster object with `name` and `ip` attributes
- `mock_ontap_spec` - A minimal ONTAP-like OpenAPI specification
- `mock_config_dir` - A complete mock configuration directory
- `sample_volume_response` - Example ONTAP volume API response
- `sample_cluster_response` - Example ONTAP cluster API response

### Test Files

- `test_ontap_client.py` - Tests for ONTAP API client interactions

## Writing Integration Tests

### Example: Testing an API Call

```python
def test_call_endpoint(self, api_wrapper, sample_response):
    """Test calling an API endpoint with mocked response."""
    with patch.object(api_wrapper.session, "request") as mock_request:
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_response
        mock_request.return_value = mock_response

        # Call the endpoint
        result = api_wrapper.call_endpoint("/storage/volumes", "GET")

        # Verify
        assert result["num_records"] == 2
```

### Example: Testing Retry Behavior

```python
def test_retry_on_503(self, api_wrapper):
    """Test retry on transient failure."""
    with patch.object(api_wrapper.session, "request") as mock_request:
        mock_503 = MagicMock()
        mock_503.status_code = 503

        mock_200 = MagicMock()
        mock_200.status_code = 200
        mock_200.json.return_value = {"data": "success"}

        mock_request.side_effect = [mock_503, mock_200]

        result = api_wrapper.call_endpoint("/endpoint", "GET")

        assert mock_request.call_count == 2
        assert result["data"] == "success"
```

### Example: Testing Config Integration

```python
def test_config_search(self, mock_config_dir, tmp_path):
    """Test searching clusters by criteria."""
    config = Config(config_dir=str(mock_config_dir), ...)

    clusters = config.search("clusters", {"env": "Prod"})

    assert "prod-cluster" in clusters
```

## Best Practices

1. **Use fixtures** - Create reusable fixtures in `conftest.py`
2. **Mock external calls** - Never make real HTTP requests
3. **Test realistic scenarios** - Use realistic data shapes
4. **Document test purpose** - Include docstrings explaining what's being tested
5. **Clean up resources** - Use `try/finally` or context managers
