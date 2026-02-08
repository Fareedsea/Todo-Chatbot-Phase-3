# MCP Server and Tool Infrastructure

**Status**: T017-T018 Complete
**Phase**: Phase III AI Chatbot Integration
**Branch**: 003-ai-chatbot-integration

## Overview

This directory contains the Model Context Protocol (MCP) server infrastructure and tool schemas for Phase III AI Chatbot integration. The MCP server enables stateless, secure, and auditable AI-driven task management operations.

## Constitutional Compliance

This implementation strictly adheres to:

- **MCP Tool Law (Law XI)**: All tools are stateless, deterministic, validate inputs, and enforce user ownership
- **Tool-Only AI Law (Law VIII)**: AI MUST ONLY act via MCP tools (no direct state manipulation)
- **Security-First Architecture (Law V)**: Tools receive user_id from verified backend context, never from AI
- **Stateless Architecture Law (Law IX)**: No in-memory state; all data comes from database
- **API Contract Enforcement (Law VI)**: All tools have explicit input/output schemas

## Directory Structure

```
backend/src/mcp/
├── __init__.py              # Module exports
├── server.py                # MCP server initialization (T017) ✅
├── schemas.py               # Input/output Pydantic models (T018) ✅
├── tools/                   # Tool implementations (T020-T056)
│   ├── __init__.py         # Tool module (empty, ready for imports)
│   ├── add_task.py         # T020 (NOT YET IMPLEMENTED)
│   ├── list_tasks.py       # T036 (NOT YET IMPLEMENTED)
│   ├── update_task.py      # T052 (NOT YET IMPLEMENTED)
│   ├── complete_task.py    # T041 (NOT YET IMPLEMENTED)
│   └── delete_task.py      # T047 (NOT YET IMPLEMENTED)
└── README.md               # This file
```

## Completed Tasks

### T017: MCP Server Initialization (`server.py`)

**File**: `backend/src/mcp/server.py`

**What It Provides**:
- `MCPServer` class: Manages tool registration and invocation
- `get_mcp_server()`: Singleton accessor for MCP server instance
- `initialize_mcp_server()`: Startup function for FastAPI app integration
- Tool registration mechanism with schema validation
- Tool invocation with user_id injection from backend context

**Key Features**:
- Singleton pattern for global server instance
- Tool registry with input/output schema storage
- User ownership enforcement (user_id injection)
- Comprehensive logging for audit trails
- Structured error handling

**Usage Example**:
```python
from src.mcp.server import get_mcp_server

# Register a tool
server = get_mcp_server()
server.register_tool(
    name="add_task",
    handler=add_task_handler,
    input_schema=AddTaskInput.model_json_schema(),
    output_schema=ToolResponse.model_json_schema(),
    description="Create a new task for the authenticated user"
)

# Invoke a tool
result = await server.invoke_tool(
    name="add_task",
    input_data={"title": "Buy groceries"},
    user_id=123  # From JWT verification
)
```

### T018: MCP Tool Schemas (`schemas.py`)

**File**: `backend/src/mcp/schemas.py`

**What It Provides**:

#### Input Schemas (Pydantic Models)
- `AddTaskInput`: title (1-500 chars), user_id
- `ListTasksInput`: user_id, completed (optional filter)
- `UpdateTaskInput`: task_id, title (1-500 chars), user_id
- `CompleteTaskInput`: task_id, user_id
- `DeleteTaskInput`: task_id, user_id

#### Output Schemas
- `ToolResponse`: Generic response (success, data, error)
- `ToolError`: Structured error (code, message)
- `TaskOutput`: Task representation (id, title, completed, created_at)

#### Utility Functions
- `create_success_response(data)`: Build success response
- `create_error_response(code, message)`: Build error response
- `get_*_input_schema()`: Export JSON Schema for MCP registration

**Key Features**:
- All inputs validated with Pydantic Field constraints
- Title validation (strip whitespace, check length)
- user_id always required for ownership enforcement
- Consistent error response structure
- JSON serialization support for MCP protocol

