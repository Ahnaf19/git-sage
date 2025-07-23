# gitsage/repo_ingest/tests/test_repo_fetcher.py

"""Unit tests for the repo_fetcher module."""

import os
import tempfile
from unittest.mock import MagicMock, Mock, patch

import pytest
import requests

from ..repo_fetcher import RepoFetcher


class TestRepoFetcher:
    """Test cases for the RepoFetcher class."""

    def test_init_default_values(self):
        """Test RepoFetcher initialization with default values."""
        repo_url = "https://github.com/user/test-repo.git"
        fetcher = RepoFetcher(repo_url)

        assert fetcher.repo_url == repo_url
        assert fetcher.mode == "clone"
        # Path("./repos") resolves to "repos" on Windows
        from pathlib import Path

        assert fetcher.target_dir == Path("./repos")
        assert fetcher.token is None

    def test_init_custom_values(self):
        """Test RepoFetcher initialization with custom values."""
        repo_url = "https://github.com/user/test-repo.git"
        mode = "api"
        target_dir = "/custom/path"
        token = "test_token"

        fetcher = RepoFetcher(repo_url, mode=mode, target_dir=target_dir, token=token)

        assert fetcher.repo_url == repo_url
        assert fetcher.mode == mode
        from pathlib import Path

        assert fetcher.target_dir == Path(target_dir)
        assert fetcher.token == token

    def test_fetch_clone_mode(self):
        """Test fetch method with clone mode."""
        repo_url = "https://github.com/user/test-repo.git"
        fetcher = RepoFetcher(repo_url, mode="clone")

        with patch.object(fetcher, "_clone_repo", return_value="/path/to/repo") as mock_clone:
            result = fetcher.fetch()

            assert result == "/path/to/repo"
            mock_clone.assert_called_once()

    def test_fetch_api_mode(self):
        """Test fetch method with api mode."""
        repo_url = "https://github.com/user/test-repo.git"
        fetcher = RepoFetcher(repo_url, mode="api")

        with patch.object(fetcher, "_download_via_api", return_value="/tmp/repo") as mock_api:
            result = fetcher.fetch()

            assert result == "/tmp/repo"
            mock_api.assert_called_once()

    def test_fetch_unsupported_mode(self):
        """Test fetch method with unsupported mode."""
        repo_url = "https://github.com/user/test-repo.git"
        fetcher = RepoFetcher(repo_url, mode="invalid")

        with pytest.raises(ValueError, match="Unsupported mode. Use 'clone' or 'api'."):
            fetcher.fetch()

    def test_extract_repo_name_with_git_extension(self):
        """Test extracting repository name from URL with .git extension."""
        repo_url = "https://github.com/user/test-repo.git"
        fetcher = RepoFetcher(repo_url)

        result = fetcher._extract_repo_name()
        assert result == "test-repo"

    def test_extract_repo_name_without_git_extension(self):
        """Test extracting repository name from URL without .git extension."""
        repo_url = "https://github.com/user/test-repo"
        fetcher = RepoFetcher(repo_url)

        result = fetcher._extract_repo_name()
        assert result == "test-repo"

    def test_extract_repo_name_with_trailing_slash(self):
        """Test extracting repository name from URL with trailing slash."""
        repo_url = "https://github.com/user/test-repo.git/"
        fetcher = RepoFetcher(repo_url)

        result = fetcher._extract_repo_name()
        assert result == "test-repo"

    def test_extract_repo_name_complex_cases(self):
        """Test extracting repository name from various URL formats."""
        test_cases = [
            ("https://github.com/user/repo-with-dashes.git", "repo-with-dashes"),
            ("git@github.com:user/repo.git", "repo"),
            ("https://gitlab.com/group/subgroup/project.git", "project"),
            ("https://github.com/user/repo_with_underscores", "repo_with_underscores"),
        ]

        for repo_url, expected_name in test_cases:
            fetcher = RepoFetcher(repo_url)
            result = fetcher._extract_repo_name()
            assert result == expected_name


