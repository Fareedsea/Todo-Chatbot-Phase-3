"""
Task SQLModel - Database entity for todo items.

Each task belongs to exactly one user (enforced by foreign key).
Tasks are automatically deleted when their owner is deleted (cascade).
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, date
import uuid


class Task(SQLModel, table=True):
    """
    Task entity representing a todo item owned by a user.

    Attributes:
        id: Unique identifier (UUID), primary key
        user_id: Foreign key to users table (owner), indexed for query performance
        title: Task title (required, 1-200 characters)
        description: Optional detailed description (max 1000 characters)
        due_date: Optional deadline (ISO date format)
        is_completed: Completion status (boolean, defaults to false)
        created_at: Creation timestamp (UTC, immutable)
        updated_at: Last modification timestamp (UTC, auto-updated)

    Relationships:
        owner: User object who owns this task

    Constraints:
        - user_id references users.id with CASCADE delete
        - All queries MUST filter by authenticated user's ID (security requirement)
        - created_at is immutable (never updated)
        - updated_at is refreshed on every modification

    Security:
        Backend MUST verify task ownership before allowing access/modification.
        Never trust user_id from request; always extract from JWT token.
    """

    __tablename__ = "tasks"

    # Primary Key
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        description="Unique task identifier (UUID)"
    )

    # Foreign Key (Owner)
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        description="Owner's user ID (references users.id)"
    )

    # Task Fields
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title (required, 1-200 characters)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional detailed description (max 1000 characters)"
    )

    due_date: Optional[date] = Field(
        default=None,
        description="Optional deadline (ISO date format YYYY-MM-DD)"
    )

    is_completed: bool = Field(
        default=False,
        description="Completion status (true/false)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC, immutable)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last modification timestamp (UTC, auto-updated)"
    )

    # Relationships
    owner: "User" = Relationship(back_populates="tasks")
