"""
MCP Tool: add_task

Creates a new task for the authenticated user.
Stateless tool that validates input, persists task to database, and returns success response.
"""

from typing import Dict, Any
import logging
from sqlmodel import Session

from ..schemas import AddTaskInput, create_success_response, create_error_response
from ...database import engine
from ...models.task import Task

logger = logging.getLogger(__name__)


def add_task_handler(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool handler for add_task operation.

    Creates a new task with the provided title for the authenticated user.
    Title is validated and trimmed before storage.

    Args:
        input_data: Dictionary with keys:
            - title (str): Task title (1-500 characters, trimmed)
            - user_id (str): Authenticated user ID from backend context

    Returns:
        ToolResponse dictionary:
            - success: True if task created
            - data: {"task": TaskOutput} with created task details
            - error: None on success, ToolError on failure

    Errors:
        - VALIDATION_ERROR: Invalid title (too short/long, empty after trim)
        - DATABASE_ERROR: Database operation failed

    Security:
        - user_id is injected by backend from JWT, never trusted from AI
        - Created task is automatically owned by user_id
        - No cross-user data access possible

    Example:
        Input:
        {
            "title": "Buy groceries",
            "user_id": "user-uuid-123"
        }

        Success Response:
        {
            "success": true,
            "data": {
                "task": {
                    "id": "task-uuid-456",
                    "title": "Buy groceries",
                    "completed": false,
                    "created_at": "2026-02-08T10:30:00Z"
                }
            },
            "error": null
        }
    """
    try:
        # 1. Validate input with Pydantic schema
        input_schema = AddTaskInput(**input_data)
        logger.info(f"add_task: Creating task for user {input_schema.user_id}")

        # 2. Create task in database
        with Session(engine) as session:
            task = Task(
                title=input_schema.title,  # Already trimmed by schema validator
                user_id=input_schema.user_id,
                is_completed=False
            )
            session.add(task)
            session.commit()
            session.refresh(task)

            # Convert to output format
            task_output = {
                "id": task.id,
                "title": task.title,
                "completed": task.is_completed,
                "created_at": task.created_at.isoformat()
            }

        # 3. Return success response
        logger.info(f"add_task: Task {task.id} created successfully for user {input_schema.user_id}")
        return create_success_response({
            "task": task_output
        })

    except ValueError as e:
        # Pydantic validation error (title too long, empty, etc.)
        logger.warning(f"add_task: Validation error - {str(e)}")
        return create_error_response("VALIDATION_ERROR", str(e))

    except Exception as e:
        # Database error or unexpected error
        logger.error(f"add_task: Database error - {str(e)}", exc_info=True)
        return create_error_response("DATABASE_ERROR", f"Failed to create task: {str(e)}")


def register_add_task_tool(server):
    """
    Register add_task tool with MCP server.

    Args:
        server: MCPServer instance to register tool with

    Tool Definition:
        - name: "add_task"
        - handler: add_task_handler (async function)
        - input_schema: AddTaskInput JSON schema
        - output_schema: ToolResponse JSON schema
        - description: Clear explanation of tool purpose
    """
    from ..schemas import get_add_task_input_schema, get_tool_response_output_schema

    server.register_tool(
        name="add_task",
        handler=add_task_handler,
        input_schema=get_add_task_input_schema(),
        output_schema=get_tool_response_output_schema(),
        description="Create a new task for the authenticated user with the specified title"
    )

    logger.info("add_task tool registered with MCP server")
