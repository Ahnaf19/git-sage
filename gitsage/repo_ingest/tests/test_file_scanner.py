# gitsage/repo_ingest/tests/test_file_scanner.py

"""Unit tests for the file_scanner module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from ..repo_scanner import SUPPORTED_CODE_EXTS, SUPPORTED_CONFIG_FILES, scan_repo


class TestFileScannerConstants:
    """Test cases for file scanner constants."""

    def test_supported_code_extensions(self):
        """Test that supported code extensions are defined correctly."""
        expected_extensions = {".py", ".js", ".ts", ".cpp", ".java", ".go"}
        assert SUPPORTED_CODE_EXTS == expected_extensions

    def test_supported_config_files(self):
        """Test that supported config files are defined correctly."""
        # Test a few key config files
        assert "README.md" in SUPPORTED_CONFIG_FILES
        assert "requirements.txt" in SUPPORTED_CONFIG_FILES
        assert "environment.yml" in SUPPORTED_CONFIG_FILES
        assert "package.json" in SUPPORTED_CONFIG_FILES
        assert "Dockerfile" in SUPPORTED_CONFIG_FILES
        assert "Makefile" in SUPPORTED_CONFIG_FILES

    def test_supported_config_files_completeness(self):
        """Test that supported config files set is comprehensive."""
        # Should contain at least 20 different config file types
        assert len(SUPPORTED_CONFIG_FILES) >= 20


class TestScanRepo:
    """Test cases for the scan_repo function."""

    @pytest.fixture
    def temp_repo(self):
        """Create a temporary repository structure for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)

            # Create some code files
            (repo_path / "main.py").write_text("print('hello')")
            (repo_path / "utils.js").write_text("console.log('test')")
            (repo_path / "component.ts").write_text("export class Test {}")
            (repo_path / "algorithm.cpp").write_text("#include <iostream>")
            (repo_path / "App.java").write_text("public class App {}")
            (repo_path / "server.go").write_text("package main")

            # Create some config files
            (repo_path / "README.md").write_text("# Test Project")
            (repo_path / "requirements.txt").write_text("pytest>=7.0.0")
            (repo_path / "environment.yml").write_text("name: test")
            (repo_path / "package.json").write_text('{"name": "test"}')
            (repo_path / "Dockerfile").write_text("FROM python:3.9")
            (repo_path / "Makefile").write_text("test:\n\techo 'test'")

            # Create some files that should be ignored
            (repo_path / "test.txt").write_text("some text")
            (repo_path / "image.png").write_bytes(b"fake image")
            (repo_path / "data.csv").write_text("col1,col2\n1,2")

            # Create subdirectory with files
            subdir = repo_path / "src"
            subdir.mkdir()
            (subdir / "module.py").write_text("def func(): pass")
            (subdir / "style.css").write_text("body { color: red; }")
            (subdir / ".gitignore").write_text("*.pyc")

            yield repo_path

    def test_scan_repo_with_string_path(self, temp_repo):
        """Test scanning repository with string path."""
        result = scan_repo(str(temp_repo))

        assert isinstance(result, dict)
        assert "code_files" in result
        assert "config_files" in result
        assert isinstance(result["code_files"], list)
        assert isinstance(result["config_files"], list)

    def test_scan_repo_with_path_object(self, temp_repo):
        """Test scanning repository with Path object."""
        result = scan_repo(temp_repo)

        assert isinstance(result, dict)
        assert "code_files" in result
        assert "config_files" in result

    def test_scan_repo_finds_code_files(self, temp_repo):
        """Test that scan_repo correctly identifies code files."""
        result = scan_repo(temp_repo)
        code_files = result["code_files"]

        # Should find all code files
        code_file_names = [Path(f).name for f in code_files]
        expected_code_files = {
            "main.py",
            "utils.js",
            "component.ts",
            "algorithm.cpp",
            "App.java",
            "server.go",
            "module.py",
        }

        assert len(code_files) == len(expected_code_files)
        for expected_file in expected_code_files:
            assert expected_file in code_file_names

    def test_scan_repo_finds_config_files(self, temp_repo):
        """Test that scan_repo correctly identifies config files."""
        result = scan_repo(temp_repo)
        config_files = result["config_files"]

        # Should find all config files
        config_file_names = [Path(f).name for f in config_files]
        expected_config_files = {
            "README.md",
            "requirements.txt",
            "environment.yml",
            "package.json",
            "Dockerfile",
            "Makefile",
            ".gitignore",
        }

        assert len(config_files) == len(expected_config_files)
        for expected_file in expected_config_files:
            assert expected_file in config_file_names

    def test_scan_repo_ignores_unsupported_files(self, temp_repo):
        """Test that scan_repo ignores unsupported file types."""
        result = scan_repo(temp_repo)
        all_files = result["code_files"] + result["config_files"]

        # Should not include unsupported files
        file_names = [Path(f).name for f in all_files]
        unsupported_files = {"test.txt", "image.png", "data.csv", "style.css"}

        for unsupported_file in unsupported_files:
            assert unsupported_file not in file_names

    def test_scan_repo_includes_subdirectories(self, temp_repo):
        """Test that scan_repo recursively scans subdirectories."""
        result = scan_repo(temp_repo)
        all_files = result["code_files"] + result["config_files"]

        # Should include files from subdirectories
        has_subdir_file = any("src" in f for f in all_files)
        assert has_subdir_file

    def test_scan_repo_empty_directory(self):
        """Test scanning an empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = scan_repo(temp_dir)

            assert result["code_files"] == []
            assert result["config_files"] == []

    def test_scan_repo_nonexistent_directory(self):
        """Test scanning a nonexistent directory."""
        nonexistent_path = "/this/path/does/not/exist"

        # os.walk() returns empty iterator for nonexistent paths
        result = scan_repo(nonexistent_path)
        assert result["code_files"] == []
        assert result["config_files"] == []

    def test_scan_repo_returns_absolute_paths(self, temp_repo):
        """Test that scan_repo returns absolute file paths."""
        result = scan_repo(temp_repo)
        all_files = result["code_files"] + result["config_files"]

        for file_path in all_files:
            assert Path(file_path).is_absolute()

    def test_scan_repo_file_path_format(self, temp_repo):
        """Test that file paths are returned as strings."""
        result = scan_repo(temp_repo)
        all_files = result["code_files"] + result["config_files"]

        for file_path in all_files:
            assert isinstance(file_path, str)

    @patch("gitsage.repo_ingest.repo_scanner.logger")
    def test_scan_repo_logging(self, mock_logger, temp_repo):
        """Test that appropriate logging messages are generated."""
        scan_repo(temp_repo)

        # Verify logging calls
        mock_logger.info.assert_called()
        mock_logger.debug.assert_called()

    def test_scan_repo_specific_extensions(self, temp_repo):
        """Test that only files with supported extensions are included."""
        result = scan_repo(temp_repo)
        code_files = result["code_files"]

        for file_path in code_files:
            file_ext = Path(file_path).suffix
            assert file_ext in SUPPORTED_CODE_EXTS

    def test_scan_repo_case_sensitivity(self):
        """Test file extension case sensitivity."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)

            # Create files with different cases
            (repo_path / "script.py").write_text("print('test')")
            (repo_path / "Script.PY").write_text("print('test')")  # Different case
            (repo_path / "app.JS").write_text("console.log('test')")  # Different case

            result = scan_repo(temp_dir)
            code_files = result["code_files"]

            # Should only find files with lowercase extensions (as defined in SUPPORTED_CODE_EXTS)
            code_file_names = [Path(f).name for f in code_files]
            assert "script.py" in code_file_names
            assert "Script.PY" not in code_file_names
            assert "app.JS" not in code_file_names

    def test_scan_repo_special_characters_in_names(self):
        """Test handling files with special characters in names."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)

            # Create files with special characters
            (repo_path / "file-with-dashes.py").write_text("print('test')")
            (repo_path / "file_with_underscores.js").write_text("console.log('test')")
            (repo_path / "file with spaces.ts").write_text("export class Test {}")

            result = scan_repo(temp_dir)
            code_files = result["code_files"]

            assert len(code_files) == 3
            file_names = [Path(f).name for f in code_files]
            assert "file-with-dashes.py" in file_names
            assert "file_with_underscores.js" in file_names
            assert "file with spaces.ts" in file_names

    def test_scan_repo_nested_directories(self):
        """Test scanning deeply nested directory structures."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)

            # Create nested structure
            deep_path = repo_path / "level1" / "level2" / "level3"
            deep_path.mkdir(parents=True)
            (deep_path / "deep.py").write_text("print('deep')")
            (deep_path / "README.md").write_text("# Config")

            result = scan_repo(temp_dir)

            # Should find files in deep directories
            code_files = result["code_files"]
            config_files = result["config_files"]

            assert len(code_files) == 1
            assert len(config_files) == 1
            assert "deep.py" in code_files[0]
            assert "README.md" in config_files[0]

    def test_scan_repo_mixed_file_types_in_directory(self):
        """Test directory with mixed supported and unsupported files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)

            # Create mix of files
            files = [
                ("app.py", "code"),
                ("config.json", "config"),
                ("data.csv", "ignore"),
                ("script.js", "code"),
                ("image.png", "ignore"),
                ("README.md", "config"),
                ("notes.txt", "ignore"),
            ]

            for filename, file_type in files:
                (repo_path / filename).write_text(f"content of {filename}")

            result = scan_repo(temp_dir)

            # Check counts
            assert len(result["code_files"]) == 2  # app.py, script.js
            assert len(result["config_files"]) == 2  # config.json, README.md

            # Verify specific files
            all_files = result["code_files"] + result["config_files"]
            all_file_names = [Path(f).name for f in all_files]

            assert "app.py" in all_file_names
            assert "script.js" in all_file_names
            assert "config.json" in all_file_names
            assert "README.md" in all_file_names
            assert "data.csv" not in all_file_names
            assert "image.png" not in all_file_names
            assert "notes.txt" not in all_file_names
