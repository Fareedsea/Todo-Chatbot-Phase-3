"""
Authentication API endpoints.

Provides user registration, login, and logout functionality with JWT tokens.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Annotated

from ..database import get_session
from ..models.user import User
from ..schemas.auth import (
    RegisterRequest,
    LoginRequest,
    AuthResponse,
    UserResponse,
    LogoutResponse
)
from ..auth.password import hash_password, verify_password
from ..auth.jwt import create_access_token
from ..auth.dependencies import get_current_user
from ..errors import raise_unauthorized, raise_conflict, raise_bad_request

router = APIRouter()


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account with email and password. Returns user info and JWT token."
)
async def register(
    request: RegisterRequest,
    session: Session = Depends(get_session)
) -> AuthResponse:
    """
    Register a new user account.

    Requirements (from spec FR-001 to FR-007):
    - FR-001: Accept email and password
    - FR-002: Validate email format (RFC 5322) - handled by EmailStr
    - FR-003: Enforce minimum 8 character password
    - FR-004: Hash password with bcrypt
    - FR-005: Check for duplicate emails (409 if exists)
    - FR-006: Generate JWT with user ID, email, iat, exp claims
    - FR-007: Set token expiration to 24 hours

    Request Body:
        {
            "email": "user@example.com",
            "password": "SecurePass123"
        }

    Success Response (201):
        {
            "user": {
                "id": "user-uuid-123",
                "email": "user@example.com"
            },
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }

    Error Responses:
        400: Invalid email format or password too short
        409: Email already registered
        500: Server error
    """
    # Check if email already exists (FR-005)
    existing_user = session.exec(
        select(User).where(User.email == request.email)
    ).first()

    if existing_user:
        raise_conflict("Email already registered")

    # Hash password (FR-004)
    password_hash = hash_password(request.password)

    # Create new user
    new_user = User(
        email=request.email,
        password_hash=password_hash
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Generate JWT token (FR-006, FR-007)
    token = create_access_token(new_user.id, new_user.email)

    # Return user info and token
    return AuthResponse(
        user=UserResponse(
            id=new_user.id,
            email=new_user.email
        ),
        token=token
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user",
    description="Verify credentials and return JWT token for authenticated user."
)
async def login(
    request: LoginRequest,
    session: Session = Depends(get_session)
) -> AuthResponse:
    """
    Authenticate user and return JWT token.

    Requirements (from spec FR-008 to FR-010):
    - FR-008: Accept email and password
    - FR-009: Verify password against hash with constant-time comparison
    - FR-010: Return 401 with generic message (don't reveal which field incorrect)

    Request Body:
        {
            "email": "user@example.com",
            "password": "SecurePass123"
        }

    Success Response (200):
        {
            "user": {
                "id": "user-uuid-123",
                "email": "user@example.com"
            },
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }

    Error Responses:
        401: Invalid email or password (generic message for security)
        400: Malformed request
        500: Server error
    """
    # Look up user by email
    user = session.exec(
        select(User).where(User.email == request.email)
    ).first()

    # Verify user exists and password correct (FR-009)
    # Use generic error message (FR-010) - don't reveal if email or password wrong
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "INVALID_CREDENTIALS",
                "message": "Invalid email or password"
            }
        )

    # Generate JWT token
    token = create_access_token(user.id, user.email)

    # Return user info and token
    return AuthResponse(
        user=UserResponse(
            id=user.id,
            email=user.email
        ),
        token=token
    )


@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="Sign out user and invalidate session. Token invalidation handled by frontend."
)
async def logout(
    current_user_id: str = Depends(get_current_user)
) -> LogoutResponse:
    """
    Logout user (requires valid JWT).

    Requirements (from spec FR-016):
    - FR-016: Accept logout requests with valid JWT
    - Return 200 status (token invalidation handled by frontend)

    Note: JWT tokens are stateless, so backend cannot invalidate them.
    Frontend removes token from storage (localStorage/cookie) on logout.
    Backend only validates the token is currently valid.

    Request Headers:
        Authorization: Bearer <jwt_token>

    Success Response (200):
        {
            "message": "Logged out successfully"
        }

    Error Responses:
        401: Missing or invalid JWT token
        500: Server error
    """
    # Token already validated by get_current_user dependency
    # Frontend will remove token from storage
    return LogoutResponse(message="Logged out successfully")
