"""Issue-related tool implementations."""
import json
from typing import Any, Dict, List

from github import Github
from github.Repository import Repository

from github_mcp.server import ToolResult

async def handle_list_issues(
    github_client: Github,
    parameters: Dict[str, Any],
) -> ToolResult:
    """Handle list_issues tool call."""
    owner = parameters["owner"]
    repo = parameters["repo"]
    state = parameters.get("state", "open")
    labels = parameters.get("labels", [])
    
    repository: Repository = github_client.get_repo(f"{owner}/{repo}")
    issues = repository.get_issues(state=state, labels=labels)
    
    return ToolResult(content=[{
        "type": "text",
        "text": json.dumps([{
            "number": issue.number,
            "title": issue.title,
            "state": issue.state,
            "url": issue.html_url,
            "body": issue.body,
            "created_at": issue.created_at.isoformat(),
            "updated_at": issue.updated_at.isoformat(),
            "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
            "labels": [label.name for label in issue.labels],
            "assignees": [assignee.login for assignee in issue.assignees],
            "author": issue.user.login,
            "comments": issue.comments,
            "locked": issue.locked,
            "milestone": issue.milestone.title if issue.milestone else None,
            "pull_request": bool(issue.pull_request),
        } for issue in issues[:10]], indent=2)
    }])

async def handle_create_issue(
    github_client: Github,
    parameters: Dict[str, Any],
) -> ToolResult:
    """Handle create_issue tool call."""
    owner = parameters["owner"]
    repo = parameters["repo"]
    title = parameters["title"]
    body = parameters.get("body", "")
    labels = parameters.get("labels", [])
    assignees = parameters.get("assignees", [])
    
    repository: Repository = github_client.get_repo(f"{owner}/{repo}")
    issue = repository.create_issue(
        title=title,
        body=body,
        labels=labels,
        assignees=assignees,
    )
    
    return ToolResult(content=[{
        "type": "text",
        "text": json.dumps({
            "number": issue.number,
            "title": issue.title,
            "state": issue.state,
            "url": issue.html_url,
            "body": issue.body,
            "created_at": issue.created_at.isoformat(),
            "updated_at": issue.updated_at.isoformat(),
            "labels": [label.name for label in issue.labels],
            "assignees": [assignee.login for assignee in issue.assignees],
            "author": issue.user.login,
            "comments": issue.comments,
            "locked": issue.locked,
            "milestone": issue.milestone.title if issue.milestone else None,
        }, indent=2)
    }]) 