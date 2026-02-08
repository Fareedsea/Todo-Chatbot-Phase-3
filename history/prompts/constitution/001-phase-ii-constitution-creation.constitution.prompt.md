---
id: 001
title: Phase II Constitution Creation
stage: constitution
date: 2026-02-04
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: master
user: user
command: /sp.constitution
labels: ["constitution", "phase-ii", "governance", "hackathon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - (none)
---

## Prompt

Create a single governing constitution for **Phase II: Todo Full-Stack Web Application**

## Purpose
This constitution defines the **mandatory rules, constraints, and execution order** for Phase II of the Hackathon Todo project.

Phase II transforms a console-based Todo application into a **secure, multi-user, full-stack web application** using a **Spec-Driven, Agentic Development Workflow**.

This constitution is **binding** on all agents, tools, and implementations.

---

## 1. Spec-Driven Development Is Mandatory

1. No agent may write or modify code without an **approved specification**.
2. All work must follow this strict order:
3. Any attempt to skip or reorder steps is a **constitutional violation**.
4. Specs must live exclusively under `/specs/` and follow Spec-Kit Plus structure.

---

## 2. Phase II Scope Definition

### In-Scope
- Full-stack web application
- Multi-user support
- Persistent storage using Neon PostgreSQL
- JWT-based authentication
- RESTful API
- Responsive frontend UI

### Out-of-Scope
- AI features
- Chatbot functionality
- Phase III or later features
- Non-specified enhancements

Agents MUST NOT introduce out-of-scope functionality.

---

## 3. Technology Constraints (Non-Negotiable)

| Layer | Technology |
|-----|-----------|
| Frontend | Next.js 16+ (App Router) |
| Backend | FastAPI (Python) |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Auth | Better Auth + JWT |
| Specs | Spec-Kit Plus |
| Implementation | Claude Code only |

No substitutions or alternatives are permitted.

---

## 4. Monorepo & Spec-Kit Compliance

1. Project MUST use a single monorepo.
2. Specs MUST be organized as:
   - `/specs/features`
   - `/specs/api`
   - `/specs/database`
   - `/specs/ui`
3. `CLAUDE.md` files MUST exist at:
   - Root
   - `/frontend`
   - `/backend`
4. Claude Code MUST reference specs using `@specs/...`.

---

## 5. Agent Authority & Boundaries

Each agent has **exclusive authority** within its domain.

| Agent | Authority |
|-----|---------|
| Spec Writer Agent | Specifications only |
| Architecture Planner Agent | System architecture only |
| Database Engineer Agent | Schema & persistence |
| Backend Engineer Agent | FastAPI backend |
| Frontend Engineer Agent | Next.js frontend |
| Integration Tester Agent | Validation & audit |

No agent may:
- Perform another agent's role
- Modify specs outside its authority
- Implement without approval

---

## 6. Authentication & Security Laws

1. All API endpoints MUST require a valid JWT.
2. JWT tokens MUST be verified by the backend.
3. Backend MUST NOT trust user identifiers from the client.
4. Data ownership MUST be enforced at the database and API level.
5. Unauthorized requests MUST return `401 Unauthorized`.

Security is a **constitutional requirement**, not an implementation detail.

---

## 7. API Behavior Laws

1. REST API endpoints MUST match the approved API specs exactly.
2. All routes MUST be prefixed with `/api/`.
3. All responses MUST be JSON.
4. Errors MUST use proper HTTP status codes.
5. Tasks MUST always be filtered by authenticated user.

---

## 8. Implementation Laws

1. Implementation is allowed **only after**:
   - Specs are approved
   - Plan is generated
   - Tasks are broken down
2. Manual coding by humans is forbidden.
3. Claude Code MUST be used for all implementations.
4. Code MUST reflect specs exactly—no silent assumptions.

---

## 9. Testing & Validation Laws

1. Integration testing is mandatory.
2. Every feature MUST be validated end-to-end.
3. Spec deviations MUST be reported and corrected.
4. Security scenarios MUST be tested:
   - Missing JWT
   - Invalid JWT
   - Cross-user access attempts

---

## 10. Change Management

1. Any requirement change MUST begin with a spec update.
2. No code changes without updated specs.
3. Integration Tester Agent MUST revalidate after changes.

---

## 11. Phase Completion Criteria

Phase II is considered complete ONLY when:
- All Phase II specs are implemented
- Authentication is enforced everywhere
- Data persistence works correctly
- Frontend and backend integrate successfully

## Response snapshot

Created comprehensive Phase II constitution v1.0.0 with:

**Six Core Principles**:
1. Spec-Driven Development Mandate - enforces Specify → Plan → Task → Implement → Validate workflow
2. Phase II Scope Boundaries - defines in-scope (full-stack, multi-user, JWT auth) and out-of-scope (AI, chatbot)
3. Technology Stack Constraints - mandates Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth
4. Agent Authority & Separation of Concerns - defines exclusive domains for 6 specialized agents
5. Security-First Architecture - requires JWT enforcement, backend verification, data isolation
6. API Contract Enforcement - mandates /api/ prefix, JSON responses, proper status codes

**Four Governance Sections**:
- Implementation Governance (monorepo structure, execution workflow with approval gates)
- Testing & Validation Requirements (integration testing, spec compliance audits, security audits)
- Change Management Protocol (spec-first changes, version control, branching strategy)
- Phase Completion Criteria (functional, security, integration, documentation checklists)

**Constitutional Authority**:
- Supersedes all other practices
- Amendments require user approval and version increment
- Integration Tester Agent has enforcement authority

**Template Alignment**: Verified spec-template.md, plan-template.md, and tasks-template.md are consistent with constitutional principles.

## Outcome

- ✅ Impact: Established binding governance framework for Phase II development; all agents and workflows now operate under constitutional constraints
- 🧪 Tests: (none - constitutional document)
- 📁 Files: Created .specify/memory/constitution.md (v1.0.0, 380 lines)
- 🔁 Next prompts: Begin Phase II work with /sp.specify to create system architecture specification or feature specs
- 🧠 Reflection: Constitution provides clear boundaries, execution order, and approval gates. Success depends on strict adherence to spec-first workflow and agent separation of concerns.

## Evaluation notes (flywheel)

- Failure modes observed: (none yet - initial creation)
- Graders run and results (PASS/FAIL): (not applicable for constitution)
- Prompt variant (if applicable): Full constitutional framework with user-provided requirements
- Next experiment (smallest change to try): Test constitution enforcement by attempting to create first spec and validating workflow compliance
