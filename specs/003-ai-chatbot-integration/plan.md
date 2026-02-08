# Implementation Plan: AI Chatbot for Todo Management (Phase III)

**Branch**: `003-ai-chatbot-integration` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot-integration/spec.md`

## Summary

Phase III adds a conversational AI chatbot interface to the existing Phase II Todo application, enabling users to manage tasks through natural language commands. The system uses Cohere API for LLM capabilities via OpenAI Agents SDK, with all task operations routed through stateless MCP (Model Context Protocol) tools. Conversations are persisted in the database to ensure stateless backend architecture and crash recovery. The frontend integrates OpenAI ChatKit UI with a persistent chatbot icon, while the backend orchestrates AI agent execution, MCP tool invocation, JWT authentication, and conversation history management.

**Technical Approach**: Stateless request-response architecture where each chat message triggers: (1) conversation history fetch from database, (2) AI agent initialization with Cohere LLM and registered MCP tools, (3) tool execution with JWT-verified user context, (4) conversation persistence, (5) structured response to frontend. Zero in-memory state, zero hallucinations, 100% tool-based AI actions.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/JavaScript with Next.js 16+ (frontend)
**Primary Dependencies**:
- Backend: FastAPI, OpenAI Agents SDK, official MCP SDK, SQLModel, httpx (Cohere API client)
- Frontend: Next.js (App Router), OpenAI ChatKit, Better Auth client
**Storage**: Neon Serverless PostgreSQL (existing + 2 new tables: conversations, chat_messages)
**Testing**: pytest (backend), Jest + React Testing Library (frontend)
**Target Platform**: Web application (Linux/Docker backend, modern browser frontend)
**Project Type**: Web (monorepo with backend/ and frontend/ workspaces)
**Performance Goals**:
- p95 chat response latency < 2 seconds
- 100 concurrent chat sessions without degradation
- MCP tool invocation success rate > 99.5%
- Zero hallucinations (100% tool-based facts)
**Constraints**:
- Backend MUST remain stateless (no in-memory conversation storage)
- AI MUST NOT directly manipulate application state (MCP tools only)
- Conversation history limited to last 20 messages per request (prevent context overflow)
- Cohere API rate limits (~500 requests/minute for 100 concurrent users)
- Phase II functionality MUST NOT break
**Scale/Scope**:
- 100+ concurrent users
- 5 MCP tools (add, list, update, complete, delete tasks)
- 1 chat endpoint (POST /api/chat)
- 2 new database tables (conversations, chat_messages)
- 1 AI agent configuration (Cohere via OpenAI Agents SDK)
- 1 frontend chat UI component (ChatKit integration)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase II Stability Protection
- ✅ **PASS**: Phase II functionality locked and immutable (no breaking changes permitted)
- ✅ **PASS**: Phase III work isolated on feature branch `003-ai-chatbot-integration`
- ✅ **PASS**: Existing REST APIs remain unchanged (chat is additive, not replacing)

### Spec-Driven Development Mandate (Law I)
- ✅ **PASS**: Specification created and approved (`specs/003-ai-chatbot-integration/spec.md`)
- ✅ **PASS**: Plan follows spec-first workflow (spec → plan → tasks → implement)
- ✅ **PASS**: No code written before plan approval

### Technology Stack Compliance (Law III)
- ✅ **PASS**: Backend uses FastAPI (constitutional requirement)
- ✅ **PASS**: Frontend uses Next.js + OpenAI ChatKit (constitutional requirement)
- ✅ **PASS**: Database uses Neon PostgreSQL (constitutional requirement)
- ✅ **PASS**: Authentication uses Better Auth JWT (constitutional requirement)
- ✅ **PASS**: AI uses OpenAI Agents SDK with Cohere API (constitutional requirement)
- ✅ **PASS**: MCP tools use Official MCP SDK (constitutional requirement)
- ✅ **PASS**: ORM uses SQLModel (constitutional requirement)

### AI Model & Provider Law (Law VII - Critical)
- ✅ **PASS**: Cohere is sole LLM provider (no direct OpenAI API calls)
- ✅ **PASS**: OpenAI Agents SDK configured to route through Cohere API
- ✅ **PASS**: API keys loaded from environment variables (`COHERE_API_KEY`)
- ✅ **PASS**: Model name configurable via environment (`COHERE_MODEL`)

### Tool-Only AI Law (Law VIII - Core Safety)
- ✅ **PASS**: AI actions limited to MCP tool invocations (no direct state manipulation)
- ✅ **PASS**: 5 MCP tools defined (add, list, update, complete, delete tasks)
- ✅ **PASS**: AI must ask clarification for ambiguous intent (specified in agent prompt)
- ✅ **PASS**: AI must confirm destructive actions (specified in agent prompt)
- ✅ **PASS**: AI cannot bypass tools (enforced by agent configuration)

### Stateless Architecture Law (Law IX)
- ✅ **PASS**: Backend has no in-memory conversation storage
- ✅ **PASS**: Conversation state persisted to database after every exchange
- ✅ **PASS**: Each request independently reproducible from database state
- ✅ **PASS**: Any server instance can handle any request (no session affinity)
- ✅ **PASS**: AI agent state reconstructed from database on every request

### Conversation Persistence Law (Law X)
- ✅ **PASS**: User messages stored in `chat_messages` table
- ✅ **PASS**: Assistant responses stored in `chat_messages` table
- ✅ **PASS**: Conversations resume after restart by loading from database
- ✅ **PASS**: History fetched per request (no in-memory caching)
- ✅ **PASS**: Context limited to last 20 messages (prevent overflow)
- ✅ **PASS**: Conversations associated with authenticated users (user_id FK)

### MCP Tool Law (Law XI)
- ✅ **PASS**: MCP tools are stateless (no internal memory)
- ✅ **PASS**: MCP tools are deterministic (same input → same output)
- ✅ **PASS**: Tools validate inputs against JSON schemas
- ✅ **PASS**: Tools enforce user ownership (user_id from JWT)
- ✅ **PASS**: Tools return structured JSON responses
- ✅ **PASS**: Tools delegate to backend APIs (no business logic duplication)

### Error Handling Law (Law XII)
- ✅ **PASS**: Errors handled gracefully (no unhandled exceptions)
- ✅ **PASS**: AI translates technical errors to user-friendly messages
- ✅ **PASS**: Backend returns consistent JSON error format
- ✅ **PASS**: Security errors don't leak details
- ✅ **PASS**: MCP tool errors propagate as structured responses
- ✅ **PASS**: AI retries transient errors with exponential backoff

### Safety & Hallucination Prevention Law (Law XIII)
- ✅ **PASS**: AI must not invent tasks, users, or states
- ✅ **PASS**: AI relies on tools for all factual data
- ✅ **PASS**: AI admits uncertainty when tools fail
- ✅ **PASS**: Tool invocation logged and auditable
- ✅ **PASS**: AI distinguishes confirmed/failed/pending actions
- ✅ **PASS**: AI does not cache task state (always fetches fresh)

### Chat Behavior & UX Law (Law XIV)
- ✅ **PASS**: Chatbot confirms all task actions
- ✅ **PASS**: Uses clear, friendly, professional language
- ✅ **PASS**: Gracefully handles errors with explanations
- ✅ **PASS**: Asks for clarification when ambiguous
- ✅ **PASS**: Never exposes internal errors, stack traces, or secrets
- ✅ **PASS**: Maintains conversation context across turns

### Security-First Architecture (Law V)
- ✅ **PASS**: All chat API requests require valid JWT
- ✅ **PASS**: JWT verified by backend (not trusted from client)
- ✅ **PASS**: User ownership enforced at query level in MCP tools
- ✅ **PASS**: Unauthorized requests return 401; forbidden return 403
- ✅ **PASS**: Frontend untrusted; validation happens on backend
- ✅ **PASS**: MCP tools receive user_id from verified backend context
- ✅ **PASS**: AI cannot fabricate or guess user identity

### API Contract Enforcement (Law VI)
- ✅ **PASS**: Chat endpoint follows REST standards (POST /api/chat)
- ✅ **PASS**: Route prefixed with `/api/`
- ✅ **PASS**: Responses are JSON with proper Content-Type
- ✅ **PASS**: Errors use proper HTTP status codes (400, 401, 403, 404, 422, 500)
- ✅ **PASS**: Tasks filtered by authenticated user (enforced in MCP tools)
- ✅ **PASS**: MCP tools have explicit input/output schemas

### Agent Authority & Separation (Law IV)
- ✅ **PASS**: Database Engineer designs conversation/message tables
- ✅ **PASS**: Backend Engineer implements chat endpoint and orchestration
- ✅ **PASS**: MCP Tool Designer creates tool specifications
- ✅ **PASS**: Frontend Engineer integrates ChatKit UI
- ✅ **PASS**: Integration Tester validates end-to-end flow
- ✅ **PASS**: No agent performs another agent's role

**Constitution Check Result**: ✅ **ALL GATES PASSED**

No violations detected. All constitutional requirements are satisfied by the planned architecture.

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot-integration/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0: Research findings (to be generated)
├── data-model.md        # Phase 1: Database schema design (to be generated)
├── quickstart.md        # Phase 1: Developer setup guide (to be generated)
├── contracts/           # Phase 1: API and MCP tool contracts (to be generated)
│   ├── chat-api.json   # OpenAPI spec for POST /api/chat endpoint
│   ├── add-task.json   # MCP tool contract: add_task
│   ├── list-tasks.json # MCP tool contract: list_tasks
│   ├── update-task.json # MCP tool contract: update_task
│   ├── complete-task.json # MCP tool contract: complete_task
│   └── delete-task.json # MCP tool contract: delete_task
├── checklists/
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2: Implementation tasks (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/           # Existing Phase II models
│   │   ├── task.py      # Existing Task model
│   │   ├── user.py      # Existing User model
│   │   ├── conversation.py  # NEW: Conversation model
│   │   └── chat_message.py  # NEW: ChatMessage model
│   ├── routes/           # Existing Phase II routes
│   │   ├── tasks.py     # Existing task CRUD routes
│   │   ├── auth.py      # Existing authentication routes
│   │   └── chat.py      # NEW: Chat endpoint (POST /api/chat)
│   ├── mcp/              # NEW: MCP server and tools
│   │   ├── __init__.py
│   │   ├── server.py    # MCP server initialization
│   │   ├── tools/       # MCP tool implementations
│   │   │   ├── __init__.py
│   │   │   ├── add_task.py
│   │   │   ├── list_tasks.py
│   │   │   ├── update_task.py
│   │   │   ├── complete_task.py
│   │   │   └── delete_task.py
│   │   └── schemas.py   # Input/output schemas for tools
│   ├── chat/             # NEW: Chat orchestration
│   │   ├── __init__.py
│   │   ├── agent.py     # AI agent configuration (Cohere via OpenAI Agents SDK)
│   │   ├── orchestrator.py  # Chat request lifecycle
│   │   └── history.py   # Conversation history management
│   ├── auth/             # Existing Phase II auth
│   │   └── jwt.py       # JWT verification utilities
│   ├── database.py       # Existing database connection
│   └── main.py           # FastAPI app entry point
└── tests/
    ├── test_chat_endpoint.py  # NEW: Chat API integration tests
    ├── test_mcp_tools.py      # NEW: MCP tool unit tests
    ├── test_agent.py          # NEW: AI agent behavior tests
    └── test_conversation.py   # NEW: Conversation persistence tests

frontend/
├── src/
│   ├── components/       # Existing Phase II components
│   │   ├── TaskList.tsx # Existing task list component
│   │   └── TaskForm.tsx # Existing task form component
│   ├── chat/             # NEW: Chat UI integration
│   │   ├── ChatbotIcon.tsx   # Persistent chatbot icon
│   │   ├── ChatWindow.tsx    # ChatKit modal/panel
│   │   └── useChatClient.ts  # Hook for chat API integration
│   ├── pages/            # Existing Phase II pages
│   │   └── dashboard.tsx # Existing dashboard (add chatbot icon here)
│   ├── lib/
│   │   ├── api-client.ts # Existing API client (extend for chat)
│   │   └── auth.ts       # Existing Better Auth integration
│   └── app/              # Next.js App Router
│       └── layout.tsx    # Root layout (add ChatbotIcon here)
└── tests/
    └── chat/             # NEW: Chat UI tests
        ├── ChatbotIcon.test.tsx
        └── ChatWindow.test.tsx

database/migrations/      # NEW: Database migrations
├── 003_create_conversations_table.sql
└── 004_create_chat_messages_table.sql
```