class TestRepoFetcherClone:
    """Test cases for the _clone_repo method."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def mock_repo(self):
        """Mock Git repository for testing."""
        with patch("gitsage.repo_ingest.repo_fetcher.Repo") as mock_repo:
            yield mock_repo

    def test_clone_repo_success(self, temp_dir, mock_repo):
        """Test successful repository cloning."""
        repo_url = "https://github.com/user/test-repo.git"
        fetcher = RepoFetcher(repo_url, target_dir=temp_dir)

        mock_repo.clone_from.return_value = MagicMock()

        result = fetcher._clone_repo()

        expected_path = os.path.join(temp_dir, "test-repo")
        assert result == expected_path
        mock_repo.clone_from.assert_called_once_with(repo_url, expected_path)

    def test_clone_repo_already_exists(self, temp_dir, mock_repo):
        """Test behavior when repository already exists."""
        repo_url = "https://github.com/user/test-repo.git"
        fetcher = RepoFetcher(repo_url, target_dir=temp_dir)

        # Create the directory to simulate existing repo
        repo_path = os.path.join(temp_dir, "test-repo")
        os.makedirs(repo_path)

        result = fetcher._clone_repo()

        assert result == repo_path
        # Should not call clone_from when repo already exists
        mock_repo.clone_from.assert_not_called()

    def test_clone_repo_creates_target_directory(self, mock_repo):
        """Test that target directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_base:
            target_dir = os.path.join(temp_base, "new_target_dir")
            repo_url = "https://github.com/user/test-repo.git"
            fetcher = RepoFetcher(repo_url, target_dir=target_dir)

            mock_repo.clone_from.return_value = MagicMock()

            result = fetcher._clone_repo()

            # Verify directory was created
            assert os.path.exists(target_dir)
            expected_path = os.path.join(target_dir, "test-repo")
            assert result == expected_path

    @patch("gitsage.repo_ingest.repo_fetcher.logger")
    def test_clone_repo_logging_success(self, mock_logger, temp_dir, mock_repo):
        """Test that appropriate logging messages are generated for successful clone."""
        repo_url = "https://github.com/user/test-repo.git"
        fetcher = RepoFetcher(repo_url, target_dir=temp_dir)

        mock_repo.clone_from.return_value = MagicMock()

        fetcher._clone_repo()

        # Verify logging calls
        mock_logger.info.assert_called()
        mock_logger.success.assert_called_once()

    @patch("gitsage.repo_ingest.repo_fetcher.logger")
    def test_clone_repo_logging_existing(self, mock_logger, temp_dir, mock_repo):
        """Test logging when repository already exists."""
        repo_url = "https://github.com/user/test-repo.git"
        fetcher = RepoFetcher(repo_url, target_dir=temp_dir)

        # Create the directory to simulate existing repo
        repo_path = os.path.join(temp_dir, "test-repo")
        os.makedirs(repo_path)

        fetcher._clone_repo()

        # Verify info logging for existing repo (check with Path.as_posix() format)
        from pathlib import Path

        expected_path = Path(repo_path).as_posix()
        mock_logger.info.assert_called_with(f"Repository already exists at {expected_path}")
        # Should not call success logger
        mock_logger.success.assert_not_called()

    def test_clone_repo_git_exception(self, temp_dir, mock_repo):
        """Test handling of Git exceptions during cloning."""
        repo_url = "https://github.com/user/nonexistent-repo.git"
        fetcher = RepoFetcher(repo_url, target_dir=temp_dir)

        # Mock Git exception
        mock_repo.clone_from.side_effect = Exception("Git clone failed")

        with pytest.raises(Exception, match="Git clone failed"):
            fetcher._clone_repo()


