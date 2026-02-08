# Phase III Database Schema - AI Chatbot Integration

## Overview

This directory contains database migrations and documentation for Phase III AI Chatbot integration. The schema adds two new tables (`conversations` and `chat_messages`) to support stateless conversation persistence.

## Constitutional Compliance

**Phase II Stability**: All migrations are additive only. No existing Phase II tables (`users`, `tasks`) are modified.

**Stateless Architecture Law (Law IX)**: All conversation state is persisted to the database. No in-memory storage is used.

**Conversation Persistence Law (Law X)**: Every user message and assistant response is stored in `chat_messages` table.

**Security-First Architecture (Law V)**: All conversations are associated with authenticated users via `user_id` foreign key.

## Database Schema

### Table: `conversations`

**Purpose**: Represents chat sessions between users and the AI assistant.

**Schema**:
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at DESC);
```

**Relationships**:
- `user_id` → `users.id` (many-to-one, CASCADE DELETE)
- One conversation has many `chat_messages` (one-to-many, CASCADE DELETE)

**Query Patterns**:
- Get all conversations for a user: `SELECT * FROM conversations WHERE user_id = ?`
- Get recent conversations: `SELECT * FROM conversations WHERE user_id = ? ORDER BY updated_at DESC`

### Table: `chat_messages`

**Purpose**: Stores individual messages in conversations (user or assistant).

**Schema**:
```sql
CREATE TYPE message_role AS ENUM ('user', 'assistant');

CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    role message_role NOT NULL,
    content TEXT NOT NULL CHECK (char_length(content) > 0 AND char_length(content) <= 10000),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

CREATE INDEX idx_chat_messages_conversation_created ON chat_messages(conversation_id, created_at ASC);
CREATE INDEX idx_chat_messages_conversation_id ON chat_messages(conversation_id);
```

**Relationships**:
- `conversation_id` → `conversations.id` (many-to-one, CASCADE DELETE)

**Constraints**:
- `role`: Must be 'user' or 'assistant' (enum enforcement)
- `content`: 1-10,000 characters (CHECK constraint)

**Query Patterns**:
- Get all messages in a conversation: `SELECT * FROM chat_messages WHERE conversation_id = ? ORDER BY created_at ASC`
- Get last N messages: `SELECT * FROM chat_messages WHERE conversation_id = ? ORDER BY created_at DESC LIMIT ?`

## SQLModel Definitions

### `Conversation` Model

Location: `backend/src/models/conversation.py`

```python
class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    owner: "User" = Relationship(back_populates="conversations")
    messages: List["ChatMessage"] = Relationship(back_populates="conversation")