**Structure Decision**: Web application monorepo structure selected because the project has distinct frontend (Next.js) and backend (FastAPI) workspaces. Phase III adds new subdirectories under `backend/src/` for MCP tools (`mcp/`) and chat orchestration (`chat/`), plus new frontend components under `frontend/src/chat/` for ChatKit integration. Database migrations are added for the two new tables (conversations, chat_messages). All Phase II directories remain unchanged to prevent breaking existing functionality.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. This section is intentionally left empty per constitutional compliance.

---

## Phase 0: Research & Technical Decisions

**Objective**: Resolve all technical unknowns and establish implementation patterns before Phase 1 design.

### Research Tasks

1. **Cohere API Integration with OpenAI Agents SDK**
   - **Question**: How to configure OpenAI Agents SDK to use Cohere API instead of OpenAI/Gemini?
   - **Research needed**:
     - OpenAI Agents SDK documentation for custom LLM providers
     - Cohere API compatibility with OpenAI-style chat completion endpoints
     - Base URL override mechanism in OpenAI Agents SDK
   - **Deliverable**: Configuration pattern for routing OpenAI Agents SDK calls through Cohere

2. **MCP SDK Integration with FastAPI**
   - **Question**: How to integrate Official MCP SDK with FastAPI backend?
   - **Research needed**:
     - MCP SDK Python package installation and initialization
     - FastAPI middleware or route integration for MCP server
     - Tool registration and invocation patterns
     - Error handling and schema validation in MCP SDK
   - **Deliverable**: Integration pattern for MCP server in FastAPI

