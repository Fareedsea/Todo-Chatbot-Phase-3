# Backend REST API - Phase II Todo Application

FastAPI backend providing secure, JWT-authenticated REST endpoints for task management with strict user data isolation.

## Architecture

- **Framework**: FastAPI (high-performance async Python)
- **ORM**: SQLModel (type-safe Pydantic + SQLAlchemy)
- **Database**: Neon PostgreSQL (serverless)
- **Authentication**: JWT tokens verified against Better Auth secret
- **Security**: User isolation enforced at database query level

## Project Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Environment variable configuration
│   ├── database.py          # SQLModel engine and session management
│   ├── errors.py            # Custom exception handlers
│   ├── models/              # SQLModel ORM models (User, Task)
│   ├── schemas/             # Pydantic request/response schemas
│   ├── auth/                # JWT verification, authentication dependencies
│   └── routes/              # API endpoint handlers (auth, tasks)
├── tests/                   # Integration tests
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variable template
└── README.md               # This file
```

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database (Neon account recommended)
- Better Auth secret (shared with frontend)

### Installation

1. **Clone repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd todo-web-app-Phase-2/backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv

   # Activate on Windows:
   venv\Scripts\activate

   # Activate on macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   # Copy template
   cp .env.example .env

   # Edit .env and set:
   # - NEON_DB_URL: Your Neon PostgreSQL connection string
   # - BETTER_AUTH_SECRET: Shared secret from Better Auth (32+ chars)
   # - FRONTEND_URL: Your frontend origin (http://localhost:3000 for dev)
   ```

5. **Verify database connection**:
   ```bash
   # Test database connectivity
   python -c "from src.database import engine; print('Database connected:', engine.url)"
   ```

## Running the Server

### Development Mode

```bash
# From backend/ directory with venv activated
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Server runs at: `http://localhost:8000`

API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Production Mode

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

All endpoints prefixed with `/api/`

### Authentication

| Method | Endpoint             | Description                  | Auth Required |
|--------|----------------------|------------------------------|---------------|
| POST   | `/api/auth/register` | Create new user account      | No            |
| POST   | `/api/auth/login`    | Authenticate and get JWT     | No            |
| POST   | `/api/auth/logout`   | Sign out (invalidate token)  | Yes           |

### Task Management

| Method | Endpoint           | Description                   | Auth Required |
|--------|--------------------|-------------------------------|---------------|
| GET    | `/api/tasks`       | Retrieve all user's tasks     | Yes           |
| POST   | `/api/tasks`       | Create new task               | Yes           |
| GET    | `/api/tasks/:id`   | Retrieve specific task        | Yes           |
| PUT    | `/api/tasks/:id`   | Update existing task          | Yes           |
| DELETE | `/api/tasks/:id`   | Delete task permanently       | Yes           |

## Authentication

All protected endpoints require JWT token in `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

JWT tokens are issued on registration and login, contain user ID in `sub` claim, and expire after 24 hours.

## Security Features

- **JWT Verification**: Backend validates JWT signature using `BETTER_AUTH_SECRET`
- **User Isolation**: All queries filter by authenticated user ID from JWT
- **Password Hashing**: Bcrypt with 12 rounds (never stores plaintext)
- **Input Validation**: Pydantic schemas validate all inputs
- **Error Sanitization**: Internal errors never exposed to clients
- **CORS Protection**: Explicit origin allow-list (no wildcards)

## Testing

### Manual Testing with curl

```bash
# Register new user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123"}'

# Create task (replace <TOKEN> with JWT from login response)
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"title": "Test task", "description": "Testing API"}'

# Get all tasks
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <TOKEN>"
```

### Integration Tests

```bash
# Run integration tests (once implemented)
pytest tests/ -v
```

## Environment Variables

| Variable            | Required | Description                                      | Example                          |
|---------------------|----------|--------------------------------------------------|----------------------------------|
| `NEON_DB_URL`       | Yes      | PostgreSQL connection string (with SSL)          | `postgresql://user:pass@host...` |
| `BETTER_AUTH_SECRET`| Yes      | JWT signature secret (32+ characters)            | `your-random-secret-key`         |
| `FRONTEND_URL`      | Yes      | Frontend origin for CORS                         | `http://localhost:3000`          |
| `ENVIRONMENT`       | No       | Runtime environment                              | `development`                    |
| `PORT`              | No       | Server port (default: 8000)                      | `8000`                           |
| `LOG_LEVEL`         | No       | Logging verbosity                                | `INFO`                           |

## Troubleshooting

### Database Connection Issues

```bash
# Verify connection string format
echo $NEON_DB_URL

# Check SSL mode is included
# Should end with: ?sslmode=require

# Test raw connection
psql "$NEON_DB_URL"
```

### JWT Verification Failures

- Ensure `BETTER_AUTH_SECRET` matches frontend configuration exactly
- Verify JWT token is valid and not expired
- Check `Authorization` header format: `Bearer <token>`

### CORS Errors

- Verify `FRONTEND_URL` matches origin in browser (exact match required)
- Check frontend is sending requests with credentials
- Inspect browser console for specific CORS error details

## Development Workflow

1. Update specification in `/specs/002-backend-api/`
2. Update SQLModel models in `src/models/`
3. Update Pydantic schemas in `src/schemas/`
4. Implement endpoint handlers in `src/routes/`
5. Test manually with curl or Postman
6. Run integration tests
7. Update this README if API changes

## Specification Reference

All implementation follows approved specifications:
- `specs/002-backend-api/spec.md` - Functional requirements
- `specs/002-backend-api/plan.md` - Architecture design
- `specs/002-backend-api/tasks.md` - Task breakdown
- `specs/001-frontend-ui/contracts/` - API contracts

## License

Phase II Hackathon Project - Internal Use Only
