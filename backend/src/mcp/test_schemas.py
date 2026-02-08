"""
Schema Validation Tests (Optional)

Quick validation script to verify Pydantic schemas work correctly.
Run with: python -m pytest backend/src/mcp/test_schemas.py
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from .schemas import (
    AddTaskInput,
    ListTasksInput,
    UpdateTaskInput,
    CompleteTaskInput,
    DeleteTaskInput,
    ToolResponse,
    ToolError,
    TaskOutput,
    create_success_response,
    create_error_response,
)


class TestAddTaskInput:
    """Test AddTaskInput validation."""

    def test_valid_input(self):
        """Valid input should pass validation."""
        data = AddTaskInput(title="Buy groceries", user_id=123)
        assert data.title == "Buy groceries"
        assert data.user_id == 123

    def test_title_too_short(self):
        """Empty title should fail validation."""
        with pytest.raises(ValidationError):
            AddTaskInput(title="", user_id=123)

    def test_title_too_long(self):
        """Title over 500 chars should fail validation."""
        with pytest.raises(ValidationError):
            AddTaskInput(title="x" * 501, user_id=123)

    def test_title_whitespace_only(self):
        """Whitespace-only title should fail validation."""
        with pytest.raises(ValidationError):
            AddTaskInput(title="   ", user_id=123)

    def test_title_trimmed(self):
        """Title should be trimmed of leading/trailing whitespace."""
        data = AddTaskInput(title="  Buy groceries  ", user_id=123)
        assert data.title == "Buy groceries"

    def test_user_id_required(self):
        """user_id is required."""
        with pytest.raises(ValidationError):
            AddTaskInput(title="Buy groceries")  # type: ignore

    def test_user_id_positive(self):
        """user_id must be positive."""
        with pytest.raises(ValidationError):
            AddTaskInput(title="Buy groceries", user_id=0)


class TestListTasksInput:
    """Test ListTasksInput validation."""

    def test_valid_input_no_filter(self):
        """Valid input without filter should pass."""
        data = ListTasksInput(user_id=123)
        assert data.user_id == 123
        assert data.completed is None

    def test_valid_input_with_filter(self):
        """Valid input with completed filter should pass."""
        data = ListTasksInput(user_id=123, completed=True)
        assert data.user_id == 123
        assert data.completed is True


class TestUpdateTaskInput:
    """Test UpdateTaskInput validation."""

    def test_valid_input(self):
        """Valid input should pass validation."""
        data = UpdateTaskInput(task_id=42, title="Updated title", user_id=123)
        assert data.task_id == 42
        assert data.title == "Updated title"
        assert data.user_id == 123

    def test_title_validation(self):
        """Title validation should work."""
        with pytest.raises(ValidationError):
            UpdateTaskInput(task_id=42, title="", user_id=123)


class TestCompleteTaskInput:
    """Test CompleteTaskInput validation."""

    def test_valid_input(self):
        """Valid input should pass validation."""
        data = CompleteTaskInput(task_id=42, user_id=123)
        assert data.task_id == 42
        assert data.user_id == 123


class TestDeleteTaskInput:
    """Test DeleteTaskInput validation."""

    def test_valid_input(self):
        """Valid input should pass validation."""
        data = DeleteTaskInput(task_id=42, user_id=123)
        assert data.task_id == 42
        assert data.user_id == 123


class TestToolError:
    """Test ToolError schema."""

    def test_valid_error(self):
        """Valid error should serialize correctly."""
        error = ToolError(code="NOT_FOUND", message="Task not found")
        assert error.code == "NOT_FOUND"
        assert error.message == "Task not found"


class TestTaskOutput:
    """Test TaskOutput schema."""

    def test_valid_task(self):
        """Valid task should serialize correctly."""
        now = datetime.now()
        task = TaskOutput(
            id=42,
            title="Buy groceries",
            completed=False,
            created_at=now
        )
        assert task.id == 42
        assert task.title == "Buy groceries"
        assert task.completed is False
        assert task.created_at == now


class TestToolResponse:
    """Test ToolResponse schema."""

    def test_success_response(self):
        """Success response should have data."""
        response = ToolResponse(
            success=True,
            data={"task": {"id": 42, "title": "Buy groceries"}},
            error=None
        )
        assert response.success is True
        assert response.data is not None
        assert response.error is None

    def test_error_response(self):
        """Error response should have error."""
        error = ToolError(code="NOT_FOUND", message="Task not found")
        response = ToolResponse(
            success=False,
            data=None,
            error=error
        )
        assert response.success is False
        assert response.data is None
        assert response.error is not None


class TestUtilityFunctions:
    """Test utility functions."""

    def test_create_success_response(self):
        """create_success_response should return proper structure."""
        response = create_success_response({"task": {"id": 42}})
        assert response["success"] is True
        assert response["data"] == {"task": {"id": 42}}
        assert response["error"] is None

    def test_create_error_response(self):
        """create_error_response should return proper structure."""
        response = create_error_response("NOT_FOUND", "Task not found")
        assert response["success"] is False
        assert response["data"] is None
        assert response["error"]["code"] == "NOT_FOUND"
        assert response["error"]["message"] == "Task not found"