3. **OpenAI ChatKit Integration with Next.js**
   - **Question**: How to integrate OpenAI ChatKit UI with Next.js App Router?
   - **Research needed**:
     - ChatKit npm package installation and configuration
     - Next.js App Router compatibility (client components, SSR considerations)
     - ChatKit customization options (theming, event handlers)
     - JWT token attachment in ChatKit HTTP requests
   - **Deliverable**: Integration pattern for ChatKit in Next.js

4. **Stateless Conversation Management**
   - **Question**: How to efficiently fetch and reconstruct conversation history from database on every request?
   - **Research needed**:
     - SQLModel query patterns for conversation history (join conversations + messages)
     - Performance optimization (indexing, limit last N messages)
     - Message ordering and pagination strategies
   - **Deliverable**: Database query pattern for conversation history retrieval

5. **AI Agent System Prompt Design**
   - **Question**: What system prompt enforces tool-only behavior and prevents hallucinations?
   - **Research needed**:
     - Best practices for tool-calling agent prompts
     - Hallucination prevention techniques (strict tool reliance, uncertainty admission)
     - Confirmation patterns for destructive actions
     - User-friendly error message templates
   - **Deliverable**: System prompt template for Cohere-powered AI agent

6. **MCP Tool Error Handling**
   - **Question**: How to structure MCP tool error responses for graceful AI agent handling?
   - **Research needed**:
     - MCP SDK error response format
     - Error codes and categorization (user error, system error, not found, unauthorized)
     - Retry-ability indicators for transient failures
   - **Deliverable**: Error response schema for MCP tools

