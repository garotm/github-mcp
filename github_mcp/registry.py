"""GitHub MCP tool registry module."""

from typing import Any, Dict

from pydantic import BaseModel, Field


class ToolDefinition(BaseModel):
    """Model for MCP tool definitions."""

    name: str = Field(..., description="Name of the tool")
    description: str = Field(..., description="Tool description")
    parameters: Dict[str, Any] = Field(..., description="Tool parameters schema")


# Tool registry
TOOLS: Dict[str, ToolDefinition] = {}


def register_tool(name: str, description: str, parameters: Dict[str, Any]) -> None:
    """Register a new tool with the MCP server."""
    TOOLS[name] = ToolDefinition(
        name=name,
        description=description,
        parameters=parameters,
    )
