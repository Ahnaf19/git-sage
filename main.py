# main.py

from gitsage.ingest.file_scanner import scan_repo
from gitsage.ingest.repo_cloner import clone_repo


def main(url: str = "https://github.com/pallets/flask"):
    github_url = url  # replace with real URL
    repo_path = clone_repo(github_url)
    _ = scan_repo(repo_path)


if __name__ == "__main__":
    main()
