# main.py

from gitsage.repo_ingest.repo_fetcher import RepoFetcher
from gitsage.repo_ingest.repo_scanner import scan_repo


def main(url: str = "https://github.com/pallets/flask"):
    fetcher = RepoFetcher(url, mode="clone")
    repo_path = fetcher.fetch()
    _ = scan_repo(repo_path)


if __name__ == "__main__":
    main()
