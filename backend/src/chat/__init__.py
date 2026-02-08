"""
Chat Module for AI Chatbot Integration (Phase III).

Provides AI agent orchestration, conversation history management, and chat request lifecycle.
"""

from .agent import get_agent, ChatAgent, SYSTEM_PROMPT
from .tools import get_tool_definitions, map_tool_response_to_message

__all__ = [
    "get_agent",
    "ChatAgent",
    "SYSTEM_PROMPT",
    "get_tool_definitions",
    "map_tool_response_to_message"
]