class TestRepoFetcherAPI:
    """Test cases for the _download_via_api method."""

    def test_download_via_api_success(self):
        """Test successful API download."""
        repo_url = "https://github.com/user/test-repo"
        fetcher = RepoFetcher(repo_url, mode="api")

        # Mock GitHub API tree response
        mock_tree_response = {
            "tree": [
                {"type": "blob", "path": "README.md"},
                {"type": "blob", "path": "src/main.py"},
                {"type": "tree", "path": "src"},
            ]
        }

        with (
            patch("requests.get") as mock_get,
            patch("tempfile.mkdtemp", return_value="/tmp/test-repo-12345") as mock_mkdtemp,
            patch("pathlib.Path.mkdir") as mock_mkdir,
            patch("pathlib.Path.write_bytes") as mock_write_bytes,
        ):

            # Setup mock responses
            mock_tree_resp = Mock()
            mock_tree_resp.raise_for_status.return_value = None
            mock_tree_resp.json.return_value = mock_tree_response

            mock_file_resp = Mock()
            mock_file_resp.status_code = 200
            mock_file_resp.content = b"file content"

            mock_get.side_effect = [mock_tree_resp, mock_file_resp, mock_file_resp]

            result = fetcher._download_via_api()

            # Normalize path for comparison (Windows vs Unix separators)
            from pathlib import Path

            assert Path(result) == Path("/tmp/test-repo-12345")
            # Verify API calls
            assert mock_get.call_count == 3  # 1 tree + 2 files
            mock_mkdtemp.assert_called_once_with(prefix="test-repo-")

            mock_mkdir.assert_called()  # Verify directories are created
            mock_write_bytes.assert_called()  # Verify files are written

    def test_download_via_api_with_token(self):
        """Test API download with authentication token."""
        repo_url = "https://github.com/user/private-repo"
        token = "test_token"
        fetcher = RepoFetcher(repo_url, mode="api", token=token)

        mock_tree_response = {"tree": []}

        with patch("requests.get") as mock_get, patch("tempfile.mkdtemp", return_value="/tmp/private-repo-12345"):

            mock_resp = Mock()
            mock_resp.raise_for_status.return_value = None
            mock_resp.json.return_value = mock_tree_response
            mock_get.return_value = mock_resp

            fetcher._download_via_api()

            # Verify token is included in headers
            expected_headers = {"Authorization": "token test_token"}
            mock_get.assert_called_with(
                "https://api.github.com/repos/user/private-repo/git/trees/HEAD?recursive=1", headers=expected_headers
            )

    def test_download_via_api_file_skip_on_error(self):
        """Test that files are skipped when download fails."""
        repo_url = "https://github.com/user/test-repo"
        fetcher = RepoFetcher(repo_url, mode="api")

        mock_tree_response = {
            "tree": [
                {"type": "blob", "path": "good_file.txt"},
                {"type": "blob", "path": "bad_file.txt"},
            ]
        }

        with (
            patch("requests.get") as mock_get,
            patch("tempfile.mkdtemp", return_value="/tmp/test-repo-12345"),
            patch("pathlib.Path.mkdir"),
            patch("pathlib.Path.write_bytes"),
            patch("gitsage.repo_ingest.repo_fetcher.logger") as mock_logger,
        ):

            # Setup mock responses
            mock_tree_resp = Mock()
            mock_tree_resp.raise_for_status.return_value = None
            mock_tree_resp.json.return_value = mock_tree_response

            mock_good_file = Mock()
            mock_good_file.status_code = 200
            mock_good_file.content = b"good content"

            mock_bad_file = Mock()
            mock_bad_file.status_code = 404

            mock_get.side_effect = [mock_tree_resp, mock_good_file, mock_bad_file]

            fetcher._download_via_api()

            # Verify warning is logged for failed file
            mock_logger.warning.assert_called_once()
            assert "404" in str(mock_logger.warning.call_args)

    def test_download_via_api_http_error(self):
        """Test handling of HTTP errors during API call."""
        repo_url = "https://github.com/user/nonexistent-repo"
        fetcher = RepoFetcher(repo_url, mode="api")

        with patch("requests.get") as mock_get:
            mock_resp = Mock()
            mock_resp.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
            mock_get.return_value = mock_resp

            with pytest.raises(requests.HTTPError):
                fetcher._download_via_api()

    @patch("gitsage.repo_ingest.repo_fetcher.logger")
    def test_download_via_api_logging(self, mock_logger):
        """Test that appropriate logging messages are generated."""
        repo_url = "https://github.com/user/test-repo"
        fetcher = RepoFetcher(repo_url, mode="api")

        mock_tree_response = {"tree": []}

        with patch("requests.get") as mock_get, patch("tempfile.mkdtemp", return_value="/tmp/test-repo-12345"):

            mock_resp = Mock()
            mock_resp.raise_for_status.return_value = None
            mock_resp.json.return_value = mock_tree_response
            mock_get.return_value = mock_resp

            fetcher._download_via_api()

            # Verify logging calls
            mock_logger.info.assert_called()
            mock_logger.success.assert_called_once()

    def test_download_via_api_url_parsing(self):
        """Test correct parsing of repository URL for API calls."""
        test_cases = [
            ("https://github.com/user/repo", "user", "repo"),
            ("https://github.com/user/repo.git", "user", "repo"),
            ("https://github.com/user/repo/", "user", "repo"),
            ("https://github.com/user/repo.git/", "user", "repo"),
        ]

        for repo_url, expected_owner, expected_repo in test_cases:
            fetcher = RepoFetcher(repo_url, mode="api")

            with patch("requests.get") as mock_get, patch("tempfile.mkdtemp", return_value="/tmp/temp"):

                mock_resp = Mock()
                mock_resp.raise_for_status.return_value = None
                mock_resp.json.return_value = {"tree": []}
                mock_get.return_value = mock_resp

                fetcher._download_via_api()

                # Verify correct API URL is constructed
                expected_api_url = (
                    f"https://api.github.com/repos/{expected_owner}/{expected_repo}/git/trees/HEAD?recursive=1"
                )
                mock_get.assert_called_with(expected_api_url, headers={})


