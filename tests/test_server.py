"""Tests for the GitHub MCP server."""
import json
import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from github_mcp.server import app, register_tool

# Test client
client = TestClient(app)

@pytest.fixture
def mock_github():
    """Mock GitHub client for testing."""
    with patch("github_mcp.server.Github") as mock:
        # Mock user and repositories
        mock_user = MagicMock()
        mock_repo = MagicMock()
        mock_repo.name = "test-repo"
        mock_repo.full_name = "test-owner/test-repo"
        mock_repo.description = "Test repository"
        mock_repo.html_url = "https://github.com/test-owner/test-repo"
        mock_repo.stargazers_count = 42
        mock_repo.forks_count = 7
        mock_repo.default_branch = "main"
        mock_repo.language = "Python"
        mock_repo.get_topics.return_value = ["test", "python"]
        
        mock_user.get_repos.return_value = [mock_repo]
        mock.return_value.get_user.return_value = mock_user
        mock.return_value.get_repo.return_value = mock_repo
        
        yield mock

def test_root_endpoint():
    """Test the root endpoint returns server information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "github-mcp"
    assert data["version"] == "0.1.0"
    assert "tools" in data

def test_list_repositories(mock_github):
    """Test the list_repositories tool."""
    response = client.post(
        "/tool",
        json={
            "name": "list_repositories",
            "parameters": {"visibility": "all", "sort": "updated"},
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert len(data["content"]) == 1
    assert data["content"][0]["type"] == "text"
    
    repos = json.loads(data["content"][0]["text"])
    assert len(repos) == 1
    assert repos[0]["name"] == "test-repo"
    assert repos[0]["full_name"] == "test-owner/test-repo"

def test_get_repository(mock_github):
    """Test the get_repository tool."""
    response = client.post(
        "/tool",
        json={
            "name": "get_repository",
            "parameters": {
                "owner": "test-owner",
                "repo": "test-repo",
            },
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert len(data["content"]) == 1
    assert data["content"][0]["type"] == "text"
    
    repo = json.loads(data["content"][0]["text"])
    assert repo["name"] == "test-repo"
    assert repo["full_name"] == "test-owner/test-repo"
    assert repo["language"] == "Python"
    assert repo["topics"] == ["test", "python"]

def test_invalid_tool():
    """Test calling an invalid tool."""
    response = client.post(
        "/tool",
        json={
            "name": "invalid_tool",
            "parameters": {},
        },
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_sse_endpoint():
    """Test the SSE endpoint."""
    response = client.get("/sse")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream"
    
    # Read the first event
    event = next(response.iter_lines())
    assert b"event: ping" in event 