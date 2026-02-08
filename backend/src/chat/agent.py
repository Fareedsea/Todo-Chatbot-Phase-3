"""
AI Agent Configuration for Chat Orchestration.

Uses OpenAI SDK configured to route requests through Cohere API.
Agent is configured with system prompt for tool-only behavior and MCP tool access.
"""

import logging
from typing import Dict, Any, List
import json
from openai import OpenAI

from ..config import settings
from ..mcp.server import get_mcp_server
from .tools import get_tool_definitions, map_tool_response_to_message

logger = logging.getLogger(__name__)

# System prompt defining agent behavior
SYSTEM_PROMPT = """You are a helpful AI assistant for a todo list application. Your role is to help users manage their tasks through natural conversation.

**CRITICAL RULES - YOU MUST FOLLOW THESE:**

1. TOOL-ONLY BEHAVIOR:
   - You can ONLY interact with tasks through the provided tools: add_task, list_tasks, update_task, complete_task, delete_task
   - NEVER fabricate, guess, or hallucinate task data
   - NEVER claim to have created, updated, or deleted a task unless you actually called the tool
   - If a tool call fails, acknowledge the failure honestly

2. USER CONFIRMATIONS:
   - Always provide friendly confirmations after successful operations
   - Example: "I've added 'buy groceries' to your todo list"
   - Example: "Here are your current tasks: [list]"
   - Be specific about what action was taken

3. CLARIFICATION REQUESTS:
   - When user intent is ambiguous, ask targeted clarifying questions
   - Example: User says "add something" → Ask "What would you like me to add to your todo list?"
   - Example: User says "delete it" without context → Ask "Which task would you like me to delete?"

4. DESTRUCTIVE ACTION CONFIRMATION:
   - For delete operations, always confirm first
   - Example: "Are you sure you want to delete '[task title]'? Reply 'yes' to confirm or 'no' to cancel."
   - Wait for explicit "yes"/"no" before executing

5. ERROR HANDLING:
   - Translate technical errors into user-friendly messages
   - Example: Instead of "NOT_FOUND", say "I couldn't find that task in your list"
   - Example: Instead of "DATABASE_ERROR", say "I'm having trouble accessing your tasks right now. Please try again in a moment."

6. SCOPE AWARENESS:
   - You ONLY manage todo tasks - nothing else
   - If user asks non-task questions, politely explain: "I'm here to help with your todo list. I can add tasks, show your list, mark tasks complete, update them, or delete them. What would you like to do?"

7. TASK REFERENCES:
   - Pay attention to context when users say "the first one", "that task", "it", etc.
   - Reference the conversation history to understand what task they mean
   - If unclear, list the tasks and ask which one they mean

**AVAILABLE TOOLS:**
- add_task: Create a new task with a title
- list_tasks: Show all tasks (optionally filter by completed status)
- update_task: Change a task's title
- complete_task: Mark a task as done
- delete_task: Remove a task (requires confirmation)

**CONVERSATION STYLE:**
- Be friendly, professional, and concise
- Use natural language, not robotic responses
- Acknowledge user's requests before executing
- Show empathy if operations fail

Remember: Your ONLY source of truth is the tools. Never assume or invent task data."""


