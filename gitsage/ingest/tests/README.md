# GitSage Ingest Module Tests

This directory contains unit and integration tests for the `gitsage.ingest` module.

## Test Structure

```
gitsage/ingest/tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Shared pytest configuration and fixtures
├── test_repo_cloner.py      # Unit tests for repository cloning
├── test_file_scanner.py     # Unit tests for file scanning
├── test_integration.py      # Integration tests for the ingest module
├── test_init.py             # Tests for module initialization
└── README.md                # This file
```

## Running Tests

### Prerequisites

Make sure you have the development dependencies installed:

```bash
# From the project root
pip install -r requirements-dev.txt

# Or using uv (faster)
uv pip install -r requirements-dev.txt
```

### Basic Test Execution

```bash
# Run all ingest tests from project root
pytest gitsage/ingest/tests/

# Run all ingest tests from ingest directory
cd gitsage/ingest
pytest tests/

# Run specific test file
pytest tests/test_repo_cloner.py

# Run specific test function
pytest tests/test_repo_cloner.py::TestCloneRepo::test_clone_repo_success

# Run with verbose output
pytest tests/ -v

# Run with coverage for ingest module only
pytest tests/ --cov=gitsage.ingest --cov-report=html
```

### Test Categories

- **Unit tests**: Fast, isolated tests for individual functions
- **Integration tests**: Tests that verify components work together
- **Module tests**: Tests for module structure and imports

## Test Files Description

### `test_repo_cloner.py`

Comprehensive unit tests for the `clone_repo` function:

- ✅ Successful cloning scenarios
- ✅ Edge cases (existing repos, complex URLs, SSH URLs)
- ✅ Error handling and Git exceptions
- ✅ Logging verification
- ✅ Directory creation and path handling
- ✅ URL parsing for different Git hosting services

### `test_file_scanner.py`

Unit tests for the `scan_repo` function and constants:

- ✅ File type detection and classification
- ✅ Directory traversal (including nested structures)
- ✅ Supported file extensions and config files
- ✅ Filtering of unsupported file types
- ✅ Edge cases (empty directories, special characters)
- ✅ Path handling (absolute paths, string vs Path objects)
- ✅ Case sensitivity handling

### `test_integration.py`

Integration tests that verify components work together:

- ✅ Complete clone-and-scan workflows
- ✅ Real-world repository structures
- ✅ Multiple repository handling
- ✅ Error handling across modules
- ✅ Logging integration
- ✅ Complex nested directory structures

### `test_init.py`

Tests for module initialization and structure:

- ✅ Module importability
- ✅ Function availability and signatures
- ✅ Constants definition and types
- ✅ File structure validation

## Test Fixtures

### `conftest.py` provides shared fixtures:

- **`temp_directory`**: Temporary directory for test isolation
- **`sample_repo_structure`**: Pre-built repository structure for testing
- **`mock_git_repo`**: Mock Git repository for clone operations
- **`configure_loguru`**: Loguru configuration for clean test output

## Running Specific Test Types

```bash
# Run only unit tests for repo_cloner
pytest tests/test_repo_cloner.py

# Run only file scanner tests
pytest tests/test_file_scanner.py

# Run only integration tests
pytest tests/test_integration.py

# Run all tests with coverage
pytest tests/ --cov=gitsage.ingest

# Run tests in parallel (if pytest-xdist is installed)
pytest tests/ -n auto
```

## Test Coverage

The test suite provides comprehensive coverage:

### Repository Cloner (`test_repo_cloner.py`)

- **15+ test cases** covering all functionality
- **Mock Git operations** for reliable testing
- **Edge case handling** for various URL formats
- **Error scenario testing** for robustness

### File Scanner (`test_file_scanner.py`)

- **20+ test cases** covering file detection
- **Realistic file structures** for thorough testing
- **Extension and config file validation**
- **Nested directory traversal**

### Integration Testing (`test_integration.py`)

- **End-to-end workflows** combining cloning and scanning
- **Complex repository structures** mimicking real projects
- **Multi-repository scenarios**
- **Cross-module error handling**

## Writing New Tests

When adding new tests to the ingest module:

1. **Use relative imports**: Import from `..module_name`
2. **Leverage fixtures**: Use shared fixtures from `conftest.py`
3. **Mock external dependencies**: Mock Git operations and file systems
4. **Test edge cases**: Include error conditions and boundary cases
5. **Keep tests isolated**: Each test should be independent

### Example Test Structure

```python
# tests/test_new_feature.py

import pytest
from unittest.mock import patch

from ..new_module import new_function


class TestNewFunction:
    """Test cases for new_function."""

    def test_normal_case(self, temp_directory):
        """Test normal operation."""
        # Test implementation
        pass

    def test_edge_case(self):
        """Test edge case handling."""
        # Test implementation
        pass

    @patch("gitsage.ingest.new_module.external_dependency")
    def test_with_mock(self, mock_dependency):
        """Test with mocked external dependency."""
        # Test implementation
        pass
```

## Continuous Integration

These tests are designed to run in CI/CD environments with:

- **No external dependencies** (all Git operations mocked)
- **Fast execution** through effective mocking
- **Clear error reporting** with descriptive test names
- **Reliable isolation** using temporary directories

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure you're running tests from the correct directory
2. **Missing dependencies**: Install `requirements-dev.txt`
3. **Mock failures**: Check that patches target the correct module paths

### Debug Tests

```bash
# Run with extra verbose output
pytest tests/ -vvs

# Run specific failing test with debugging
pytest tests/test_file.py::test_function -vv --tb=long

# Use pdb for interactive debugging
pytest tests/test_file.py::test_function --pdb
```

## Test Philosophy

The ingest module tests follow these principles:

- **Fast Feedback**: Unit tests run quickly for rapid development
- **Reliable**: Mocked external dependencies prevent flaky tests
- **Comprehensive**: Cover both happy path and error scenarios
- **Maintainable**: Clear test structure and naming conventions
- **Realistic**: Use realistic test data and scenarios

For more information about testing in Python, see the [pytest documentation](https://docs.pytest.org/).