7. **JWT Extraction and Validation in Chat Endpoint**
   - **Question**: How to extract and validate JWT in chat endpoint to pass user_id to MCP tools?
   - **Research needed**:
     - FastAPI dependency injection for JWT verification
     - Better Auth JWT token structure and claims extraction
     - Error handling for expired, invalid, or missing tokens
   - **Deliverable**: JWT verification dependency pattern for chat endpoint

8. **Database Migration Strategy**
   - **Question**: How to safely add conversations and chat_messages tables without breaking Phase II?
   - **Research needed**:
     - SQLModel/Alembic migration patterns
     - Foreign key constraints (conversations.user_id → users.id, messages.conversation_id → conversations.id)
     - Indexing strategy (conversation lookups by user, message ordering by conversation)
   - **Deliverable**: Migration scripts for new tables with rollback plan

**Output**: `research.md` document with all decisions, rationales, alternatives considered, and code examples.

---

## Phase 1: Data Model & API Contracts

**Prerequisites**: `research.md` completed

### 1. Data Model Design

**Task**: Extract entities from feature spec and design database schema in `data-model.md`.

#### New Entities

**Conversation**
- **Purpose**: Represents a chat session between a user and the AI assistant
- **Fields**:
  - `id`: Integer, primary key, auto-increment
  - `user_id`: Integer, foreign key to users.id (NOT NULL, indexed)
  - `created_at`: Timestamp, auto-set on insert
  - `updated_at`: Timestamp, auto-update on modification
