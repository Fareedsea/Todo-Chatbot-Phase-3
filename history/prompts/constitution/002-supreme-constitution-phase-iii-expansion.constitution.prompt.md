---
id: 002
title: Supreme Constitution Phase III Expansion
stage: constitution
date: 2026-02-08
surface: agent
model: claude-opus-4-5
feature: none
branch: 002-backend-api
user: Claude Sonnet 4.5
command: /sp.constitution
labels: ["constitution", "phase-iii", "governance", "ai-chatbot", "mcp-tools"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - None (constitutional governance change)
---

## Prompt

Create a single, supreme constitution governing the Full-Stack Todo Application with AI Chatbot (Phase II + Phase III)

## Purpose
This constitution defines the **highest, non-negotiable laws** governing the design, specification, planning, implementation, and validation of a **secure, stateless, AI-powered Todo application**.

The system includes:
- A production-grade full-stack Todo app (Phase II)
- An AI chatbot interface powered by MCP and OpenAI Agents SDK (Phase III)
- Cohere as the underlying LLM provider
- A FastAPI backend integrated with Neon PostgreSQL
- JWT-based authentication using Better Auth

This constitution applies to **all agents, specs, plans, tasks, tools, and implementations**.

---

## 1. Absolute Authority Rule

This constitution is the **highest authority**.

If any conflict arises between:
- Agent prompts
- Specifications
- Plans
- Tasks
- Implementation decisions
- Tool behavior

➡️ **This constitution always prevails.**

---

## 2. Spec-Driven Development Is Mandatory

All work MUST follow this order without exception:

### Laws
1. No code may be written or modified without an approved specification.
2. No specification may be implemented without an approved plan.
3. No plan may be executed without approved tasks.
4. Manual human coding is strictly forbidden.
5. Claude Code (or equivalent agentic executor) is the only implementation mechanism.

Violation of this order invalidates the phase.

---

## 3. Phase Scope Laws

### Phase II (Completed & Locked)
- Full-stack Todo application
- REST APIs
- JWT authentication
- Neon PostgreSQL persistence
- Frontend UI

⚠️ Phase II functionality MUST NOT be broken or altered during Phase III.

---

### Phase III (AI Chatbot Integration)
- Conversational Todo management
- MCP-based tool invocation
- Stateless chat server
- Persistent conversation history
- Tool-only AI behavior

No AI feature may bypass existing backend rules.

---

## 4. Technology Stack Laws (Non-Negotiable)

| Layer | Technology |
|-----|-----------|
| Frontend UI | Next.js + OpenAI ChatKit |
| Backend | Python FastAPI |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth (JWT) |
| AI Agent Logic | OpenAI Agents SDK |
| LLM Provider | Cohere API |
| Tooling Protocol | Official MCP SDK |
| Specs | Spec-Kit Plus |

No substitutions are permitted without constitutional amendment.

---

## 5. AI Model & Provider Law (Critical)

1. **Cohere is the sole LLM provider**.
2. OpenAI Agents SDK MAY be used for:
   - Agent orchestration
   - Tool calling
   - Reasoning flow
3. All OpenAI Agents SDK calls MUST route through Cohere's API.
4. No direct OpenAI API calls are permitted.
5. API keys MUST be loaded from environment variables only.

The AI layer is a **replaceable reasoning engine**, not a source of authority.

---

## 6. Tool-Only AI Law (Core Safety Rule)

The AI assistant:
- MUST NOT directly modify application state
- MUST NOT hallucinate task actions
- MUST ONLY act via MCP tools

All task changes MUST happen through:
- add_task
- list_tasks
- update_task
- complete_task
- delete_task

If a tool does not exist, the AI **cannot perform the action**.

---

## 7. Stateless Architecture Law

1. The backend MUST remain stateless.
2. No in-memory session state is allowed.
3. Conversation state MUST be persisted in the database.
4. Each request MUST be independently reproducible.
5. Any server instance MUST be able to handle any request.

This ensures:
- Horizontal scalability
- Crash resilience
- Deterministic testing

---

## 8. Authentication & Identity Law

1. All requests MUST be authenticated via JWT.
2. JWT verification MUST occur on every request.
3. User identity MUST be derived from the JWT — never from client input.
4. MCP tools MUST receive user identity from verified backend context.
5. AI MUST NOT fabricate or guess user identity.

User identity is **cryptographic**, not conversational.

---

## 9. Data Ownership & Isolation Law

1. Every task, conversation, and message MUST belong to a single user.
2. Cross-user data access is strictly forbidden.
3. All database queries MUST be filtered by authenticated user.
4. Unauthorized access MUST return 401 or 403.
5. AI agents MUST NEVER see data belonging to another user.

This applies equally to:
- REST APIs
- MCP tools
- Chat flows

---

## 10. Chat Behavior & UX Law

The chatbot MUST:
- Confirm all task actions
- Use clear, friendly, professional language
- Gracefully handle errors
- Ask for clarification when intent is ambiguous
- Never expose internal errors, stack traces, or secrets

The chatbot is an **assistant**, not an authority.

---

## 11. Conversation Persistence Law

1. Every user message MUST be stored.
2. Every assistant response MUST be stored.
3. Conversations MUST resume after server restart.
4. Conversation history MUST be fetched per request.
5. The AI agent MUST receive only the minimum required context.

Memory is **explicit and stored**, never implicit.

---

## 12. MCP Tool Law

1. MCP tools MUST be stateless.
2. MCP tools MUST be deterministic.
3. MCP tools MUST validate inputs.
4. MCP tools MUST enforce ownership rules.
5. MCP tools MUST return structured responses.

MCP tools are the **only bridge** between AI and application state.

---

## 13. Error Handling Law

1. Errors MUST be handled gracefully.
2. Task-not-found scenarios MUST NOT crash the system.
3. AI MUST explain errors in human-friendly terms.
4. Backend MUST return consistent JSON error formats.
5. Security-related errors MUST NOT leak details.

---

## 14. Safety & Hallucination Prevention Law

1. The AI MUST NOT invent tasks, users, or states.
2. The AI MUST rely on tools for all factual data.
3. The AI MUST admit uncertainty when required.
4. Tool invocation MUST be logged and auditable.

The system favors **correctness over fluency**.

---

## 15. Integration & Testing Law

1. End-to-end integration testing is mandatory.
2. AI → MCP → Backend → DB → Response must be validated.
3. Stateless behavior must be proven.
4. Security boundaries must be tested.
5. Spec deviations MUST be corrected before acceptance.

---

## 16. Completion Criteria (Phase III)

Phase III is considered complete ONLY when:
- Chatbot manages todos fully via natural language
- MCP tools handle all state changes
- Conversations persist across restarts
- Security & isolation are enforced
- Cohere-powered AI behaves deterministically
- No constitutional violations remain

---

## Final Clause

This constitution defines the **soul of the system**.

Anything not explicitly permitted here is **forbidden by default**.

## Response snapshot

Constitution successfully updated from v1.0.0 to v2.0.0.

**Major Constitutional Expansion**: This is a backward-incompatible governance change that expands the Phase II constitution to govern Phase III AI Chatbot integration.

**Key Changes**:

1. **Added Absolute Authority Rule (Principle 0)** - Establishes this constitution as supreme law over all other artifacts
2. **Expanded Phase Scope Laws** - Added Phase III scope boundaries while locking Phase II as complete and immutable
3. **Expanded Technology Stack** - Added AI/MCP/Cohere requirements (OpenAI Agents SDK, Cohere API, MCP SDK, ChatKit)
4. **Added 8 New Core Principles**:
   - VII. AI Model & Provider Law (Cohere mandate, no direct OpenAI calls)
   - VIII. Tool-Only AI Law (MCP tools only, no direct state manipulation)
   - IX. Stateless Architecture Law (backend statelessness, conversation persistence)
   - X. Conversation Persistence Law (database storage, crash recovery)
   - XI. MCP Tool Law (stateless, deterministic, validated tools)
   - XII. Error Handling Law (graceful failures, user-friendly messages)
   - XIII. Safety & Hallucination Prevention Law (tool-based facts only)
   - XIV. Chat Behavior & UX Law (confirmations, clarity, professional tone)

5. **Enhanced Security Requirements** - Extended to include AI identity security and MCP tool authorization
6. **Enhanced Testing Requirements** - Added AI safety audits, stateless behavior validation, hallucination prevention tests
7. **Added Phase III Completion Criteria** - 6 categories covering AI chatbot, MCP tools, conversations, security, AI behavior, stateless architecture

**Database Schema Requirements Added**:
- `conversations` table with user_id foreign key
- `chat_messages` table with conversation_id foreign key and role (user/assistant)

**Repository Structure Expanded**:
- Added `/specs/mcp/` for MCP tool specifications
- Added `backend/src/mcp/` for tool implementations
- Added `backend/src/chat/` for conversation logic
- Added `backend/src/agents/` for AI orchestration
- Added `frontend/src/chat/` for ChatKit integration

**Version History Created**:
- v1.0.0 (2026-02-04): Initial Phase II constitution
- v2.0.0 (2026-02-08): Phase III expansion with AI chatbot governance

## Outcome

- ✅ Impact: Constitutional expansion from Phase II to Phase II+III governance. Established supreme authority rule, 8 new core principles for AI safety, stateless architecture, MCP tool protocols, and comprehensive Phase III completion criteria.
- 🧪 Tests: None (constitutional governance document)
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: Update spec-template.md to add MCP tool specifications section; Update plan-template.md to add AI architecture and stateless design sections; Update tasks-template.md to add MCP tool implementation and AI integration testing task types; Begin Phase III specification work using /sp.specify
- 🧠 Reflection: This constitutional amendment successfully unifies Phase II and Phase III governance under a single supreme law. The addition of the Absolute Authority Rule ensures conflict resolution. The Tool-Only AI Law and Stateless Architecture Law are the critical safety mechanisms that prevent hallucinations and ensure scalability. The conversation persistence requirements enable crash recovery while maintaining statelessness. All Phase III requirements are now formally codified and enforceable.

## Evaluation notes (flywheel)

- Failure modes observed: None. Constitutional structure is comprehensive and addresses all known requirements.
- Graders run and results (PASS/FAIL): Manual review - PASS (all requirements captured, no contradictions, clear enforcement mechanisms)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Monitor for constitutional conflicts during Phase III implementation. If conflicts arise, create PATCH amendments to clarify ambiguous rules.
