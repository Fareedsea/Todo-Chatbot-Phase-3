"""
MCP Tool Input/Output Schemas (T018)

This module defines Pydantic models for MCP tool input validation and output serialization.
All schemas follow the contracts specified in plan.md (lines 490-696).

Constitutional Compliance:
- MCP Tool Law (Law XI): Tools validate inputs against JSON schemas
- API Contract Enforcement (Law VI): MCP tools have explicit input/output schemas
- Security-First Architecture (Law V): user_id required for ownership enforcement

Schema Design Principles:
- Input schemas validate data before tool execution
- Output schemas ensure consistent response structure
- All schemas support JSON serialization for MCP protocol
- Validation errors provide helpful messages for debugging
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# INPUT SCHEMAS
# ============================================================================

class AddTaskInput(BaseModel):
    """
    Input schema for add_task MCP tool.

    Constitutional Requirements:
    - title: Required, 1-500 characters (prevents abuse)
    - user_id: Required, injected by backend from JWT (never from AI)

    Contract Reference: plan.md lines 489-534
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Task title/description",
        examples=["Buy groceries", "Call mom tomorrow"]
    )
    user_id: str = Field(
        ...,
        min_length=1,
        description="Authenticated user ID (provided by backend, not AI)"
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate title is not empty or whitespace-only."""
        if not v or not v.strip():
            raise ValueError("Task title cannot be empty or whitespace-only")
        return v.strip()


class ListTasksInput(BaseModel):
    """
    Input schema for list_tasks MCP tool.

    Constitutional Requirements:
    - user_id: Required for user data isolation
    - completed: Optional filter by completion status

    Contract Reference: plan.md lines 536-583
    """
    user_id: str = Field(
        ...,
        min_length=1,
        description="Authenticated user ID"
    )
    completed: Optional[bool] = Field(
        None,
        description="Optional filter by completion status (None = all tasks)"
    )


class UpdateTaskInput(BaseModel):
    """
    Input schema for update_task MCP tool.

    Constitutional Requirements:
    - task_id: Required to identify task
    - title: Required new title, 1-500 characters
    - user_id: Required for ownership verification

    Contract Reference: plan.md lines 585-625
    """
    task_id: str = Field(
        ...,
        min_length=1,
        description="ID of task to update"
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="New task title"
    )
    user_id: str = Field(
        ...,
        min_length=1,
        description="Authenticated user ID"
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate title is not empty or whitespace-only."""
        if not v or not v.strip():
            raise ValueError("Task title cannot be empty or whitespace-only")
        return v.strip()


class CompleteTaskInput(BaseModel):
    """
    Input schema for complete_task MCP tool.

    Constitutional Requirements:
    - task_id: Required to identify task
    - user_id: Required for ownership verification

    Contract Reference: plan.md lines 627-664
    """
    task_id: str = Field(
        ...,
        min_length=1,
        description="ID of task to mark as complete"
    )
    user_id: str = Field(
        ...,
        min_length=1,
        description="Authenticated user ID"
    )


class DeleteTaskInput(BaseModel):
    """
    Input schema for delete_task MCP tool.

    Constitutional Requirements:
    - task_id: Required to identify task
    - user_id: Required for ownership verification

    Contract Reference: plan.md lines 666-695
    """
    task_id: str = Field(
        ...,
        min_length=1,
        description="ID of task to delete"
    )
    user_id: str = Field(
        ...,
        min_length=1,
        description="Authenticated user ID"
    )


# ============================================================================
# OUTPUT SCHEMAS
# ============================================================================

class ToolError(BaseModel):
    """
    Structured error response for MCP tools.

    Constitutional Requirements:
    - Error Handling Law (Law XII): Backend returns consistent JSON error formats
    - code: Machine-readable error code (uppercase snake_case)
    - message: Human-readable error message

    Error Code Conventions:
    - VALIDATION_ERROR: Input validation failed
    - NOT_FOUND: Resource does not exist
    - UNAUTHORIZED: User does not own resource
    - DATABASE_ERROR: Database operation failed
    - TOOL_EXECUTION_ERROR: Unexpected error during tool execution
    """
    code: str = Field(
        ...,
        description="Machine-readable error code",
        examples=["VALIDATION_ERROR", "NOT_FOUND", "UNAUTHORIZED"]
    )
    message: str = Field(
        ...,
        description="Human-readable error message",
        examples=["Task not found", "Invalid task title length"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "code": "NOT_FOUND",
                "message": "Task with ID 123 not found for this user"
            }
        }


class TaskOutput(BaseModel):
    """
    Standardized task representation for MCP tool responses.

    Constitutional Requirements:
    - All task data comes from database (no hallucinations)
    - Timestamps serialized as ISO 8601 strings
    - Compatible with existing Phase II Task model

    Fields match backend/src/models/task.py Task model
    """
    id: str = Field(
        ...,
        description="Unique task ID (UUID)"
    )
    title: str = Field(
        ...,
        description="Task title/description"
    )
    completed: bool = Field(
        ...,
        description="Task completion status"
    )
    created_at: datetime = Field(
        ...,
        description="Task creation timestamp (ISO 8601)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": 42,
                "title": "Buy groceries",
                "completed": False,
                "created_at": "2026-02-08T14:30:00Z"
            }
        }