- **Relationships**:
  - Belongs to one User (via user_id foreign key)
  - Has many ChatMessages (via conversation_id in chat_messages table)
- **Constraints**:
  - `user_id` must exist in users table (foreign key constraint)
  - Index on `user_id` for fast user conversation lookups
- **State Transitions**:
  - Created when user sends first message in new conversation
  - Updated timestamp modified on every new message
  - No explicit "closed" state (conversations remain open indefinitely)

**ChatMessage**
- **Purpose**: Represents a single message in a conversation (user or assistant)
- **Fields**:
  - `id`: Integer, primary key, auto-increment
  - `conversation_id`: Integer, foreign key to conversations.id (NOT NULL, indexed)
  - `role`: Enum('user', 'assistant') (NOT NULL)
  - `content`: Text (NOT NULL, max 10,000 characters)
  - `created_at`: Timestamp, auto-set on insert
- **Relationships**:
  - Belongs to one Conversation (via conversation_id foreign key)
- **Constraints**:
  - `conversation_id` must exist in conversations table (foreign key constraint)
  - `role` must be either 'user' or 'assistant'
  - `content` limited to 10,000 characters (prevent abuse)
  - Index on `(conversation_id, created_at)` for fast message ordering
- **Validation Rules**:
  - User messages must not be empty (min 1 character)
  - Assistant messages must not be empty
  - No HTML/script tags allowed in content (sanitized on input)

#### Existing Entities (Phase II - No Changes)

**User** (unchanged)
**Task** (unchanged)

#### Entity Relationships Diagram

```
User (1) ---< (N) Conversation
             |
             | (via conversation_id)
             |
             v
         ChatMessage (N)

User (1) ---< (N) Task (existing Phase II relationship, unchanged)
```

### 2. API Contract Generation

**Task**: Generate OpenAPI specifications for chat endpoint and MCP tool contracts.

