# gitsage/ingest/tests/conftest.py

"""Shared pytest configuration and fixtures for ingest module tests."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def temp_directory():
    """Fixture providing a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_repo_structure(temp_directory):
    """Fixture creating a sample repository structure for testing."""
    repo_path = temp_directory / "sample_repo"
    repo_path.mkdir()

    # Create Python files
    (repo_path / "main.py").write_text("#!/usr/bin/env python3\nprint('Hello World')")
    (repo_path / "utils.py").write_text("def helper_function():\n    return True")

    # Create JavaScript files
    (repo_path / "app.js").write_text("console.log('Hello World');")
    (repo_path / "script.ts").write_text("interface Test { name: string; }")

    # Create config files
    (repo_path / "README.md").write_text("# Sample Repository\n\nThis is a test repository.")
    (repo_path / "requirements.txt").write_text("pytest>=7.0.0\nloguru>=0.6.0")
    (repo_path / "package.json").write_text('{\n  "name": "sample-repo",\n  "version": "1.0.0"\n}')

    # Create subdirectory with files
    src_dir = repo_path / "src"
    src_dir.mkdir()
    (src_dir / "module.py").write_text("class SampleClass:\n    pass")
    (src_dir / "component.js").write_text("export default function Component() {}")

    # Create test directory
    test_dir = repo_path / "tests"
    test_dir.mkdir()
    (test_dir / "test_main.py").write_text("def test_example():\n    assert True")

    return repo_path


@pytest.fixture
def mock_git_repo():
    """Fixture providing a mock git repository."""
    mock_repo = MagicMock()
    mock_repo.clone_from.return_value = mock_repo
    return mock_repo


@pytest.fixture(autouse=True)
def configure_loguru():
    """Configure loguru for testing to avoid log pollution."""
    from loguru import logger

    # Remove default logger
    logger.remove()

    # Add a test-specific logger that captures logs
    logger.add(lambda record: None, level="DEBUG", format="{time} | {level} | {message}")  # Don't output during tests

    yield

    # Clean up after test
    logger.remove()
