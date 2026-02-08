# Feature Specification: Backend REST API for Phase II Todo Application

**Feature Branch**: `002-backend-api`
**Created**: 2026-02-05
**Status**: Draft
**Input**: User description: "Create complete backend specifications for Phase II Todo Full-Stack Web Application"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

A new user creates an account with email and password, receives a JWT token, and can authenticate for subsequent requests. The backend verifies credentials securely and issues tokens that expire after 24 hours.

**Why this priority**: Without authentication, no user can access the system. This is the foundational capability that enables all other features. Must be implemented first to unblock task management features.

**Independent Test**: Backend can be tested by sending POST requests to `/api/auth/register` and `/api/auth/login` endpoints. Success means receiving a valid JWT token that can be decoded to extract user identity. Can be validated entirely through API testing without frontend.

**Acceptance Scenarios**:

1. **Given** no existing account, **When** user submits valid email and password to `/api/auth/register`, **Then** system creates user account, returns 201 status with user object and JWT token
2. **Given** existing account, **When** user submits correct credentials to `/api/auth/login`, **Then** system validates password hash, returns 200 status with JWT token containing user ID
3. **Given** existing account, **When** user submits incorrect password to `/api/auth/login`, **Then** system returns 401 status with "Invalid credentials" message
4. **Given** duplicate email, **When** user attempts registration with existing email, **Then** system returns 409 status with "Email already registered" message
5. **Given** authenticated user, **When** user sends request to `/api/auth/logout` with valid JWT, **Then** system invalidates token and returns 200 status

---

### User Story 2 - Task Retrieval (Priority: P2)

An authenticated user requests their task list and receives only tasks they own, sorted by creation date. The backend enforces strict user isolation by filtering all queries based on the authenticated user's ID extracted from the JWT token.

**Why this priority**: Task retrieval is the foundation for all task management operations. Users must be able to view their tasks before they can create, update, or delete them. This validates the core data isolation security model.

**Independent Test**: After authentication, send GET request to `/api/tasks` with valid JWT. Success means receiving a JSON array of tasks where every task's `userId` matches the authenticated user's ID from the JWT. Can verify user isolation by attempting to access another user's tasks (should return empty array or 403).

**Acceptance Scenarios**:

1. **Given** authenticated user with 3 tasks, **When** user requests GET `/api/tasks`, **Then** system returns 200 status with array of 3 tasks, all belonging to authenticated user
2. **Given** authenticated user with no tasks, **When** user requests GET `/api/tasks`, **Then** system returns 200 status with empty array
3. **Given** unauthenticated request, **When** request sent to `/api/tasks` without JWT, **Then** system returns 401 status with "Missing or invalid authentication token"
4. **Given** expired JWT token, **When** request sent to `/api/tasks`, **Then** system returns 401 status with token expiration message
5. **Given** authenticated user, **When** user requests GET `/api/tasks/:id` for task they own, **Then** system returns 200 status with task object
6. **Given** authenticated user, **When** user requests GET `/api/tasks/:id` for task owned by different user, **Then** system returns 403 status with "Access denied" or 404 status

---

### User Story 3 - Task Creation (Priority: P3)

An authenticated user submits task details (title, optional description, optional due date) and the backend persists the task to the database with the authenticated user's ID as owner. The system validates input constraints and returns the created task with generated ID and timestamps.

**Why this priority**: Task creation is the primary value-add feature. Once users can authenticate and view tasks, the natural next step is creating new tasks. This enables the core todo functionality.

**Independent Test**: Send POST request to `/api/tasks` with valid JWT and task payload. Success means receiving 201 status with created task object containing server-generated `id`, `createdAt`, `updatedAt`, and the authenticated user's `userId`. Verify task appears in subsequent GET `/api/tasks` request.

**Acceptance Scenarios**:

1. **Given** authenticated user, **When** user submits POST `/api/tasks` with valid title, **Then** system creates task, assigns UUID, sets timestamps, returns 201 status with task object
2. **Given** authenticated user, **When** user submits POST `/api/tasks` with title exceeding 200 characters, **Then** system returns 422 status with validation error for title field
3. **Given** authenticated user, **When** user submits POST `/api/tasks` without title field, **Then** system returns 400 status with "Title is required" message
4. **Given** authenticated user, **When** user submits POST `/api/tasks` with optional description and due date, **Then** system creates task with all provided fields
5. **Given** unauthenticated request, **When** POST sent to `/api/tasks`, **Then** system returns 401 status