**Usage Example**:
```python
from src.mcp.schemas import (
    AddTaskInput,
    create_success_response,
    create_error_response
)

# Validate input
try:
    input_data = AddTaskInput(title="Buy groceries", user_id=123)
except ValidationError as e:
    return create_error_response("VALIDATION_ERROR", str(e))

# Return success
return create_success_response({
    "task": {
        "id": 42,
        "title": "Buy groceries",
        "completed": False,
        "created_at": "2026-02-08T14:30:00Z"
    }
})
```

## Next Steps: Tool Implementation (T020-T056)

The MCP infrastructure is now ready for tool implementation. The next agent should implement the 5 MCP tools according to their respective tasks:

### Phase 3: User Story 1 - Task Creation (T020-T021)
- **T020**: Implement `add_task.py` tool
  - Validate AddTaskInput
  - Query database to create task
  - Return TaskOutput in ToolResponse
  - Handle validation errors, database errors

### Phase 4: User Story 2 - Task Listing (T036-T037)
- **T036**: Implement `list_tasks.py` tool
  - Validate ListTasksInput
  - Query database with optional completed filter
  - Return array of TaskOutput in ToolResponse
  - Handle empty results gracefully

### Phase 5: User Story 3 - Task Completion (T041-T042)
- **T041**: Implement `complete_task.py` tool
  - Validate CompleteTaskInput
  - Verify task exists and user owns it
  - Update task completed status
  - Return updated TaskOutput
  - Handle NOT_FOUND, UNAUTHORIZED errors

### Phase 6: User Story 4 - Task Deletion (T047-T048)
- **T047**: Implement `delete_task.py` tool
  - Validate DeleteTaskInput
  - Verify task exists and user owns it
  - Delete task from database
  - Return success message
  - Handle NOT_FOUND, UNAUTHORIZED errors

### Phase 7: User Story 5 - Task Update (T052-T053)
- **T052**: Implement `update_task.py` tool
  - Validate UpdateTaskInput
  - Verify task exists and user owns it
  - Update task title
  - Return updated TaskOutput
  - Handle NOT_FOUND, UNAUTHORIZED, VALIDATION_ERROR

## Tool Implementation Guidelines

### Required Patterns

Each tool MUST follow this structure:

```python
from typing import Dict, Any
from src.mcp.schemas import *Input, create_success_response, create_error_response
from src.database import get_session
from sqlmodel import select

async def *_tool_handler(input_data: Dict[str, Any]) -> Dict[str, Any]:
    \"\"\"
    MCP tool handler for * operation.

    Args:
        input_data: Validated input dict with user_id injected by server

    Returns:
        ToolResponse dict (success/error)
    \"\"\"
    try:
        # 1. Validate input with Pydantic schema
        input_schema = *Input(**input_data)

        # 2. Database operation with user ownership enforcement
        async with get_session() as session:
            # Query with WHERE user_id = input_schema.user_id
            result = await session.execute(...)

        # 3. Return success response
        return create_success_response({"task": result_dict})

    except ValidationError as e:
        return create_error_response("VALIDATION_ERROR", str(e))
    except NotFoundError:
        return create_error_response("NOT_FOUND", "Task not found for this user")
    except Exception as e:
        return create_error_response("DATABASE_ERROR", str(e))

def register_*_tool(server: MCPServer) -> None:
    \"\"\"Register * tool with MCP server.\"\"\"
    server.register_tool(
        name="*",
        handler=*_tool_handler,
        input_schema=get_*_input_schema(),
        output_schema=get_tool_response_output_schema(),
        description="..."
    )
```

### Constitutional Requirements for Tools

1. **Stateless**: No class-level or module-level state
2. **Deterministic**: Same input → same output (given same DB state)
3. **Ownership**: Always filter queries by user_id
4. **Validation**: Use Pydantic schemas for all inputs
5. **Error Handling**: Return structured ToolError, never raise exceptions to AI
6. **Logging**: Log all invocations with user_id for audit trail
7. **Database**: Use SQLModel queries, never raw SQL
8. **Isolation**: Never access tasks belonging to other users

