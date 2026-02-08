"""
MCP Tools Module

This module will contain individual MCP tool implementations for Phase III AI Chatbot.
Tools will be implemented in subsequent tasks (T020-T056).

Constitutional Requirements:
- MCP Tool Law (Law XI): Tools MUST be stateless, deterministic, validate inputs, enforce ownership
- Tool-Only AI Law (Law VIII): AI MUST ONLY act via MCP tools

Planned Tools (to be implemented):
- add_task (T020): Create new task for user
- list_tasks (T036): Retrieve all user tasks with optional filter
- update_task (T052): Update task title
- complete_task (T041): Mark task as complete
- delete_task (T047): Remove task

Each tool will:
1. Validate input against schema
2. Verify user ownership
3. Delegate to backend APIs or database
4. Return structured response (success/error)
"""

# All MCP tools for Phase III AI Chatbot
from .add_task import register_add_task_tool
from .list_tasks import register_list_tasks_tool
from .update_task import register_update_task_tool
from .complete_task import register_complete_task_tool
from .delete_task import register_delete_task_tool

__all__ = [
    "register_add_task_tool",
    "register_list_tasks_tool",
    "register_update_task_tool",
    "register_complete_task_tool",
    "register_delete_task_tool"
]
