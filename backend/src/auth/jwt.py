"""
JWT token creation and verification using python-jose.

SECURITY REQUIREMENTS:
- JWT signature MUST be verified using BETTER_AUTH_SECRET
- Tokens expire after 24 hours (configurable)
- User ID stored in 'sub' (subject) claim
- Expiration checked automatically during verification
"""

from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Dict, Optional

from ..config import settings


def create_access_token(user_id: str, email: str) -> str:
    """
    Create a JWT access token for authenticated user.

    Args:
        user_id: Unique user identifier (UUID)
        email: User's email address

    Returns:
        Encoded JWT token string

    Token Structure:
        {
            "sub": "user-uuid-123",      # User ID (CRITICAL: used for all queries)
            "email": "user@example.com",  # User email (informational)
            "iat": 1704067200,            # Issued at (Unix timestamp)
            "exp": 1704153600             # Expires (24 hours later)
        }

    Security:
        - Signed with BETTER_AUTH_SECRET using HS256 algorithm
        - Expiration enforced during verification
        - User ID in 'sub' claim is the authoritative source for user identity

    Example:
        >>> token = create_access_token("user-123", "test@example.com")
        >>> len(token) > 100  # JWT tokens are typically 150-200 chars
        True
    """
    # Calculate expiration time
    now = datetime.utcnow()
    expires_delta = timedelta(hours=settings.jwt_expiration_hours)
    expire = now + expires_delta

    # Build JWT claims
    payload = {
        "sub": user_id,  # Subject (user ID) - CRITICAL for authorization
        "email": email,  # User email (informational)
        "iat": int(now.timestamp()),  # Issued at
        "exp": int(expire.timestamp()),  # Expiration
    }

    # Encode and sign JWT
    encoded_jwt = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.jwt_algorithm
    )

    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, any]]:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string (without "Bearer " prefix)

    Returns:
        Decoded token payload (dict) if valid, None if invalid/expired

    Raises:
        Does not raise exceptions; returns None for any verification failure

    Token Claims (if valid):
        {
            "sub": str,    # User ID
            "email": str,  # User email
            "iat": int,    # Issued at timestamp
            "exp": int     # Expiration timestamp
        }

    Security:
        - Verifies signature using BETTER_AUTH_SECRET
        - Checks expiration automatically (rejects expired tokens)
        - Returns None for tampered, malformed, or expired tokens
        - Never exposes JWTError details to prevent information leakage

    Example:
        >>> token = create_access_token("user-123", "test@example.com")
        >>> payload = verify_token(token)
        >>> payload["sub"] == "user-123"
        True
    """
    try:
        # Decode and verify JWT
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        return payload

    except JWTError:
        # Token invalid, expired, or tampered
        # Return None instead of raising (caller handles error response)
        return None


def extract_user_id(token: str) -> Optional[str]:
    """
    Extract user ID from JWT token.

    Args:
        token: JWT token string

    Returns:
        User ID (str) if token valid, None if invalid/expired

    Security:
        This is the ONLY authoritative source for user identity.
        NEVER trust user_id from request path, query params, or body.

    Example:
        >>> token = create_access_token("user-123", "test@example.com")
        >>> extract_user_id(token)
        'user-123'
    """
    payload = verify_token(token)
    if payload:
        return payload.get("sub")
    return None