### Error Code Standards

Use these error codes consistently:

| Code | When to Use |
|------|-------------|
| `VALIDATION_ERROR` | Input validation failed (Pydantic) |
| `NOT_FOUND` | Task ID doesn't exist for user |
| `UNAUTHORIZED` | User doesn't own the task |
| `DATABASE_ERROR` | Database query/connection failed |
| `TOOL_EXECUTION_ERROR` | Unexpected error during execution |

### Testing Checklist

For each tool, verify:

- [ ] Input validation works (invalid title, missing user_id, etc.)
- [ ] User ownership is enforced (cannot access other user's tasks)
- [ ] Success case returns proper TaskOutput
- [ ] Error cases return structured ToolError
- [ ] Logging captures user_id and operation
- [ ] Tool registered with MCP server on startup
- [ ] Integration with AI agent works (tool callable via agent)

## Integration with FastAPI

To integrate MCP server with FastAPI (T019):

```python
# In backend/src/main.py

from src.mcp.server import initialize_mcp_server
from src.mcp.tools.add_task import register_add_task_tool
# ... import other tool registrations

@app.on_event("startup")
async def startup():
    """Initialize MCP server and register tools."""
    server = initialize_mcp_server()

    # Register all tools
    register_add_task_tool(server)
    register_list_tasks_tool(server)
    register_update_task_tool(server)
    register_complete_task_tool(server)
    register_delete_task_tool(server)

    logger.info("MCP server initialized with all tools")
```

## Contract References

All tool contracts are defined in:
- **Spec**: `specs/003-ai-chatbot-integration/spec.md`
- **Plan**: `specs/003-ai-chatbot-integration/plan.md` (lines 490-696)
- **Tasks**: `specs/003-ai-chatbot-integration/tasks.md`

Tool contracts specify:
- Input parameters (name, type, constraints)
- Output format (success/error structure)
- Error codes and messages
- Ownership rules
- Validation requirements

## Status Summary

| Component | Task | Status | Files |
|-----------|------|--------|-------|
| MCP Server | T017 | ✅ Complete | `server.py` |
| Schemas | T018 | ✅ Complete | `schemas.py` |
| Tools Module | T018 | ✅ Complete | `tools/__init__.py` |
| add_task | T020 | ❌ Not Started | `tools/add_task.py` |
| list_tasks | T036 | ❌ Not Started | `tools/list_tasks.py` |
| complete_task | T041 | ❌ Not Started | `tools/complete_task.py` |
| delete_task | T047 | ❌ Not Started | `tools/delete_task.py` |
| update_task | T052 | ❌ Not Started | `tools/update_task.py` |

## Dependencies

**Required for tool implementation**:
- SQLModel (already installed in Phase II)
- Pydantic (already installed in Phase II)
- FastAPI async support (already installed in Phase II)
- Database session management (from `src.database`)
- Task model (from `src.models.task`)

**Not yet required** (will be needed for AI agent in later tasks):
- OpenAI Agents SDK (T001)
- Official MCP SDK (T002)
- Cohere API client (T003)

## Notes for Next Agent

1. **Start with T020 (add_task)**: This is the MVP tool for User Story 1
2. **Follow the tool implementation pattern**: See "Tool Implementation Guidelines" above
3. **Test each tool independently**: Use pytest to validate tool behavior before AI integration
4. **Verify user isolation**: Always test cross-user access attempts return errors
5. **Register tools in main.py**: After implementation, add registration to FastAPI startup
6. **Log everything**: Use structured logging for debugging and audit trails

## Support

For questions or clarifications:
- Review constitution: `.specify/memory/constitution.md`
- Review spec: `specs/003-ai-chatbot-integration/spec.md`
- Review plan: `specs/003-ai-chatbot-integration/plan.md`
- Review tasks: `specs/003-ai-chatbot-integration/tasks.md`

---

**Last Updated**: 2026-02-08
**Implemented By**: MCP Tool Design Specialist
**Constitutional Version**: 2.0.0