class TestRepoFetcherIntegration:
    """Integration tests for RepoFetcher functionality."""

    def test_clone_mode_integration(self):
        """Test complete clone workflow."""
        repo_url = "https://github.com/user/test-repo.git"

        with tempfile.TemporaryDirectory() as temp_dir:
            fetcher = RepoFetcher(repo_url, mode="clone", target_dir=temp_dir)

            with patch("gitsage.repo_ingest.repo_fetcher.Repo") as mock_repo:
                mock_repo.clone_from.return_value = MagicMock()

                result = fetcher.fetch()

                expected_path = os.path.join(temp_dir, "test-repo")
                assert result == expected_path
                assert os.path.exists(temp_dir)

    def test_api_mode_integration(self):
        """Test complete API download workflow."""
        repo_url = "https://github.com/user/test-repo"
        fetcher = RepoFetcher(repo_url, mode="api")

        mock_tree_response = {"tree": [{"type": "blob", "path": "README.md"}]}

        with (
            patch("requests.get") as mock_get,
            patch("tempfile.mkdtemp", return_value="/tmp/test-repo-12345"),
            patch("pathlib.Path.mkdir"),
            patch("pathlib.Path.write_bytes"),
        ):

            mock_tree_resp = Mock()
            mock_tree_resp.raise_for_status.return_value = None
            mock_tree_resp.json.return_value = mock_tree_response

            mock_file_resp = Mock()
            mock_file_resp.status_code = 200
            mock_file_resp.content = b"# Test Repo"

            mock_get.side_effect = [mock_tree_resp, mock_file_resp]

            result = fetcher.fetch()

            # Normalize path for comparison (Windows vs Unix separators)
            from pathlib import Path

            assert Path(result) == Path("/tmp/test-repo-12345")

    def test_mode_switching(self):
        """Test that mode can be changed and affects behavior."""
        repo_url = "https://github.com/user/test-repo.git"
        fetcher = RepoFetcher(repo_url, mode="clone")

        # Test clone mode
        with patch.object(fetcher, "_clone_repo", return_value="/clone/path") as mock_clone:
            result = fetcher.fetch()
            assert result == "/clone/path"
            mock_clone.assert_called_once()

        # Change to API mode
        fetcher.mode = "api"

        # Test API mode
        with patch.object(fetcher, "_download_via_api", return_value="/api/path") as mock_api:
            result = fetcher.fetch()
            assert result == "/api/path"
            mock_api.assert_called_once()
