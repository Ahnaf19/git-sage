# gitsage/repo_ingest/repo_fetcher.py

import os
import tempfile
from typing import Optional

import requests
from git.repo.base import Repo
from loguru import logger


class RepoFetcher:
    def __init__(self, repo_url: str, mode: str = "clone", target_dir: str = "./repos", token: Optional[str] = None):
        self.repo_url = repo_url
        self.mode = mode
        self.target_dir = target_dir
        self.token = token

    def fetch(self) -> str:
        if self.mode == "clone":
            return self._clone_repo()
        elif self.mode == "api":
            return self._download_via_api()
        else:
            raise ValueError("Unsupported mode. Use 'clone' or 'api'.")

    def _extract_repo_name(self) -> str:
        return self.repo_url.rstrip("/").split("/")[-1].replace(".git", "")

    def _clone_repo(self) -> str:
        os.makedirs(self.target_dir, exist_ok=True)
        repo_name = self._extract_repo_name()
        repo_path = os.path.join(self.target_dir, repo_name)

        if os.path.exists(repo_path):
            logger.info(f"Repository already exists at {repo_path}")
            return repo_path

        logger.info(f"Cloning {self.repo_url} into {repo_path}...")
        Repo.clone_from(self.repo_url, repo_path)
        logger.success(f"Repository cloned successfully to {repo_path}")
        return repo_path

    def _download_via_api(self) -> str:
        headers = {}
        if self.token:
            headers["Authorization"] = f"token {self.token}"

        owner, repo = self.repo_url.rstrip("/").split("/")[-2:]
        repo = repo.replace(".git", "")  # Remove .git extension if present
        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
        logger.info(f"Fetching GitHub tree via API: {api_url}")
        res = requests.get(api_url, headers=headers)
        res.raise_for_status()

        tree = res.json().get("tree", [])
        temp_dir = tempfile.mkdtemp(prefix=f"{repo}-")
        for item in tree:
            if item["type"] == "blob":
                file_url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{item['path']}"
                local_path = os.path.join(temp_dir, item["path"])
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                file_res = requests.get(file_url, headers=headers)
                if file_res.status_code == 200:
                    with open(local_path, "wb") as f:
                        f.write(file_res.content)
                else:
                    logger.warning(f"Skipped: {file_url} ({file_res.status_code})")
        logger.success(f"Repo downloaded to temp dir: {temp_dir}")
        return temp_dir
