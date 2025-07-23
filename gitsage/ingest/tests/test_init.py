# gitsage/ingest/tests/test_init.py

"""Test cases for the gitsage.ingest module initialization."""

import pytest


class TestIngestModule:
    """Test cases for the ingest module."""

    def test_import_ingest_module(self):
        """Test that the ingest module can be imported."""
        try:
            from gitsage import ingest

            assert ingest is not None
        except ImportError:
            pytest.fail("Could not import gitsage.ingest module")

    def test_import_repo_cloner(self):
        """Test that repo_cloner can be imported from ingest."""
        try:
            from ..repo_cloner import clone_repo

            assert clone_repo is not None
            assert callable(clone_repo)
        except ImportError:
            pytest.fail("Could not import clone_repo from repo_cloner")

    def test_import_file_scanner(self):
        """Test that file_scanner can be imported from ingest."""
        try:
            from ..file_scanner import scan_repo

            assert scan_repo is not None
            assert callable(scan_repo)
        except ImportError:
            pytest.fail("Could not import scan_repo from file_scanner")

    def test_import_constants(self):
        """Test that constants can be imported from file_scanner."""
        try:
            from ..file_scanner import SUPPORTED_CODE_EXTS, SUPPORTED_CONFIG_FILES

            assert SUPPORTED_CODE_EXTS is not None
            assert SUPPORTED_CONFIG_FILES is not None
            assert isinstance(SUPPORTED_CODE_EXTS, set)
            assert isinstance(SUPPORTED_CONFIG_FILES, set)
        except ImportError:
            pytest.fail("Could not import constants from file_scanner")

    def test_module_structure(self):
        """Test that the module has the expected structure."""
        from pathlib import Path

        # Get the ingest module directory
        ingest_dir = Path(__file__).parent.parent

        # Check that expected files exist
        expected_files = [
            ingest_dir / "__init__.py",
            ingest_dir / "repo_cloner.py",
            ingest_dir / "file_scanner.py",
        ]

        for expected_file in expected_files:
            assert expected_file.exists(), f"Expected file not found: {expected_file}"

    def test_function_signatures(self):
        """Test that functions have expected signatures."""
        # Test clone_repo signature
        import inspect

        from ..file_scanner import scan_repo
        from ..repo_cloner import clone_repo

        clone_sig = inspect.signature(clone_repo)
        assert "repo_url" in clone_sig.parameters
        assert "clone_dir" in clone_sig.parameters

        # Test scan_repo signature
        scan_sig = inspect.signature(scan_repo)
        assert "repo_path" in scan_sig.parameters

    def test_all_imports_work(self):
        """Test that all main functionality can be imported together."""
        try:
            from ..file_scanner import SUPPORTED_CODE_EXTS, SUPPORTED_CONFIG_FILES, scan_repo
            from ..repo_cloner import clone_repo

            # Verify all are accessible
            assert callable(clone_repo)
            assert callable(scan_repo)
            assert isinstance(SUPPORTED_CODE_EXTS, set)
            assert isinstance(SUPPORTED_CONFIG_FILES, set)

        except ImportError as e:
            pytest.fail(f"Could not import all required components: {e}")
