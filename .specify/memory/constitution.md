# Full-Stack Todo Application with AI Chatbot Constitution

<!--
SYNC IMPACT REPORT
==================
Version Change: 1.0.0 → 2.0.0
Rationale: Major constitutional expansion to govern Phase III AI Chatbot integration alongside Phase II full-stack application. This is a backward-incompatible governance change that adds supreme authority rules, MCP tool protocols, and stateless AI architecture requirements.

Modified Principles:
- I. Spec-Driven Development Mandate → retained with enhanced enforcement
- II. Phase II Scope Boundaries → expanded to include Phase III scope laws
- III. Technology Stack Constraints → expanded to include AI/MCP/Cohere requirements
- V. Security-First Architecture → expanded to include AI identity and tool security
- VI. API Contract Enforcement → retained with MCP tool contract requirements

Added Principles:
- 0. Absolute Authority Rule (supreme governance)
- VII. AI Model & Provider Law (Cohere LLM mandate)
- VIII. Tool-Only AI Law (MCP tool safety)
- IX. Stateless Architecture Law (backend and conversation persistence)
- X. Conversation Persistence Law (chat history requirements)
- XI. MCP Tool Law (tool design and behavior)
- XII. Error Handling Law (graceful failure handling)
- XIII. Safety & Hallucination Prevention Law (AI safety)
- XIV. Chat Behavior & UX Law (chatbot personality and response standards)

Added Sections:
- Phase III (AI Chatbot Integration) scope boundaries
- Cohere API integration requirements
- OpenAI Agents SDK usage constraints
- MCP tool design and enforcement rules
- Conversation database schema requirements
- Phase III completion criteria

Templates Status:
⚠ spec-template.md - REQUIRES UPDATE (add MCP tool spec section)
⚠ plan-template.md - REQUIRES UPDATE (add AI architecture and stateless design sections)
⚠ tasks-template.md - REQUIRES UPDATE (add MCP tool implementation and AI integration task types)
✅ constitution.md - UPDATED

Follow-up Items:
- Update spec-template.md to include MCP tool specifications section
- Update plan-template.md to include AI agent architecture and conversation flow planning
- Update tasks-template.md to include MCP tool development and AI integration testing tasks
- Review agent-specific CLAUDE.md files to ensure Phase III agent boundaries are documented
-->

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

## 0. Absolute Authority Rule

This constitution is the **highest authority**.

If any conflict arises between:
- Agent prompts
- Specifications
- Plans
- Tasks
- Implementation decisions
- Tool behavior

➡️ **This constitution always prevails.**

**Rationale**: A single source of truth prevents contradictions, enables deterministic conflict resolution, and ensures all system components operate under unified governance.

---

## Core Principles

### I. Spec-Driven Development Mandate

**Non-Negotiable Rule**: No agent may write or modify code without an **approved specification**.

All work MUST follow this strict order:
1. **Specify** → Create or update specifications in `/specs/`
2. **Plan** → Generate architectural plan from spec
3. **Task Breakdown** → Decompose plan into executable tasks
4. **Implement** → Execute tasks using Claude Code (or equivalent agentic executor)
5. **Validate** → Integration testing and spec compliance audit

**Additional Laws**:
1. No code may be written or modified without an approved specification.
2. No specification may be implemented without an approved plan.
3. No plan may be executed without approved tasks.
4. Manual human coding is strictly forbidden.
5. Claude Code (or equivalent agentic executor) is the only implementation mechanism.

Any attempt to skip or reorder steps is a **constitutional violation**.

Violation of this order invalidates the phase.

**Rationale**: Spec-driven development ensures alignment between requirements and implementation, enables traceability, prevents scope creep through ad-hoc coding, and maintains audit trails for AI-assisted development.

---

### II. Phase Scope Laws

#### Phase II (Completed & Locked)

**In-Scope** (Mandatory):
- Full-stack web application
- Multi-user support with user isolation
- Persistent storage using Neon PostgreSQL
- JWT-based authentication via Better Auth
- RESTful API with `/api/` prefix
- Responsive frontend UI
- Task CRUD operations

⚠️ **Phase II functionality MUST NOT be broken or altered during Phase III.**

**Out-of-Scope** (Prohibited in Phase II):
- AI features
- Chatbot functionality
- Phase III or later features
- Non-specified enhancements
- Technology substitutions

---

