---
id: 001
title: AI Chatbot Phase III Specification
stage: spec
date: 2026-02-08
surface: agent
model: claude-opus-4-5
feature: ai-chatbot-integration
branch: 003-ai-chatbot-integration
user: Claude Sonnet 4.5
command: /sp.specify
labels: ["spec", "phase-iii", "ai-chatbot", "cohere", "mcp-tools", "conversation-persistence"]
links:
  spec: specs/003-ai-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-ai-chatbot-integration/spec.md
  - specs/003-ai-chatbot-integration/checklists/requirements.md
tests:
  - Specification quality checklist validation (all items passed)
---

## Prompt

Create complete AI Chatbot specifications for Phase III of the Todo Full-Stack Web Application using Cohere as the LLM provider

## Context
- Project: Full-stack Todo App (Phase II already completed)
- Phase III: AI Chatbot integration
- Stack:
  - Frontend: OpenAI ChatKit UI with chatbot icon integration
  - Backend: FastAPI
  - AI Framework: OpenAI Agents SDK using Cohere API instead of Gemini
  - MCP Server: Official MCP SDK
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Authentication: Better Auth (JWT-based)
- Spec-Driven Development is mandatory
- No manual coding allowed

## Objective
Define a **full specification for the AI chatbot** that:
1. Allows users to manage tasks via natural language commands.
2. Integrates seamlessly with Phase II backend.
3. Uses MCP tools to perform all task operations (add, delete, update, complete, list).
4. Persists conversation state to the database.
5. Provides a chatbot icon in the frontend UI.
6. Uses Cohere API for AI reasoning through OpenAI Agents SDK.

---

## 1. AI Agent Specification

### Role
The AI agent acts as a natural language interface to the Todo system.

### Requirements
1. Must use **Cohere** as the LLM provider.
2. Must only perform actions via MCP tools.
3. Must maintain multi-turn conversation context using database-stored messages.
4. Must provide friendly confirmations for each action.
5. Must gracefully handle errors (e.g., task not found, invalid input).

### Behavior Mapping
- User intents → Tool calls:
  - Add task → `add_task`
  - Delete task → `delete_task`
  - Update task → `update_task`
  - Complete task → `complete_task`
  - List tasks → `list_tasks`
  - User info → fetch from backend using JWT-verified user

---

## 2. MCP Tool Specification

### Tools
1. `add_task` – Create a task
2. `delete_task` – Remove a task
3. `update_task` – Update task title/description
4. `complete_task` – Mark task complete
5. `list_tasks` – Retrieve tasks for the user

### Requirements
- Tools must be **stateless**.
- Tools must **validate inputs**.
- Tools must enforce **user ownership** via JWT.
- Tools must return **structured JSON responses**.

---

## 3. Backend Chat Orchestration Specification

### Endpoint
- POST `/api/chat`

### Request Fields
- `conversation_id` (integer, optional)
- `message` (string, required)

### Response Fields
- `conversation_id` (integer)
- `response` (string)
- `tool_calls` (array of tool results)

### Behavior
1. Store user message in database.
2. Fetch conversation history for context.
3. Construct agent message array for Cohere model.
4. Run agent via OpenAI Agents SDK using Cohere.
5. Agent invokes MCP tools.
6. Store assistant response in database.
7. Return response to frontend.

---

## 4. Frontend Integration Specification

### Chat UI
- Chatbot icon always visible.
- Clicking icon opens chat window.
- Chat window uses OpenAI ChatKit frontend.
- Messages display user and assistant roles.
- Loading states and streaming responses must be handled.

### API Integration
- Chat frontend attaches JWT token to every request.
- Backend validates JWT and filters user data.
- Responses are rendered in real time.

---

## 5. Error Handling & Edge Cases

- Missing or invalid JWT → return 401 Unauthorized
- Non-existent conversation → create new conversation
- Invalid task ID → friendly error message
- AI hallucinations → prevent by forcing tool-only execution

---

## 6. Cohere Integration Guidelines

1. Use OpenAI Agents SDK with **Cohere API** instead of Gemini.
2. Load API key from environment variable `COHERE_API_KEY`.
3. Configure agent to call MCP tools as functions.
4. Enable verbose logging for debugging (optional, via `enable_verbose_stdout_logging()`).
5. Maintain stateless request-response cycle.

---

## 7. Deliverables

1. `/specs/features/ai-chatbot.md` – Full behavior specification
2. `/specs/features/mcp-tools.md` – MCP tool specification
3. `/specs/ui/chat-ui.md` – Frontend chat window and icon specification
4. Backend chat endpoint spec fully integrated with Cohere agent
5. Conversation persistence and logging rules

---

## Constraints
❌ No code
❌ No direct database manipulation by AI
❌ No bypassing MCP tools
❌ No frontend implementation outside ChatKit

## Success Criteria
- AI chatbot fully manages tasks via natural language
- Cohere-based agent is fully integrated
- Frontend displays chatbot icon and chat window
- Stateless backend handles multi-turn conversations
- MCP tools enforce task ownership and correctness

## Response snapshot

Successfully created comprehensive Phase III AI Chatbot specification in `specs/003-ai-chatbot-integration/spec.md`.

