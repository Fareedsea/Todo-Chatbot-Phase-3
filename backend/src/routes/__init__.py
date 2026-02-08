"""
API endpoint route handlers.

Organizes endpoints by domain: authentication, task management.
"""

from .auth import router as auth_router
from .tasks import router as tasks_router

__all__ = ["auth_router", "tasks_router"]