```

### `ChatMessage` Model

Location: `backend/src/models/chat_message.py`

```python
class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: MessageRole = Field(description="Message sender role")
    content: str = Field(min_length=1, max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
```

## Migration Files

### 003_create_conversations_table.sql

Creates the `conversations` table with:
- Auto-increment primary key
- Foreign key to `users.id` with CASCADE DELETE
- Indexes on `user_id` and `created_at`
- Timestamps for creation and last update

### 004_create_chat_messages_table.sql

Creates the `chat_messages` table with:
- Auto-increment primary key
- Foreign key to `conversations.id` with CASCADE DELETE
- Enum type `message_role` with values 'user' and 'assistant'
- CHECK constraint for content length (1-10,000 characters)
- Composite index on `(conversation_id, created_at)` for fast ordered retrieval

## Running Migrations

### Option 1: SQLModel Automatic Creation (Recommended for Development)

The backend automatically creates tables on startup using SQLModel's `create_all()`:

```bash
cd backend
python -c "from src.database import create_db_and_tables; create_db_and_tables()"
```

This approach:
- ✅ Idempotent (safe to run multiple times)
- ✅ Creates missing tables only
- ✅ Automatically creates indexes and constraints
- ✅ Type-safe (SQLModel validates schema matches code)

### Option 2: Manual SQL Migration (Production)

For explicit migration control:

```bash
cd database/migrations
python run_migrations.py
```

This approach:
- ✅ Explicit control over migration order
- ✅ Can include custom SQL (triggers, functions, etc.)
- ✅ Audit trail of migration history
- ⚠️ Requires manual tracking of applied migrations

## Verification

After running migrations, verify the schema:

```bash
cd backend
python -c "
from sqlmodel import Session, text
from src.database import engine

session = Session(engine)

# Verify tables exist
result = session.exec(text(
    \"SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'public' ORDER BY table_name\"
))
print('Tables:', [row[0] for row in result])

# Verify foreign keys
result = session.exec(text(
    \"SELECT tc.table_name, kcu.column_name, ccu.table_name AS foreign_table
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_name IN ('conversations', 'chat_messages')\"
))
print('Foreign Keys:', [(row[0], row[1], row[2]) for row in result])
"
```

Expected output:
```
Tables: ['chat_messages', 'conversations', 'tasks', 'users']
Foreign Keys: [('chat_messages', 'conversation_id', 'conversations'), ('conversations', 'user_id', 'users')]
```

## Performance Considerations

### Indexes

**conversations table**:
- `ix_conversations_user_id`: Fast lookup of conversations by user
- `ix_conversations_created_at`: Fast time-based ordering

**chat_messages table**:
- `ix_chat_messages_conversation_created`: Composite index for ordered message retrieval
- `ix_chat_messages_conversation_id`: Fast conversation message count queries

### Query Optimization

**Limit conversation history**: Always fetch last N messages (20 recommended) to prevent context overflow:
```sql
SELECT * FROM chat_messages
WHERE conversation_id = ?
ORDER BY created_at DESC
LIMIT 20
```

**Filter by user**: Always include user_id in conversation queries to leverage index:
```sql
SELECT c.*, COUNT(cm.id) as message_count
FROM conversations c
LEFT JOIN chat_messages cm ON c.id = cm.conversation_id
WHERE c.user_id = ?
GROUP BY c.id
ORDER BY c.updated_at DESC
```

## Security Enforcement

### User Isolation

**Rule**: All conversation queries MUST filter by authenticated `user_id` from JWT token.

**Enforcement**:
- Backend extracts `user_id` from verified JWT (never trusts client input)
- All queries include `WHERE conversations.user_id = ?` clause
- Foreign key constraints prevent orphaned conversations or messages

### Data Access Rules

**Conversations**:
- User can only access their own conversations (`user_id` filter)
- Deleting a user cascades to delete all their conversations
- Deleting a conversation cascades to delete all its messages

**Chat Messages**:
- Access controlled via parent conversation ownership
- No direct user_id filtering needed (enforced by conversation ownership)
- Content sanitized to prevent XSS (HTML/script tags removed)

## Rollback Plan

To rollback Phase III database changes:

```sql
-- Drop chat_messages table (must drop first due to foreign key)
DROP TABLE IF EXISTS chat_messages CASCADE;

-- Drop conversations table
DROP TABLE IF EXISTS conversations CASCADE;

-- Drop message_role enum type
DROP TYPE IF EXISTS message_role;
```

**Note**: This rollback will permanently delete all conversation data. Back up data before rollback if needed.

## Compliance Verification

✅ **Stateless Architecture**: All state persisted to database (no in-memory storage)
✅ **User Isolation**: All conversations linked to users via foreign key
✅ **Phase II Stability**: No modifications to existing tables
✅ **Cascading Delete**: User deletion removes conversations and messages
✅ **Indexed Queries**: All common query patterns have supporting indexes
✅ **Schema Validation**: SQLModel enforces data types and constraints
✅ **Migration Safety**: Additive migrations only, idempotent execution

## Next Steps

After completing database foundation (T010-T014):
1. Implement authentication foundation (T015-T016)
2. Create MCP tool infrastructure (T017-T019)
3. Build AI chatbot features (User Stories 1-6)

---

**Version**: 1.0.0
**Last Updated**: 2026-02-08
**Phase**: III (AI Chatbot Integration)
