"""
Custom exception handlers for consistent error responses.

Implements security-first error handling that never exposes internal details.
All error responses follow the frontend API contract structure.
"""

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register custom exception handlers with FastAPI application.

    Call this function during app initialization in main.py.
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """
        Handle FastAPI HTTPException with consistent error response format.

        Transforms HTTPException into standardized error structure matching
        frontend API contract expectations.
        """
        # Extract error details if provided as dict, otherwise use detail string
        if isinstance(exc.detail, dict):
            error_code = exc.detail.get("error", "ERROR")
            message = exc.detail.get("message", "An error occurred")
            details = exc.detail.get("details")
        else:
            # Map status codes to error codes
            error_code = _get_error_code_from_status(exc.status_code)
            message = str(exc.detail) if exc.detail else "An error occurred"
            details = None

        response = {
            "error": error_code,
            "message": message
        }

        if details:
            response["details"] = details

        # Log error for debugging (but don't expose to client)
        logger.warning(
            f"HTTP {exc.status_code}: {message}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "error_code": error_code
            }
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=response
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """
        Handle Pydantic validation errors (422 Unprocessable Entity).

        Transforms validation errors into field-specific error messages
        for frontend form display.
        """
        # Extract field-level errors from Pydantic validation
        details = {}
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
            message = error["msg"]
            details[field] = message

        response = {
            "error": "VALIDATION_ERROR",
            "message": "Validation failed",
            "details": details
        }

        logger.info(
            f"Validation error on {request.url.path}",
            extra={"fields": list(details.keys())}
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=response
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(
        request: Request, exc: ValidationError
    ) -> JSONResponse:
        """
        Handle standalone Pydantic ValidationError (rare, but possible).
        """
        details = {}
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            details[field] = error["msg"]

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "VALIDATION_ERROR",
                "message": "Validation failed",
                "details": details
            }
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Catch-all handler for unhandled exceptions.

        CRITICAL SECURITY REQUIREMENT:
        - Never expose internal error details to clients
        - Always log full error server-side for debugging
        - Return generic "Something went wrong" message
        """
        # Log full error details server-side
        logger.error(
            f"Unhandled exception on {request.method} {request.url.path}: {exc}",
            exc_info=True,
            extra={
                "path": request.url.path,
                "method": request.method,
                "exception_type": type(exc).__name__
            }
        )

        # Return sanitized error to client (never expose internals)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "SERVER_ERROR",
                "message": "Something went wrong"
            }
        )


def _get_error_code_from_status(status_code: int) -> str:
    """
    Map HTTP status codes to frontend-compatible error codes.
    """
    mapping = {
        400: "VALIDATION_ERROR",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "EMAIL_EXISTS",
        422: "VALIDATION_ERROR",
        500: "SERVER_ERROR",
    }
    return mapping.get(status_code, "ERROR")


# Helper functions for raising standardized errors

def raise_unauthorized(message: str = "Missing or invalid authentication token") -> None:
    """Raise 401 Unauthorized with standardized error structure."""
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "error": "UNAUTHORIZED",
            "message": message
        }
    )


def raise_forbidden(message: str = "Access denied") -> None:
    """Raise 403 Forbidden with standardized error structure."""
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "error": "FORBIDDEN",
            "message": message
        }
    )


def raise_not_found(message: str = "Resource not found") -> None:
    """Raise 404 Not Found with standardized error structure."""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": "NOT_FOUND",
            "message": message
        }
    )


def raise_conflict(message: str = "Resource already exists") -> None:
    """Raise 409 Conflict with standardized error structure."""
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={
            "error": "EMAIL_EXISTS",
            "message": message
        }
    )


def raise_bad_request(message: str, details: dict = None) -> None:
    """Raise 400 Bad Request with standardized error structure."""
    detail = {
        "error": "VALIDATION_ERROR",
        "message": message
    }
    if details:
        detail["details"] = details

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )
