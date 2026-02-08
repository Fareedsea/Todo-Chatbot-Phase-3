# Tasks: AI Chatbot for Todo Management (Phase III)

**Input**: Design documents from `/specs/003-ai-chatbot-integration/`
**Prerequisites**: plan.md (complete), spec.md (complete)

**Tests**: Not explicitly requested in specification - test tasks omitted per constitutional guidance

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/` (monorepo structure)
- **Database**: `database/migrations/` for SQL migration scripts
- All paths relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation for Phase III

- [ ] T001 Install OpenAI Agents SDK in backend/requirements.txt
- [ ] T002 [P] Install official MCP SDK in backend/requirements.txt
- [ ] T003 [P] Install httpx (Cohere API client) in backend/requirements.txt
- [ ] T004 [P] Install OpenAI ChatKit in frontend/package.json
- [ ] T005 Create backend/src/mcp/ directory structure (server.py, tools/, schemas.py)
- [ ] T006 [P] Create backend/src/chat/ directory structure (agent.py, orchestrator.py, history.py)
- [ ] T007 [P] Create frontend/src/chat/ directory structure (ChatbotIcon.tsx, ChatWindow.tsx, useChatClient.ts)
- [ ] T008 [P] Create database/migrations/ directory if not exists
- [ ] T009 Configure environment variables in backend/.env.example (COHERE_API_KEY, COHERE_MODEL)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core database and authentication infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Foundation

- [X] T010 Create database migration 003_create_conversations_table.sql in database/migrations/ (id, user_id FK, created_at, updated_at, index on user_id)
- [X] T011 Create database migration 004_create_chat_messages_table.sql in database/migrations/ (id, conversation_id FK, role enum, content text, created_at, index on conversation_id + created_at)
- [X] T012 Run database migrations to create conversations and chat_messages tables
- [X] T013 [P] Create Conversation SQLModel in backend/src/models/conversation.py (fields: id, user_id, created_at, updated_at, relationship to User and ChatMessage)
- [X] T014 [P] Create ChatMessage SQLModel in backend/src/models/chat_message.py (fields: id, conversation_id, role enum, content, created_at, relationship to Conversation)

### Authentication Foundation

- [ ] T015 Verify existing JWT verification dependency in backend/src/auth/jwt.py extracts user_id from token
- [ ] T016 Create JWT dependency for chat endpoint in backend/src/routes/chat.py (get_current_user_from_jwt)

### MCP Tool Infrastructure

- [X] T017 Initialize MCP server in backend/src/mcp/server.py (import MCP SDK, create server instance)
- [X] T018 Define MCP tool input/output schemas in backend/src/mcp/schemas.py (AddTaskInput, ListTasksInput, UpdateTaskInput, CompleteTaskInput, DeleteTaskInput, ToolResponse)
- [ ] T019 Register MCP server with FastAPI app in backend/src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks by typing natural language commands into the chatbot

**Independent Test**: Send message "Add buy groceries to my todo list" and verify task appears in task list with chatbot confirmation

### MCP Tool: add_task (US1)

- [ ] T020 [P] [US1] Implement add_task MCP tool in backend/src/mcp/tools/add_task.py (accept title and user_id, validate inputs against schema, call existing task creation API, return structured response)
- [ ] T021 [P] [US1] Register add_task tool with MCP server in backend/src/mcp/server.py

### AI Agent Configuration (US1)

- [ ] T022 [US1] Configure Cohere API client in backend/src/chat/agent.py (load COHERE_API_KEY from env, set base_url for OpenAI Agents SDK, configure model)
- [ ] T023 [US1] Create system prompt for AI agent in backend/src/chat/agent.py (tool-only behavior, friendly confirmations, clarification requests, hallucination prevention instructions)
- [ ] T024 [US1] Initialize OpenAI Agents SDK agent in backend/src/chat/agent.py (register add_task tool, configure Cohere LLM, set system prompt)

### Conversation Management (US1)

- [ ] T025 [P] [US1] Implement conversation history fetch in backend/src/chat/history.py (query conversations and chat_messages, limit to last 20 messages, order by created_at)
- [ ] T026 [P] [US1] Implement message persistence in backend/src/chat/history.py (save user message, save assistant response, update conversation timestamp)

### Chat Orchestration (US1)

- [ ] T027 [US1] Implement chat request lifecycle in backend/src/chat/orchestrator.py (fetch history, build agent message array, invoke agent with Cohere, persist messages, return response)
- [ ] T028 [US1] Create POST /api/chat endpoint in backend/src/routes/chat.py (validate JWT, parse request body, call orchestrator, return structured response)
- [ ] T029 [US1] Handle conversation creation in backend/src/chat/orchestrator.py (if conversation_id null, create new conversation for user)

### Frontend Chat UI (US1)

- [ ] T030 [P] [US1] Create ChatbotIcon component in frontend/src/chat/ChatbotIcon.tsx (floating button, click handler to toggle chat window)
- [ ] T031 [P] [US1] Create ChatWindow component in frontend/src/chat/ChatWindow.tsx (integrate OpenAI ChatKit, message display, input field, send button)
- [ ] T032 [US1] Create useChatClient hook in frontend/src/chat/useChatClient.ts (API client for POST /api/chat, attach JWT token, handle responses)
- [ ] T033 [US1] Add ChatbotIcon to root layout in frontend/src/app/layout.tsx (always visible for authenticated users)

### Error Handling (US1)

- [ ] T034 [US1] Implement error translation in backend/src/chat/agent.py (catch MCP tool errors, translate to user-friendly messages, return gracefully)
- [ ] T035 [US1] Handle authentication errors in frontend/src/chat/useChatClient.ts (detect 401, prompt user to refresh page)

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create tasks via natural language and see confirmation

---

## Phase 4: User Story 2 - Task Listing and Viewing (Priority: P1)

**Goal**: Enable users to view their tasks by asking natural language questions

**Independent Test**: Ask "What's on my todo list?" and verify chatbot returns correct tasks for authenticated user

### MCP Tool: list_tasks (US2)

- [ ] T036 [P] [US2] Implement list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py (accept user_id and optional completed filter, query tasks from database, return structured array)
- [ ] T037 [P] [US2] Register list_tasks tool with MCP server in backend/src/mcp/server.py

### AI Agent Enhancement (US2)

- [ ] T038 [US2] Update AI agent system prompt in backend/src/chat/agent.py (add instructions for listing tasks, handling empty task lists, offering to add tasks)
- [ ] T039 [US2] Register list_tasks tool with agent in backend/src/chat/agent.py

### Frontend Enhancement (US2)

- [ ] T040 [US2] Enhance ChatWindow component in frontend/src/chat/ChatWindow.tsx (render task lists in formatted manner, support markdown or structured display)

**Checkpoint**: At this point, User Story 2 should be fully functional - users can view tasks conversationally and get helpful responses for empty lists

---

## Phase 5: User Story 3 - Task Completion via Chat (Priority: P2)

**Goal**: Enable users to mark tasks as complete by telling the chatbot

**Independent Test**: Say "Mark 'buy groceries' as done" and verify task status updates correctly with confirmation

### MCP Tool: complete_task (US3)

- [ ] T041 [P] [US3] Implement complete_task MCP tool in backend/src/mcp/tools/complete_task.py (accept task_id and user_id, validate ownership, update task status, return updated task)
- [ ] T042 [P] [US3] Register complete_task tool with MCP server in backend/src/mcp/server.py

### AI Agent Enhancement (US3)

- [ ] T043 [US3] Update AI agent system prompt in backend/src/chat/agent.py (add confirmation pattern for destructive actions, request clarification for ambiguous task references)
- [ ] T044 [US3] Register complete_task tool with agent in backend/src/chat/agent.py

### Error Handling (US3)

- [ ] T045 [US3] Implement task-not-found handling in backend/src/mcp/tools/complete_task.py (return structured error if task doesn't exist or belongs to another user)
- [ ] T046 [US3] Update error translation in backend/src/chat/agent.py (translate task-not-found errors to friendly messages like "I couldn't find that task")

**Checkpoint**: At this point, User Story 3 should be fully functional - users can complete tasks with confirmation and get helpful error messages

---

## Phase 6: User Story 4 - Task Deletion via Chat (Priority: P2)

**Goal**: Enable users to delete tasks by asking the chatbot

**Independent Test**: Say "Delete 'buy groceries'" and verify task is removed after confirmation

### MCP Tool: delete_task (US4)

- [ ] T047 [P] [US4] Implement delete_task MCP tool in backend/src/mcp/tools/delete_task.py (accept task_id and user_id, validate ownership, delete task, return success message)
- [ ] T048 [P] [US4] Register delete_task tool with MCP server in backend/src/mcp/server.py

### AI Agent Enhancement (US4)

- [ ] T049 [US4] Update AI agent system prompt in backend/src/chat/agent.py (add explicit confirmation requirement for delete actions, wait for "yes" confirmation)
- [ ] T050 [US4] Register delete_task tool with agent in backend/src/chat/agent.py

### Confirmation Flow (US4)

- [ ] T051 [US4] Implement multi-turn confirmation handling in backend/src/chat/orchestrator.py (maintain confirmation state in conversation history, detect "yes"/"no"/"cancel" responses)

**Checkpoint**: At this point, User Story 4 should be fully functional - users can delete tasks with explicit confirmation and option to cancel

---

## Phase 7: User Story 5 - Task Update and Editing (Priority: P3)

**Goal**: Enable users to update task titles or descriptions by telling the chatbot

**Independent Test**: Say "Change 'buy groceries' to 'buy groceries and milk'" and verify task title updates correctly

### MCP Tool: update_task (US5)

- [ ] T052 [P] [US5] Implement update_task MCP tool in backend/src/mcp/tools/update_task.py (accept task_id, title, user_id, validate ownership, update task, return updated task)
- [ ] T053 [P] [US5] Register update_task tool with MCP server in backend/src/mcp/server.py

### AI Agent Enhancement (US5)

- [ ] T054 [US5] Update AI agent system prompt in backend/src/chat/agent.py (add instructions for task editing, request new title if not provided)
- [ ] T055 [US5] Register update_task tool with agent in backend/src/chat/agent.py

### Error Handling (US5)

- [ ] T056 [US5] Implement validation in backend/src/mcp/tools/update_task.py (check title length 1-500 characters, return validation errors if invalid)

**Checkpoint**: At this point, User Story 5 should be fully functional - users can update task titles with validation feedback

---

## Phase 8: User Story 6 - Multi-Turn Conversation Context (Priority: P3)

**Goal**: Enable chatbot to remember conversation history during the session

**Independent Test**: Have conversation "Add buy milk" → "Also add buy bread" → "Show me what I just added" and verify chatbot understands contextual references

### Conversation Context Enhancement (US6)

- [ ] T057 [US6] Enhance conversation history fetch in backend/src/chat/history.py (ensure last 20 messages are passed to agent with proper role attribution)
- [ ] T058 [US6] Update AI agent system prompt in backend/src/chat/agent.py (add instructions to reference previous messages, understand contextual pronouns like "also", "the first one", "that task")

### Stateless Behavior Verification (US6)

- [ ] T059 [US6] Verify conversation persistence across server restart in backend/src/chat/orchestrator.py (test that conversations resume correctly after backend restart)

**Checkpoint**: At this point, User Story 6 should be fully functional - users can have natural multi-turn conversations with context awareness

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Edge case handling, performance optimization, and production readiness

### Edge Case Handling

- [ ] T060 [P] Handle empty messages in backend/src/routes/chat.py (return friendly prompt if message is empty)
- [ ] T061 [P] Handle long task titles in backend/src/mcp/tools/add_task.py (truncate to 500 characters, confirm truncation in response)
- [ ] T062 [P] Handle rapid message sending in backend/src/routes/chat.py (queue messages if needed, show "Processing..." indicator)
- [ ] T063 [P] Handle JWT expiration in frontend/src/chat/useChatClient.ts (detect 401, display session expired message)
- [ ] T064 [P] Handle MCP tool failures in backend/src/chat/agent.py (catch network errors, return "I couldn't complete that action" message)
- [ ] T065 [P] Handle non-existent tasks in backend/src/mcp/tools/complete_task.py and delete_task.py (return structured error for already-deleted tasks)
- [ ] T066 [P] Handle non-task questions in backend/src/chat/agent.py (return helpful message explaining chatbot capabilities)
- [ ] T067 [P] Handle large task lists in backend/src/mcp/tools/list_tasks.py (limit to first 20 tasks, offer pagination prompt)
- [ ] T068 [P] Handle Cohere API downtime in backend/src/chat/agent.py (catch API errors, log for monitoring, return user-friendly error)

### Security & Validation

- [ ] T069 [P] Sanitize user message content in backend/src/routes/chat.py (remove HTML/script tags, validate max 1000 characters)
- [ ] T070 [P] Sanitize assistant response in backend/src/chat/orchestrator.py (validate max 10,000 characters, remove any leaked internal details)
- [ ] T071 [P] Verify user_id extraction from JWT in backend/src/routes/chat.py (ensure user_id is never trusted from client)
- [ ] T072 [P] Verify conversation ownership in backend/src/chat/history.py (ensure user can only access their own conversations)

### Performance & Monitoring

- [ ] T073 [P] Add logging for MCP tool invocations in backend/src/mcp/tools/ (log tool name, user_id, timestamp, success/failure)
- [ ] T074 [P] Add logging for AI agent responses in backend/src/chat/orchestrator.py (log response time, token usage if available)
- [ ] T075 [P] Implement exponential backoff for Cohere API errors in backend/src/chat/agent.py (retry transient errors with backoff)
- [ ] T076 [P] Optimize conversation history query in backend/src/chat/history.py (ensure indexes are used, limit to last 20 messages)

### Frontend Polish

- [ ] T077 [P] Add loading indicator to ChatWindow in frontend/src/chat/ChatWindow.tsx (show typing indicator while waiting for response)
- [ ] T078 [P] Add error display to ChatWindow in frontend/src/chat/ChatWindow.tsx (show user-friendly error messages in chat)
- [ ] T079 [P] Add scroll-to-bottom behavior in ChatWindow in frontend/src/chat/ChatWindow.tsx (auto-scroll to latest message)
- [ ] T080 [P] Style ChatbotIcon in frontend/src/chat/ChatbotIcon.tsx (match application theme, add hover effects)

### Configuration & Deployment

- [ ] T081 [P] Document environment variables in backend/README.md (COHERE_API_KEY, COHERE_MODEL, required setup)
- [ ] T082 [P] Add environment variable validation in backend/src/main.py (check COHERE_API_KEY exists on startup)
- [ ] T083 [P] Configure CORS for chat endpoint in backend/src/main.py (allow frontend origin)
- [ ] T084 [P] Add healthcheck endpoint in backend/src/routes/chat.py (GET /api/chat/health to verify Cohere connectivity)

**Checkpoint**: Phase III is production-ready - all edge cases handled, security verified, performance optimized

---

## Dependencies & Execution Strategy

### User Story Dependencies

**Parallel Execution Opportunities**:

- **Phase 3 (US1)** and **Phase 4 (US2)** can be developed in parallel after Phase 2 is complete
  - US1: add_task tool + chat UI
  - US2: list_tasks tool
  - Both are P1 priority and independent

- **Phase 5 (US3)**, **Phase 6 (US4)**, **Phase 7 (US5)** can be developed in parallel after Phase 3 and 4
  - US3: complete_task tool
  - US4: delete_task tool
  - US5: update_task tool
  - All are P2/P3 priority and independent MCP tools

- **Phase 8 (US6)** depends on Phase 3-7 (needs existing conversation history to demonstrate context)

- **Phase 9 (Polish)** tasks are all parallel and can start once core features exist

### Critical Path

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundation) ← BLOCKING
    ↓
Phase 3 (US1: Task Creation) + Phase 4 (US2: Task Viewing) ← MVP
    ↓
Phase 5 (US3: Complete) + Phase 6 (US4: Delete) + Phase 7 (US5: Update)
    ↓
Phase 8 (US6: Multi-turn Context)
    ↓
Phase 9 (Polish) ← Production Ready
```

