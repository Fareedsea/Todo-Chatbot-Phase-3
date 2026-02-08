"""
Pydantic schemas for task API requests and responses.

Defines validation rules and camelCase field aliases matching frontend API contracts.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, date


class TaskCreate(BaseModel):
    """
    Request schema for creating a new task.

    Validates field constraints per spec (FR-024 to FR-027).
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title (required, 1-200 characters)",
        examples=["Buy groceries"]
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional detailed description (max 1000 characters)",
        examples=["Milk, eggs, bread"]
    )

    due_date: Optional[date] = Field(
        default=None,
        description="Optional deadline (ISO date format YYYY-MM-DD)",
        examples=["2026-02-10"],
        alias="dueDate"  # Accept camelCase from frontend
    )

    is_completed: bool = Field(
        default=False,
        description="Completion status (defaults to false)",
        alias="isCompleted"  # Accept camelCase from frontend
    )

    class Config:
        populate_by_name = True  # Accept both snake_case and camelCase


class TaskUpdate(BaseModel):
    """
    Request schema for updating an existing task.

    All fields optional for partial updates (FR-034).
    """
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Updated task title",
        examples=["Buy groceries"]
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Updated description",
        examples=["Milk, eggs, bread, butter"]
    )

    due_date: Optional[date] = Field(
        default=None,
        description="Updated deadline (ISO date format)",
        examples=["2026-02-15"],
        alias="dueDate"
    )

    is_completed: Optional[bool] = Field(
        default=None,
        description="Updated completion status",
        alias="isCompleted"
    )

    class Config:
        populate_by_name = True

    @field_validator("title", "description", "due_date", "is_completed")
    @classmethod
    def at_least_one_field(cls, v, info):
        """
        Validate that at least one field is provided (FR-031).
        This is checked in the endpoint handler.
        """
        return v


class TaskResponse(BaseModel):
    """
    Response schema for task objects.

    Returns camelCase field names matching frontend API contracts (FR-062, FR-063).
    Timestamps formatted as ISO 8601 with UTC timezone (FR-064).
    """
    id: str = Field(
        ...,
        description="Unique task identifier (UUID)"
    )

    title: str = Field(
        ...,
        description="Task title"
    )

    description: Optional[str] = Field(
        ...,
        description="Task description (null if not set)",
        alias="description"
    )

    due_date: Optional[date] = Field(
        ...,
        description="Task deadline (null if not set)",
        alias="dueDate"
    )

    is_completed: bool = Field(
        ...,
        description="Completion status",
        alias="isCompleted"
    )

    created_at: datetime = Field(
        ...,
        description="Creation timestamp (ISO 8601 UTC)",
        alias="createdAt"
    )

    updated_at: datetime = Field(
        ...,
        description="Last update timestamp (ISO 8601 UTC)",
        alias="updatedAt"
    )

    user_id: str = Field(
        ...,
        description="Owner's user ID",
        alias="userId"
    )

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility
        populate_by_name = True  # Support both snake_case and camelCase
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ") if v else None,
            date: lambda v: v.strftime("%Y-%m-%d") if v else None
        }


class TaskListResponse(BaseModel):
    """
    Response schema for task list endpoint (GET /api/tasks).

    Returns array of tasks wrapped in "tasks" field per API contract.
    """
    tasks: list[TaskResponse] = Field(
        ...,
        description="Array of task objects"
    )


class TaskSingleResponse(BaseModel):
    """
    Response schema for single task endpoints (GET/POST/PUT /api/tasks/:id).

    Returns single task wrapped in "task" field per API contract.
    """
    task: TaskResponse = Field(
        ...,
        description="Task object"
    )


class TaskDeleteResponse(BaseModel):
    """
    Response schema for task deletion (DELETE /api/tasks/:id).
    """
    message: str = Field(
        default="Task deleted successfully",
        description="Success confirmation message"
    )
