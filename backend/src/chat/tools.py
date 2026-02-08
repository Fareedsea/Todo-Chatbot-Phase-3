"""
OpenAI Function Definitions for MCP Tools.

Converts MCP tools into OpenAI function calling format for Cohere integration.
These definitions are passed to the OpenAI SDK when invoking the agent.
"""

from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def get_tool_definitions() -> List[Dict[str, Any]]:
    """
    Get all MCP tool definitions in OpenAI function calling format.

    Returns a list of tool definitions that can be passed to the OpenAI SDK.
    Each tool definition includes name, description, and parameter schema.

    Returns:
        List of tool definition dictionaries compatible with OpenAI SDK

    Example:
        tools = get_tool_definitions()
        response = client.chat.completions.create(
            model="command-r-plus",
            messages=[...],
            tools=tools
        )
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task for the user. Use this when the user wants to add something to their todo list.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The task title or description (1-500 characters)",
                            "minLength": 1,
                            "maxLength": 500
                        }
                    },
                    "required": ["title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "Retrieve all tasks for the user. Can optionally filter by completion status. Use this when the user asks to see their tasks, todo list, or what they need to do.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "completed": {
                            "type": "boolean",
                            "description": "Filter by completion status: true for completed tasks, false for incomplete tasks, omit for all tasks",
                            "nullable": True
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as completed. Use this when the user indicates they finished a task or want to mark it as done.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The unique ID (UUID) of the task to complete"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update a task's title. Use this when the user wants to change, edit, or rename a task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The unique ID (UUID) of the task to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "The new task title (1-500 characters)",
                            "minLength": 1,
                            "maxLength": 500
                        }
                    },
                    "required": ["task_id", "title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Permanently delete a task. Use this when the user wants to remove a task from their list. Always confirm with the user before calling this.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The unique ID (UUID) of the task to delete"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        }
    ]


def map_tool_response_to_message(tool_call_id: str, tool_name: str, tool_result: Dict[str, Any]) -> str:
    """
    Map MCP tool response to user-friendly message.

    Converts structured tool responses into natural language messages
    that can be shown to the user.

    Args:
        tool_call_id: OpenAI tool call ID
        tool_name: Name of the tool that was called
        tool_result: Result from MCP tool execution

    Returns:
        User-friendly message string

    Example:
        result = {"success": True, "data": {"task": {"id": "123", "title": "Buy milk"}}}
        message = map_tool_response_to_message("call_1", "add_task", result)
        # Returns: "I've added 'Buy milk' to your todo list"
    """
    if not tool_result.get("success"):
        # Handle error
        error = tool_result.get("error", {})
        error_code = error.get("code", "UNKNOWN_ERROR")
        error_message = error.get("message", "An error occurred")

        # Translate technical errors to user-friendly messages
        if error_code == "NOT_FOUND":
            return f"I couldn't find that task. It may have already been deleted."
        elif error_code == "VALIDATION_ERROR":
            return f"I couldn't process that: {error_message}"
        elif error_code == "DATABASE_ERROR":
            return "I'm having trouble accessing your tasks right now. Please try again in a moment."
        else:
            return "I encountered an error while processing your request. Please try again."

    # Handle success responses by tool type
    data = tool_result.get("data", {})

    if tool_name == "add_task":
        task = data.get("task", {})
        title = task.get("title", "a new task")
        return f"I've added '{title}' to your todo list."

    elif tool_name == "list_tasks":
        tasks = data.get("tasks", [])
        if not tasks:
            return "You don't have any tasks yet. Would you like to add one?"

        task_list = "\n".join([
            f"{'✓' if task['completed'] else '○'} {task['title']}"
            for task in tasks
        ])
        count = len(tasks)
        return f"You have {count} task{'s' if count != 1 else ''}:\n\n{task_list}"

    elif tool_name == "complete_task":
        task = data.get("task", {})
        title = task.get("title", "the task")
        return f"I've marked '{title}' as complete. Great job!"

    elif tool_name == "update_task":
        task = data.get("task", {})
        title = task.get("title", "the task")
        return f"I've updated the task to '{title}'."

    elif tool_name == "delete_task":
        title = data.get("title", "the task")
        return f"I've deleted '{title}' from your list."

    else:
        return "Done!"
