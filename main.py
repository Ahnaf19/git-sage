# main.py

import argparse
import sys

from gitsage.repo_ingest.repo_fetcher import RepoFetcher
from gitsage.repo_ingest.repo_scanner import scan_repo


def main():
    parser = argparse.ArgumentParser(
        description="Git Sage - Repository analysis tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://github.com/pallets/flask
  %(prog)s https://github.com/microsoft/vscode --mode api
  %(prog)s git@github.com:user/repo.git --target-dir ./my-repos
        """,
    )

    parser.add_argument("url", help="GitHub repository URL (https or ssh format)")

    parser.add_argument(
        "--mode",
        choices=["clone", "api"],
        default="clone",
        help="Fetch mode: 'clone' (git clone) or 'api' (GitHub API) [default: clone]",
    )

    parser.add_argument(
        "--target-dir", default="./repos", help="Target directory for cloned repositories [default: ./repos]"
    )

    parser.add_argument("--token", help="GitHub token for API access (for private repos or higher rate limits)")

    args = parser.parse_args()

    try:
        fetcher = RepoFetcher(repo_url=args.url, mode=args.mode, target_dir=args.target_dir, token=args.token)
        repo_path = fetcher.fetch()
        _ = scan_repo(repo_path)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
