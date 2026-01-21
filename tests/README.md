# Testing Guide for ViDownloader

This document provides information about the test suite for ViDownloader.

## Overview

ViDownloader uses `pytest` as its testing framework. The test suite provides comprehensive coverage of core functionality including:

- URL parsing and link extraction
- Video metadata models and serialization
- File I/O operations (VIIO format)
- HTTP request handling with retry logic
- Settings management
- Utility functions

## Running Tests

### Install Development Dependencies

```powershell
pip install -e ".[dev]"
```

This installs:
- `pytest` - Testing framework
- `pytest-qt` - PyQt5 testing support
- `pytest-cov` - Code coverage reporting
- `pytest-mock` - Advanced mocking capabilities

### Run All Tests

```powershell
pytest tests/
```

### Run Tests with Verbose Output

```powershell
pytest tests/ -v
```

### Run Tests with Coverage Report

```powershell
pytest tests/ --cov=vidownloader --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`.

### Run Specific Test Files

```powershell
# Test models only
pytest tests/test_models.py -v

# Test HTTP module only
pytest tests/test_http.py -v

# Test VIIO file operations only
pytest tests/test_viio.py -v
```

### Run Specific Test Classes or Methods

```powershell
# Run a specific test class
pytest tests/test_utils.py::TestParseLinks -v

# Run a specific test method
pytest tests/test_utils.py::TestParseLinks::test_parse_youtube_video_url -v
```

## Test Structure

```
tests/
├── __init__.py              # Empty init file
├── conftest.py              # Shared fixtures
├── test_http.py             # HTTP request tests
├── test_models.py           # Data model tests
├── test_parser.py           # YouTube parser tests
├── test_settings.py         # Settings management tests
├── test_utils.py            # Utility function tests
└── test_viio.py             # File I/O tests
```

## Available Fixtures

The `conftest.py` file provides several fixtures for testing:

### Session Fixtures
- `qapp` - QApplication instance (required for PyQt5 tests)

### Function Fixtures
- `temp_dir` - Temporary directory for file operations
- `sample_video_data` - Mock YouTube video data
- `sample_shorts_data` - Mock YouTube shorts data
- `sample_link` - Sample Link object
- `sample_video` - Sample Video object
- `sample_videos_list` - List of sample Video objects

## Writing New Tests

### Basic Test Example

```python
def test_my_function():
    """Test description."""
    result = my_function(input_value)
    assert result == expected_value
```

### Using Fixtures

```python
def test_with_fixture(sample_video):
    """Test using a fixture."""
    assert sample_video.caption == "Test Video"
    assert sample_video.video_id == "test123"
```

### Testing Exceptions

```python
def test_error_handling():
    """Test error handling."""
    with pytest.raises(ValueError, match="Invalid input"):
        risky_function(bad_input)
```

### Mocking External Dependencies

```python
from unittest.mock import Mock, patch

@patch('vidownloader.core.http.curl_requests.request')
def test_http_request(mock_request):
    """Test HTTP request with mocking."""
    mock_response = Mock()
    mock_response.ok = True
    mock_request.return_value = mock_response
    
    response = get("https://example.com")
    assert response.ok
```

## Test Coverage

Current test coverage includes:

- **Models** - 100% coverage of dataclasses and serialization
- **VIIO** - Complete coverage of file I/O operations
- **HTTP** - Comprehensive retry logic and error handling tests
- **Utils** - All utility functions tested
- **Parser** - YouTube response parsing tests
- **Settings** - Settings storage and retrieval tests

## Continuous Integration

Tests should be run before:
- Committing changes
- Creating pull requests
- Releasing new versions

## Best Practices

1. **Write descriptive test names** - Test names should clearly indicate what is being tested
2. **One assertion per concept** - Keep tests focused on a single behavior
3. **Use fixtures** - Reuse common test data through fixtures
4. **Mock external dependencies** - Don't make real HTTP requests or file operations when possible
5. **Test edge cases** - Include tests for boundary conditions and error cases
6. **Keep tests independent** - Tests should not depend on each other

## Troubleshooting

### QApplication Issues

If you encounter issues with PyQt5 tests, ensure you have the `qapp` fixture in scope:

```python
def test_qt_widget(qapp):
    """Test that uses Qt widgets."""
    # Your test code here
```

### Path Issues

Use `temp_dir` fixture for file operations:

```python
def test_file_operation(temp_dir):
    """Test file operations."""
    file_path = temp_dir / "test.txt"
    file_path.write_text("content")
```

### Import Errors

Ensure the project is installed in development mode:

```powershell
pip install -e .
```

## Contributing

When adding new features:
1. Write tests first (TDD approach recommended)
2. Ensure all tests pass
3. Maintain or improve code coverage
4. Update this README if adding new test patterns