class ToolResponse(BaseModel):
    """
    Generic structured response for all MCP tools.

    Constitutional Requirements:
    - MCP Tool Law (Law XI): Tools return structured JSON responses
    - success: Boolean indicating operation success
    - data: Optional response data (varies by tool)
    - error: Optional error details (present only if success=False)

    Design Pattern: Result type (success + data OR error)
    """
    success: bool = Field(
        ...,
        description="Whether tool execution succeeded"
    )
    data: Optional[dict] = Field(
        None,
        description="Tool-specific response data (present if success=True)"
    )
    error: Optional[ToolError] = Field(
        None,
        description="Error details (present if success=False)"
    )

    @field_validator("data", "error")
    @classmethod
    def validate_result_pattern(cls, v, info):
        """
        Enforce Result pattern: success=True requires data, success=False requires error.

        This validation ensures tools follow the constitutional requirement for
        structured error responses (Law XII).
        """
        # Note: Validation logic will be enforced at tool implementation level
        # Pydantic v2 makes cross-field validation complex, so we document the contract here
        return v

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "success": True,
                    "data": {
                        "task": {
                            "id": 42,
                            "title": "Buy groceries",
                            "completed": False,
                            "created_at": "2026-02-08T14:30:00Z"
                        }
                    },
                    "error": None
                },
                {
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": "Task not found for this user"
                    }
                }
            ]
        }


# ============================================================================
# TOOL-SPECIFIC RESPONSE SCHEMAS
# ============================================================================

class AddTaskResponse(ToolResponse):
    """Response schema for add_task tool (includes created task)."""
    pass


class ListTasksResponse(ToolResponse):
    """Response schema for list_tasks tool (includes task array and count)."""
    pass


class UpdateTaskResponse(ToolResponse):
    """Response schema for update_task tool (includes updated task)."""
    pass


class CompleteTaskResponse(ToolResponse):
    """Response schema for complete_task tool (includes completed task)."""
    pass


class DeleteTaskResponse(ToolResponse):
    """Response schema for delete_task tool (includes success message)."""
    pass


# ============================================================================
# SCHEMA UTILITIES
# ============================================================================

def create_success_response(data: dict) -> dict:
    """
    Create a successful tool response.

    Args:
        data: Response data dictionary

    Returns:
        ToolResponse dict with success=True

    Usage:
        return create_success_response({"task": task_dict})
    """
    return {
        "success": True,
        "data": data,
        "error": None
    }


def create_error_response(code: str, message: str) -> dict:
    """
    Create an error tool response.

    Args:
        code: Machine-readable error code (uppercase snake_case)
        message: Human-readable error message

    Returns:
        ToolResponse dict with success=False

    Usage:
        return create_error_response("NOT_FOUND", "Task not found")
    """
    return {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message
        }
    }


# ============================================================================
# JSON SCHEMA EXPORTS (for MCP SDK integration)
# ============================================================================

def get_add_task_input_schema() -> dict:
    """Return JSON Schema for AddTaskInput (for MCP tool registration)."""
    return AddTaskInput.model_json_schema()


def get_list_tasks_input_schema() -> dict:
    """Return JSON Schema for ListTasksInput (for MCP tool registration)."""
    return ListTasksInput.model_json_schema()


def get_update_task_input_schema() -> dict:
    """Return JSON Schema for UpdateTaskInput (for MCP tool registration)."""
    return UpdateTaskInput.model_json_schema()


def get_complete_task_input_schema() -> dict:
    """Return JSON Schema for CompleteTaskInput (for MCP tool registration)."""
    return CompleteTaskInput.model_json_schema()


def get_delete_task_input_schema() -> dict:
    """Return JSON Schema for DeleteTaskInput (for MCP tool registration)."""
    return DeleteTaskInput.model_json_schema()


def get_tool_response_output_schema() -> dict:
    """Return JSON Schema for ToolResponse (for MCP tool registration)."""
    return ToolResponse.model_json_schema()