#### Phase III (AI Chatbot Integration)

**In-Scope** (Mandatory):
- Conversational Todo management via natural language
- MCP-based tool invocation for all task operations
- Stateless chat server architecture
- Persistent conversation history in database
- Tool-only AI behavior (no direct state manipulation)
- Cohere-powered AI agent using OpenAI Agents SDK
- Integration with existing Phase II REST APIs

**Out-of-Scope** (Prohibited in Phase III):
- Breaking changes to Phase II functionality
- Direct AI manipulation of application state
- Stateful in-memory conversation storage
- Non-MCP tool interfaces
- Non-Cohere LLM providers
- Bypassing existing backend security rules

**Enforcement**: Agents MUST NOT introduce out-of-scope functionality. Any feature not explicitly listed in approved specs is prohibited. No AI feature may bypass existing backend authentication, authorization, or data isolation rules.

**Rationale**: Strict scope control prevents feature creep, maintains focus on deliverables, ensures Phase II stability during Phase III integration, and guarantees security boundaries are not compromised.

---

### III. Technology Stack Laws (Non-Negotiable)

**Mandatory Technology Requirements**:

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| Frontend UI | Next.js (App Router) | 16+ | Modern React framework with SSR/SSG |
| Chat Interface | OpenAI ChatKit | Latest | Pre-built AI chat components |
| Backend | FastAPI | Latest | High-performance Python async API |
| ORM | SQLModel | Latest | Type-safe Pydantic + SQLAlchemy |
| Database | Neon PostgreSQL | Serverless | Managed PostgreSQL with instant scaling |
| Auth | Better Auth | Latest | Modern auth library with JWT support |
| AI Agent Logic | OpenAI Agents SDK | Latest | Agent orchestration and tool calling |
| LLM Provider | Cohere API | Latest | Primary language model provider |
| Tooling Protocol | Official MCP SDK | Latest | Model Context Protocol for tool invocation |
| Specs | Spec-Kit Plus | Current | Structured specification framework |
| Implementation | Claude Code | Current | AI-assisted development tool |

**No substitutions or alternatives are permitted** without constitutional amendment.

**Rationale**: Technology constraints ensure consistent architecture, enable agent specialization, prevent integration conflicts, and maintain security guarantees. The AI stack (Cohere + OpenAI Agents SDK + MCP) is carefully selected to ensure stateless, tool-based AI behavior.

---

### IV. Agent Authority & Separation of Concerns

Each agent has **exclusive authority** within its domain:

| Agent | Authority | Boundaries |
|-------|----------|------------|
| Spec Writer Agent | Create/update specifications in `/specs/` | Cannot implement code |
| Architecture Planner Agent | System architecture design in plan.md | Cannot write specs or code |
| Database Engineer Agent | Schema design, SQLModel models, migrations | Cannot modify API or UI |
| Backend Engineer Agent | FastAPI endpoints, business logic, JWT validation | Cannot modify frontend or schema |
| Frontend Engineer Agent | Next.js UI, API client, Better Auth integration | Cannot modify backend or API contracts |
| MCP Tool Designer Agent | MCP tool specifications, stateless tool design | Cannot implement backend logic or AI agent code |
| Integration Tester Agent | End-to-end validation, spec compliance audits | Cannot implement features |

**Prohibitions** (apply to all agents):
- No agent may perform another agent's role
- No agent may modify specs outside its authority
- No agent may implement without approved specs and plan
- No agent may introduce out-of-scope technology

**Rationale**: Clear boundaries prevent conflicts, enable parallel work, ensure accountability for deliverables, and maintain separation between specification, design, and implementation concerns.

---

### V. Security-First Architecture

**Mandatory Security Requirements**:

1. **Authentication Enforcement**: All API endpoints MUST require a valid JWT token
2. **Backend Verification**: JWT tokens MUST be verified by the backend; client-provided user IDs are never trusted
3. **Data Ownership**: Backend MUST enforce user ownership at the query level (e.g., `WHERE user_id = authenticated_user.id`)
4. **Authorization Failures**: Unauthorized requests MUST return `401 Unauthorized`; forbidden access MUST return `403 Forbidden`
5. **No Trust Boundaries**: Frontend is untrusted; all validation and authorization happens on the backend
6. **AI Identity Security**: MCP tools MUST receive user identity from verified backend context, never from AI agent conversation
7. **Tool Authorization**: AI MUST NOT fabricate or guess user identity; identity is cryptographic, not conversational

