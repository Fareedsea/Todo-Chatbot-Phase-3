"""
MCP Tool: list_tasks

Retrieves all tasks for the authenticated user with optional filtering by completion status.
Stateless tool that queries database and returns task array.
"""

from typing import Dict, Any, List
import logging
from sqlmodel import Session, select

from ..schemas import ListTasksInput, create_success_response, create_error_response
from ...database import engine
from ...models.task import Task

logger = logging.getLogger(__name__)


def list_tasks_handler(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool handler for list_tasks operation.

    Retrieves all tasks belonging to the authenticated user.
    Can optionally filter by completion status (completed=true/false).

    Args:
        input_data: Dictionary with keys:
            - user_id (str): Authenticated user ID from backend context
            - completed (bool, optional): Filter by completion status

    Returns:
        ToolResponse dictionary:
            - success: True if tasks retrieved
            - data: {"tasks": [TaskOutput, ...]} with task array
            - error: None on success, ToolError on failure

    Errors:
        - DATABASE_ERROR: Database query failed

    Security:
        - Only returns tasks belonging to user_id
        - No cross-user data access possible

    Example:
        Input:
        {
            "user_id": "user-uuid-123",
            "completed": false
        }

        Success Response:
        {
            "success": true,
            "data": {
                "tasks": [
                    {
                        "id": "task-uuid-1",
                        "title": "Buy groceries",
                        "completed": false,
                        "created_at": "2026-02-08T10:30:00Z"
                    },
                    {
                        "id": "task-uuid-2",
                        "title": "Call mom",
                        "completed": false,
                        "created_at": "2026-02-08T11:00:00Z"
                    }
                ]
            },
            "error": null
        }
    """
    try:
        # 1. Validate input with Pydantic schema
        input_schema = ListTasksInput(**input_data)
        logger.info(f"list_tasks: Fetching tasks for user {input_schema.user_id}")

        # 2. Query tasks from database
        with Session(engine) as session:
            # Build base query with user filtering
            query = select(Task).where(Task.user_id == input_schema.user_id)

            # Apply completion filter if provided
            if input_schema.completed is not None:
                query = query.where(Task.is_completed == input_schema.completed)

            # Order by creation date (newest first)
            query = query.order_by(Task.created_at.desc())

            # Execute query
            tasks = session.exec(query).all()

            # Convert to output format
            task_list = [
                {
                    "id": task.id,
                    "title": task.title,
                    "completed": task.is_completed,
                    "created_at": task.created_at.isoformat()
                }
                for task in tasks
            ]

        # 3. Return success response
        logger.info(f"list_tasks: Found {len(task_list)} tasks for user {input_schema.user_id}")
        return create_success_response({
            "tasks": task_list
        })

    except ValueError as e:
        # Pydantic validation error
        logger.warning(f"list_tasks: Validation error - {str(e)}")
        return create_error_response("VALIDATION_ERROR", str(e))

    except Exception as e:
        # Database error or unexpected error
        logger.error(f"list_tasks: Database error - {str(e)}", exc_info=True)
        return create_error_response("DATABASE_ERROR", f"Failed to retrieve tasks: {str(e)}")


def register_list_tasks_tool(server):
    """
    Register list_tasks tool with MCP server.

    Args:
        server: MCPServer instance to register tool with

    Tool Definition:
        - name: "list_tasks"
        - handler: list_tasks_handler (function)
        - input_schema: ListTasksInput JSON schema
        - output_schema: ToolResponse JSON schema
        - description: Clear explanation of tool purpose
    """
    from ..schemas import get_list_tasks_input_schema, get_tool_response_output_schema

    server.register_tool(
        name="list_tasks",
        handler=list_tasks_handler,
        input_schema=get_list_tasks_input_schema(),
        output_schema=get_tool_response_output_schema(),
        description="Retrieve all tasks for the authenticated user, optionally filtered by completion status"
    )

    logger.info("list_tasks tool registered with MCP server")
