---
description: "Task list for Backend REST API implementation"
---

# Tasks: Backend REST API for Phase II Todo Application

**Input**: Design documents from `/specs/002-backend-api/`
**Prerequisites**: spec.md (✅), research.md (✅), plan.md (in progress)

**Tests**: No tests requested - focus on implementation
**Organization**: Tasks grouped by user story to enable independent implementation and testing of each story

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`
- Root configuration: `backend/`
- Tests: `backend/tests/`
- Models: `backend/src/models/`
- Schemas: `backend/src/schemas/`
- Routes: `backend/src/routes/`
- Auth: `backend/src/auth/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure (backend/src/, backend/tests/)
- [x] T002 Create requirements.txt with dependencies (FastAPI, SQLModel, python-jose, passlib, psycopg2-binary, uvicorn, email-validator)
- [x] T003 [P] Create .env.example with NEON_DB_URL, BETTER_AUTH_SECRET, FRONTEND_URL in backend/
- [x] T004 [P] Create backend/README.md with project overview and setup instructions
- [x] T005 [P] Create __init__.py files for all Python packages (backend/src/, backend/src/models/, backend/src/schemas/, backend/src/auth/, backend/src/routes/)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 [P] Create config.py to load environment variables (NEON_DB_URL, BETTER_AUTH_SECRET, FRONTEND_URL) in backend/src/config.py
- [x] T007 [P] Create database.py with SQLModel engine setup and get_session() dependency in backend/src/database.py
- [x] T008 [P] Create User SQLModel in backend/src/models/user.py (id, email, password_hash, created_at)
- [x] T009 [P] Create Task SQLModel in backend/src/models/task.py (id, user_id, title, description, due_date, is_completed, created_at, updated_at)
- [x] T010 [P] Create errors.py with custom exception handlers (HTTPException, RequestValidationError, generic Exception) in backend/src/errors.py
- [x] T011 [P] Create main.py with FastAPI app initialization, CORS middleware, exception handlers in backend/src/main.py
- [x] T012 [P] Add database table creation on startup in backend/src/main.py (SQLModel.metadata.create_all)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to register, login, and authenticate with JWT tokens for subsequent requests

**Independent Test**: Send POST to `/api/auth/register` and `/api/auth/login`, verify JWT token received and can be decoded to extract user ID

### Implementation for User Story 1

- [x] T013 [P] [US1] Create password.py with hash_password() and verify_password() using passlib/bcrypt in backend/src/auth/password.py
- [x] T014 [P] [US1] Create jwt.py with create_access_token() and verify_token() using python-jose in backend/src/auth/jwt.py
- [x] T015 [P] [US1] Create dependencies.py with get_current_user() FastAPI dependency in backend/src/auth/dependencies.py
- [x] T016 [P] [US1] Create auth schemas (RegisterRequest, LoginRequest, AuthResponse) in backend/src/schemas/auth.py
- [x] T017 [US1] Implement POST /api/auth/register endpoint in backend/src/routes/auth.py (validate email, check duplicates, hash password, create user, return JWT)
- [x] T018 [US1] Implement POST /api/auth/login endpoint in backend/src/routes/auth.py (lookup user, verify password, return JWT)
- [x] T019 [US1] Implement POST /api/auth/logout endpoint in backend/src/routes/auth.py (require JWT, return success message)
- [x] T020 [US1] Register auth router in backend/src/main.py with /api/auth prefix

**Checkpoint**: User Story 1 complete - authentication fully functional, all subsequent stories unblocked

---

## Phase 4: User Story 2 - Task Retrieval (Priority: P2)

**Goal**: Enable authenticated users to retrieve their tasks with strict user isolation

**Independent Test**: Send GET to `/api/tasks` with valid JWT, verify only authenticated user's tasks returned

### Implementation for User Story 2

- [x] T021 [P] [US2] Create task schemas (TaskResponse) with camelCase aliases in backend/src/schemas/task.py
- [x] T022 [US2] Implement GET /api/tasks endpoint in backend/src/routes/tasks.py (require auth, filter by user_id, return empty array if no tasks)
- [x] T023 [US2] Implement GET /api/tasks/:id endpoint in backend/src/routes/tasks.py (require auth, verify ownership, return 403/404 if not owner)
- [x] T024 [US2] Register tasks router in backend/src/main.py with /api/tasks prefix

**Checkpoint**: User Story 2 complete - users can view their task list with full user isolation

---

## Phase 5: User Story 3 - Task Creation (Priority: P3)

**Goal**: Enable authenticated users to create new tasks with validation

**Independent Test**: Send POST to `/api/tasks` with valid JWT and task data, verify task created with generated ID and timestamps

### Implementation for User Story 3