**Security is a constitutional requirement, not an implementation detail.**

**Rationale**: Multi-user applications require strict isolation to prevent data leaks, unauthorized access, and privilege escalation. AI chatbot integration introduces new attack surfaces that require cryptographic identity verification at the tool invocation layer.

---

### VI. API Contract Enforcement

**Mandatory API Standards**:

1. **Spec Compliance**: REST API endpoints MUST match approved API specs exactly (path, method, request/response schemas)
2. **Route Prefix**: All routes MUST be prefixed with `/api/`
3. **Response Format**: All responses MUST be JSON with proper `Content-Type: application/json`
4. **Status Codes**: Errors MUST use proper HTTP status codes (400, 401, 403, 404, 422, 500)
5. **User Filtering**: Tasks MUST always be filtered by authenticated user (enforced at database query level)
6. **MCP Tool Contracts**: All MCP tools MUST have explicit input/output schemas validated at runtime

**Rationale**: Contract enforcement ensures frontend-backend compatibility, enables independent development, prevents runtime integration failures, and guarantees AI tool invocations conform to expected interfaces.

---

### VII. AI Model & Provider Law (Critical)

1. **Cohere is the sole LLM provider** for natural language understanding and generation.
2. OpenAI Agents SDK MAY be used for:
   - Agent orchestration
   - Tool calling logic
   - Reasoning flow management
3. **All OpenAI Agents SDK calls MUST route through Cohere's API** (no direct OpenAI API calls permitted).
4. No direct OpenAI API calls are permitted.
5. **API keys MUST be loaded from environment variables only** (never hardcoded).
6. LLM model selection MUST be configurable via environment variables.

**The AI layer is a replaceable reasoning engine, not a source of authority.**

**Rationale**: Cohere provides the required LLM capabilities while OpenAI Agents SDK provides robust tool orchestration. This separation ensures the AI provider can be swapped without rewriting agent logic. Environment-based configuration prevents credential leaks and enables deployment flexibility.

---

### VIII. Tool-Only AI Law (Core Safety Rule)

The AI assistant:
- **MUST NOT directly modify application state**
- **MUST NOT hallucinate task actions or data**
- **MUST ONLY act via MCP tools**

All task changes MUST happen through defined MCP tools:
- `add_task` – Create new tasks
- `list_tasks` – Retrieve user's tasks
- `update_task` – Modify existing tasks
- `complete_task` – Mark tasks as complete
- `delete_task` – Remove tasks

**If a tool does not exist, the AI cannot perform the action.**

The AI MUST:
- Ask for clarification when intent is ambiguous
- Confirm all destructive actions (delete, complete)
- Admit when it cannot fulfill a request without appropriate tools
- Never bypass tool invocation by directly manipulating conversation state

**Rationale**: Tool-only behavior prevents hallucinations, ensures auditability, enforces security boundaries, and guarantees all state changes are validated by backend logic. This is the core safety mechanism that prevents AI from inventing data or bypassing authorization.

---

### IX. Stateless Architecture Law

1. **The backend MUST remain stateless** (no in-memory session state).
2. No in-memory session state is allowed (conversations, user context, etc.).
3. **Conversation state MUST be persisted in the database** after every exchange.
4. Each request MUST be independently reproducible given the conversation history.
5. Any server instance MUST be able to handle any request (no session affinity required).
6. AI agent state MUST be reconstructed from database on every request.

