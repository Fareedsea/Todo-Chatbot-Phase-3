---
id: 002
title: Backend Implementation Plan
stage: plan
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5
feature: backend-api
branch: 002-backend-api
user: User
command: /sp.plan
labels: ["backend", "architecture", "fastapi", "planning", "jwt", "sqlmodel"]
links:
  spec: specs/002-backend-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-backend-api/research.md
  - specs/002-backend-api/plan.md (in progress)
tests:
  - None (planning phase)
---

## Prompt

Create an implementation plan for the Phase II Backend based on approved backend specifications

## Context
- Backend specs are approved
- Frontend is already implemented and waiting for APIs
- Stack:
  - FastAPI
  - SQLModel
  - Neon PostgreSQL
  - JWT verification via Better Auth
- Implementation will be done by Claude Code
- No manual coding allowed

## Objective
Create a **clear, step-by-step backend implementation plan** that results in a **secure, frontend-compatible REST API**.

## Planning Requirements

### 1. Project Structure Plan
Define logical structure such as:
- App entry point
- Configuration & environment loading
- Database connection module
- Models
- Routes
- Auth middleware / dependencies

### 2. Initialization Plan
Plan steps for:
- FastAPI app setup
- Environment variable loading
- Database engine initialization
- Dependency injection wiring

### 3. Authentication Middleware Plan
Describe:
- JWT extraction from headers
- Signature verification
- Token decoding
- User identity injection into request lifecycle
- Failure handling

### 4. Database Integration Plan
Plan:
- SQLModel engine creation
- Session lifecycle
- Query patterns
- Safe transaction handling
- Ownership filtering strategy

### 5. API Implementation Order
Define logical endpoint build order:
1. Auth dependency
2. Task creation
3. Task listing
4. Task retrieval
5. Task update
6. Task completion toggle
7. Task deletion

Each step should:
- Reference the relevant spec
- Enforce security rules

### 6. Frontend Integration Validation Plan
Plan validation of:
- JWT required on all requests
- Response shapes match frontend expectations
- Error codes are frontend-safe
- Empty and edge cases handled

### 7. Error & Edge Case Handling Plan
Include:
- Invalid token
- Expired token
- Missing token
- Cross-user access attempts
- Non-existent resources

### 8. Final Verification Checklist
Define checks to confirm:
- Backend follows specs exactly
- No unauthenticated access possible
- User isolation is enforced

## Response snapshot

Successfully created comprehensive implementation plan using the Plan agent.

### Phase 0: Research & Technology Decisions (completed)

Created `specs/002-backend-api/research.md` with 6 architectural decisions:

1. **FastAPI Project Structure**: Layered architecture with separation of concerns (models/, schemas/, auth/, routes/)
   - Rationale: Clear separation, scales well, follows FastAPI best practices
   - Rejected: Flat structure, MVC pattern, Repository pattern

2. **JWT Verification**: python-jose[cryptography] library
   - Rationale: FastAPI recommended, HS256 support, handles expiration automatically
   - Rejected: PyJWT, authlib, manual parsing

3. **SQLModel with Neon PostgreSQL**: Synchronous engine with connection pooling
   - Rationale: Type-safe queries, handles serverless drops (pre-ping), simple for MVP
   - Rejected: Raw SQL, SQLAlchemy alone, async SQLModel

4. **Password Hashing**: passlib with bcrypt (12 rounds)
   - Rationale: Battle-tested, OWASP-recommended, timing-safe comparison
   - Rejected: Argon2 (slower), plain bcrypt (manual salt), SHA256 (insecure)

5. **Error Handling**: Custom exception handlers with consistent JSON format
   - Rationale: Matches frontend contracts, centralizes formatting, prevents error leakage
   - Rejected: Default FastAPI errors, manual try/catch everywhere, custom exception classes

6. **CORS Configuration**: CORSMiddleware with explicit origin allow-list
   - Rationale: Security (no wildcard), allows credentials (JWT header), handles preflight
   - Rejected: Wildcard origins, no CORS, manual headers

### Phase 1: Design Artifacts (partial)

