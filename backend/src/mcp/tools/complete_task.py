"""
MCP Tool: complete_task

Marks a task as completed for the authenticated user.
Stateless tool that validates ownership, updates status, and returns updated task.
"""

from typing import Dict, Any
import logging
from datetime import datetime
from sqlmodel import Session, select

from ..schemas import CompleteTaskInput, create_success_response, create_error_response
from ...database import engine
from ...models.task import Task

logger = logging.getLogger(__name__)


def complete_task_handler(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool handler for complete_task operation.

    Marks a task as completed (is_completed=true) for the authenticated user.
    Validates task ownership before updating.

    Args:
        input_data: Dictionary with keys:
            - task_id (str): Task UUID to complete
            - user_id (str): Authenticated user ID from backend context

    Returns:
        ToolResponse dictionary:
            - success: True if task completed
            - data: {"task": TaskOutput} with updated task details
            - error: None on success, ToolError on failure

    Errors:
        - VALIDATION_ERROR: Invalid task_id format
        - NOT_FOUND: Task not found or belongs to another user
        - DATABASE_ERROR: Database operation failed

    Security:
        - Validates task belongs to user_id before updating
        - Cannot complete tasks belonging to other users

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
                "task": {
                    "id": "task-uuid-456",
                    "title": "Buy groceries",
                    "completed": true,
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
                "message": "Task not found or you don't have permission to complete it"
            }
        }
    """
    try:
        # 1. Validate input with Pydantic schema
        input_schema = CompleteTaskInput(**input_data)
        logger.info(f"complete_task: Completing task {input_schema.task_id} for user {input_schema.user_id}")

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
                logger.warning(f"complete_task: Task {input_schema.task_id} not found for user {input_schema.user_id}")
                return create_error_response(
                    "NOT_FOUND",
                    "Task not found or you don't have permission to complete it"
                )

            # Check if already completed
            if task.is_completed:
                logger.info(f"complete_task: Task {input_schema.task_id} already completed")
                # Return success with current state (idempotent operation)
            else:
                # Update task status
                task.is_completed = True
                task.updated_at = datetime.utcnow()
                session.add(task)
                session.commit()
                session.refresh(task)
                logger.info(f"complete_task: Task {input_schema.task_id} marked as completed")

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
        logger.warning(f"complete_task: Validation error - {str(e)}")
        return create_error_response("VALIDATION_ERROR", str(e))

    except Exception as e:
        # Database error or unexpected error
        logger.error(f"complete_task: Database error - {str(e)}", exc_info=True)
        return create_error_response("DATABASE_ERROR", f"Failed to complete task: {str(e)}")


def register_complete_task_tool(server):
    """
    Register complete_task tool with MCP server.

    Args:
        server: MCPServer instance to register tool with

    Tool Definition:
        - name: "complete_task"
        - handler: complete_task_handler (function)
        - input_schema: CompleteTaskInput JSON schema
        - output_schema: ToolResponse JSON schema
        - description: Clear explanation of tool purpose
    """
    from ..schemas import get_complete_task_input_schema, get_tool_response_output_schema

    server.register_tool(
        name="complete_task",
        handler=complete_task_handler,
        input_schema=get_complete_task_input_schema(),
        output_schema=get_tool_response_output_schema(),
        description="Mark a task as completed for the authenticated user"
    )

    logger.info("complete_task tool registered with MCP server")