---

### User Story 4 - Task Update (Priority: P4)

An authenticated user modifies existing task fields (title, description, due date, completion status) and the backend validates ownership, updates only the provided fields, refreshes the `updatedAt` timestamp, and returns the updated task.

**Why this priority**: Users need to edit tasks to reflect changing priorities, add details, or fix mistakes. This completes the standard CRUD operations for task management.

**Independent Test**: Send PUT request to `/api/tasks/:id` with valid JWT and partial task payload. Success means receiving 200 status with updated task object where only submitted fields changed, `updatedAt` is refreshed, but `createdAt` remains unchanged. Verify ownership by attempting to update another user's task (should return 403 or 404).

**Acceptance Scenarios**:

1. **Given** authenticated user owns task, **When** user submits PUT `/api/tasks/:id` with updated title, **Then** system validates ownership, updates title, refreshes `updatedAt`, returns 200 status with updated task
2. **Given** authenticated user owns task, **When** user submits PUT `/api/tasks/:id` with partial fields (only `isCompleted`), **Then** system updates only completion status, preserves other fields
3. **Given** authenticated user, **When** user attempts PUT `/api/tasks/:id` for task owned by different user, **Then** system returns 403 status with "Access denied"
4. **Given** authenticated user, **When** user submits PUT `/api/tasks/:id` with invalid task ID, **Then** system returns 404 status with "Task not found"
5. **Given** authenticated user, **When** user submits PUT `/api/tasks/:id` with title exceeding 200 characters, **Then** system returns 422 status with validation error

---

### User Story 5 - Task Deletion (Priority: P5)

An authenticated user deletes a task permanently from the database. The backend validates ownership, removes the task record, and confirms successful deletion.

**Why this priority**: Users need to remove completed or obsolete tasks to keep their list clean. This completes the full CRUD lifecycle and is the lowest priority since viewing, creating, and editing provide core value.

**Independent Test**: Send DELETE request to `/api/tasks/:id` with valid JWT. Success means receiving 200 status with confirmation message. Verify task is removed by attempting GET `/api/tasks/:id` (should return 404). Verify ownership enforcement by attempting to delete another user's task (should return 403 or 404).

**Acceptance Scenarios**:

1. **Given** authenticated user owns task, **When** user sends DELETE `/api/tasks/:id`, **Then** system validates ownership, deletes task from database, returns 200 status with success message
2. **Given** authenticated user, **When** user attempts DELETE `/api/tasks/:id` for task owned by different user, **Then** system returns 403 status with "Access denied"
3. **Given** authenticated user, **When** user sends DELETE `/api/tasks/:id` with invalid task ID, **Then** system returns 404 status with "Task not found"
4. **Given** unauthenticated request, **When** DELETE sent to `/api/tasks/:id`, **Then** system returns 401 status
5. **Given** task deleted, **When** user attempts to access deleted task via GET or PUT, **Then** system returns 404 status

---

### Edge Cases

- **Concurrent Updates**: What happens when two requests update the same task simultaneously? System should use database transaction isolation to prevent lost updates. Last write wins (based on `updatedAt` timestamp).

- **Malformed JWT**: How does system handle tampered or corrupted tokens? System must reject with 401 status and "Invalid authentication token" message without exposing internal errors.

- **SQL Injection Attempts**: What happens when user submits task title with SQL syntax? System must use parameterized queries (SQLModel ORM handles this) to prevent injection attacks.

- **Extremely Long Description**: What happens when description is exactly 1000 characters vs 1001 characters? System validates at 1000 character boundary and returns 422 status for 1001+ characters.

- **Invalid Date Formats**: How does system handle due dates like "2026-13-45" or "not a date"? System validates ISO 8601 date format and returns 422 status with field-specific error message.

- **Expired Token**: What happens when user sends request with expired JWT? System returns 401 status with "Token expired" message and frontend redirects to sign-in.

- **Database Connection Failure**: How does system respond when database is unreachable? System catches connection errors and returns 500 status with generic "Something went wrong" message (does not expose database details).

- **Duplicate Task Titles**: Can user create multiple tasks with identical titles? Yes, system allows duplicate titles since tasks are uniquely identified by UUID, not title.

