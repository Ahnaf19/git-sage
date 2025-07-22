# main.py

from loguru import logger

from gitsage.ingest.file_scanner import scan_repo
from gitsage.ingest.repo_cloner import clone_repo


def main():
    github_url = "https://github.com/pallets/flask"  # replace with real URL
    repo_path = clone_repo(github_url)
    scanned = scan_repo(repo_path)

    logger.info("Scan complete.")
    logger.info(f"Code files: {len(scanned['code_files'])}")
    logger.info(f"Config files: {len(scanned['config_files'])}")


if __name__ == "__main__":
    main()