**Feature Branch**: `003-ai-chatbot-integration`

**Specification Contents**:

1. **6 Prioritized User Stories** (P1-P3):
   - P1: Natural Language Task Creation (core value)
   - P1: Task Listing and Viewing (essential read capability)
   - P2: Task Completion via Chat (basic CRUD completion)
   - P2: Task Deletion via Chat (full CRUD with confirmation)
   - P3: Task Update and Editing (advanced editing)
   - P3: Multi-Turn Conversation Context (UX enhancement)

2. **40 Functional Requirements** covering:
   - Chat UI and chatbot icon (FR-001 to FR-003)
   - Cohere and OpenAI Agents SDK integration (FR-004 to FR-005)
   - MCP tool implementation (FR-006 to FR-009)
   - AI agent behavior and safety (FR-010 to FR-014)
   - Conversation persistence (FR-015 to FR-020)
   - Backend API endpoints (FR-021 to FR-022)
   - JWT authentication and authorization (FR-023 to FR-027)
   - Frontend integration (FR-028 to FR-031)
   - Configuration and environment (FR-032 to FR-033)
   - Logging and error handling (FR-034 to FR-036)
   - Hallucination prevention (FR-037 to FR-039)
   - Stateless architecture (FR-040)

3. **4 Key Entities**:
   - Conversation (chat sessions)
   - ChatMessage (individual messages)
   - MCP Tool (callable functions)
   - ToolCall (logged invocations)

4. **14 Measurable Success Criteria**:
   - Task creation under 10 seconds
   - 95% intent interpretation accuracy
   - 2-second p95 response latency
   - Zero data loss across restarts
   - Zero hallucinations in testing
   - 100% user-friendly error messages
   - 100 concurrent sessions without degradation
   - 100% JWT enforcement
   - 100% cross-user access blocked
   - 100% conversation persistence
   - 99.5% tool invocation success
   - 100% destructive action confirmations
   - 50% faster task creation vs forms
   - 80%+ user satisfaction

5. **9 Edge Cases** covering:
   - Empty messages
   - Long task titles
   - Rapid message sending
   - JWT expiration
   - Tool failures
   - Deleted tasks
   - Non-task questions
   - Large task lists
   - Cohere API downtime

6. **Clear Scope Boundaries**:
   - 10 Assumptions (Phase II operational, Cohere rate limits, SDK compatibility, etc.)
   - 8 Dependencies (Phase II, Cohere API, SDKs, database migrations, etc.)
   - 13 Out-of-Scope items (voice, multi-language, rich media, analytics, etc.)

**Specification Quality Validation**: ✅ **ALL CHECKS PASSED**

Created `specs/003-ai-chatbot-integration/checklists/requirements.md` with comprehensive validation:
- Content Quality: 4/4 items passed
- Requirement Completeness: 8/8 items passed
- Feature Readiness: 4/4 items passed

**Zero issues found** - no spec updates required.

**Constitutional Compliance**:
- ✅ Cohere as sole LLM provider (Law VII)
- ✅ Tool-only AI behavior (Law VIII)
- ✅ Stateless architecture (Law IX)
- ✅ Conversation persistence (Law X)
- ✅ MCP tool design (Law XI)
- ✅ Error handling (Law XII)
- ✅ Hallucination prevention (Law XIII)
- ✅ Chat behavior standards (Law XIV)
- ✅ JWT authentication (Law V)
- ✅ User data isolation (Law IX)

## Outcome

- ✅ Impact: Created complete Phase III AI Chatbot specification with 6 user stories, 40 functional requirements, 14 measurable success criteria, and comprehensive edge case coverage. Specification is ready for architectural planning.
- 🧪 Tests: Specification quality checklist validation - all 16 items passed
- 📁 Files: 2 files created (spec.md, checklists/requirements.md)
- 🔁 Next prompts: `/sp.plan` to design system architecture for AI chatbot integration; `/sp.clarify` if user wants to refine scope or add clarifications; `/sp.tasks` after plan approval to generate implementation tasks
- 🧠 Reflection: This specification successfully captures all Phase III requirements from the constitution while remaining implementation-agnostic. The prioritization (P1: core CRUD, P2: full CRUD with confirmations, P3: UX enhancements) enables incremental delivery. The 40 functional requirements cover every system layer (frontend, backend, AI agent, MCP tools, database, authentication) with testable acceptance criteria. Zero clarifications needed because all technical choices (Cohere, MCP, stateless, JWT) are constitutional mandates, not spec decisions. The spec is ready for architectural design without further refinement.

## Evaluation notes (flywheel)

- Failure modes observed: None. Specification generation was successful on first attempt without requiring clarifications or revisions.
- Graders run and results (PASS/FAIL): Specification quality checklist - PASS (16/16 items, 100%). Manual constitutional compliance review - PASS (10/10 laws adhered to).
- Prompt variant (if applicable): N/A (standard /sp.specify workflow)
- Next experiment (smallest change to try): Consider adding more specific latency targets for individual MCP tool calls (currently only have overall 2s p95 latency). Could refine success criteria to include per-tool performance metrics if needed during implementation.
