"""
User SQLModel - Database entity for user accounts.

Stores authentication credentials with secure password hashing.
Each user can own zero or more tasks.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .conversation import Conversation


class User(SQLModel, table=True):
    """
    User entity representing an authenticated account.

    Attributes:
        id: Unique identifier (UUID), primary key
        email: User's email address (unique, used for login)
        password_hash: Bcrypt-hashed password (never stores plaintext)
        created_at: Account creation timestamp (UTC, immutable)

    Relationships:
        tasks: List of Task objects owned by this user (cascade delete)
        conversations: List of Conversation objects owned by this user (cascade delete)

    Constraints:
        - email MUST be unique (enforced by database index)
        - password_hash MUST never be exposed in API responses
        - created_at is immutable (set once on creation)
    """

    __tablename__ = "users"

    # Primary Key
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        description="Unique user identifier (UUID)"
    )

    # Authentication Fields
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="User's email address (RFC 5322 format)"
    )

    password_hash: str = Field(
        max_length=255,
        description="Bcrypt-hashed password (never plaintext)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp (UTC, immutable)"
    )

    # Relationships
    tasks: List["Task"] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    conversations: List["Conversation"] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
