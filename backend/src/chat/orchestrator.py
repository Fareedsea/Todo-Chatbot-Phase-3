"""
Chat Request Orchestration.

Coordinates the full chat request lifecycle:
1. Create or fetch conversation
2. Fetch conversation history
3. Invoke AI agent
4. Persist user message and assistant response
5. Return response to client
"""

import logging
from typing import Dict, Any, Optional

from .agent import get_agent
from .history import (
    fetch_conversation_history,
    create_conversation,
    persist_user_message,
    persist_assistant_message
)

logger = logging.getLogger(__name__)


def process_chat_message(
    user_message: str,
    user_id: str,
    conversation_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Process a chat message through the full orchestration lifecycle.

    This is the main entry point for chat requests. It handles:
    - Conversation creation (if needed)
    - History fetching
    - AI agent invocation
    - Message persistence
    - Error handling

    Args:
        user_message: User's message text (1-1000 characters)
        user_id: Authenticated user ID from JWT
        conversation_id: Existing conversation ID, or None to create new

    Returns:
        Dictionary with:
            - success (bool): True if processed successfully
            - message (str): Assistant's response
            - conversation_id (str): Conversation ID (new or existing)
            - error (str|None): Error message if failed

    Example:
        result = process_chat_message(
            "Add buy groceries to my list",
            "user-uuid-123",
            None  # Create new conversation
        )
        # Returns: {
        #   "success": True,
        #   "message": "I've added 'buy groceries' to your todo list",
        #   "conversation_id": "conv-uuid-456",
        #   "error": None
        # }
    """
    try:
        # Step 1: Create or validate conversation
        if not conversation_id:
            logger.info(f"Creating new conversation for user {user_id}")
            conversation_id = create_conversation(user_id)

            if not conversation_id:
                return {
                    "success": False,
                    "message": "Failed to create conversation",
                    "conversation_id": "",
                    "error": "CONVERSATION_CREATE_FAILED"
                }

        # Step 2: Fetch conversation history (last 20 messages)
        history = fetch_conversation_history(
            conversation_id,
            user_id,
            limit=20
        )

        logger.info(
            f"Fetched {len(history)} messages for conversation {conversation_id}"
        )

        # Step 3: Invoke AI agent
        agent = get_agent()

        if not agent:
            return {
                "success": False,
                "message": "AI agent is not configured. Please set COHERE_API_KEY environment variable.",
                "conversation_id": conversation_id,
                "error": "AGENT_NOT_CONFIGURED"
            }

        agent_result = agent.invoke(
            user_message,
            history,
            user_id
        )

        assistant_message = agent_result.get("message", "")
        agent_error = agent_result.get("error")

        if agent_error:
            logger.error(f"Agent invocation error: {agent_error}")
            # Return error but still persist messages for debugging
            assistant_message = "I'm having trouble processing your request right now. Please try again in a moment."

        # Step 4: Persist messages to database
        # Persist user message
        user_persisted = persist_user_message(
            conversation_id,
            user_message,
            user_id
        )

        if not user_persisted:
            logger.warning(f"Failed to persist user message for conversation {conversation_id}")

        # Persist assistant response
        assistant_persisted = persist_assistant_message(
            conversation_id,
            assistant_message,
            user_id
        )

        if not assistant_persisted:
            logger.warning(f"Failed to persist assistant message for conversation {conversation_id}")

        # Step 5: Return response
        return {
            "success": True,
            "message": assistant_message,
            "conversation_id": conversation_id,
            "error": agent_error
        }

    except Exception as e:
        logger.error(f"Chat orchestration error: {str(e)}", exc_info=True)
        # Ensure conversation_id is never None in the response
        safe_conversation_id = conversation_id or ""
        return {
            "success": False,
            "message": "An unexpected error occurred. Please try again.",
            "conversation_id": safe_conversation_id,
            "error": str(e)
        }


def handle_chat_request(
    message: str,
    user_id: str,
    conversation_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Public API for handling chat requests.

    Validates input and delegates to process_chat_message.

    Args:
        message: User message (1-1000 characters)
        user_id: Authenticated user ID
        conversation_id: Optional existing conversation ID

    Returns:
        Dictionary with success, message, conversation_id, error

    Raises:
        ValueError: If message is empty or too long
    """
    # Validate message
    if not message or not message.strip():
        raise ValueError("Message cannot be empty")

    if len(message) > 1000:
        raise ValueError("Message too long (max 1000 characters)")

    # Sanitize message (trim whitespace)
    message = message.strip()

    # Process through orchestration
    return process_chat_message(message, user_id, conversation_id)