- **Empty Request Body**: What happens when PUT request has no fields to update? System returns 400 status with "At least one field required" message.

- **User ID Mismatch**: What happens when JWT contains user ID "123" but request path has `/api/456/tasks`? System ignores path user ID and uses only authenticated user ID from JWT for all queries.

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication & Authorization

- **FR-001**: System MUST accept user registration requests with email and password at `/api/auth/register` endpoint
- **FR-002**: System MUST validate email format using RFC 5322 standard and reject invalid emails with 400 status
- **FR-003**: System MUST enforce minimum password length of 8 characters and reject shorter passwords with 400 status
- **FR-004**: System MUST hash passwords using bcrypt or argon2 before storing in database (never store plaintext passwords)
- **FR-005**: System MUST check for duplicate emails and return 409 status with "Email already registered" message
- **FR-006**: System MUST generate JWT tokens containing user ID (`sub` claim), email, issued-at (`iat`), and expiration (`exp`) claims
- **FR-007**: System MUST set JWT token expiration to 24 hours from issuance time
- **FR-008**: System MUST accept authentication requests with email and password at `/api/auth/login` endpoint
- **FR-009**: System MUST verify password against stored hash using constant-time comparison to prevent timing attacks
- **FR-010**: System MUST return 401 status with "Invalid email or password" message for failed authentication (do not reveal which field was incorrect)
- **FR-011**: System MUST extract JWT token from `Authorization: Bearer <token>` header for all protected endpoints
- **FR-012**: System MUST verify JWT signature using shared secret from environment variable `BETTER_AUTH_SECRET`
- **FR-013**: System MUST reject expired tokens with 401 status and "Token expired" message
- **FR-014**: System MUST reject malformed or tampered tokens with 401 status and "Invalid authentication token" message
- **FR-015**: System MUST extract authenticated user ID from JWT `sub` claim for all data access operations
- **FR-016**: System MUST accept logout requests at `/api/auth/logout` and return 200 status (token invalidation handled by frontend)

#### Task Data Operations

- **FR-017**: System MUST accept GET requests to `/api/tasks` and return array of tasks belonging to authenticated user
- **FR-018**: System MUST filter all task queries by authenticated user ID extracted from JWT (never trust user ID from request path or body)
- **FR-019**: System MUST return empty array when user has no tasks (200 status, not 404)
- **FR-020**: System MUST accept GET requests to `/api/tasks/:id` and return single task if owned by authenticated user
- **FR-021**: System MUST return 404 status for non-existent task IDs
- **FR-022**: System MUST return 403 status or 404 status when authenticated user attempts to access task owned by different user
- **FR-023**: System MUST accept POST requests to `/api/tasks` with JSON body containing task details
- **FR-024**: System MUST validate required field: `title` (1-200 characters, non-empty)
- **FR-025**: System MUST validate optional field: `description` (null or 0-1000 characters)
- **FR-026**: System MUST validate optional field: `dueDate` (null or ISO 8601 date format YYYY-MM-DD)
- **FR-027**: System MUST validate optional field: `isCompleted` (boolean, defaults to false if not provided)
- **FR-028**: System MUST return 400 status with "Title is required" for missing title field
- **FR-029**: System MUST return 422 status with field-specific errors for validation failures
- **FR-030**: System MUST generate UUID for new tasks and set `userId` to authenticated user's ID
- **FR-031**: System MUST set `createdAt` and `updatedAt` timestamps to current UTC time on task creation
- **FR-032**: System MUST return 201 status with created task object including generated ID and timestamps
- **FR-033**: System MUST accept PUT requests to `/api/tasks/:id` for updating existing tasks
- **FR-034**: System MUST allow partial updates (only include fields to change, preserve others)
- **FR-035**: System MUST verify task ownership before allowing updates (403 or 404 if not owner)
- **FR-036**: System MUST refresh `updatedAt` timestamp on every successful update
- **FR-037**: System MUST preserve `createdAt` timestamp (immutable field)
- **FR-038**: System MUST return 200 status with updated task object
- **FR-039**: System MUST accept DELETE requests to `/api/tasks/:id` for permanent task removal
- **FR-040**: System MUST verify task ownership before allowing deletion (403 or 404 if not owner)
- **FR-041**: System MUST permanently delete task record from database
- **FR-042**: System MUST return 200 status with "Task deleted successfully" message

