import re
import requests


def _parse_owner_repo(repo_url: str) -> tuple[str, str]:
    match = re.search(r"github\.com/([^/]+)/([^/]+?)(?:\.git)?$", repo_url)
    if not match:
        raise ValueError(f"Cannot parse GitHub URL: {repo_url}")
    return match.group(1), match.group(2)


def get_repo_metadata(repo_url: str) -> dict:
    """Fetch repository metadata from the GitHub REST API."""
    try:
        owner, repo = _parse_owner_repo(repo_url)
    except ValueError:
        return {}

    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}", timeout=10
    )
    if response.status_code != 200:
        return {}

    data = response.json()
    return {
        "full_name": data.get("full_name", ""),
        "description": data.get("description", ""),
        "language": data.get("language", ""),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "open_issues": data.get("open_issues_count", 0),
        "default_branch": data.get("default_branch", "main"),
    }
