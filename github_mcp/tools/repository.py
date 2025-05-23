"""Repository-related tool implementations."""
import json
from typing import Any, Dict, List

from github import Github
from github.Repository import Repository

from github_mcp.server import ToolResult

async def handle_list_repositories(
    github_client: Github,
    parameters: Dict[str, Any],
) -> ToolResult:
    """Handle list_repositories tool call."""
    visibility = parameters.get("visibility", "all")
    sort = parameters.get("sort", "updated")
    repos = github_client.get_user().get_repos(visibility=visibility, sort=sort)
    
    return ToolResult(content=[{
        "type": "text",
        "text": json.dumps([{
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "url": repo.html_url,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "private": repo.private,
            "archived": repo.archived,
            "default_branch": repo.default_branch,
            "language": repo.language,
            "topics": repo.get_topics(),
            "created_at": repo.created_at.isoformat(),
            "updated_at": repo.updated_at.isoformat(),
            "pushed_at": repo.pushed_at.isoformat() if repo.pushed_at else None,
        } for repo in repos[:10]], indent=2)
    }])

async def handle_get_repository(
    github_client: Github,
    parameters: Dict[str, Any],
) -> ToolResult:
    """Handle get_repository tool call."""
    owner = parameters["owner"]
    repo = parameters["repo"]
    repository: Repository = github_client.get_repo(f"{owner}/{repo}")
    
    return ToolResult(content=[{
        "type": "text",
        "text": json.dumps({
            "name": repository.name,
            "full_name": repository.full_name,
            "description": repository.description,
            "url": repository.html_url,
            "stars": repository.stargazers_count,
            "forks": repository.forks_count,
            "private": repository.private,
            "archived": repository.archived,
            "default_branch": repository.default_branch,
            "language": repository.language,
            "topics": repository.get_topics(),
            "created_at": repository.created_at.isoformat(),
            "updated_at": repository.updated_at.isoformat(),
            "pushed_at": repository.pushed_at.isoformat() if repository.pushed_at else None,
            "open_issues_count": repository.open_issues_count,
            "subscribers_count": repository.subscribers_count,
            "network_count": repository.network_count,
            "size": repository.size,
            "license": repository.license.name if repository.license else None,
            "permissions": {
                "admin": repository.permissions.admin,
                "push": repository.permissions.push,
                "pull": repository.permissions.pull,
            },
        }, indent=2)
    }]) 