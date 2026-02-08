"""
Chat API endpoints for AI chatbot integration.

Provides conversational interface for task management using natural language.
All endpoints require JWT authentication and enforce user data isolation.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import Session
import logging

from ..auth.dependencies import get_current_user
from ..database import get_session
from ..errors import raise_unauthorized, raise_bad_request
from ..chat.orchestrator import handle_chat_request

router = APIRouter(prefix="/api/chat", tags=["chat"])
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    """
    Request schema for chat message.

    Fields:
        message: User's natural language message (1-1000 characters)
        conversation_id: Optional conversation ID to continue existing conversation
    """
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID (optional)")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Add buy groceries to my todo list",
                "conversation_id": "conv-uuid-123"
            }
        }


class ChatResponse(BaseModel):
    """
    Response schema for chat message.

    Fields:
        message: Assistant's response message
        conversation_id: Conversation ID for this exchange
        task_action: Optional action performed (create, list, update, complete, delete)
    """
    message: str = Field(..., description="Assistant response")
    conversation_id: str = Field(..., description="Conversation ID")
    task_action: Optional[str] = Field(None, description="Task action performed")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "I've added 'buy groceries' to your todo list",
                "conversation_id": "conv-uuid-123",
                "task_action": "create"
            }
        }


@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def send_chat_message(
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Send a message to the AI chatbot.

    Processes natural language input and performs task operations via MCP tools.
    Creates new conversation if conversation_id not provided.

    Args:
        request: Chat message request
        current_user_id: Authenticated user ID from JWT (auto-injected)
        session: Database session (auto-injected)

    Returns:
        ChatResponse with assistant's reply and conversation ID

    Raises:
        HTTPException 401: Invalid or missing authentication token
        HTTPException 400: Empty message or invalid conversation_id
        HTTPException 500: AI agent or MCP tool error

    Security:
        - JWT authentication required (enforced by get_current_user dependency)
        - User can only access their own conversations
        - user_id passed to MCP tools for data isolation

    Example:
        POST /api/chat
        Authorization: Bearer eyJhbGci...
        {
            "message": "Add buy groceries to my list",
            "conversation_id": null
        }

        Response:
        {
            "message": "I've added 'buy groceries' to your todo list",
            "conversation_id": "conv-uuid-123",
            "task_action": "create"
        }
    """
    # Validate message not empty (additional check beyond Pydantic)
    if not request.message.strip():
        raise_bad_request("Message cannot be empty")

    # Process chat message through orchestration
    try:
        result = handle_chat_request(
            message=request.message,
            user_id=current_user_id,
            conversation_id=request.conversation_id
        )

        if not result["success"]:
            # Log error but return friendly message to user
            logger.error(f"Chat processing failed: {result.get('error')}")

        # Return response
        return ChatResponse(
            message=result["message"],
            conversation_id=result["conversation_id"],
            task_action=None  # TODO: Extract from agent tool_calls in future enhancement
        )

    except ValueError as e:
        # Input validation error
        raise_bad_request(str(e))

    except Exception as e:
        # Unexpected error
        logger.error(f"Chat endpoint error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred processing your message"
        )


@router.get("/health", status_code=status.HTTP_200_OK)
async def chat_health_check():
    """
    Health check endpoint for chat service.

    Verifies chat API is accessible and ready.
    Does not require authentication.

    Returns:
        {"status": "ok", "service": "chat"}

    Example:
        GET /api/chat/health

        Response:
        {
            "status": "ok",
            "service": "chat"
        }
    """
    return {"status": "ok", "service": "chat"}
