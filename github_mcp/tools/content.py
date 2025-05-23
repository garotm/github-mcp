"""Content-related tool implementations."""

import base64
import json
from typing import Any, Dict

from github import Github
from github.Repository import Repository

from github_mcp.server import ToolResult


async def handle_get_file_content(
    github_client: Github,
    parameters: Dict[str, Any],
) -> ToolResult:
    """Handle get_file_content tool call."""
    owner = parameters["owner"]
    repo = parameters["repo"]
    path = parameters["path"]
    ref = parameters.get("ref")

    repository: Repository = github_client.get_repo(f"{owner}/{repo}")
    file_content = repository.get_contents(path, ref=ref)

    if isinstance(file_content, list):
        raise ValueError(f"Path '{path}' is a directory, not a file")

    content = base64.b64decode(file_content.content).decode("utf-8")

    return ToolResult(
        content=[
            {
                "type": "text",
                "text": json.dumps(
                    {
                        "name": file_content.name,
                        "path": file_content.path,
                        "sha": file_content.sha,
                        "size": file_content.size,
                        "url": file_content.html_url,
                        "download_url": file_content.download_url,
                        "type": file_content.type,
                        "encoding": file_content.encoding,
                        "content": content,
                    },
                    indent=2,
                ),
            }
        ]
    )


async def handle_list_directory(
    github_client: Github,
    parameters: Dict[str, Any],
) -> ToolResult:
    """Handle list_directory tool call."""
    owner = parameters["owner"]
    repo = parameters["repo"]
    path = parameters.get("path", "")
    ref = parameters.get("ref")

    repository: Repository = github_client.get_repo(f"{owner}/{repo}")
    contents = repository.get_contents(path, ref=ref)

    if not isinstance(contents, list):
        contents = [contents]

    return ToolResult(
        content=[
            {
                "type": "text",
                "text": json.dumps(
                    [
                        {
                            "name": item.name,
                            "path": item.path,
                            "sha": item.sha,
                            "size": item.size,
                            "url": item.html_url,
                            "download_url": item.download_url,
                            "type": item.type,
                            "encoding": (
                                item.encoding if hasattr(item, "encoding") else None
                            ),
                        }
                        for item in contents
                    ],
                    indent=2,
                ),
            }
        ]
    )
