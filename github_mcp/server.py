"""GitHub MCP Server implementation."""
import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from github import Github
from githubauthlib import get_github_token, GitHubAuthError
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

from github_mcp.tools import register_all_tools
from github_mcp.tools.content import handle_get_file_content, handle_list_directory
from github_mcp.tools.issues import handle_create_issue, handle_list_issues
from github_mcp.tools.pull_requests import handle_create_pull_request, handle_list_pull_requests
from github_mcp.tools.repository import handle_get_repository, handle_list_repositories

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="GitHub MCP Server")

# Initialize GitHub client using githubauthlib
try:
    github_token = get_github_token()
    if not github_token:
        raise ValueError("No GitHub token found in system keychain")
    github_client = Github(github_token)
    logger.info("Successfully authenticated with GitHub using system keychain")
except GitHubAuthError as e:
    logger.error(f"Failed to authenticate with GitHub: {str(e)}")
    raise ValueError(f"GitHub authentication failed: {str(e)}")

class ToolCall(BaseModel):
    """Model for MCP tool calls."""
    name: str = Field(..., description="Name of the tool to call")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Tool parameters")

class ToolDefinition(BaseModel):
    """Model for MCP tool definitions."""
    name: str = Field(..., description="Name of the tool")
    description: str = Field(..., description="Tool description")
    parameters: Dict[str, Any] = Field(..., description="Tool parameters schema")

class ToolResult(BaseModel):
    """Model for MCP tool results."""
    content: List[Dict[str, Any]] = Field(..., description="Tool result content")

# Tool registry
TOOLS: Dict[str, ToolDefinition] = {}

def register_tool(name: str, description: str, parameters: Dict[str, Any]) -> None:
    """Register a new tool with the MCP server."""
    TOOLS[name] = ToolDefinition(
        name=name,
        description=description,
        parameters=parameters,
    )

# Register all available tools
register_all_tools()

# Tool handler mapping
TOOL_HANDLERS = {
    "list_repositories": handle_list_repositories,
    "get_repository": handle_get_repository,
    "list_issues": handle_list_issues,
    "create_issue": handle_create_issue,
    "list_pull_requests": handle_list_pull_requests,
    "create_pull_request": handle_create_pull_request,
    "get_file_content": handle_get_file_content,
    "list_directory": handle_list_directory,
}

async def tool_handler(tool_call: ToolCall) -> ToolResult:
    """Handle tool calls and return results."""
    if tool_call.name not in TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool {tool_call.name} not found")

    if tool_call.name not in TOOL_HANDLERS:
        raise HTTPException(status_code=501, detail=f"Tool {tool_call.name} not implemented")

    try:
        handler = TOOL_HANDLERS[tool_call.name]
        return await handler(github_client, tool_call.parameters)

    except Exception as e:
        logger.error(f"Error handling tool {tool_call.name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint returning server information."""
    return {
        "name": "github-mcp",
        "version": "0.1.0",
        "tools": [tool.dict() for tool in TOOLS.values()],
    }

@app.post("/tool")
async def call_tool(tool_call: ToolCall) -> ToolResult:
    """Endpoint for synchronous tool calls."""
    return await tool_handler(tool_call)

@app.get("/sse")
async def sse_endpoint() -> EventSourceResponse:
    """SSE endpoint for streaming tool results."""
    async def event_generator():
        try:
            while True:
                # Keep the connection alive
                yield {
                    "event": "ping",
                    "data": "",
                }
                await asyncio.sleep(30)
        except Exception as e:
            logger.error(f"SSE error: {str(e)}")
            yield {
                "event": "error",
                "data": str(e),
            }

    return EventSourceResponse(event_generator())

def main() -> None:
    """Run the MCP server."""
    uvicorn.run(
        "github_mcp.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

if __name__ == "__main__":
    main() 