#### Data Persistence

- **FR-043**: System MUST persist all user and task data to Neon PostgreSQL database
- **FR-044**: System MUST use connection string from environment variable `NEON_DB_URL`
- **FR-045**: System MUST create database tables if they do not exist on application startup
- **FR-046**: System MUST use UUIDs for all primary keys (users and tasks)
- **FR-047**: System MUST enforce foreign key relationship between tasks and users (task.user_id references user.id)
- **FR-048**: System MUST set cascading delete behavior so deleting user removes all their tasks
- **FR-049**: System MUST store timestamps in UTC timezone with ISO 8601 format
- **FR-050**: System MUST create index on `tasks.user_id` column for query performance
- **FR-051**: System MUST create unique constraint on `users.email` column

#### Error Handling & Responses

- **FR-052**: System MUST return JSON responses with consistent structure for all endpoints
- **FR-053**: System MUST include `error` code and `message` fields in all error responses
- **FR-054**: System MUST include `details` object for validation errors (422 status) mapping field names to error messages
- **FR-055**: System MUST return appropriate HTTP status codes: 200 (success), 201 (created), 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 422 (validation error), 500 (server error)
- **FR-056**: System MUST catch all unhandled exceptions and return 500 status with "Something went wrong" message
- **FR-057**: System MUST never expose internal error details, stack traces, or database information in responses
- **FR-058**: System MUST log all errors to application logs with timestamps and request context

#### API Contract Compliance

- **FR-059**: System MUST prefix all API endpoints with `/api/` path
- **FR-060**: System MUST set `Content-Type: application/json` header on all responses
- **FR-061**: System MUST accept requests with `Content-Type: application/json` header
- **FR-062**: System MUST return task objects with exact field names: `id`, `title`, `description`, `dueDate`, `isCompleted`, `createdAt`, `updatedAt`, `userId`
- **FR-063**: System MUST use camelCase for all JSON field names (not snake_case)
- **FR-064**: System MUST format timestamps as ISO 8601 with UTC timezone: `2026-02-05T12:00:00Z`
- **FR-065**: System MUST return `null` for optional fields that have no value (not empty strings or omit field)

### Key Entities

- **User**: Represents an authenticated account with unique email and hashed password. Owns zero or more tasks. Attributes: unique identifier, email address, password hash, account creation timestamp.

- **Task**: Represents a todo item belonging to a single user. Attributes: unique identifier, title (required), description (optional), due date (optional), completion status (boolean), creation timestamp, last update timestamp, owner reference (user identifier).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All API endpoints respond within 500ms for single-task operations under normal load
- **SC-002**: Backend successfully handles 100 concurrent authenticated requests without errors
- **SC-003**: Zero unauthorized data access incidents—every task query filtered by authenticated user ID
- **SC-004**: JWT tokens successfully expire after 24 hours and are rejected on subsequent requests
- **SC-005**: 100% of password storage uses secure hashing (bcrypt or argon2), zero plaintext passwords
- **SC-006**: All task CRUD operations (create, read, update, delete) complete successfully for authenticated users
- **SC-007**: Database constraints prevent orphaned tasks (all tasks have valid user_id referencing existing user)
- **SC-008**: API contract compliance validated—all response field names match frontend expectations exactly
- **SC-009**: Error responses consistently include error code and message fields across all endpoints
- **SC-010**: Frontend can complete full user journey (register → login → create task → view tasks → update task → delete task → logout) without backend errors

## Scope & Boundaries *(mandatory)*

### In Scope

- FastAPI backend application structure with separation of concerns
- User registration and authentication endpoints (`/api/auth/*`)
- JWT token generation, validation, and expiration handling
- Task CRUD operations endpoints (`/api/tasks`, `/api/tasks/:id`)
- User data isolation enforced at database query level
- SQLModel ORM integration for type-safe database operations
- Neon PostgreSQL database connection and schema management
- Environment variable configuration for secrets and database connection
- Request validation and consistent error response formatting
- API contract compliance matching frontend expectations
- CORS configuration to allow frontend requests

### Out of Scope

