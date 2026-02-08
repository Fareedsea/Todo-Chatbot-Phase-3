"""
MCP Tool: delete_task

Deletes a task for the authenticated user.
Stateless tool that validates ownership and permanently removes task from database.
"""

from typing import Dict, Any
import logging
from sqlmodel import Session, select

from ..schemas import DeleteTaskInput, create_success_response, create_error_response
from ...database import engine
from ...models.task import Task

logger = logging.getLogger(__name__)


def delete_task_handler(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool handler for delete_task operation.

    Permanently deletes a task for the authenticated user.
    Validates task ownership before deletion.

    Args:
        input_data: Dictionary with keys:
            - task_id (str): Task UUID to delete
            - user_id (str): Authenticated user ID from backend context

    Returns:
        ToolResponse dictionary:
            - success: True if task deleted
            - data: {"message": "Task deleted successfully"}
            - error: None on success, ToolError on failure

    Errors:
        - VALIDATION_ERROR: Invalid task_id format
        - NOT_FOUND: Task not found or belongs to another user
        - DATABASE_ERROR: Database operation failed

    Security:
        - Validates task belongs to user_id before deletion
        - Cannot delete tasks belonging to other users

    Example:
        Input:
        {
            "task_id": "task-uuid-456",
            "user_id": "user-uuid-123"
        }

        Success Response:
        {
            "success": true,
            "data": {
                "message": "Task deleted successfully",
                "task_id": "task-uuid-456"
            },
            "error": null
        }

        Error Response (task not found):
        {
            "success": false,
            "data": null,
            "error": {
                "code": "NOT_FOUND",
                "message": "Task not found or you don't have permission to delete it"
            }
        }
    """
    try:
        # 1. Validate input with Pydantic schema
        input_schema = DeleteTaskInput(**input_data)
        logger.info(f"delete_task: Deleting task {input_schema.task_id} for user {input_schema.user_id}")

        # 2. Find and delete task in database
        with Session(engine) as session:
            # Query task with ownership validation
            task = session.exec(
                select(Task).where(
                    Task.id == input_schema.task_id,
                    Task.user_id == input_schema.user_id
                )
            ).first()

            if not task:
                logger.warning(f"delete_task: Task {input_schema.task_id} not found for user {input_schema.user_id}")
                return create_error_response(
                    "NOT_FOUND",
                    "Task not found or you don't have permission to delete it"
                )

            # Store task title for response message
            task_title = task.title

            # Delete task
            session.delete(task)
            session.commit()

            logger.info(f"delete_task: Task {input_schema.task_id} ('{task_title}') deleted successfully")

        # 3. Return success response
        return create_success_response({
            "message": "Task deleted successfully",
            "task_id": input_schema.task_id,
            "title": task_title
        })

    except ValueError as e:
        # Pydantic validation error
        logger.warning(f"delete_task: Validation error - {str(e)}")
        return create_error_response("VALIDATION_ERROR", str(e))

    except Exception as e:
        # Database error or unexpected error
        logger.error(f"delete_task: Database error - {str(e)}", exc_info=True)
        return create_error_response("DATABASE_ERROR", f"Failed to delete task: {str(e)}")


def register_delete_task_tool(server):
    """
    Register delete_task tool with MCP server.

    Args:
        server: MCPServer instance to register tool with

    Tool Definition:
        - name: "delete_task"
        - handler: delete_task_handler (function)
        - input_schema: DeleteTaskInput JSON schema
        - output_schema: ToolResponse JSON schema
        - description: Clear explanation of tool purpose
    """
    from ..schemas import get_delete_task_input_schema, get_tool_response_output_schema

    server.register_tool(
        name="delete_task",
        handler=delete_task_handler,
        input_schema=get_delete_task_input_schema(),
        output_schema=get_tool_response_output_schema(),
        description="Permanently delete a task for the authenticated user"
    )

    logger.info("delete_task tool registered with MCP server")
