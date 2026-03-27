from unittest.mock import patch, MagicMock
from repomind.utils.github_client import get_repo_metadata

MOCK_RESPONSE = {
    "full_name": "owner/repo",
    "description": "A test repo",
    "language": "Python",
    "stargazers_count": 100,
    "forks_count": 20,
    "open_issues_count": 5,
    "default_branch": "main",
}


def test_get_repo_metadata_returns_dict():
    with patch("repomind.utils.github_client.requests.get") as mock_get:
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: MOCK_RESPONSE,
        )
        result = get_repo_metadata("https://github.com/owner/repo")
    assert result["full_name"] == "owner/repo"
    assert result["stars"] == 100
    assert result["language"] == "Python"


def test_get_repo_metadata_handles_api_failure():
    with patch("repomind.utils.github_client.requests.get") as mock_get:
        mock_get.return_value = MagicMock(status_code=404, json=lambda: {})
        result = get_repo_metadata("https://github.com/owner/repo")
    assert result == {}
