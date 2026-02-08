"""
Task management API endpoints.

Provides CRUD operations for tasks with strict user isolation.
All endpoints require JWT authentication and filter by authenticated user ID.
"""

from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from datetime import datetime

from ..database import get_session
from ..models.task import Task
from ..schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    TaskSingleResponse,
    TaskDeleteResponse
)
from ..auth.dependencies import get_current_user
from ..errors import raise_not_found, raise_forbidden, raise_bad_request

router = APIRouter()


@router.get(
    "",
    response_model=TaskListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all tasks",
    description="Retrieve all tasks for authenticated user. Returns empty array if no tasks."
)
async def get_tasks(
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskListResponse:
    """
    Retrieve all tasks for authenticated user.

    Requirements (from spec FR-017 to FR-019):
    - FR-017: Accept GET /api/tasks
    - FR-018: Filter all queries by authenticated user ID from JWT
    - FR-019: Return empty array when user has no tasks (200, not 404)

    Security (CRITICAL):
    - User isolation enforced: WHERE user_id = authenticated_user_id
    - Never trust user_id from request; always use JWT claim

    Request Headers:
        Authorization: Bearer <jwt_token>

    Success Response (200):
        {
            "tasks": [
                {
                    "id": "task-uuid-1",
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread",
                    "dueDate": "2026-02-10",
                    "isCompleted": false,
                    "createdAt": "2026-02-04T10:00:00Z",
                    "updatedAt": "2026-02-04T10:00:00Z",
                    "userId": "user-uuid-123"
                }
            ]
        }

    Empty Response (200):
        {
            "tasks": []
        }

    Error Responses:
        401: Missing or invalid JWT token
        500: Server error
    """
    # Query tasks filtered by authenticated user (FR-018)
    statement = select(Task).where(Task.user_id == current_user_id)
    tasks = session.exec(statement).all()

    # Return tasks (empty array if none - FR-019)
    return TaskListResponse(
        tasks=[TaskResponse.model_validate(task) for task in tasks]
    )


@router.get(
    "/{task_id}",
    response_model=TaskSingleResponse,
    status_code=status.HTTP_200_OK,
    summary="Get specific task",
    description="Retrieve single task by ID. Returns 403/404 if not owned by authenticated user."
)
async def get_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskSingleResponse:
    """
    Retrieve specific task by ID.

    Requirements (from spec FR-020 to FR-022):
    - FR-020: Accept GET /api/tasks/:id
    - FR-021: Return 404 for non-existent task IDs
    - FR-022: Return 403 or 404 when user attempts to access another user's task

    Security (CRITICAL):
    - Verify task ownership before returning
    - Filter by authenticated user ID from JWT

    Request Headers:
        Authorization: Bearer <jwt_token>

    Success Response (200):
        {
            "task": {
                "id": "task-uuid-1",
                "title": "Buy groceries",
                ...
            }
        }

    Error Responses:
        401: Missing or invalid JWT token
        403: Task belongs to different user (access denied)
        404: Task not found
        500: Server error
    """
    # Query task with user ownership filter (FR-018)
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user_id  # User isolation
    )
    task = session.exec(statement).first()

    if not task:
        # Task doesn't exist or belongs to different user (FR-021, FR-022)
        raise_not_found("Task not found")

    return TaskSingleResponse(
        task=TaskResponse.model_validate(task)
    )