**This ensures**:
- Horizontal scalability (add more backend instances)
- Crash resilience (server restarts don't lose conversations)
- Deterministic testing (replay conversations from database state)
- Load balancer compatibility (no sticky sessions required)

**Rationale**: Stateless architecture is a fundamental requirement for cloud-native applications. By persisting conversation history in the database, the system can scale horizontally, recover from failures, and maintain consistent behavior across multiple backend instances.

---

### X. Conversation Persistence Law

1. **Every user message MUST be stored** in the `chat_messages` table.
2. **Every assistant response MUST be stored** in the `chat_messages` table.
3. **Conversations MUST resume after server restart** by loading history from database.
4. Conversation history MUST be fetched per request (no in-memory caching).
5. The AI agent MUST receive only the minimum required context (last N messages or token-limited window).
6. **Conversation threads MUST be associated with authenticated users** (user_id foreign key).

**Database Schema Requirements**:
- `conversations` table: `id`, `user_id`, `created_at`, `updated_at`
- `chat_messages` table: `id`, `conversation_id`, `role` (user/assistant), `content`, `created_at`
- Foreign key: `chat_messages.conversation_id` → `conversations.id`
- Foreign key: `conversations.user_id` → `users.id`

**Memory is explicit and stored, never implicit.**

**Rationale**: Persistent conversation history enables multi-session interactions, crash recovery, and audit trails. By storing every message, the system can reconstruct context, debug issues, and provide continuity across user sessions.

---

### XI. MCP Tool Law

1. **MCP tools MUST be stateless** (no internal memory between invocations).
2. **MCP tools MUST be deterministic** (same input → same output).
3. **MCP tools MUST validate inputs** against declared schemas.
4. **MCP tools MUST enforce ownership rules** (user_id from authenticated context).
5. **MCP tools MUST return structured responses** (JSON schemas defined in specs).
6. MCP tools MUST NOT access global state or environment variables for user data.
7. MCP tools MUST delegate to backend APIs, not duplicate business logic.

**MCP tools are the only bridge between AI and application state.**

**Design Requirements**:
- Each tool MUST have an explicit input schema (JSON Schema format).
- Each tool MUST have an explicit output schema.
- Tools MUST accept `user_id` as a parameter (from authenticated backend context).
- Tools MUST handle errors gracefully and return structured error responses.
- Tool documentation MUST specify success cases, error cases, and edge cases.

**Rationale**: Stateless, deterministic tools ensure predictable behavior, enable testing, and prevent side effects. By enforcing ownership rules at the tool layer, the system guarantees AI agents cannot bypass security constraints.

---

### XII. Error Handling Law

1. **Errors MUST be handled gracefully** (no unhandled exceptions exposed to users).
2. Task-not-found scenarios MUST NOT crash the system (return 404 or empty list).
3. **AI MUST explain errors in human-friendly terms** (translate technical errors to natural language).
4. **Backend MUST return consistent JSON error formats**:
   ```json
   {"error": "descriptive message", "code": "ERROR_CODE"}
   ```
5. **Security-related errors MUST NOT leak details** (e.g., "Invalid credentials" not "User not found").
6. MCP tool errors MUST propagate to AI agent as structured error responses.
7. AI agent MUST retry transient errors (network timeouts) with exponential backoff.

**Rationale**: Graceful error handling improves UX, prevents information leakage, and ensures the system degrades gracefully under failure conditions. By translating technical errors to user-friendly messages, the AI assistant maintains conversational quality even when backend errors occur.

---

### XIII. Safety & Hallucination Prevention Law

1. **The AI MUST NOT invent tasks, users, or states** (only report data from tools).
2. **The AI MUST rely on tools for all factual data** (never generate task IDs or content from memory).
3. **The AI MUST admit uncertainty when required** ("I couldn't find that task" not "Task deleted").
4. **Tool invocation MUST be logged and auditable** (all tool calls recorded in database or logs).
5. AI responses MUST clearly distinguish between:
   - Confirmed actions (tool executed successfully)
   - Failed actions (tool returned error)
   - Pending actions (awaiting user confirmation)
6. AI MUST NOT cache or remember task state across conversations (always fetch fresh data).

**The system favors correctness over fluency.**

**Rationale**: Hallucination prevention is critical for task management applications where incorrect data (invented tasks, wrong IDs, fabricated completion status) causes user trust erosion. By enforcing tool-only data access and requiring explicit uncertainty admission, the system maintains factual accuracy.

---

### XIV. Chat Behavior & UX Law

The chatbot MUST:
- **Confirm all task actions** ("I've added 'Buy groceries' to your todo list")
- Use **clear, friendly, professional language** (avoid jargon, explain technical errors)
- **Gracefully handle errors** (explain what went wrong, suggest next steps)
- **Ask for clarification when intent is ambiguous** ("Did you mean task #3 or task #13?")
- **Never expose internal errors, stack traces, or secrets** (sanitize all error messages)
- Maintain conversation context across multiple turns (reference previous messages)
- Use natural language for task descriptions (don't require JSON formatting from users)

**The chatbot is an assistant, not an authority.**

**Prohibited Behaviors**:
- Assuming user intent without clarification
- Executing destructive actions without confirmation
- Exposing database schema or internal IDs in responses
- Using technical jargon without explanation
- Fabricating task data or status

**Rationale**: UX quality determines chatbot adoption. By enforcing conversational norms, error explanations, and confirmation patterns, the system provides a trustworthy and user-friendly AI assistant.

---

## Implementation Governance

### Monorepo & Spec-Kit Compliance

**Repository Structure** (Mandatory):

```
/                           # Monorepo root
├── specs/                  # All specifications (Spec-Kit Plus)
│   ├── features/          # Feature specifications
│   ├── api/               # API endpoint contracts
│   ├── database/          # Schema definitions
│   ├── ui/                # UI component specs
│   └── mcp/               # MCP tool specifications (Phase III)
├── backend/               # FastAPI application
│   ├── src/
│   │   ├── mcp/          # MCP tool implementations
│   │   ├── chat/         # Chat and conversation logic
│   │   └── agents/       # AI agent orchestration
│   ├── tests/
│   └── CLAUDE.md         # Backend-specific guidance
├── frontend/              # Next.js application
│   ├── src/
│   │   ├── components/   # UI components
│   │   └── chat/         # ChatKit integration
│   ├── tests/
│   └── CLAUDE.md         # Frontend-specific guidance
└── CLAUDE.md             # Root project guidance
```

**Spec Organization Rules**:
1. All specs MUST live under `/specs/` (never in code directories)
2. Spec subdirectories MUST follow Spec-Kit Plus conventions
3. Claude Code MUST reference specs using `@specs/...` syntax
4. Each workspace (backend, frontend) MUST have local `CLAUDE.md` with agent-specific guidance
5. MCP tool specs MUST live under `/specs/mcp/` with schemas and behavior documentation

**Rationale**: Consistent structure enables agent navigation, supports monorepo tooling, separates specification from implementation, and provides clear boundaries for Phase III AI chatbot artifacts.

---

### Execution Order & Approval Gates

**Mandatory Workflow** (violations block progress):

```
┌─────────────┐
│   Specify   │  Spec Writer Agent creates specifications
└──────┬──────┘
       │ ✓ Spec Approved
       ▼
┌─────────────┐
│    Plan     │  Architecture Planner generates design
└──────┬──────┘
       │ ✓ Plan Approved
       ▼
┌─────────────┐
│ Task Break  │  Generate tasks.md from plan
└──────┬──────┘
       │ ✓ Tasks Approved
       ▼
┌─────────────┐
│  Implement  │  Backend/Frontend/Database/MCP Tool agents execute
└──────┬──────┘
       │ ✓ Implementation Complete
       ▼
┌─────────────┐
│  Validate   │  Integration Tester audits & verifies
└─────────────┘
```

**Approval Authority**:
- Spec approval: User or designated reviewer
- Plan approval: User or tech lead
- Task approval: Automatic (if generated from approved plan)
- Implementation approval: Integration Tester Agent

**Rationale**: Phased approval gates prevent rework, ensure alignment, maintain traceability, and enforce constitutional compliance at every stage.

---

## Testing & Validation Requirements

### Mandatory Testing

**Integration Testing** (Non-Negotiable):
1. Every feature MUST be validated end-to-end before marking complete
2. Spec deviations MUST be reported and corrected (no silent drifts)
3. **Security scenarios MUST be tested**:
   - Missing JWT → `401 Unauthorized`
   - Invalid JWT → `401 Unauthorized`
   - Cross-user access attempts → `403 Forbidden` or filtered results
   - Expired JWT → `401 Unauthorized`
4. **Phase III AI chatbot scenarios MUST be tested**:
   - AI → MCP tool → Backend → Database → Response (full integration)
   - Stateless behavior (conversation resume after restart)
   - Security boundaries (AI cannot bypass authentication)
   - Hallucination prevention (AI does not invent tasks)
   - Tool error handling (graceful failures)

**Test Execution Authority**: Integration Tester Agent

**Acceptance Criteria**:
- All API endpoints respond per spec
- Authentication is enforced everywhere
- User data isolation is verified
- Frontend successfully communicates with backend
- Error handling matches specification
- Chatbot correctly invokes MCP tools for all task operations
- Conversations persist and resume correctly
- AI responses are factually accurate (no hallucinations)

**Rationale**: Integration testing catches contract mismatches, security gaps, spec deviations, and AI behavior issues before deployment. Phase III adds critical requirements for stateless conversation handling and tool-based AI safety.

---

### Validation Protocols

**Spec Compliance Audit**:
1. Compare implemented API contracts against `/specs/api/`
2. Verify database schema matches `/specs/database/`
3. Confirm UI behavior matches `/specs/ui/`
4. Verify MCP tool behavior matches `/specs/mcp/`
5. Report deviations with severity (Critical, Major, Minor)

**Security Audit**:
1. Test all endpoints without JWT → expect `401`
2. Test all endpoints with invalid JWT → expect `401`
3. Attempt cross-user access → expect `403` or empty results
4. Verify user filtering in all queries
5. Verify MCP tools enforce user ownership rules
6. Test AI agent cannot bypass authentication via conversation manipulation

**AI Safety Audit** (Phase III):
1. Verify AI only acts via MCP tools (no direct state manipulation)
2. Test hallucination scenarios (AI asked about non-existent tasks)
3. Verify conversation persistence (restart server, resume conversation)
4. Test stateless behavior (same conversation history → same AI response)
5. Verify tool invocation logging and auditability

**Rationale**: Systematic audits ensure implementation fidelity, prevent security vulnerabilities, and validate AI safety guarantees. Phase III introduces AI-specific validation requirements that are critical for trust and correctness.

---

## Change Management Protocol

### Spec-First Change Process

**Any requirement change MUST follow this process**:

1. **Identify Change**: Document requested change and rationale
2. **Update Spec**: Spec Writer Agent updates relevant spec in `/specs/`
3. **Update Plan**: Architecture Planner revises plan.md if architectural impact
4. **Update Tasks**: Regenerate tasks.md if task breakdown changes
5. **Implement**: Backend/Frontend/MCP Tool agents execute updated tasks
6. **Revalidate**: Integration Tester Agent re-runs full test suite

**Prohibited Actions**:
- No code changes without updated specs
- No "quick fixes" that bypass spec updates
- No spec updates without user approval
- No Phase III changes that break Phase II functionality

**Rationale**: Spec-first changes maintain traceability, prevent drift, ensure all artifacts stay synchronized, and protect Phase II stability during Phase III integration.

---

### Version Control & Branching

**Branch Strategy**:
- `main` or `master`: Production-ready code only (Phase II complete)
- Feature branches: `###-feature-name` (e.g., `001-authentication`, `003-ai-chatbot`)
- Spec changes: Commit to feature branch alongside code
- Phase III work: Separate feature branch until integration complete

**Commit Standards**:
- Prefix: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
- Include spec reference: `feat: implement MCP add_task tool (per @specs/mcp/add-task.md)`
- Co-authored by: `Co-Authored-By: Claude Code <noreply@anthropic.com>`

**Rationale**: Structured branching and commits enable traceability, rollback, and clear separation between Phase II (stable) and Phase III (integration) work.

---

## Phase Completion Criteria

### Phase II Completion (Locked)

Phase II is considered **complete** and locked. The following criteria were met:

#### Functional Completeness
- [x] All Phase II specs are implemented per approved specifications
- [x] Authentication flow is complete (register, login, logout, token refresh)
- [x] Task CRUD operations work (create, read, update, delete)
- [x] User data isolation is enforced (users only see their own tasks)
- [x] Data persistence works correctly (Neon PostgreSQL)
- [x] Frontend and backend communicate successfully

#### Security Validation
- [x] All API endpoints require valid JWT
- [x] JWT verification is backend-enforced
- [x] Cross-user access is prevented
- [x] Unauthorized requests return proper status codes

#### Integration Validation
- [x] Integration Tester Agent has completed full audit
- [x] No critical or major spec deviations remain
- [x] All security tests pass
- [x] Frontend-backend contracts validated

#### Documentation Completeness
- [x] All specs in `/specs/` are current and approved
- [x] Architecture plan matches implementation
- [x] CLAUDE.md files are accurate for each workspace

---

### Phase III Completion Criteria

Phase III is considered **complete** ONLY when:

#### AI Chatbot Integration
- [ ] Chatbot manages todos fully via natural language
- [ ] User can create, read, update, complete, and delete tasks through conversation
- [ ] AI asks for clarification when intent is ambiguous
- [ ] AI confirms all destructive actions before executing

#### MCP Tool Implementation
- [ ] All MCP tools handle state changes (add_task, list_tasks, update_task, complete_task, delete_task)
- [ ] MCP tools are stateless and deterministic
- [ ] MCP tools enforce user ownership rules
- [ ] MCP tools validate inputs and return structured outputs
- [ ] Tool invocation is logged and auditable

#### Conversation Persistence
- [ ] Conversations persist across server restarts
- [ ] Conversation history is fetched from database per request
- [ ] AI agent receives minimum required context
- [ ] Conversation threads are associated with authenticated users

#### Security & Isolation
- [ ] AI cannot bypass authentication via conversation manipulation
- [ ] MCP tools receive user identity from verified backend context
- [ ] Cross-user conversation access is prevented
- [ ] AI respects same authorization rules as REST APIs

#### AI Behavior & Safety
- [ ] Cohere-powered AI behaves deterministically (same history → same response pattern)
- [ ] AI does not hallucinate tasks, users, or states
- [ ] AI relies on tools for all factual data
- [ ] AI admits uncertainty when tools fail or return errors
- [ ] AI translates technical errors to user-friendly messages

#### Stateless Architecture
- [ ] Backend remains stateless (no in-memory conversation storage)
- [ ] Any server instance can handle any request
- [ ] Conversation state is reconstructed from database on every request
- [ ] System scales horizontally without session affinity

#### Integration Validation
- [ ] End-to-end integration testing validates AI → MCP → Backend → DB → Response flow
- [ ] Stateless behavior is proven (restart server, resume conversation)
- [ ] Security boundaries are tested (AI cannot bypass auth)
- [ ] Spec deviations are corrected
- [ ] No constitutional violations remain

#### Phase II Compatibility
- [ ] All Phase II functionality remains operational
- [ ] REST API endpoints continue to work
- [ ] Frontend UI continues to work
- [ ] No breaking changes to Phase II architecture

**Rationale**: Clear completion criteria prevent premature deployment, ensure all constitutional requirements are met, and validate both AI behavior and system integration quality.

---

## Governance

### Constitutional Authority

1. **Supremacy**: This constitution supersedes all other practices, conventions, and informal agreements
2. **Amendments**: Require explicit user approval and version increment (semantic versioning)
3. **Compliance**: All PRs and reviews MUST verify constitutional compliance
4. **Justification**: Complexity or deviations MUST be justified in plan.md "Complexity Tracking" section
5. **Enforcement**: Integration Tester Agent has authority to block non-compliant implementations

### Amendment Process

**To amend this constitution**:
1. Propose change with rationale
2. Update this document via `/sp.constitution` command
3. Increment version per semantic versioning rules:
   - **MAJOR**: Backward-incompatible governance/principle removals or redefinitions
   - **MINOR**: New principle/section added or materially expanded guidance
   - **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements
4. Propagate changes to dependent templates (spec, plan, tasks, commands)
5. Notify all agents of constitutional updates

### Versioning Policy

**Current Version**: 2.0.0
**Ratified**: 2026-02-04 (Phase II)
**Last Amended**: 2026-02-08 (Phase III expansion)

**Version History**:
- **2.0.0** (2026-02-08): Major expansion to govern Phase III AI Chatbot integration. Added supreme authority rule, AI model law, tool-only AI law, stateless architecture law, conversation persistence law, MCP tool law, error handling law, safety & hallucination prevention law, and chat behavior law. Expanded technology stack, security, and testing requirements for AI integration.
- **1.0.0** (2026-02-04): Initial constitution for Phase II Hackathon Todo project. Established spec-driven development mandate, phase scope boundaries, technology stack constraints, agent authority, security-first architecture, and API contract enforcement.

### Runtime Guidance

**For operational development guidance**, refer to:
- Root: `CLAUDE.md` (project-level guidance)
- Backend: `backend/CLAUDE.md` (FastAPI-specific guidance)
- Frontend: `frontend/CLAUDE.md` (Next.js-specific guidance)

**For architectural decisions**, document in:
- `history/adr/` (Architecture Decision Records)

**For prompt history**, store in:
- `history/prompts/` (Prompt History Records)

---

## Final Clause

This constitution defines the **soul of the system**.

Anything not explicitly permitted here is **forbidden by default**.

All agents, tools, specifications, plans, tasks, and implementations are bound by these laws.

Violations are not bugs—they are constitutional violations requiring immediate remediation.

**The constitution is supreme. The constitution is law.**
