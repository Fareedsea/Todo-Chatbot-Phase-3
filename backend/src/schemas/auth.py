"""
Pydantic schemas for authentication API requests and responses.

Defines validation rules and response structures matching frontend API contracts.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class RegisterRequest(BaseModel):
    """
    Request schema for user registration.

    Validates email format and password strength.
    """
    email: EmailStr = Field(
        ...,
        description="User's email address (RFC 5322 format)",
        examples=["user@example.com"]
    )

    password: str = Field(
        ...,
        min_length=8,
        description="Password (minimum 8 characters)",
        examples=["SecurePass123"]
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password meets minimum security requirements.

        Requirements:
        - Minimum 8 characters (enforced by Field min_length)
        - Additional complexity rules can be added here
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginRequest(BaseModel):
    """
    Request schema for user login.

    Validates email format.
    """
    email: EmailStr = Field(
        ...,
        description="User's email address",
        examples=["user@example.com"]
    )

    password: str = Field(
        ...,
        description="User's password",
        examples=["SecurePass123"]
    )


class UserResponse(BaseModel):
    """
    User information returned in authentication responses.

    SECURITY: Never includes password_hash or sensitive fields.
    """
    id: str = Field(
        ...,
        description="Unique user identifier (UUID)"
    )

    email: str = Field(
        ...,
        description="User's email address"
    )

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility


class AuthResponse(BaseModel):
    """
    Response schema for successful authentication (register, login).

    Returns user information and JWT token.
    """
    user: UserResponse = Field(
        ...,
        description="Authenticated user information"
    )

    token: str = Field(
        ...,
        description="JWT access token (valid for 24 hours)",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )


class LogoutResponse(BaseModel):
    """
    Response schema for logout endpoint.

    Note: Token invalidation handled by frontend (removes from storage).
    Backend returns success confirmation.
    """
    message: str = Field(
        default="Logged out successfully",
        description="Success confirmation message"
    )


class ErrorResponse(BaseModel):
    """
    Standard error response structure.

    Used across all endpoints for consistent error formatting.
    """
    error: str = Field(
        ...,
        description="Error code (e.g., VALIDATION_ERROR, UNAUTHORIZED)",
        examples=["VALIDATION_ERROR"]
    )

    message: str = Field(
        ...,
        description="Human-readable error message",
        examples=["Invalid email format"]
    )

    details: Optional[dict] = Field(
        default=None,
        description="Field-specific error details (for validation errors)",
        examples=[{"email": "must be valid email"}]
    )