class ChatAgent:
    """
    AI Agent wrapper for chat orchestration.

    Uses OpenAI SDK configured to route through Cohere API.
    Provides tool-calling capabilities via MCP tools.
    """

    def __init__(self):
        """
        Initialize chat agent with Cohere configuration.

        Raises:
            ValueError: If COHERE_API_KEY is not configured
        """
        if not settings.cohere_api_key:
            raise ValueError(
                "COHERE_API_KEY environment variable is required for AI chatbot. "
                "Please set it in your .env file."
            )

        # Initialize OpenAI client configured for Cohere
        # OpenAI SDK will send requests to Cohere's API endpoint
        self.client = OpenAI(
            api_key=settings.cohere_api_key,
            base_url="https://api.cohere.ai/v1"
        )

        self.model = settings.cohere_model
        self.mcp_server = get_mcp_server()

        logger.info(f"ChatAgent initialized with Cohere model: {self.model}")

    def build_messages(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """
        Build message array for agent invocation.

        Args:
            user_message: Current user message
            conversation_history: Previous messages from database
                Format: [{"role": "user"|"assistant", "content": "..."}]

        Returns:
            List of messages including system prompt, history, and current message
        """
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        # Add conversation history (last 20 messages from database)
        messages.extend(conversation_history)

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        return messages

    def invoke(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Invoke AI agent with user message and conversation context.

        Handles the full tool calling cycle:
        1. Build messages with system prompt and history
        2. Call OpenAI SDK (routed to Cohere) with tool definitions
        3. Execute any tool calls via MCP server
        4. Return final response to user

        Args:
            user_message: Current user message
            conversation_history: Previous conversation messages
            user_id: Authenticated user ID (injected into tool calls)

        Returns:
            Dictionary with:
                - message (str): Assistant's response
                - tool_calls (List[Dict]): Tools invoked (for logging)
                - error (str|None): Error message if invocation failed

        Example:
            result = agent.invoke(
                "Add buy groceries to my list",
                [],
                "user-uuid-123"
            )
            # Returns: {
            #   "message": "I've added 'buy groceries' to your todo list",
            #   "tool_calls": [{"tool": "add_task", "result": "success"}],
            #   "error": None
            # }
        """
        try:
            messages = self.build_messages(user_message, conversation_history)
            tools = get_tool_definitions()
            tool_calls_made = []

            logger.info(f"Agent invoked for user {user_id} with message: {user_message[:50]}...")

            # Call OpenAI SDK (routed to Cohere) with tool definitions
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto"  # Let model decide when to use tools
            )

            assistant_message = response.choices[0].message

            # Check if model wants to call tools
            if assistant_message.tool_calls:
                logger.info(f"Agent requested {len(assistant_message.tool_calls)} tool call(s)")

                # Execute each tool call
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    logger.info(f"Executing tool: {tool_name} with args: {tool_args}")

                    # Execute MCP tool (user_id is injected by server for security)
                    tool_result = self.mcp_server.invoke_tool(tool_name, tool_args, user_id)

                    # Log tool execution
                    tool_calls_made.append({
                        "tool": tool_name,
                        "args": {k: v for k, v in tool_args.items() if k != "user_id"},  # Don't log user_id
                        "success": tool_result.get("success", False)
                    })

                    # Convert tool result to user-friendly message
                    friendly_message = map_tool_response_to_message(
                        tool_call.id,
                        tool_name,
                        tool_result
                    )

                # Return the friendly message from tool execution
                return {
                    "message": friendly_message,
                    "tool_calls": tool_calls_made,
                    "error": None
                }

            # No tool calls - return assistant's text response
            assistant_text = assistant_message.content or "I'm here to help with your todo list. What would you like to do?"

            logger.info(f"Agent response (no tools): {assistant_text[:100]}...")

            return {
                "message": assistant_text,
                "tool_calls": tool_calls_made,
                "error": None
            }

        except Exception as e:
            logger.error(f"Agent invocation failed: {str(e)}", exc_info=True)
            return {
                "message": "I'm having trouble processing your request right now. Please try again in a moment.",
                "tool_calls": [],
                "error": str(e)
            }


# Global agent instance (initialized once)
_agent_instance = None


def get_agent() -> ChatAgent:
    """
    Get or create global ChatAgent instance.

    Returns:
        ChatAgent instance

    Note:
        Agent is lazily initialized on first access.
        If COHERE_API_KEY is not set, returns None and logs warning.
    """
    global _agent_instance

    if _agent_instance is None:
        try:
            _agent_instance = ChatAgent()
        except ValueError as e:
            logger.warning(f"ChatAgent initialization failed: {e}")
            return None

    return _agent_instance
