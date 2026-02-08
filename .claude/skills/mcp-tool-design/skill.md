## MCP Tool Design Skill

**Used By:** MCP Server Agent  
**Phase:** III – AI Chatbot Integration

---

### Skill Overview
The **MCP Tool Design Skill** is the ability to design **stateless, deterministic, and safely composable tools** that expose application capabilities to AI agents through the **Model Context Protocol (MCP)**.

This skill ensures that AI agents can reliably manipulate application state **only through approved tools**, without direct database access, while maintaining security, correctness, and scalability.

---

### Core Principles

#### 1. Stateless Tool Design
Each MCP tool invocation must be **fully self-contained**.

- Tools must NOT rely on in-memory state
- All required context must be provided via parameters
- Persistent state must be read from and written to the database
- Tools must behave correctly even if executed on different server instances

**Outcome:**  
Tools remain horizontally scalable and safe in distributed environments.

---

#### 2. Clear Input / Output Contracts
Every tool must define an explicit, machine-readable contract.

**Inputs**
- Required vs optional parameters must be clearly defined
- Parameter types and constraints must be explicit
- User identity (`user_id`) must always be provided and validated

**Outputs**
- Return values must be predictable and minimal
- Responses must describe the outcome, not internal implementation
- Error responses must be structured and unambiguous

**Outcome:**  
AI agents can reason about tool usage without ambiguity or guesswork.

---

#### 3. Tool Chaining Support
Tools must be designed to support **multi-step agent reasoning**.

- Tool outputs should be usable as inputs to other tools
- Tools should not assume exclusive control of a conversation turn
- Tools must avoid side effects that break chaining logic

**Example**
- `list_tasks` → AI selects a task → `complete_task`
- `list_tasks` → AI identifies ambiguity → `delete_task`

**Outcome:**  
AI agents can compose complex behaviors from simple tools.

---

#### 4. Safe Side-Effect Handling
Every tool invocation must enforce **strict safety guarantees**.

- Tools may only affect resources owned by the authenticated user
- No tool may perform destructive actions without explicit intent
- Cross-user access must be impossible by design
- Failure must be handled gracefully without partial state corruption

**Safety Rules**
- Validate ownership before mutation
- Fail fast on invalid input
- Never silently succeed or partially apply changes

**Outcome:**  
AI-driven actions remain safe, auditable, and reversible where possible.

---

#### 5. Deterministic Behavior
Given the same input and database state, a tool must always produce the same result.

- No randomness
- No hidden time-dependent behavior
- No reliance on conversation history
- No reliance on agent memory

**Error Handling**
- Errors must be consistent and predictable
- Similar failures must yield similar responses

**Outcome:**  
Tools are reliable, testable, and trustworthy for AI automation.

---

### Non-Responsibilities (Explicitly Out of Scope)
This skill does **NOT** include:
- Natural language understanding
- Conversation memory management
- UI rendering
- Agent reasoning or decision-making
- Prompt engineering

Those concerns belong to other agents.

---

### Why This Skill Matters (Hackathon Evaluation)
Strong MCP Tool Design demonstrates:
- Deep understanding of AI-tool boundaries
- Production-grade AI integration
- Secure multi-user AI systems
- Scalable, stateless backend architecture

It is the foundation that allows an AI chatbot to act **powerfully, safely, and correctly** inside a real application.

---