@router.post(
    "",
    response_model=TaskSingleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new task",
    description="Create a new task for authenticated user. Returns created task with generated ID and timestamps."
)
async def create_task(
    request: TaskCreate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskSingleResponse:
    """
    Create a new task.

    Requirements (from spec FR-023 to FR-032):
    - FR-023: Accept POST /api/tasks with JSON body
    - FR-024: Validate title (1-200 characters, non-empty)
    - FR-025: Validate description (null or 0-1000 characters)
    - FR-026: Validate dueDate (null or ISO 8601 date)
    - FR-027: Validate isCompleted (boolean, defaults to false)
    - FR-028: Return 400 for missing title
    - FR-029: Return 422 for validation failures
    - FR-030: Generate UUID and set user_id from JWT
    - FR-031: Set createdAt and updatedAt to current UTC time
    - FR-032: Return 201 with created task

    Security (CRITICAL):
    - Set user_id from JWT (never from request body)
    - User can only create tasks for themselves

    Request Headers:
        Authorization: Bearer <jwt_token>

    Request Body:
        {
            "title": "New task",
            "description": "Optional description",
            "dueDate": "2026-02-15",
            "isCompleted": false
        }

    Success Response (201):
        {
            "task": {
                "id": "task-uuid-new",
                "title": "New task",
                "description": "Optional description",
                "dueDate": "2026-02-15",
                "isCompleted": false,
                "createdAt": "2026-02-04T11:30:00Z",
                "updatedAt": "2026-02-04T11:30:00Z",
                "userId": "user-uuid-123"
            }
        }

    Error Responses:
        400: Missing title field
        401: Missing or invalid JWT token
        422: Validation failure (title too long, etc.)
        500: Server error
    """
    # Validate title is present (Pydantic handles this, but explicit check for clarity)
    if not request.title or not request.title.strip():
        raise_bad_request("Title is required")

    # Create new task with authenticated user as owner (FR-030)
    new_task = Task(
        user_id=current_user_id,  # CRITICAL: Set from JWT, not request
        title=request.title,
        description=request.description,
        due_date=request.due_date,
        is_completed=request.is_completed,
        created_at=datetime.utcnow(),  # FR-031
        updated_at=datetime.utcnow()   # FR-031
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    # Return created task (FR-032)
    return TaskSingleResponse(
        task=TaskResponse.model_validate(new_task)
    )


@router.put(
    "/{task_id}",
    response_model=TaskSingleResponse,
    status_code=status.HTTP_200_OK,
    summary="Update existing task",
    description="Update task fields. Only provided fields are updated (partial updates supported)."
)
async def update_task(
    task_id: str,
    request: TaskUpdate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskSingleResponse:
    """
    Update existing task.

    Requirements (from spec FR-033 to FR-038):
    - FR-033: Accept PUT /api/tasks/:id
    - FR-034: Allow partial updates (only include fields to change)
    - FR-035: Verify task ownership (403 or 404 if not owner)
    - FR-036: Refresh updatedAt timestamp
    - FR-037: Preserve createdAt timestamp (immutable)
    - FR-038: Return 200 with updated task

    Security (CRITICAL):
    - Verify task ownership before allowing update
    - User can only update their own tasks

    Request Headers:
        Authorization: Bearer <jwt_token>

    Request Body (partial update example):
        {
            "isCompleted": true
        }

    Success Response (200):
        {
            "task": {
                "id": "task-uuid-1",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "dueDate": "2026-02-10",
                "isCompleted": true,
                "createdAt": "2026-02-04T10:00:00Z",
                "updatedAt": "2026-02-04T12:15:00Z",
                "userId": "user-uuid-123"
            }
        }

    Error Responses:
        400: No fields to update
        401: Missing or invalid JWT token
        403: Task belongs to different user
        404: Task not found
        422: Validation failure
        500: Server error
    """
    # Query task with ownership filter (FR-035)
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user_id  # User isolation
    )
    task = session.exec(statement).first()

    if not task:
        # Task doesn't exist or belongs to different user
        raise_not_found("Task not found")

    # Check that at least one field is provided (FR-034)
    update_data = request.model_dump(exclude_unset=True)
    if not update_data:
        raise_bad_request("At least one field required")

    # Apply partial updates (FR-034)
    for field, value in update_data.items():
        setattr(task, field, value)

    # Refresh updatedAt timestamp (FR-036)
    task.updated_at = datetime.utcnow()

    # createdAt is immutable (FR-037) - never updated

    session.add(task)
    session.commit()
    session.refresh(task)

    # Return updated task (FR-038)
    return TaskSingleResponse(
        task=TaskResponse.model_validate(task)
    )


@router.delete(
    "/{task_id}",
    response_model=TaskDeleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete task",
    description="Permanently delete task. Returns success message."
)
async def delete_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskDeleteResponse:
    """
    Delete task permanently.

    Requirements (from spec FR-039 to FR-042):
    - FR-039: Accept DELETE /api/tasks/:id
    - FR-040: Verify task ownership (403 or 404 if not owner)
    - FR-041: Permanently delete from database
    - FR-042: Return 200 with success message

    Security (CRITICAL):
    - Verify task ownership before allowing deletion
    - User can only delete their own tasks

    Request Headers:
        Authorization: Bearer <jwt_token>

    Success Response (200):
        {
            "message": "Task deleted successfully"
        }

    Error Responses:
        401: Missing or invalid JWT token
        403: Task belongs to different user
        404: Task not found
        500: Server error
    """
    # Query task with ownership filter (FR-040)
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user_id  # User isolation
    )
    task = session.exec(statement).first()

    if not task:
        # Task doesn't exist or belongs to different user
        raise_not_found("Task not found")

    # Permanently delete task (FR-041)
    session.delete(task)
    session.commit()

    # Return success message (FR-042)
    return TaskDeleteResponse(message="Task deleted successfully")
