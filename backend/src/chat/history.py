"""
Conversation History Management.

Handles fetching conversation history from database and persisting new messages.
All operations enforce user ownership for data isolation.
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime
from sqlmodel import Session, select
import uuid

from ..database import engine
from ..models.conversation import Conversation
from ..models.chat_message import ChatMessage

logger = logging.getLogger(__name__)


def fetch_conversation_history(
    conversation_id: str,
    user_id: str,
    limit: int = 20
) -> List[Dict[str, str]]:
    """
    Fetch conversation history for authenticated user.

    Retrieves last N messages from the specified conversation, ordered chronologically.
    Enforces user ownership - only returns messages from user's conversations.

    Args:
        conversation_id: Conversation UUID
        user_id: Authenticated user ID (from JWT)
        limit: Maximum number of messages to retrieve (default: 20)

    Returns:
        List of message dictionaries:
            [{"role": "user"|"assistant", "content": "message text"}, ...]

    Security:
        - Verifies conversation belongs to user_id before fetching messages
        - Returns empty list if conversation doesn't exist or belongs to another user

    Example:
        history = fetch_conversation_history("conv-123", "user-456", limit=20)
        # Returns: [
        #   {"role": "user", "content": "Add buy groceries"},
        #   {"role": "assistant", "content": "I've added 'buy groceries'..."}
        # ]
    """
    try:
        with Session(engine) as session:
            # Verify conversation exists and belongs to user
            conversation = session.exec(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
            ).first()

            if not conversation:
                logger.warning(
                    f"Conversation {conversation_id} not found for user {user_id}"
                )
                return []

            # Fetch last N messages ordered by created_at
            messages = session.exec(
                select(ChatMessage)
                .where(ChatMessage.conversation_id == conversation_id)
                .order_by(ChatMessage.created_at.asc())
                .limit(limit)
            ).all()

            # Convert to format expected by AI agent
            history = [
                {
                    "role": msg.role,
                    "content": msg.content
                }
                for msg in messages
            ]

            logger.info(
                f"Fetched {len(history)} messages for conversation {conversation_id}"
            )
            return history

    except Exception as e:
        logger.error(f"Error fetching conversation history: {str(e)}", exc_info=True)
        return []


def create_conversation(user_id: str) -> Optional[str]:
    """
    Create a new conversation for user.

    Args:
        user_id: Authenticated user ID

    Returns:
        Conversation ID (UUID) if created successfully, None on error

    Example:
        conversation_id = create_conversation("user-uuid-123")
        # Returns: "conv-uuid-456"
    """
    try:
        with Session(engine) as session:
            conversation = Conversation(
                user_id=user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

            logger.info(f"Created conversation {conversation.id} for user {user_id}")
            return conversation.id

    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}", exc_info=True)
        return None


def persist_message(
    conversation_id: str,
    role: str,
    content: str,
    user_id: str
) -> bool:
    """
    Persist a message to the database.

    Saves user or assistant message and updates conversation timestamp.
    Enforces user ownership - only persists to user's conversations.

    Args:
        conversation_id: Conversation UUID
        role: Message role ("user" or "assistant")
        content: Message text (1-10000 characters)
        user_id: Authenticated user ID (for ownership verification)

    Returns:
        True if message persisted successfully, False on error

    Security:
        - Verifies conversation belongs to user_id before persisting
        - Validates role is either "user" or "assistant"
        - Sanitizes content length (max 10,000 characters)

    Example:
        success = persist_message(
            "conv-123",
            "user",
            "Add buy groceries",
            "user-456"
        )
    """
    try:
        # Validate role
        if role not in ["user", "assistant"]:
            logger.error(f"Invalid role: {role}")
            return False

        # Validate content length
        if not content or len(content) > 10000:
            logger.error(f"Invalid content length: {len(content)}")
            return False

        with Session(engine) as session:
            # Verify conversation exists and belongs to user
            conversation = session.exec(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
            ).first()

            if not conversation:
                logger.error(
                    f"Conversation {conversation_id} not found for user {user_id}"
                )
                return False

            # Create and save message
            message = ChatMessage(
                id=str(uuid.uuid4()),
                conversation_id=conversation_id,
                role=role,
                content=content,
                created_at=datetime.utcnow()
            )
            session.add(message)

            # Update conversation timestamp
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)

            session.commit()

            logger.info(
                f"Persisted {role} message to conversation {conversation_id}"
            )
            return True

    except Exception as e:
        logger.error(f"Error persisting message: {str(e)}", exc_info=True)
        return False


def persist_user_message(
    conversation_id: str,
    content: str,
    user_id: str
) -> bool:
    """
    Convenience wrapper for persisting user messages.

    Args:
        conversation_id: Conversation UUID
        content: User message text
        user_id: Authenticated user ID

    Returns:
        True if persisted successfully
    """
    return persist_message(conversation_id, "user", content, user_id)


def persist_assistant_message(
    conversation_id: str,
    content: str,
    user_id: str
) -> bool:
    """
    Convenience wrapper for persisting assistant messages.

    Args:
        conversation_id: Conversation UUID
        content: Assistant response text
        user_id: Authenticated user ID

    Returns:
        True if persisted successfully
    """
    return persist_message(conversation_id, "assistant", content, user_id)
