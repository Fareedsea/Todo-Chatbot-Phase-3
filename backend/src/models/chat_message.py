"""
ChatMessage SQLModel - Database entity for individual chat messages.

Each message belongs to exactly one conversation (enforced by foreign key).
Messages are either from the user or the AI assistant (role enforcement).
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from .conversation import Conversation


class MessageRole(str, Enum):
    """
    Enum for message sender role.

    Values:
        USER: Message sent by the user
        ASSISTANT: Message sent by the AI assistant
    """
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(SQLModel, table=True):
    """
    ChatMessage entity representing a single message in a conversation.

    Attributes:
        id: Unique identifier (auto-increment), primary key
        conversation_id: Foreign key to conversations table (parent), indexed for query performance
        role: Message sender role (enum: 'user' or 'assistant')
        content: Message text content (required, 1-10000 characters)
        created_at: Creation timestamp (UTC, immutable)

    Relationships:
        conversation: Conversation object this message belongs to

    Constraints:
        - conversation_id references conversations.id with CASCADE delete
        - role must be either 'user' or 'assistant' (enum enforcement)
        - content must be between 1 and 10,000 characters (validated by database CHECK)
        - created_at is immutable (never updated)
        - Composite index on (conversation_id, created_at) for fast ordered retrieval

    Security:
        Backend MUST verify conversation ownership (via conversation.user_id) before allowing access.
        Message content MUST be sanitized to prevent XSS (remove HTML/script tags).

    Validation Rules:
        - User messages must not be empty (min 1 character)
        - Assistant messages must not be empty (min 1 character)
        - Maximum 10,000 characters to prevent abuse
        - No HTML/script tags allowed in content (sanitized on input)

    Query Patterns:
        - Fetch all messages for a conversation:
          SELECT * FROM chat_messages WHERE conversation_id = ? ORDER BY created_at ASC
        - Fetch last N messages:
          SELECT * FROM chat_messages WHERE conversation_id = ? ORDER BY created_at DESC LIMIT N
    """

    __tablename__ = "chat_messages"

    # Primary Key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        index=True,
        description="Unique message identifier (auto-increment)"
    )

    # Foreign Key (Parent Conversation)
    conversation_id: str = Field(
        foreign_key="conversations.id",
        index=True,
        description="Parent conversation ID (references conversations.id)"
    )

    # Message Fields
    role: MessageRole = Field(
        description="Message sender role: 'user' or 'assistant'"
    )

    content: str = Field(
        min_length=1,
        max_length=10000,
        description="Message text content (1-10000 characters)"
    )

    # Timestamp
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Message creation timestamp (UTC, immutable)"
    )

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
