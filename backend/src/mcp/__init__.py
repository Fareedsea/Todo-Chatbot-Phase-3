"""
MCP (Model Context Protocol) Server Module

This module provides MCP server initialization and tool registration for Phase III AI Chatbot.
All AI actions MUST go through MCP tools to ensure stateless, auditable, and secure operation.

Constitutional Requirements:
- MCP Tool Law (Law XI): Tools MUST be stateless, deterministic, validate inputs, and enforce ownership
- Tool-Only AI Law (Law VIII): AI MUST ONLY act via MCP tools (no direct state manipulation)
- Security-First Architecture (Law V): Tools MUST receive user_id from verified backend context
"""

from .server import get_mcp_server
from .schemas import (
    AddTaskInput,
    ListTasksInput,
    UpdateTaskInput,
    CompleteTaskInput,
    DeleteTaskInput,
    ToolResponse,
    ToolError,
    TaskOutput,
)

__all__ = [
    "get_mcp_server",
    "AddTaskInput",
    "ListTasksInput",
    "UpdateTaskInput",
    "CompleteTaskInput",
    "DeleteTaskInput",
    "ToolResponse",
    "ToolError",
    "TaskOutput",
]
