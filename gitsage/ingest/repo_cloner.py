# gitsage/ingest/repo_cloner.py

import os

from git.repo.base import Repo
from loguru import logger


def clone_repo(repo_url: str, clone_dir: str = "./repos") -> str:
    os.makedirs(clone_dir, exist_ok=True)
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    repo_path = os.path.join(clone_dir, repo_name)

    if os.path.exists(repo_path):
        logger.info(f"Repository already exists at {repo_path}")
        return repo_path

    logger.info(f"Cloning {repo_url} into {repo_path}...")
    Repo.clone_from(repo_url, repo_path)
    logger.success(f"Repository cloned successfully to {repo_path}")
    return repo_path
