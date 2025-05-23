"""Pull request-related tool implementations."""
import json
from typing import Any, Dict, List

from github import Github
from github.Repository import Repository

from github_mcp.server import ToolResult

async def handle_list_pull_requests(
    github_client: Github,
    parameters: Dict[str, Any],
) -> ToolResult:
    """Handle list_pull_requests tool call."""
    owner = parameters["owner"]
    repo = parameters["repo"]
    state = parameters.get("state", "open")
    sort = parameters.get("sort", "created")
    
    repository: Repository = github_client.get_repo(f"{owner}/{repo}")
    pulls = repository.get_pulls(state=state, sort=sort)
    
    return ToolResult(content=[{
        "type": "text",
        "text": json.dumps([{
            "number": pr.number,
            "title": pr.title,
            "state": pr.state,
            "url": pr.html_url,
            "body": pr.body,
            "created_at": pr.created_at.isoformat(),
            "updated_at": pr.updated_at.isoformat(),
            "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
            "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
            "head": {
                "ref": pr.head.ref,
                "sha": pr.head.sha,
                "user": pr.head.user.login,
                "repo": pr.head.repo.full_name if pr.head.repo else None,
            },
            "base": {
                "ref": pr.base.ref,
                "sha": pr.base.sha,
                "user": pr.base.user.login,
                "repo": pr.base.repo.full_name,
            },
            "author": pr.user.login,
            "assignees": [assignee.login for assignee in pr.assignees],
            "labels": [label.name for label in pr.labels],
            "comments": pr.comments,
            "review_comments": pr.review_comments,
            "commits": pr.commits,
            "additions": pr.additions,
            "deletions": pr.deletions,
            "changed_files": pr.changed_files,
            "draft": pr.draft,
            "mergeable": pr.mergeable,
            "mergeable_state": pr.mergeable_state,
        } for pr in pulls[:10]], indent=2)
    }])

async def handle_create_pull_request(
    github_client: Github,
    parameters: Dict[str, Any],
) -> ToolResult:
    """Handle create_pull_request tool call."""
    owner = parameters["owner"]
    repo = parameters["repo"]
    title = parameters["title"]
    body = parameters.get("body", "")
    head = parameters["head"]
    base = parameters.get("base", "main")
    draft = parameters.get("draft", False)
    
    repository: Repository = github_client.get_repo(f"{owner}/{repo}")
    pr = repository.create_pull(
        title=title,
        body=body,
        head=head,
        base=base,
        draft=draft,
    )
    
    return ToolResult(content=[{
        "type": "text",
        "text": json.dumps({
            "number": pr.number,
            "title": pr.title,
            "state": pr.state,
            "url": pr.html_url,
            "body": pr.body,
            "created_at": pr.created_at.isoformat(),
            "updated_at": pr.updated_at.isoformat(),
            "head": {
                "ref": pr.head.ref,
                "sha": pr.head.sha,
                "user": pr.head.user.login,
                "repo": pr.head.repo.full_name if pr.head.repo else None,
            },
            "base": {
                "ref": pr.base.ref,
                "sha": pr.base.sha,
                "user": pr.base.user.login,
                "repo": pr.base.repo.full_name,
            },
            "author": pr.user.login,
            "assignees": [assignee.login for assignee in pr.assignees],
            "labels": [label.name for label in pr.labels],
            "comments": pr.comments,
            "review_comments": pr.review_comments,
            "commits": pr.commits,
            "additions": pr.additions,
            "deletions": pr.deletions,
            "changed_files": pr.changed_files,
            "draft": pr.draft,
            "mergeable": pr.mergeable,
            "mergeable_state": pr.mergeable_state,
        }, indent=2)
    }]) 