### MVP Scope (Recommended First Delivery)

**Minimum Viable Product** = Phase 1 + Phase 2 + Phase 3 (US1)

This delivers:
- Chatbot icon in UI
- Chat window with OpenAI ChatKit
- Natural language task creation via "Add [task]" commands
- Conversation persistence across sessions
- JWT authentication enforcement
- Basic error handling

**Value Delivered**: Users can create tasks conversationally without forms or navigation - the core value proposition of Phase III.

---

## Task Summary

**Total Tasks**: 84
- **Phase 1 (Setup)**: 9 tasks
- **Phase 2 (Foundation)**: 10 tasks (BLOCKING)
- **Phase 3 (US1 - P1)**: 16 tasks 🎯 MVP
- **Phase 4 (US2 - P1)**: 5 tasks
- **Phase 5 (US3 - P2)**: 6 tasks
- **Phase 6 (US4 - P2)**: 5 tasks
- **Phase 7 (US5 - P3)**: 5 tasks
- **Phase 8 (US6 - P3)**: 3 tasks
- **Phase 9 (Polish)**: 25 tasks

**Parallel Execution Opportunities**: 52 tasks marked with [P] (62% parallelizable)

**Independent Test Criteria**:
- ✅ US1: Send "Add buy groceries" → verify task created with confirmation
- ✅ US2: Ask "What's on my list?" → verify tasks displayed correctly
- ✅ US3: Say "Mark buy groceries as done" → verify status updates with confirmation
- ✅ US4: Say "Delete buy groceries" → verify deletion after confirmation
- ✅ US5: Say "Change buy groceries to buy milk" → verify title updates
- ✅ US6: Conversation "Add milk" → "Also add bread" → verify context understanding

**Constitutional Compliance**:
- ✅ All tasks follow spec-driven development (no code before specs)
- ✅ All MCP tools enforce user ownership (user_id parameter)
- ✅ All tasks maintain stateless architecture (database persistence)
- ✅ All AI actions go through MCP tools (tool-only behavior)
- ✅ All tasks protect Phase II stability (additive changes only)

**Format Validation**: ✅ All tasks follow checklist format (checkbox, ID, P marker if parallel, Story label where applicable, file path in description)
