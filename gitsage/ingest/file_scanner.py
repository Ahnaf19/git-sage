import os
from pathlib import Path
from typing import Union

from loguru import logger

SUPPORTED_CODE_EXTS = {".py", ".js", ".ts", ".cpp", ".java", ".go"}
SUPPORTED_CONFIG_FILES = {
    "README.md",
    "requirements.txt",
    "environment.yml",
    ".env",
    ".ini",
    ".yaml",
    ".yml",
    "pyproject.toml",
    "setup.cfg",
    "Dockerfile",
    "Makefile",
    "package.json",
    "pom.xml",
    "build.gradle",
    "config.json",
    ".gitignore",
    ".gitattributes",
    "tsconfig.json",
    "webpack.config.js",
    "babel.config.js",
    "eslint.config.js",
    "prettier.config.js",
    "rollup.config.js",
    "vite.config.js",
}


def scan_repo(repo_path: Union[str, Path]) -> dict:
    repo_path = Path(repo_path)
    code_files = []
    config_files = []

    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in SUPPORTED_CODE_EXTS:
                code_files.append(str(file_path))
            elif file_path.name in SUPPORTED_CONFIG_FILES:
                config_files.append(str(file_path))

    logger.info(f"Scanned repo at {repo_path}")
    logger.debug(f"Found {len(code_files)} code files and {len(config_files)} config files.")

    return {"code_files": code_files, "config_files": config_files}