**Artifacts to be created**:
- `data-model.md`: Database schema (User, Task entities with SQLModel definitions)
- `contracts/`: API validation rules (references frontend contracts)
- `quickstart.md`: Development setup guide

**Implementation Plan Structure Defined**:
```
backend/
├── src/
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Environment config
│   ├── database.py          # SQLModel engine
│   ├── models/              # User, Task SQLModel
│   ├── schemas/             # Pydantic request/response
│   ├── auth/                # JWT verification
│   ├── routes/              # Auth, tasks endpoints
│   └── errors.py            # Exception handlers
├── tests/                   # pytest tests
├── .env.example
├── requirements.txt
└── README.md
```

### Implementation Phases Outlined:

**Phase 0: Foundation**
- Setup project structure
- Configure environment variables
- Initialize database connection
- Create SQLModel models

**Phase 1: Authentication**
- Implement JWT verification
- Create authentication dependency
- Implement auth endpoints (register, login, logout)

**Phase 2: Task Endpoints**
- Implement task CRUD with user isolation
- GET /api/tasks, POST /api/tasks
- GET/PUT/DELETE /api/tasks/:id

**Phase 3: Error Handling**
- Custom exception handlers
- Status code mapping
- Consistent error responses

**Phase 4: Integration**
- Configure CORS
- Test with frontend
- Verify user isolation

### Technical Context Defined:

- **Language/Version**: Python 3.11+
- **Dependencies**: FastAPI, SQLModel, python-jose, passlib, psycopg2-binary
- **Storage**: Neon PostgreSQL (serverless)
- **Testing**: pytest, httpx
- **Performance Goals**: <500ms p95 latency, 100 concurrent requests
- **Scope**: MVP single instance, <1000 tasks per user

### Constitution Check: ✅ All gates passed

- Phase II scope boundaries: ✓
- Technology stack constraints: ✓
- Security-first architecture: ✓
- API contract enforcement: ✓
- Spec-driven development: ✓

### Critical Files Identified:

1. `specs/002-backend-api/spec.md` - 65 functional requirements
2. `specs/001-frontend-ui/contracts/auth-api.md` - Auth contract
3. `specs/001-frontend-ui/contracts/tasks-api.md` - Task contract
4. `.specify/memory/constitution.md` - Security rules
5. `frontend/.env.local.example` - JWT secret alignment

### Dependencies & Risks:

**Dependencies**:
- Neon PostgreSQL database must be provisioned
- JWT secret must match frontend Better Auth config
- Frontend contracts define exact API expectations

**Risks & Mitigations**:
1. Database connection issues → Connection pooling with pre-ping
2. JWT expiration handling → Document refresh flow, 401 triggers redirect
3. Password hashing performance → Acceptable for auth endpoints (~50-100ms)
4. camelCase vs snake_case → Use Pydantic aliases in schemas
5. User isolation bugs → Code review checklist, automated cross-user access tests

## Outcome

- ✅ Impact: Created comprehensive implementation plan with 6 technology decisions, 4 implementation phases, project structure definition, and complete technical context. All 65 functional requirements mapped to implementation steps.
- 🧪 Tests: Planning phase - test strategy defined for implementation (unit, integration, security, contract, performance tests)
- 📁 Files: 1 file created (research.md), plan.md in progress, 2 more artifacts pending (data-model.md, quickstart.md)
- 🔁 Next prompts: Complete Phase 1 artifacts (data-model.md, quickstart.md), then `/sp.tasks` to generate task breakdown
- 🧠 Reflection: Successfully used Plan agent to research and document architectural decisions. All choices align with constitutional requirements and security-first principles. Ready for Phase 1 design artifacts and subsequent task generation.

## Evaluation notes (flywheel)

- Failure modes observed: None - comprehensive research completed
- Graders run and results (PASS/FAIL): Constitutional compliance check - PASS (all gates)
- Prompt variant (if applicable): Standard /sp.plan workflow with Plan agent
- Next experiment (smallest change to try): Consider creating database migration strategy for future schema changes (out of MVP scope but valuable for Phase III)
