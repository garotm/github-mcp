"""GitHub MCP tools package."""
from typing import Dict, Any

from github_mcp.server import register_tool

def register_repository_tools() -> None:
    """Register repository-related tools."""
    register_tool(
        name="list_repositories",
        description="List GitHub repositories accessible to the authenticated user",
        parameters={
            "type": "object",
            "properties": {
                "visibility": {
                    "type": "string",
                    "enum": ["all", "public", "private"],
                    "default": "all",
                },
                "sort": {
                    "type": "string",
                    "enum": ["created", "updated", "pushed", "full_name"],
                    "default": "updated",
                },
            },
        },
    )

    register_tool(
        name="get_repository",
        description="Get information about a specific repository",
        parameters={
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner"},
                "repo": {"type": "string", "description": "Repository name"},
            },
            "required": ["owner", "repo"],
        },
    )

def register_issue_tools() -> None:
    """Register issue-related tools."""
    register_tool(
        name="list_issues",
        description="List issues in a repository",
        parameters={
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner"},
                "repo": {"type": "string", "description": "Repository name"},
                "state": {
                    "type": "string",
                    "enum": ["open", "closed", "all"],
                    "default": "open",
                },
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Filter by labels",
                },
            },
            "required": ["owner", "repo"],
        },
    )

    register_tool(
        name="create_issue",
        description="Create a new issue in a repository",
        parameters={
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner"},
                "repo": {"type": "string", "description": "Repository name"},
                "title": {"type": "string", "description": "Issue title"},
                "body": {"type": "string", "description": "Issue body/description"},
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Issue labels",
                },
                "assignees": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Issue assignees",
                },
            },
            "required": ["owner", "repo", "title"],
        },
    )

def register_pull_request_tools() -> None:
    """Register pull request-related tools."""
    register_tool(
        name="list_pull_requests",
        description="List pull requests in a repository",
        parameters={
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner"},
                "repo": {"type": "string", "description": "Repository name"},
                "state": {
                    "type": "string",
                    "enum": ["open", "closed", "all"],
                    "default": "open",
                },
                "sort": {
                    "type": "string",
                    "enum": ["created", "updated", "popularity", "long-running"],
                    "default": "created",
                },
            },
            "required": ["owner", "repo"],
        },
    )

    register_tool(
        name="create_pull_request",
        description="Create a new pull request",
        parameters={
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner"},
                "repo": {"type": "string", "description": "Repository name"},
                "title": {"type": "string", "description": "Pull request title"},
                "body": {"type": "string", "description": "Pull request description"},
                "head": {"type": "string", "description": "Source branch"},
                "base": {"type": "string", "description": "Target branch", "default": "main"},
                "draft": {"type": "boolean", "description": "Create as draft", "default": False},
            },
            "required": ["owner", "repo", "title", "head"],
        },
    )

def register_content_tools() -> None:
    """Register content-related tools."""
    register_tool(
        name="get_file_content",
        description="Get the content of a file in a repository",
        parameters={
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner"},
                "repo": {"type": "string", "description": "Repository name"},
                "path": {"type": "string", "description": "File path in repository"},
                "ref": {"type": "string", "description": "Branch/tag/commit reference"},
            },
            "required": ["owner", "repo", "path"],
        },
    )

    register_tool(
        name="list_directory",
        description="List contents of a directory in a repository",
        parameters={
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner"},
                "repo": {"type": "string", "description": "Repository name"},
                "path": {"type": "string", "description": "Directory path", "default": ""},
                "ref": {"type": "string", "description": "Branch/tag/commit reference"},
            },
            "required": ["owner", "repo"],
        },
    )

def register_all_tools() -> None:
    """Register all available tools."""
    register_repository_tools()
    register_issue_tools()
    register_pull_request_tools()
    register_content_tools() 