- User profile management (name, avatar, preferences)
- Password reset or recovery flows
- Email verification for new accounts
- Token refresh endpoint (Better Auth handles on frontend)
- Task sharing or collaboration features
- Task categories, tags, or priority levels
- Task search or filtering by title/description
- Pagination for large task lists (MVP returns all tasks)
- Rate limiting or request throttling
- API versioning strategy
- Database migrations tooling (manual schema updates)
- Comprehensive logging and monitoring infrastructure
- Admin endpoints or user management
- Unit and integration test suite (focus on implementation)
- Deployment configuration or containerization

### Dependencies

- **Frontend Application**: Backend APIs must match contracts defined in `specs/001-frontend-ui/contracts/`
- **Neon PostgreSQL**: Requires active Neon database instance with connection string
- **Better Auth Secret**: Shared secret for JWT signature verification must match frontend configuration
- **Python Runtime**: Python 3.11+ for FastAPI and SQLModel compatibility

### Assumptions

- Frontend handles JWT token storage and refresh logic
- Frontend attaches `Authorization: Bearer <token>` header to all protected requests
- Frontend handles redirect to sign-in on 401 responses
- Database connection string includes SSL mode and is accessible from backend runtime environment
- Task list size remains manageable without pagination (< 1000 tasks per user)
- Single backend instance sufficient for MVP (no load balancing or horizontal scaling)
- User time zones handled by frontend (backend stores all times in UTC)

### Constraints

- **No Frontend Code**: Backend specification cannot dictate frontend behavior beyond API contract
- **Constitution Compliance**: Backend must follow Phase II scope boundaries and security-first architecture
- **Technology Stack**: Must use FastAPI, SQLModel, and Neon PostgreSQL as specified
- **Security Mandate**: All endpoints except `/api/auth/register` and `/api/auth/login` require valid JWT authentication
- **Data Isolation**: Database queries MUST always filter by authenticated user ID from JWT
- **API Contract**: All response structures MUST match frontend expectations exactly (field names, types, formats)

## Non-Functional Requirements *(optional)*

### Performance

- **NFR-001**: API endpoints respond within 500ms at p95 latency for single-task operations
- **NFR-002**: Database connection pool maintains 5-20 concurrent connections
- **NFR-003**: JWT token verification completes within 50ms
- **NFR-004**: Task list retrieval completes within 200ms for users with up to 100 tasks

### Security

- **NFR-005**: All database queries use parameterized statements to prevent SQL injection
- **NFR-006**: Password hashing uses minimum 12 rounds for bcrypt or standard parameters for argon2
- **NFR-007**: JWT secret must be at least 32 characters and stored as environment variable
- **NFR-008**: Error messages never expose internal system details or database schema
- **NFR-009**: CORS configuration allows only specified frontend origin (no wildcard in production)

### Reliability

- **NFR-010**: Application handles database connection failures gracefully with 500 status responses
- **NFR-011**: Application restarts automatically recover database connection pool
- **NFR-012**: Unhandled exceptions caught globally and logged without exposing to clients

### Maintainability

- **NFR-013**: Code organized into modules: routes, models, database, authentication, configuration
- **NFR-014**: All environment variables documented with purpose and expected format
- **NFR-015**: Database schema changes require updating SQLModel models to maintain type safety

## API Endpoint Summary *(reference)*

### Authentication Endpoints

| Method | Endpoint             | Purpose                          | Auth Required |
|--------|----------------------|----------------------------------|---------------|
| POST   | `/api/auth/register` | Create new user account          | No            |
| POST   | `/api/auth/login`    | Authenticate and receive JWT     | No            |
| POST   | `/api/auth/logout`   | Sign out (invalidate token)      | Yes           |

### Task Management Endpoints

| Method | Endpoint           | Purpose                   | Auth Required |
|--------|--------------------|---------------------------|---------------|
| GET    | `/api/tasks`       | Retrieve all user's tasks | Yes           |
| POST   | `/api/tasks`       | Create new task           | Yes           |
| GET    | `/api/tasks/:id`   | Retrieve specific task    | Yes           |
| PUT    | `/api/tasks/:id`   | Update existing task      | Yes           |
| DELETE | `/api/tasks/:id`   | Delete task permanently   | Yes           |

---

**Specification Status**: ✅ Draft Complete
**Next Steps**: Proceed to validation checklist creation
**Frontend Contract Reference**: See `specs/001-frontend-ui/contracts/` for exact API expectations