#### Chat API Contract (`contracts/chat-api.json`)

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Chat API",
    "version": "1.0.0"
  },
  "paths": {
    "/api/chat": {
      "post": {
        "summary": "Send chat message to AI assistant",
        "security": [{"BearerAuth": []}],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": ["message"],
                "properties": {
                  "conversation_id": {
                    "type": "integer",
                    "description": "Optional conversation ID to continue existing conversation. Omit to start new conversation."
                  },
                  "message": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 1000,
                    "description": "User message content"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful chat response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "required": ["conversation_id", "response"],
                  "properties": {
                    "conversation_id": {
                      "type": "integer",
                      "description": "Conversation ID (new or existing)"
                    },
                    "response": {
                      "type": "string",
                      "description": "AI assistant response"
                    },
                    "tool_calls": {
                      "type": "array",
                      "description": "Optional array of tool execution results",
                      "items": {
                        "type": "object",
                        "properties": {
                          "tool": {"type": "string"},
                          "result": {"type": "object"}
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "401": {"description": "Unauthorized (missing or invalid JWT)"},
          "422": {"description": "Validation error (invalid request body)"},
          "500": {"description": "Internal server error"}
        }
      }
    }
  },
  "components": {
    "securitySchemes": {
      "BearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
      }
    }
  }
}
```

#### MCP Tool Contracts

**add_task Tool** (`contracts/add-task.json`)
```json
{
  "name": "add_task",
  "description": "Create a new task for the authenticated user",
  "inputSchema": {
    "type": "object",
    "required": ["title", "user_id"],
    "properties": {
      "title": {
        "type": "string",
        "minLength": 1,
        "maxLength": 500,
        "description": "Task title/description"
      },
      "user_id": {
        "type": "integer",
        "description": "Authenticated user ID (provided by backend, not AI)"
      }
    }
  },
  "outputSchema": {
    "type": "object",
    "required": ["success", "task"],
    "properties": {
      "success": {"type": "boolean"},
      "task": {
        "type": "object",
        "properties": {
          "id": {"type": "integer"},
          "title": {"type": "string"},
          "completed": {"type": "boolean"},
          "created_at": {"type": "string", "format": "date-time"}
        }
      },
      "error": {
        "type": "object",
        "properties": {
          "code": {"type": "string"},
          "message": {"type": "string"}
        }
      }
    }
  }
}
```

**list_tasks Tool** (`contracts/list-tasks.json`)
```json
{
  "name": "list_tasks",
  "description": "Retrieve all tasks for the authenticated user",
  "inputSchema": {
    "type": "object",
    "required": ["user_id"],
    "properties": {
      "user_id": {
        "type": "integer",
        "description": "Authenticated user ID"
      },
      "completed": {
        "type": "boolean",
        "description": "Optional filter by completion status"
      }
    }
  },
  "outputSchema": {
    "type": "object",
    "required": ["success", "tasks"],
    "properties": {
      "success": {"type": "boolean"},
      "tasks": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "completed": {"type": "boolean"},
            "created_at": {"type": "string", "format": "date-time"}
          }
        }
      },
      "count": {"type": "integer"},
      "error": {
        "type": "object",
        "properties": {
          "code": {"type": "string"},
          "message": {"type": "string"}
        }
      }
    }
  }
}
```

**update_task Tool** (`contracts/update-task.json`)
```json
{
  "name": "update_task",
  "description": "Update a task title for the authenticated user",
  "inputSchema": {
    "type": "object",
    "required": ["task_id", "title", "user_id"],
    "properties": {
      "task_id": {"type": "integer"},
      "title": {
        "type": "string",
        "minLength": 1,
        "maxLength": 500
      },
      "user_id": {"type": "integer"}
    }
  },
  "outputSchema": {
    "type": "object",
    "required": ["success"],
    "properties": {
      "success": {"type": "boolean"},
      "task": {
        "type": "object",
        "properties": {
          "id": {"type": "integer"},
          "title": {"type": "string"},
          "completed": {"type": "boolean"}
        }
      },
      "error": {
        "type": "object",
        "properties": {
          "code": {"type": "string"},
          "message": {"type": "string"}
        }
      }
    }
  }
}
```

**complete_task Tool** (`contracts/complete-task.json`)
```json
{
  "name": "complete_task",
  "description": "Mark a task as complete for the authenticated user",
  "inputSchema": {
    "type": "object",
    "required": ["task_id", "user_id"],
    "properties": {
      "task_id": {"type": "integer"},
      "user_id": {"type": "integer"}
    }
  },
  "outputSchema": {
    "type": "object",
    "required": ["success"],
    "properties": {
      "success": {"type": "boolean"},
      "task": {
        "type": "object",
        "properties": {
          "id": {"type": "integer"},
          "title": {"type": "string"},
          "completed": {"type": "boolean"}
        }
      },
      "error": {
        "type": "object",
        "properties": {
          "code": {"type": "string"},
          "message": {"type": "string"}
        }
      }
    }
  }
}
```

**delete_task Tool** (`contracts/delete-task.json`)
```json
{
  "name": "delete_task",
  "description": "Delete a task for the authenticated user",
  "inputSchema": {
    "type": "object",
    "required": ["task_id", "user_id"],
    "properties": {
      "task_id": {"type": "integer"},
      "user_id": {"type": "integer"}
    }
  },
  "outputSchema": {
    "type": "object",
    "required": ["success"],
    "properties": {
      "success": {"type": "boolean"},
      "message": {"type": "string"},
      "error": {
        "type": "object",
        "properties": {
          "code": {"type": "string"},
          "message": {"type": "string"}
        }
      }
    }
  }
}
```

### 3. Developer Quickstart Guide

**Task**: Create `quickstart.md` with setup instructions for Phase III development.

**Content Outline**:
1. Prerequisites (Python 3.11+, Node.js 18+, Neon PostgreSQL access)
2. Environment Variables Setup
   - `COHERE_API_KEY`: Cohere API key
   - `COHERE_MODEL`: Model name (default: "command-r-plus")
   - `DATABASE_URL`: Neon PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: JWT signing secret
3. Backend Setup
   - Install dependencies: `pip install -r backend/requirements.txt`
   - Run migrations: Database migrations for conversations, chat_messages tables
   - Start dev server: `uvicorn backend.src.main:app --reload`
4. Frontend Setup
   - Install dependencies: `npm install` in frontend/
   - Configure ChatKit (API base URL, authentication)
   - Start dev server: `npm run dev`
5. Testing Chat Flow
   - Authenticate to get JWT token
   - Open chat window via chatbot icon
   - Send test messages: "Add buy groceries", "Show my tasks", "Complete the first task"
   - Verify responses and task updates
6. Troubleshooting
   - Cohere API errors (rate limits, invalid key)
   - MCP tool failures (check logs for tool invocation errors)
   - Conversation persistence issues (check database connections)

### 4. Agent Context Update

**Task**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude` to update Claude Code guidance with Phase III technologies.

