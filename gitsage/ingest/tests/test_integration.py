# gitsage/ingest/tests/test_integration.py

"""Integration tests for the ingest module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from ..file_scanner import scan_repo
from ..repo_cloner import clone_repo


class TestIngestIntegration:
    """Integration tests for the ingest module components."""

    @pytest.fixture
    def mock_git_repo_with_files(self):
        """Create a mock repository with actual file structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir) / "test-repo"
            repo_path.mkdir()

            # Create a realistic repository structure
            (repo_path / "main.py").write_text(
                """
#!/usr/bin/env python3
\"\"\"Main application entry point.\"\"\"

def main():
    print("Hello, GitSage!")

if __name__ == "__main__":
    main()
"""
            )

            (repo_path / "utils.py").write_text(
                """
\"\"\"Utility functions.\"\"\"

def parse_url(url: str) -> dict:
    \"\"\"Parse a URL into components.\"\"\"
    return {"url": url}

def validate_path(path: str) -> bool:
    \"\"\"Validate a file path.\"\"\"
    return len(path) > 0
"""
            )

            # Create JavaScript files
            (repo_path / "app.js").write_text(
                """
// Main application
function main() {
    console.log("Hello from JavaScript!");
}

main();
"""
            )

            # Create config files
            (repo_path / "README.md").write_text(
                """
# Test Repository

This is a test repository for GitSage integration testing.

## Features

- Python modules
- JavaScript files
- Configuration files
- Documentation

## Usage

```bash
python main.py
```
"""
            )

            (repo_path / "requirements.txt").write_text(
                """
loguru>=0.6.0
gitpython>=3.1.0
pathlib>=1.0.1
"""
            )

            (repo_path / "package.json").write_text(
                """
{
  "name": "test-repo",
  "version": "1.0.0",
  "description": "Test repository for GitSage",
  "main": "app.js",
  "scripts": {
    "start": "node app.js",
    "test": "echo 'No tests specified'"
  },
  "dependencies": {
    "lodash": "^4.17.21"
  }
}
"""
            )

            # Create subdirectories
            src_dir = repo_path / "src"
            src_dir.mkdir()
            (src_dir / "models.py").write_text(
                """
\"\"\"Data models.\"\"\"

class User:
    def __init__(self, name: str):
        self.name = name
"""
            )

            tests_dir = repo_path / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_utils.py").write_text(
                """
\"\"\"Tests for utility functions.\"\"\"

def test_parse_url():
    result = parse_url("https://example.com")
    assert result["url"] == "https://example.com"

def test_validate_path():
    assert validate_path("/some/path") == True
    assert validate_path("") == False
"""
            )

            (tests_dir / ".gitignore").write_text(
                """
__pycache__/
*.pyc
*.pyo
.pytest_cache/
"""
            )

            yield repo_path

    @patch("gitsage.ingest.repo_cloner.Repo")
    def test_clone_and_scan_workflow(self, mock_repo_class, mock_git_repo_with_files):
        """Test the complete workflow of cloning and scanning a repository."""
        with tempfile.TemporaryDirectory() as temp_clone_dir:
            # Mock the clone operation to copy our test repo
            def mock_clone_from(url, path):
                import shutil

                shutil.copytree(mock_git_repo_with_files, path)

            mock_repo_class.clone_from.side_effect = mock_clone_from

            # Step 1: Clone the repository
            repo_url = "https://github.com/test/test-repo.git"
            cloned_path = clone_repo(repo_url, temp_clone_dir)

            # Verify clone operation
            assert Path(cloned_path).exists()
            assert Path(cloned_path).name == "test-repo"

            # Step 2: Scan the cloned repository
            scan_result = scan_repo(cloned_path)

            # Verify scan results
            assert "code_files" in scan_result
            assert "config_files" in scan_result

            code_files = scan_result["code_files"]
            config_files = scan_result["config_files"]

            # Check code files
            code_file_names = [Path(f).name for f in code_files]
            expected_code_files = {"main.py", "utils.py", "app.js", "models.py", "test_utils.py"}
            assert len(code_files) == len(expected_code_files)
            for expected_file in expected_code_files:
                assert expected_file in code_file_names

            # Check config files
            config_file_names = [Path(f).name for f in config_files]
            expected_config_files = {"README.md", "requirements.txt", "package.json", ".gitignore"}
            assert len(config_files) == len(expected_config_files)
            for expected_file in expected_config_files:
                assert expected_file in config_file_names

    @patch("gitsage.ingest.repo_cloner.Repo")
    def test_clone_existing_then_scan(self, mock_repo_class, mock_git_repo_with_files):
        """Test scanning a repository that already exists locally."""
        with tempfile.TemporaryDirectory() as temp_clone_dir:
            # Pre-create the repository directory
            import shutil

            target_path = Path(temp_clone_dir) / "test-repo"
            shutil.copytree(mock_git_repo_with_files, target_path)

            # Attempt to clone (should detect existing repo)
            repo_url = "https://github.com/test/test-repo.git"
            cloned_path = clone_repo(repo_url, temp_clone_dir)

            # Should return existing path without cloning
            assert cloned_path == str(target_path)
            mock_repo_class.clone_from.assert_not_called()

            # Scan should still work
            scan_result = scan_repo(cloned_path)
            assert len(scan_result["code_files"]) > 0
            assert len(scan_result["config_files"]) > 0

    def test_scan_empty_cloned_repo(self):
        """Test scanning an empty repository."""
        with tempfile.TemporaryDirectory() as temp_dir:
            empty_repo = Path(temp_dir) / "empty-repo"
            empty_repo.mkdir()

            scan_result = scan_repo(empty_repo)

            assert scan_result["code_files"] == []
            assert scan_result["config_files"] == []

    @patch("gitsage.ingest.repo_cloner.Repo")
    def test_real_world_repo_structure(self, mock_repo_class):
        """Test with a more complex, real-world-like repository structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a complex repo structure
            repo_path = Path(temp_dir) / "complex-repo"
            repo_path.mkdir()

            # Create multiple language files
            (repo_path / "backend.py").write_text("# Python backend")
            (repo_path / "frontend.js").write_text("// JavaScript frontend")
            (repo_path / "types.ts").write_text("// TypeScript definitions")
            (repo_path / "algorithm.cpp").write_text("// C++ algorithm")
            (repo_path / "service.java").write_text("// Java service")
            (repo_path / "server.go").write_text("// Go server")

            # Create nested directories
            api_dir = repo_path / "api" / "v1"
            api_dir.mkdir(parents=True)
            (api_dir / "endpoints.py").write_text("# API endpoints")
            (api_dir / "routes.js").write_text("// Express routes")

            frontend_dir = repo_path / "frontend" / "src" / "components"
            frontend_dir.mkdir(parents=True)
            (frontend_dir / "App.ts").write_text("// React component")
            (frontend_dir / "utils.js").write_text("// Utility functions")

            docs_dir = repo_path / "docs"
            docs_dir.mkdir()
            (docs_dir / "README.md").write_text("# Documentation")

            # Create various config files
            configs = {
                "pyproject.toml": "[tool.poetry]",
                "setup.cfg": "[metadata]",
                ".env": "DEBUG=true",
                "package.json": '{"name": "complex-repo"}',
                "tsconfig.json": '{"compilerOptions": {}}',
                ".gitignore": "*.pyc",
                "Dockerfile": "FROM python:3.9",
            }

            for filename, content in configs.items():
                (repo_path / filename).write_text(content)

            # Mock clone operation
            def mock_clone_from(url, path):
                import shutil

                shutil.copytree(repo_path, path)

            mock_repo_class.clone_from.side_effect = mock_clone_from

            # Test the workflow
            with tempfile.TemporaryDirectory() as clone_dir:
                cloned_path = clone_repo("https://github.com/test/complex-repo.git", clone_dir)
                scan_result = scan_repo(cloned_path)

                # Verify comprehensive scanning
                assert len(scan_result["code_files"]) == 10  # All code files across languages
                assert len(scan_result["config_files"]) >= 6  # Various config files

                # Verify nested directories are scanned
                all_files = scan_result["code_files"] + scan_result["config_files"]
                nested_files = [f for f in all_files if "api" in f or "frontend" in f or "docs" in f]
                assert len(nested_files) > 0

    def test_error_handling_integration(self):
        """Test error handling in the integrated workflow."""
        # Test with non-existent directory for scanning
        # os.walk() returns empty iterator for nonexistent paths
        result = scan_repo("/this/path/does/not/exist")
        assert result["code_files"] == []
        assert result["config_files"] == []

        # Test cloning to a file (not directory) - should handle gracefully
        with tempfile.NamedTemporaryFile() as temp_file:
            with patch("gitsage.ingest.repo_cloner.Repo") as mock_repo:
                mock_repo.clone_from.side_effect = Exception("Cannot clone to file")

                with pytest.raises(Exception):
                    clone_repo("https://github.com/test/repo.git", temp_file.name)

    @patch("gitsage.ingest.repo_cloner.logger")
    @patch("gitsage.ingest.file_scanner.logger")
    def test_logging_integration(self, scanner_logger, cloner_logger, mock_git_repo_with_files):
        """Test that logging works correctly across both modules."""
        with tempfile.TemporaryDirectory() as temp_clone_dir:
            with patch("gitsage.ingest.repo_cloner.Repo") as mock_repo:

                def mock_clone_from(url, path):
                    import shutil

                    shutil.copytree(mock_git_repo_with_files, path)

                mock_repo.clone_from.side_effect = mock_clone_from

                # Execute the workflow
                cloned_path = clone_repo("https://github.com/test/repo.git", temp_clone_dir)
                scan_repo(cloned_path)

                # Verify both modules logged appropriately
                cloner_logger.info.assert_called()
                cloner_logger.success.assert_called()
                scanner_logger.info.assert_called()
                scanner_logger.debug.assert_called()

    @patch("gitsage.ingest.repo_cloner.Repo")
    def test_multiple_repos_workflow(self, mock_repo_class, mock_git_repo_with_files):
        """Test cloning and scanning multiple repositories."""
        with tempfile.TemporaryDirectory() as temp_clone_dir:

            def mock_clone_from(url, path):
                import shutil

                shutil.copytree(mock_git_repo_with_files, path)

            mock_repo_class.clone_from.side_effect = mock_clone_from

            repos = [
                "https://github.com/test/repo1.git",
                "https://github.com/test/repo2.git",
                "https://github.com/test/repo3.git",
            ]

            results = []
            for repo_url in repos:
                cloned_path = clone_repo(repo_url, temp_clone_dir)
                scan_result = scan_repo(cloned_path)
                results.append((cloned_path, scan_result))

            # Verify all repos were processed
            assert len(results) == 3

            for cloned_path, scan_result in results:
                assert Path(cloned_path).exists()
                assert len(scan_result["code_files"]) > 0
                assert len(scan_result["config_files"]) > 0
