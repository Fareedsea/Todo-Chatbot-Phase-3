# Research: Backend REST API Technology Decisions

**Feature**: Backend REST API for Phase II Todo Application
**Branch**: `002-backend-api`
**Date**: 2026-02-05

## Phase 0: Technology Research & Architectural Decisions

This document captures technology choices, patterns, and best practices researched for implementing the Phase II Backend REST API.

---

## 1. FastAPI Project Structure

**Decision**: Layered architecture with separation of concerns

**Structure**:
```
backend/src/
├── main.py              # Application entry point, middleware setup
├── config.py            # Environment variables, settings
├── database.py          # SQLModel engine, session management
├── models/              # SQLModel ORM models
├── schemas/             # Pydantic request/response schemas
├── auth/                # JWT verification, authentication dependencies
├── routes/              # API endpoint handlers
└── errors.py            # Custom exception handlers
```

**Rationale**:
- **models/**: Database entities with SQLModel (combines SQLAlchemy + Pydantic)
- **schemas/**: API contracts separate from database models (allows different field names: snake_case DB, camelCase API)
- **auth/**: Centralized authentication logic as reusable FastAPI dependencies
- **routes/**: Endpoint handlers organized by domain (auth, tasks)
- Clear separation enables independent testing and follows single responsibility principle
- Scales well as features are added
- Follows FastAPI official recommendations

**Alternatives Considered**:
- **Flat structure**: Simpler initially but difficult to navigate as project grows (rejected for maintainability)
- **MVC pattern**: Too heavy for REST API, unnecessary abstraction layer (rejected as over-engineering)
- **Repository pattern**: Adds complexity; SQLModel queries are already clean and type-safe (rejected for simplicity)

**References**:
- FastAPI Best Practices: https://fastapi.tiangolo.com/tutorial/bigger-applications/
- Real-World FastAPI Project Structure: https://github.com/zhanymkanov/fastapi-best-practices

---

## 2. JWT Verification with Better Auth

**Decision**: Use `python-jose[cryptography]` library for JWT operations

**Implementation Pattern**:
```python
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401)
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Rationale**:
- `python-jose` is FastAPI's recommended library for JWT operations
- Built-in support for HS256 algorithm (matches Better Auth default configuration)
- Handles token expiration automatically via `exp` claim validation
- Cryptography backend provides secure signature verification
- Well-documented with extensive FastAPI examples
- Active maintenance and security updates

**Alternatives Considered**:
- **PyJWT**: Requires additional configuration, less FastAPI integration examples (rejected for complexity)
- **authlib**: Feature-rich but overkill for simple JWT verification (rejected for over-engineering)
- **Manual JWT parsing**: Security risk, reinventing the wheel (rejected for safety)

**JWT Claims Structure** (matches Better Auth):
```json
{
  "sub": "user-uuid-123",       // User ID (required)
  "email": "user@example.com",   // User email
  "iat": 1704067200,             // Issued at (Unix timestamp)
  "exp": 1704153600              // Expires (24 hours later)
}
```

**References**:
- python-jose Documentation: https://python-jose.readthedocs.io/
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

---

## 3. SQLModel with Neon PostgreSQL

**Decision**: Use SQLModel with synchronous engine for Neon PostgreSQL connection

**Connection Pattern**:
```python
from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    echo=False,               # Disable SQL logging in production
    pool_size=5,              # Maintain 5 persistent connections
    max_overflow=10,          # Allow 10 additional connections under load
    pool_pre_ping=True,       # Verify connections before use (handles serverless drops)
    poolclass=QueuePool       # Standard connection pool
)

def get_session():
    with Session(engine) as session:
        yield session
```

**Session Management**:
- Use FastAPI dependency injection for automatic session lifecycle
- Automatic commit on success, rollback on exception
- Connection pooling handles serverless PostgreSQL efficiently
- Pre-ping validates connections before executing queries

**Query Pattern for User Isolation**:
```python
from sqlmodel import select

# CRITICAL: Always filter by authenticated user ID
tasks = session.exec(
    select(Task).where(Task.user_id == current_user_id)
).all()
```

**Rationale**:
- SQLModel provides type-safe queries with Pydantic validation built-in
- Neon PostgreSQL supports standard PostgreSQL drivers (psycopg2)
- Synchronous mode simpler than async for MVP scope (<1000 tasks per user)
- Pool pre-ping handles serverless connection drops gracefully (Neon has cold starts)
- Connection pool reuses connections, reducing latency
- SQLModel integrates seamlessly with FastAPI

**Alternatives Considered**:
- **Raw SQL with psycopg2**: Error-prone, no type safety, manual validation required (rejected for safety)
- **SQLAlchemy Core/ORM alone**: More boilerplate than SQLModel, no Pydantic integration (rejected for complexity)
- **Async SQLModel with asyncio**: Adds complexity, unnecessary for MVP scope (rejected for simplicity)

**Database Configuration**:
- **Pool Size**: 5 persistent connections (sufficient for single instance)
- **Max Overflow**: 10 additional connections under load spikes
- **Pre-Ping**: Validates connection before query (handles serverless reconnects)
- **SSL Mode**: Required by Neon (`?sslmode=require` in connection string)

**References**:
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- Neon PostgreSQL Connection Guide: https://neon.tech/docs/connect/connection-pooling

---

## 4. Password Hashing Strategy

**Decision**: Use `passlib` with bcrypt algorithm

**Configuration**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**Parameters**:
- **Rounds**: 12 (bcrypt default, balances security and performance)
- **Salt**: Automatically generated per password (handled by passlib)
- **Timing-safe comparison**: Built into passlib (prevents timing attacks)

**Rationale**:
- Bcrypt is battle-tested, widely adopted, and OWASP-recommended for password hashing
- Passlib handles salt generation and constant-time comparison automatically
- 12 rounds provides strong security with acceptable performance (~50-100ms hash time)
- Better Auth (Node.js) likely uses bcrypt as it's the standard auth library choice
- Automatic handling of deprecated schemes (future-proof)
- Simple API reduces implementation errors

**Alternatives Considered**:
- **Argon2**: Newer and technically stronger but significantly slower (300ms+ hash time), overkill for MVP (rejected for performance)
- **Plain bcrypt library**: Requires manual salt generation and timing-safe comparison (rejected for complexity and error potential)
- **SHA256/SHA512**: NOT secure for passwords—too fast and no built-in salt (rejected for security)
- **PBKDF2**: Older algorithm, slower than bcrypt for equivalent security (rejected for performance)

**Security Considerations**:
- **Salt**: Unique per password, prevents rainbow table attacks
- **Rounds**: 12 iterations makes brute-force attacks computationally expensive
- **Timing-safe comparison**: Prevents timing attacks during password verification
- **Never log or expose passwords**: Hash immediately on receipt, never store plaintext

**References**:
- Passlib Documentation: https://passlib.readthedocs.io/
- OWASP Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

---

## 5. Error Handling Patterns

**Decision**: Custom exception handlers with consistent error response format

**Pattern**:
```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail.get("code", "ERROR"),
            "message": exc.detail.get("message", str(exc.detail)),
            "details": exc.detail.get("details", None)
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Validation failed",
            "details": {field: error for field, error in exc.errors()}
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log error internally
    logger.error(f"Unhandled error: {exc}", exc_info=True)

    # Return generic message (don't expose internal errors)
    return JSONResponse(
        status_code=500,
        content={
            "error": "SERVER_ERROR",
            "message": "Something went wrong"
        }
    )
```

**Status Code Mapping**:
| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | Success | GET, PUT, DELETE operations |
| 201 | Created | POST operations |
| 400 | Bad Request | Missing required fields |
| 401 | Unauthorized | Invalid/missing JWT token |
| 403 | Forbidden | Ownership violation |
| 404 | Not Found | Resource doesn't exist |
| 422 | Validation Error | Field validation failures |
| 500 | Server Error | Uncaught exceptions |

**Rationale**:
- Consistent error structure matches frontend expectations exactly (from API contracts)
- Custom exception handlers centralize error formatting (single source of truth)
- Generic handler prevents internal error leakage (security best practice)
- Status codes follow REST best practices and HTTP standards
- Field-level validation errors (422) provide actionable feedback to frontend
- Logging captures full error context for debugging without exposing to clients

**Alternatives Considered**:
- **Default FastAPI errors**: Inconsistent structure, expose internal details, don't match frontend contracts (rejected)
- **Manual try/catch everywhere**: Code duplication, error-prone, hard to maintain (rejected)
- **Custom exception classes**: Over-engineering for this scope, adds unnecessary abstraction (rejected)

**Error Code Mapping** (matches frontend contracts):
- `VALIDATION_ERROR`: 400/422 - Input validation failed
- `EMAIL_EXISTS`: 409 - Duplicate email registration
- `INVALID_CREDENTIALS`: 401 - Wrong email or password
- `UNAUTHORIZED`: 401 - Missing or invalid JWT
- `FORBIDDEN`: 403 - User lacks permission (ownership violation)
- `NOT_FOUND`: 404 - Resource doesn't exist
- `SERVER_ERROR`: 500 - Internal server error

**References**:
- FastAPI Exception Handlers: https://fastapi.tiangolo.com/tutorial/handling-errors/
- HTTP Status Codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

---

## 6. CORS Configuration

**Decision**: Use FastAPI CORSMiddleware with explicit origin allow-list

**Configuration**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",          # Development frontend
        os.getenv("FRONTEND_URL", ""),    # Production frontend (from env var)
    ],
    allow_credentials=True,   # Allow cookies and Authorization header
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

**Rationale**:
- Explicit origin allow-list prevents CORS attacks (no wildcard `*`)
- `allow_credentials=True` required for JWT in Authorization header
- Restrictive methods and headers reduce attack surface
- Environment variable for production origins maintains security flexibility
- Handles preflight requests (OPTIONS) automatically
- Prevents CORS errors during frontend-backend integration

**Alternatives Considered**:
- **Wildcard origins (`*`)**: Security vulnerability, allows any domain to access API (rejected for security)
- **No CORS middleware**: Frontend requests blocked by browser same-origin policy (rejected for functionality)
- **Manual CORS headers**: Error-prone, misses preflight requests, hard to maintain (rejected for reliability)

**Preflight Request Handling**:
- FastAPI automatically handles OPTIONS requests for preflight
- Responds with appropriate `Access-Control-*` headers
- No custom implementation needed

**Development vs Production**:
- Development: Allow `http://localhost:3000` for local frontend testing
- Production: Read from `FRONTEND_URL` environment variable (e.g., `https://app.example.com`)
- Never use wildcard origins in any environment

**References**:
- FastAPI CORS: https://fastapi.tiangolo.com/tutorial/cors/
- MDN CORS Guide: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

---

## Summary

All technology decisions support the core requirements:
- **Security-first**: JWT verification, password hashing, user isolation, error handling
- **Performance**: Connection pooling, efficient queries, fast hashing
- **Maintainability**: Clear structure, type safety, separation of concerns
- **Frontend integration**: Consistent errors, CORS support, API contract compliance

No constitutional violations. All choices align with Phase II constraints and MVP scope.

**Next Steps**: Proceed to Phase 1 (Design Artifacts) to create data-model.md, contracts/, and quickstart.md.
