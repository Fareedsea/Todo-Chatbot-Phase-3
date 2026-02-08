"""
Conversation SQLModel - Database entity for AI chatbot chat sessions.

Each conversation belongs to exactly one user (enforced by foreign key).
Conversations contain multiple chat messages and track when they were last active.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .user import User
    from .chat_message import ChatMessage


class Conversation(SQLModel, table=True):
    """
    Conversation entity representing a chat session between a user and the AI assistant.

    Attributes:
        id: Unique identifier (auto-increment), primary key
        user_id: Foreign key to users table (owner), indexed for query performance
        created_at: Creation timestamp (UTC, immutable)
        updated_at: Last modification timestamp (UTC, auto-updated on new messages)

    Relationships:
        owner: User object who owns this conversation
        messages: List of ChatMessage objects in this conversation (cascade delete)

    Constraints:
        - user_id references users.id with CASCADE delete
        - All queries MUST filter by authenticated user's ID (security requirement)
        - created_at is immutable (never updated)
        - updated_at is refreshed when new messages are added

    Security:
        Backend MUST verify conversation ownership before allowing access.
        Never trust user_id or conversation_id from request; always extract user_id from JWT token.

    State Transitions:
        - Created when user sends first message in new conversation
        - Updated timestamp modified on every new message (user or assistant)
        - No explicit "closed" state - conversations remain open indefinitely
    """

    __tablename__ = "conversations"

    # Primary Key
    id: str = Field(
        default_factory=lambda: str(__import__('uuid').uuid4()),
        primary_key=True,
        index=True,
        description="Unique conversation identifier (UUID)",
        max_length=36  # UUID length
    )

    # Foreign Key (Owner)
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        max_length=36,
        description="Owner's user ID (references users.id)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Conversation creation timestamp (UTC, immutable)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last message timestamp (UTC, auto-updated)"
    )

    # Relationships
    owner: "User" = Relationship(back_populates="conversations")
    messages: List["ChatMessage"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
