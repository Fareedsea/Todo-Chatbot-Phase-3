"""
MCP Server Initialization (T017)

This module initializes the Model Context Protocol (MCP) server and provides
tool registration mechanisms for Phase III AI Chatbot integration.

Constitutional Compliance:
- MCP Tool Law (Law XI): Tools are stateless, deterministic, validate inputs, enforce ownership
- Tool-Only AI Law (Law VIII): AI actions limited to MCP tool invocations
- Stateless Architecture Law (Law IX): No in-memory state; tools reconstruct context from database

Architecture:
- MCP server is initialized once at application startup
- Tools are registered with explicit input/output schemas
- Each tool invocation is independent and stateless
- User context (user_id) is injected by backend, never trusted from AI

Design Pattern: Singleton MCP server instance with lazy initialization
"""

from typing import Dict, Any, Optional, Callable
import logging

# NOTE: Import the official MCP SDK when available
# For now, we define a minimal server interface compatible with MCP SDK patterns
# TODO: Replace with actual MCP SDK import once installed (T001-T002)
# from mcp import Server, Tool, ToolSchema

logger = logging.getLogger(__name__)


class MCPServer:
    """
    Model Context Protocol Server

    Manages tool registration and invocation for AI agent integration.
    Follows MCP SDK patterns for stateless, schema-validated tool execution.

    Constitutional Requirements:
    - Tools MUST be stateless (no internal memory between invocations)
    - Tools MUST validate inputs against declared schemas
    - Tools MUST enforce user ownership (user_id from authenticated context)
    - Tools MUST return structured JSON responses
    """

    def __init__(self):
        """Initialize MCP server with empty tool registry."""
        self.tools: Dict[str, Callable] = {}
        self.tool_schemas: Dict[str, Dict[str, Any]] = {}
        logger.info("MCP Server initialized")

    def register_tool(
        self,
        name: str,
        handler: Callable,
        input_schema: Dict[str, Any],
        output_schema: Dict[str, Any],
        description: str
    ) -> None:
        """
        Register an MCP tool with the server.

        Args:
            name: Tool name (snake_case, e.g., 'add_task')
            handler: Async function that implements tool logic
            input_schema: JSON Schema for input validation
            output_schema: JSON Schema for output validation
            description: Natural language description for AI agent

        Constitutional Compliance:
        - Validates that tool name follows MCP conventions (snake_case)
        - Ensures input schema includes user_id parameter
        - Stores schema for runtime validation

        Raises:
            ValueError: If tool name is invalid or schema is missing required fields
        """
        if not name or not name.islower() or " " in name:
            raise ValueError(f"Tool name must be lowercase snake_case: {name}")

        # Verify input schema includes user_id for ownership enforcement
        if input_schema.get("properties", {}).get("user_id") is None:
            logger.warning(
                f"Tool '{name}' input schema missing 'user_id' field. "
                "This may violate Security-First Architecture (Law V)."
            )

        self.tools[name] = handler
        self.tool_schemas[name] = {
            "input": input_schema,
            "output": output_schema,
            "description": description
        }

        logger.info(f"Registered MCP tool: {name}")

    def get_tool(self, name: str) -> Optional[Callable]:
        """
        Retrieve a registered tool handler by name.

        Args:
            name: Tool name

        Returns:
            Tool handler function or None if not found
        """
        return self.tools.get(name)

    def get_tool_schema(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve tool schema for validation and AI agent discovery.

        Args:
            name: Tool name

        Returns:
            Dict with 'input', 'output', 'description' keys or None if not found
        """
        return self.tool_schemas.get(name)

    def list_tools(self) -> Dict[str, str]:
        """
        List all registered tools with descriptions.

        Returns:
            Dict mapping tool names to descriptions
        """
        return {
            name: schema["description"]
            for name, schema in self.tool_schemas.items()
        }

    def invoke_tool(
        self,
        name: str,
        input_data: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Invoke an MCP tool with validated input.

        Args:
            name: Tool name
            input_data: Tool input parameters (without user_id)
            user_id: Authenticated user ID from backend JWT verification (string)

        Returns:
            Tool response (structured per tool's output schema)

        Constitutional Compliance:
        - Injects user_id from verified backend context (never trust AI-provided ID)
        - Validates input against tool's input schema
        - Handles errors gracefully and returns structured error responses
        - Logs all invocations for audit trail (Law XIII)

        Raises:
            ValueError: If tool not found
        """
        handler = self.get_tool(name)
        if handler is None:
            logger.error(f"Tool not found: {name}")
            raise ValueError(f"Tool '{name}' not registered")

        # Inject verified user_id from backend context (Security-First Architecture)
        input_data_with_user = {**input_data, "user_id": user_id}

        logger.info(f"Invoking tool: {name} for user_id={user_id}")

        try:
            # TODO: Add input schema validation here when MCP SDK is integrated
            result = handler(input_data_with_user)
            logger.info(f"Tool {name} executed successfully")
            return result
        except Exception as e:
            logger.error(f"Tool {name} execution failed: {str(e)}", exc_info=True)
            # Return structured error response per Error Handling Law (Law XII)
            return {
                "success": False,
                "error": {
                    "code": "TOOL_EXECUTION_ERROR",
                    "message": str(e)
                }
            }


# Singleton instance (lazy initialization)
_mcp_server: Optional[MCPServer] = None


def get_mcp_server() -> MCPServer:
    """
    Get or create the singleton MCP server instance.

    Returns:
        MCPServer instance

    Usage:
        from src.mcp.server import get_mcp_server

        server = get_mcp_server()
        server.register_tool(...)
    """
    global _mcp_server
    if _mcp_server is None:
        _mcp_server = MCPServer()
        logger.info("MCP Server singleton created")
    return _mcp_server


def initialize_mcp_server() -> MCPServer:
    """
    Initialize MCP server and register all tools.

    This function should be called during FastAPI application startup.

    Returns:
        Initialized MCP server instance

    Usage in main.py:
        from src.mcp.server import initialize_mcp_server

        @app.on_event("startup")
        async def startup():
            server = initialize_mcp_server()
            # Tools will be registered by individual tool modules
    """
    server = get_mcp_server()
    logger.info("MCP Server initialized for FastAPI app")
    return server
