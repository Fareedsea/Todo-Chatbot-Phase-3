"""
FastAPI authentication dependencies for JWT verification.

Provides get_current_user dependency that extracts and validates JWT tokens
from Authorization headers. All protected endpoints MUST use this dependency.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from .jwt import verify_token
from ..errors import raise_unauthorized

# HTTP Bearer authentication scheme
# Automatically extracts "Authorization: Bearer <token>" header
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    FastAPI dependency that extracts and validates JWT token.

    Validates the JWT token from Authorization header and returns authenticated user ID.
    This is the ONLY authoritative source for user identity in protected endpoints.

    Args:
        credentials: HTTPAuthorizationCredentials from Bearer token (auto-injected)

    Returns:
        User ID (str) extracted from JWT 'sub' claim

    Raises:
        HTTPException 401: If token is missing, invalid, expired, or malformed

    Security:
        - MUST be used on ALL protected endpoints
        - Verifies JWT signature using BETTER_AUTH_SECRET
        - Checks token expiration automatically
        - Returns user ID for database query filtering
        - NEVER trust user_id from request path/body; only from JWT

    Usage:
        @app.get("/api/tasks")
        def get_tasks(user_id: str = Depends(get_current_user)):
            # user_id is guaranteed valid and authenticated
            tasks = session.query(Task).filter(Task.user_id == user_id).all()
            return tasks

    Example:
        # Valid request with JWT:
        # Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        # Returns: "user-uuid-123"

        # Invalid/missing token:
        # Raises: HTTPException(status_code=401)
    """
    # Extract token from credentials
    token = credentials.credentials

    # Verify token and extract payload
    payload = verify_token(token)

    if not payload:
        # Token invalid, expired, or tampered
        raise_unauthorized("Missing or invalid authentication token")

    # Extract user ID from 'sub' claim
    user_id = payload.get("sub")

    if not user_id:
        # Token missing required 'sub' claim (malformed)
        raise_unauthorized("Invalid token structure")

    return user_id


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    )
) -> Optional[str]:
    """
    Optional authentication dependency (for endpoints that support both authenticated and anonymous access).

    Returns user ID if valid token provided, None if no token.
    Raises 401 if token provided but invalid.

    Usage:
        @app.get("/api/public")
        def public_endpoint(user_id: Optional[str] = Depends(get_current_user_optional)):
            if user_id:
                # Authenticated user - return personalized content
                pass
            else:
                # Anonymous user - return public content
                pass
    """
    if not credentials:
        return None

    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise_unauthorized("Invalid authentication token")

    return payload.get("sub")
