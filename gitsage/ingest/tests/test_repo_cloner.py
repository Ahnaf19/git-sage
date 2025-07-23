# gitsage/ingest/tests/test_repo_cloner.py

"""Unit tests for the repo_cloner module."""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from ..repo_cloner import clone_repo


class TestCloneRepo:
    """Test cases for the clone_repo function."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def mock_repo(self):
        """Mock Git repository for testing."""
        with patch("gitsage.ingest.repo_cloner.Repo") as mock_repo:
            yield mock_repo

    def test_clone_repo_success(self, temp_dir, mock_repo):
        """Test successful repository cloning."""
        repo_url = "https://github.com/user/test-repo.git"

        # Mock successful cloning
        mock_repo.clone_from.return_value = MagicMock()

        result = clone_repo(repo_url, temp_dir)

        expected_path = os.path.join(temp_dir, "test-repo")
        assert result == expected_path
        mock_repo.clone_from.assert_called_once_with(repo_url, expected_path)

    def test_clone_repo_without_git_extension(self, temp_dir, mock_repo):
        """Test cloning repository URL without .git extension."""
        repo_url = "https://github.com/user/test-repo"

        mock_repo.clone_from.return_value = MagicMock()

        result = clone_repo(repo_url, temp_dir)

        expected_path = os.path.join(temp_dir, "test-repo")
        assert result == expected_path
        mock_repo.clone_from.assert_called_once_with(repo_url, expected_path)

    def test_clone_repo_with_trailing_slash(self, temp_dir, mock_repo):
        """Test cloning repository URL with trailing slash."""
        repo_url = "https://github.com/user/test-repo.git/"

        mock_repo.clone_from.return_value = MagicMock()

        result = clone_repo(repo_url, temp_dir)

        expected_path = os.path.join(temp_dir, "test-repo")
        assert result == expected_path
        # The URL is passed as-is to clone_from, trailing slash intact
        mock_repo.clone_from.assert_called_once_with(repo_url, expected_path)

    def test_clone_repo_already_exists(self, temp_dir, mock_repo):
        """Test behavior when repository already exists."""
        repo_url = "https://github.com/user/test-repo.git"
        repo_path = os.path.join(temp_dir, "test-repo")

        # Create the directory to simulate existing repo
        os.makedirs(repo_path)

        result = clone_repo(repo_url, temp_dir)

        assert result == repo_path
        # Should not call clone_from when repo already exists
        mock_repo.clone_from.assert_not_called()

    def test_clone_repo_creates_clone_directory(self, mock_repo):
        """Test that clone directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_base:
            clone_dir = os.path.join(temp_base, "new_clone_dir")
            repo_url = "https://github.com/user/test-repo.git"

            mock_repo.clone_from.return_value = MagicMock()

            result = clone_repo(repo_url, clone_dir)

            # Verify directory was created
            assert os.path.exists(clone_dir)
            expected_path = os.path.join(clone_dir, "test-repo")
            assert result == expected_path

    def test_clone_repo_default_directory(self, mock_repo):
        """Test cloning with default directory."""
        repo_url = "https://github.com/user/test-repo.git"

        mock_repo.clone_from.return_value = MagicMock()

        with patch("os.makedirs") as mock_makedirs:
            clone_repo(repo_url)

            # Should create default "./repos" directory
            mock_makedirs.assert_called_once_with("./repos", exist_ok=True)

    def test_clone_repo_complex_url_parsing(self, temp_dir, mock_repo):
        """Test parsing complex repository URLs."""
        test_cases = [
            ("https://github.com/user/repo-with-dashes.git", "repo-with-dashes"),
            ("git@github.com:user/repo.git", "repo"),
            ("https://gitlab.com/group/subgroup/project.git", "project"),
            ("https://github.com/user/repo", "repo"),
        ]

        mock_repo.clone_from.return_value = MagicMock()

        for repo_url, expected_name in test_cases:
            result = clone_repo(repo_url, temp_dir)
            expected_path = os.path.join(temp_dir, expected_name)
            assert result == expected_path

    @patch("gitsage.ingest.repo_cloner.logger")
    def test_clone_repo_logging(self, mock_logger, temp_dir, mock_repo):
        """Test that appropriate logging messages are generated."""
        repo_url = "https://github.com/user/test-repo.git"

        mock_repo.clone_from.return_value = MagicMock()

        clone_repo(repo_url, temp_dir)

        # Verify logging calls
        mock_logger.info.assert_called()
        mock_logger.success.assert_called_once()

    @patch("gitsage.ingest.repo_cloner.logger")
    def test_clone_repo_existing_logging(self, mock_logger, temp_dir, mock_repo):
        """Test logging when repository already exists."""
        repo_url = "https://github.com/user/test-repo.git"
        repo_path = os.path.join(temp_dir, "test-repo")

        # Create the directory to simulate existing repo
        os.makedirs(repo_path)

        clone_repo(repo_url, temp_dir)

        # Verify info logging for existing repo
        mock_logger.info.assert_called_with(f"Repository already exists at {repo_path}")
        # Should not call success logger
        mock_logger.success.assert_not_called()

    def test_clone_repo_git_exception(self, temp_dir, mock_repo):
        """Test handling of Git exceptions during cloning."""
        repo_url = "https://github.com/user/nonexistent-repo.git"

        # Mock Git exception
        mock_repo.clone_from.side_effect = Exception("Git clone failed")

        with pytest.raises(Exception, match="Git clone failed"):
            clone_repo(repo_url, temp_dir)

    def test_clone_repo_return_type(self, temp_dir, mock_repo):
        """Test that function returns correct type."""
        repo_url = "https://github.com/user/test-repo.git"

        mock_repo.clone_from.return_value = MagicMock()

        result = clone_repo(repo_url, temp_dir)

        assert isinstance(result, str)
        assert result.endswith("test-repo")

    def test_clone_repo_ssh_url(self, temp_dir, mock_repo):
        """Test cloning with SSH URL format."""
        repo_url = "git@github.com:user/test-repo.git"

        mock_repo.clone_from.return_value = MagicMock()

        result = clone_repo(repo_url, temp_dir)

        expected_path = os.path.join(temp_dir, "test-repo")
        assert result == expected_path
        mock_repo.clone_from.assert_called_once_with(repo_url, expected_path)

    def test_clone_repo_url_with_port(self, temp_dir, mock_repo):
        """Test cloning with URL that includes port number."""
        repo_url = "https://github.com:443/user/test-repo.git"

        mock_repo.clone_from.return_value = MagicMock()

        result = clone_repo(repo_url, temp_dir)

        expected_path = os.path.join(temp_dir, "test-repo")
        assert result == expected_path

    def test_clone_repo_special_characters_in_name(self, temp_dir, mock_repo):
        """Test repository names with special characters."""
        test_cases = [
            "https://github.com/user/repo_with_underscores.git",
            "https://github.com/user/repo-with-hyphens.git",
            "https://github.com/user/repo.with.dots.git",
        ]

        mock_repo.clone_from.return_value = MagicMock()

        for repo_url in test_cases:
            result = clone_repo(repo_url, temp_dir)
            assert isinstance(result, str)
            assert len(result) > 0