- [x] T025 [P] [US3] Add TaskCreate schema with validation (title 1-200 chars, description max 1000, dueDate ISO format) to backend/src/schemas/task.py
- [x] T026 [US3] Implement POST /api/tasks endpoint in backend/src/routes/tasks.py (require auth, validate input, generate UUID, set user_id from JWT, set timestamps, return 201)
- [x] T027 [US3] Add validation error handling for title length, description length, invalid date format in backend/src/routes/tasks.py

**Checkpoint**: User Story 3 complete - users can create tasks with instant validation feedback

---

## Phase 6: User Story 4 - Task Update (Priority: P4)

**Goal**: Enable authenticated users to update their existing tasks with partial updates

**Independent Test**: Send PUT to `/api/tasks/:id` with valid JWT and partial update, verify only provided fields updated and updatedAt refreshed

### Implementation for User Story 4

- [x] T028 [P] [US4] Add TaskUpdate schema with all optional fields to backend/src/schemas/task.py
- [x] T029 [US4] Implement PUT /api/tasks/:id endpoint in backend/src/routes/tasks.py (require auth, verify ownership, validate partial update, refresh updated_at, return 200)
- [x] T030 [US4] Add error handling for ownership violations (403) and non-existent tasks (404) in backend/src/routes/tasks.py
- [x] T031 [US4] Add validation for at least one field required in PUT request in backend/src/routes/tasks.py

**Checkpoint**: User Story 4 complete - users can edit existing tasks

---

## Phase 7: User Story 5 - Task Deletion (Priority: P5)

**Goal**: Enable authenticated users to permanently delete their tasks

**Independent Test**: Send DELETE to `/api/tasks/:id` with valid JWT, verify task removed and returns 404 on subsequent GET

### Implementation for User Story 5

- [x] T032 [US5] Implement DELETE /api/tasks/:id endpoint in backend/src/routes/tasks.py (require auth, verify ownership, delete from database, return 200 with success message)
- [x] T033 [US5] Add error handling for ownership violations (403) and non-existent tasks (404) in backend/src/routes/tasks.py

**Checkpoint**: User Story 5 complete - users can delete tasks with confirmation

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T034 [P] Add comprehensive error messages matching frontend contracts (VALIDATION_ERROR, EMAIL_EXISTS, INVALID_CREDENTIALS, UNAUTHORIZED, FORBIDDEN, NOT_FOUND, SERVER_ERROR) in backend/src/errors.py
- [x] T035 [P] Verify all responses use camelCase field names (id, userId, createdAt, updatedAt, isCompleted, dueDate) in backend/src/schemas/task.py
- [x] T036 [P] Verify all timestamps format as ISO 8601 with UTC timezone (YYYY-MM-DDTHH:MM:SSZ) in backend/src/schemas/task.py
- [x] T037 [P] Add logging for authentication failures, ownership violations, and errors in backend/src/auth/ and backend/src/routes/
- [x] T038 [P] Verify CORS configuration allows frontend origin (http://localhost:3000 for dev) in backend/src/main.py
- [x] T039 [P] Create backend/CLAUDE.md with backend-specific development guidance
- [ ] T040 [P] Verify database indexes created (users.email unique, tasks.user_id) in backend/src/models/
- [ ] T041 [P] Verify foreign key constraints and cascading deletes in backend/src/models/task.py
- [ ] T042 [P] Test all endpoints with missing JWT (expect 401) manually with curl/httpie
- [ ] T043 [P] Test all endpoints with invalid JWT (expect 401) manually with curl/httpie
- [ ] T044 [P] Test cross-user access attempts (expect 403 or 404) manually with curl/httpie
- [ ] T045 [P] Test password hashing (verify no plaintext passwords stored) by checking database
- [ ] T046 [P] Verify all 65 functional requirements implemented per spec.md
- [ ] T047 [P] Test duplicate email registration (expect 409)
- [ ] T048 [P] Test invalid email format (expect 400)
- [ ] T049 [P] Test short password (expect 400)
- [ ] T050 [P] Test task creation without title (expect 400)
- [ ] T051 [P] Test task creation with long title >200 chars (expect 422)
- [ ] T052 [P] Test task creation with long description >1000 chars (expect 422)
- [ ] T053 [P] Test task update with invalid date format (expect 422)
- [ ] T054 [P] Test empty PUT request body (expect 400)
- [ ] T055 Verify frontend can complete full user journey (register → login → create task → view → update → delete → logout)
- [ ] T056 Final code review and validation against spec.md

**Checkpoint**: Application meets all success criteria and quality standards

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) and US1 complete - Requires authentication
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) and US1 complete - Requires authentication
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) and US1 complete - Requires authentication
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) and US1 complete - Requires authentication

### Within Each User Story

- Schemas before routes (Pydantic models needed for validation)
- Auth utilities (password, JWT) before auth routes
- Models already exist (created in Foundational phase)
- Core implementation before error handling refinements
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes:
  - US1 auth utilities (T013, T014, T015, T016) can build in parallel
  - After US1 complete, US2-US5 schemas can all be created in parallel
  - US2 task retrieval endpoints can build while US3-US5 are planned