**Technologies to Add**:
- OpenAI Agents SDK (agent orchestration)
- Cohere API (LLM provider)
- Official MCP SDK (tool protocol)
- OpenAI ChatKit (chat UI components)
- Conversation persistence patterns (stateless backend, database history fetch)

**Update Locations**:
- `CLAUDE.md` (root project guidance)
- `backend/CLAUDE.md` (Backend-specific guidance for MCP tools, chat orchestration)
- `frontend/CLAUDE.md` (Frontend-specific guidance for ChatKit integration)

**Output**: Updated CLAUDE.md files with Phase III context.

---

## Phase 2: Task Generation (Not Part of /sp.plan)

**Note**: This phase is executed by the `/sp.tasks` command, not `/sp.plan`. The plan ends after Phase 1 completion.

Task generation will produce `specs/003-ai-chatbot-integration/tasks.md` with ordered, atomic implementation tasks covering:
1. Database migrations (conversations, chat_messages tables)
2. SQLModel model definitions (Conversation, ChatMessage)
3. MCP tool implementations (5 tools with schemas and error handling)
4. MCP server initialization and registration
5. AI agent configuration (Cohere via OpenAI Agents SDK)
6. Chat orchestration logic (request lifecycle, history fetch, persistence)
7. Chat API endpoint (POST /api/chat with JWT verification)
8. Frontend ChatKit integration (icon, modal, API client)
9. Integration testing (end-to-end chat flow, stateless behavior, security)
10. Deployment configuration (environment variables, monitoring)

---

## Constitutional Re-Check (Post-Phase 1)

*Re-evaluation after Phase 1 design artifacts are generated*

### Data Model Compliance
- ✅ **PASS**: Conversation and ChatMessage entities follow constitutional requirements
- ✅ **PASS**: Foreign keys enforce user ownership (conversations.user_id → users.id)
- ✅ **PASS**: Message role enum restricts values to 'user' | 'assistant'
- ✅ **PASS**: Indexes support efficient conversation history queries

### API Contract Compliance
- ✅ **PASS**: Chat endpoint follows REST standards (POST /api/chat)
- ✅ **PASS**: JWT authentication required (Bearer token in Authorization header)
- ✅ **PASS**: Request/response schemas validated (OpenAPI spec)
- ✅ **PASS**: Error responses use proper HTTP status codes

### MCP Tool Contract Compliance
- ✅ **PASS**: All 5 tools have explicit input/output schemas (JSON Schema format)
- ✅ **PASS**: All tools accept user_id parameter (from authenticated backend context)
- ✅ **PASS**: All tools return structured error responses
- ✅ **PASS**: Tool descriptions enable AI to understand when to invoke

### Phase II Integrity
- ✅ **PASS**: No changes to existing Task or User models
- ✅ **PASS**: No changes to existing REST API routes
- ✅ **PASS**: New tables use separate names (conversations, chat_messages)
- ✅ **PASS**: Migrations are additive only (no ALTER existing tables)

**Post-Design Constitution Check Result**: ✅ **ALL GATES PASSED**

The planned architecture maintains full constitutional compliance. Phase III can proceed to task generation (`/sp.tasks`) once this plan is approved.

---

## Next Steps

1. **User reviews and approves this plan**
2. **Run `/sp.tasks`** to generate detailed implementation tasks in `tasks.md`
3. **Backend Engineer Agent** implements MCP tools, chat orchestration, and API endpoint
4. **Database Engineer Agent** creates migrations and model definitions
5. **Frontend Engineer Agent** integrates ChatKit and chatbot icon
6. **Integration Tester Agent** validates full chat flow, stateless behavior, and security

**Plan Status**: ✅ **READY FOR APPROVAL**

All research questions identified, data model designed, API contracts specified, and constitutional compliance verified. The plan is complete and awaiting user approval to proceed to task generation.
