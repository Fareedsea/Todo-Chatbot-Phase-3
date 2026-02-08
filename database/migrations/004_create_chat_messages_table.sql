-- Migration: 004_create_chat_messages_table.sql
-- Purpose: Create chat_messages table for storing user and assistant messages
-- Phase: III (AI Chatbot Integration)
-- Constitutional Compliance: Additive migration - does not modify Phase II tables

-- Create custom enum type for message roles
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'message_role') THEN
        CREATE TYPE message_role AS ENUM ('user', 'assistant');
    END IF;
END $$;

-- Create chat_messages table
CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    role message_role NOT NULL,
    content TEXT NOT NULL CHECK (char_length(content) > 0 AND char_length(content) <= 10000),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key constraint: messages belong to conversations
    CONSTRAINT fk_chat_messages_conversation_id
        FOREIGN KEY (conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE
);

-- Create composite index for fast message retrieval ordered by time
-- Query pattern: SELECT * FROM chat_messages WHERE conversation_id = ? ORDER BY created_at ASC
CREATE INDEX IF NOT EXISTS idx_chat_messages_conversation_created
    ON chat_messages(conversation_id, created_at ASC);

-- Create index on conversation_id alone for conversation message count queries
-- Query pattern: SELECT COUNT(*) FROM chat_messages WHERE conversation_id = ?
CREATE INDEX IF NOT EXISTS idx_chat_messages_conversation_id
    ON chat_messages(conversation_id);

-- Comments for documentation
COMMENT ON TABLE chat_messages IS 'Individual messages in chat conversations (user or assistant)';
COMMENT ON COLUMN chat_messages.id IS 'Unique message identifier (auto-increment)';
COMMENT ON COLUMN chat_messages.conversation_id IS 'Foreign key to conversations.id (parent conversation)';
COMMENT ON COLUMN chat_messages.role IS 'Message sender role: user or assistant';
COMMENT ON COLUMN chat_messages.content IS 'Message text content (1-10000 characters)';
COMMENT ON COLUMN chat_messages.created_at IS 'Message creation timestamp (UTC, immutable)';