- Polish phase: All testing and validation tasks (T034-T054) can run in parallel

---

## Parallel Example: User Story 1 (Authentication)

```bash
# Phase 2 Foundational (can run in parallel):
Task: "Create config.py with environment variables" (T006)
Task: "Create database.py with SQLModel engine" (T007)
Task: "Create User SQLModel" (T008)
Task: "Create Task SQLModel" (T009)
Task: "Create error handlers" (T010)
Task: "Create main.py with FastAPI app" (T011)

# User Story 1 auth utilities (can run in parallel after Foundational):
Task: "Create password.py with hashing functions" (T013)
Task: "Create jwt.py with token functions" (T014)
Task: "Create dependencies.py with get_current_user" (T015)
Task: "Create auth schemas" (T016)

# Then sequentially:
Task: "Implement POST /api/auth/register" (T017) - depends on T013, T014, T016
Task: "Implement POST /api/auth/login" (T018) - depends on T013, T014, T016
Task: "Implement POST /api/auth/logout" (T019) - depends on T015
Task: "Register auth router" (T020) - depends on T017, T018, T019
```

---

## Parallel Example: User Stories 2-5 (After US1 Complete)

```bash
# All task-related schemas can be created in parallel:
Task: "Create TaskResponse schema" (T021) [US2]
Task: "Add TaskCreate schema" (T025) [US3]
Task: "Add TaskUpdate schema" (T028) [US4]

# Then implement endpoints sequentially per story, or parallelize across stories:
Task: "Implement GET /api/tasks" (T022) [US2]
Task: "Implement POST /api/tasks" (T026) [US3]
Task: "Implement PUT /api/tasks/:id" (T029) [US4]
Task: "Implement DELETE /api/tasks/:id" (T032) [US5]
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T012) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T013-T020)
4. **STOP and VALIDATE**: Test authentication independently (register, login, JWT verification)
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (T001-T012)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP - authentication working!)
3. Add User Story 2 → Test independently → Deploy/Demo (can now view tasks)
4. Add User Story 3 → Test independently → Deploy/Demo (can now create tasks)
5. Add User Story 4 → Test independently → Deploy/Demo (can now edit tasks)
6. Add User Story 5 → Test independently → Deploy/Demo (full CRUD complete)
7. Add Polish → Final validation → Production ready

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T012)
2. Once Foundational is done:
   - Developer A: User Story 1 (T013-T020) - Authentication
   - (After US1 complete)
   - Developer B: User Story 2 (T021-T024) - Task retrieval
   - Developer C: User Story 3 (T025-T027) - Task creation
   - Developer D: User Story 4 (T028-T031) - Task update
   - Developer E: User Story 5 (T032-T033) - Task deletion
3. Stories complete and integrate independently
4. Team runs Polish phase together (T034-T056)

---

## Task Statistics

- **Total Tasks**: 56
- **Setup Phase**: 5 tasks (T001-T005)
- **Foundational Phase**: 7 tasks (T006-T012) - BLOCKS all user stories
- **User Story 1 (Authentication)**: 8 tasks (T013-T020) - MVP
- **User Story 2 (Task Retrieval)**: 4 tasks (T021-T024)
- **User Story 3 (Task Creation)**: 3 tasks (T025-T027)
- **User Story 4 (Task Update)**: 4 tasks (T028-T031)
- **User Story 5 (Task Deletion)**: 2 tasks (T032-T033)
- **Polish Phase**: 23 tasks (T034-T056)

### Parallel Opportunities Identified

- **Phase 1 (Setup)**: 3 tasks can run in parallel (T003, T004, T005)
- **Phase 2 (Foundational)**: 6 tasks can run in parallel (T006-T011)
- **Phase 3 (US1)**: 4 tasks can run in parallel (T013-T016)
- **Phase 8 (Polish)**: 21 tasks can run in parallel (T034-T054)

### MVP Scope (User Story 1 Only)

Minimum viable product includes:
- T001-T012: Setup + Foundational (12 tasks)
- T013-T020: User Story 1 - Authentication (8 tasks)
- **Total MVP**: 20 tasks

This delivers:
- User registration with email/password
- User login with JWT token generation
- JWT verification for protected endpoints
- Secure password hashing with bcrypt
- Token expiration after 24 hours
- CORS configuration for frontend integration

---

## Notes

- [P] tasks = different files, no dependencies within the phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No tests requested - focus on implementation and manual validation
- Commit after each task or logical group of related tasks
- Stop at any checkpoint to validate story independently
- Functional requirements FR-001 through FR-065 addressed across all phases
- All 10 success criteria (SC-001 through SC-010) validated in Polish phase
- Security-first: JWT verification, password hashing, user isolation enforced throughout
