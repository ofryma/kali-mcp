# Test Suite for Kali MCP Server

This directory contains the comprehensive test suite for the Kali MCP Server project.

## Structure

```
tests/
├── conftest.py                    # Pytest fixtures and configuration
├── test_kali_client.py           # Tests for KaliToolsClient
├── test_kali_server.py           # Tests for Flask API endpoints
├── test_command_executor.py      # Tests for CommandExecutor class
├── test_mcp_server.py            # Tests for MCP server setup
├── test_integration.py           # Integration tests
└── test_tools/                   # Tool-specific tests
    ├── test_network_scanning.py
    ├── test_web_scanning.py
    └── test_password_cracking.py
```

## Running Tests

### All Tests
```bash
make test
# or
pytest
```

### Unit Tests Only
```bash
make test-unit
# or
pytest -m "not integration"
```

### Integration Tests Only
```bash
make test-integration
# or
pytest -m integration
```

### With Coverage Report
```bash
make test-coverage
# or
pytest --cov=server --cov=kali_server --cov-report=html
```

### Specific Test File
```bash
make test-file FILE=tests/test_kali_client.py
# or
pytest tests/test_kali_client.py -v
```

### Specific Test
```bash
pytest tests/test_kali_client.py::TestKaliToolsClient::test_client_initialization -v
```

## Test Categories

### Unit Tests
- Test individual components in isolation
- Mock external dependencies
- Fast execution
- Run by default

### Integration Tests
- Test component interactions
- May require running server
- Marked with `@pytest.mark.integration`
- Can be skipped in CI/CD

### Network Tests
- Tests that require network access
- Marked with `@pytest.mark.network`
- Often skipped by default

## Writing Tests

### Basic Test Structure

```python
import pytest

class TestMyComponent:
    """Test suite for MyComponent"""
    
    def test_basic_functionality(self, mock_kali_client):
        """Test description"""
        # Arrange
        # Act
        # Assert
        pass
```

### Using Fixtures

Common fixtures available in `conftest.py`:
- `mock_kali_client` - Mocked KaliToolsClient
- `kali_client` - Real KaliToolsClient (for integration tests)
- `flask_app` - Flask application instance
- `flask_client` - Flask test client
- `sample_nmap_response` - Sample nmap response
- `sample_error_response` - Sample error response
- `sample_timeout_response` - Sample timeout response

### Example Test

```python
def test_nmap_scan(mock_kali_client):
    """Test nmap scan functionality"""
    # Configure mock response
    mock_kali_client.safe_post.return_value = {
        "stdout": "Nmap scan report",
        "success": True
    }
    
    # Execute test
    result = mock_kali_client.safe_post("api/tools/nmap", {
        "target": "127.0.0.1"
    })
    
    # Verify
    assert result["success"] is True
    mock_kali_client.safe_post.assert_called_once()
```

## Mocking

The test suite uses several mocking strategies:

### responses Library
For mocking HTTP requests:
```python
import responses

@responses.activate
def test_api_call():
    responses.add(
        responses.GET,
        "http://localhost:5001/health",
        json={"status": "healthy"},
        status=200
    )
    # Test code here
```

### unittest.mock
For mocking Python objects:
```python
from unittest.mock import Mock, patch

@patch('module.function')
def test_with_patch(mock_function):
    mock_function.return_value = "mocked"
    # Test code here
```

## Coverage

Test coverage reports are generated in multiple formats:
- Terminal output (default)
- HTML report in `htmlcov/` directory
- XML report for CI/CD systems

View HTML coverage report:
```bash
make test-coverage
open htmlcov/index.html
```

## Continuous Integration

Tests run automatically on:
- Push to main/develop branches
- Pull requests
- Multiple Python versions (3.9, 3.10, 3.11, 3.12)

See `.github/workflows/tests.yml` for CI configuration.

## Best Practices

1. **Test Naming**: Use descriptive names that explain what is being tested
2. **Test Organization**: Group related tests in classes
3. **Arrange-Act-Assert**: Structure tests clearly
4. **Mocking**: Mock external dependencies to keep tests fast and reliable
5. **Coverage**: Aim for >80% code coverage
6. **Documentation**: Add docstrings to test functions
7. **Markers**: Use pytest markers to categorize tests
8. **Fixtures**: Use fixtures to reduce code duplication

## Troubleshooting

### Tests Fail Due to Missing Dependencies
```bash
pip install -r requirements.txt
```

### Import Errors
Make sure you're running pytest from the project root:
```bash
cd /path/to/kali-mcp
pytest
```

### Integration Tests Fail
Integration tests may require a running Kali API server:
```bash
# Skip integration tests
pytest -m "not integration"
```

### Permission Errors on macOS
Some tests may fail on macOS due to security restrictions. Run with appropriate permissions or skip those tests.

## Adding New Tests

1. Create test file in appropriate directory
2. Import required fixtures from `conftest.py`
3. Write test class and methods
4. Add appropriate markers
5. Run tests to verify
6. Check coverage impact

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [responses Library](https://github.com/getsentry/responses)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)

