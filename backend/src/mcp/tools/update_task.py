"""
MCP Tool: update_task

Updates a task's title for the authenticated user.
Stateless tool that validates ownership, updates title, and returns updated task.
"""

from typing import Dict, Any
import logging
from datetime import datetime
from sqlmodel import Session, select

from ..schemas import UpdateTaskInput, create_success_response, create_error_response
from ...database import engine
from ...models.task import Task

logger = logging.getLogger(__name__)


def update_task_handler(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool handler for update_task operation.

    Updates a task's title for the authenticated user.
    Validates task ownership and title constraints before updating.

    Args:
        input_data: Dictionary with keys:
            - task_id (str): Task UUID to update
            - title (str): New task title (1-500 characters, trimmed)
            - user_id (str): Authenticated user ID from backend context

    Returns:
        ToolResponse dictionary:
            - success: True if task updated
            - data: {"task": TaskOutput} with updated task details
            - error: None on success, ToolError on failure

    Errors:
        - VALIDATION_ERROR: Invalid task_id or title (too short/long)
        - NOT_FOUND: Task not found or belongs to another user
        - DATABASE_ERROR: Database operation failed

    Security:
        - Validates task belongs to user_id before updating
        - Cannot update tasks belonging to other users

    Example:
        Input:
        {
            "task_id": "task-uuid-456",
            "title": "Buy groceries and milk",
            "user_id": "user-uuid-123"
        }

        Success Response:
        {
            "success": true,
            "data": {
                "task": {
                    "id": "task-uuid-456",
                    "title": "Buy groceries and milk",
                    "completed": false,
                    "created_at": "2026-02-08T10:30:00Z"
                }
            },
            "error": null
        }

        Error Response (task not found):
        {
            "success": false,
            "data": null,
            "error": {
                "code": "NOT_FOUND",
                "message": "Task not found or you don't have permission to update it"
            }
        }
    """
    try:
        # 1. Validate input with Pydantic schema
        input_schema = UpdateTaskInput(**input_data)
        logger.info(f"update_task: Updating task {input_schema.task_id} for user {input_schema.user_id}")

        # 2. Find and update task in database
        with Session(engine) as session:
            # Query task with ownership validation
            task = session.exec(
                select(Task).where(
                    Task.id == input_schema.task_id,
                    Task.user_id == input_schema.user_id
                )
            ).first()

            if not task:
                logger.warning(f"update_task: Task {input_schema.task_id} not found for user {input_schema.user_id}")
                return create_error_response(
                    "NOT_FOUND",
                    "Task not found or you don't have permission to update it"
                )

            # Store old title for logging
            old_title = task.title

            # Update task title and timestamp
            task.title = input_schema.title  # Already trimmed by schema validator
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)

            logger.info(f"update_task: Task {input_schema.task_id} title updated from '{old_title}' to '{task.title}'")

            # Convert to output format
            task_output = {
                "id": task.id,
                "title": task.title,
                "completed": task.is_completed,
                "created_at": task.created_at.isoformat()
            }

        # 3. Return success response
        return create_success_response({
            "task": task_output
        })

    except ValueError as e:
        # Pydantic validation error
        logger.warning(f"update_task: Validation error - {str(e)}")
        return create_error_response("VALIDATION_ERROR", str(e))

    except Exception as e:
        # Database error or unexpected error
        logger.error(f"update_task: Database error - {str(e)}", exc_info=True)
        return create_error_response("DATABASE_ERROR", f"Failed to update task: {str(e)}")


def register_update_task_tool(server):
    """
    Register update_task tool with MCP server.

    Args:
        server: MCPServer instance to register tool with

    Tool Definition:
        - name: "update_task"
        - handler: update_task_handler (function)
        - input_schema: UpdateTaskInput JSON schema
        - output_schema: ToolResponse JSON schema
        - description: Clear explanation of tool purpose
    """
    from ..schemas import get_update_task_input_schema, get_tool_response_output_schema

    server.register_tool(
        name="update_task",
        handler=update_task_handler,
        input_schema=get_update_task_input_schema(),
        output_schema=get_tool_response_output_schema(),
        description="Update a task's title for the authenticated user"
    )

    logger.info("update_task tool registered with MCP server")
