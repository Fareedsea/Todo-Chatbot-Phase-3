-- Migration: 003_create_conversations_table.sql
-- Purpose: Create conversations table for AI chatbot chat sessions
-- Phase: III (AI Chatbot Integration)
-- Constitutional Compliance: Additive migration - does not modify Phase II tables

-- Create conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key constraint: conversations belong to users
    CONSTRAINT fk_conversations_user_id
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Create index on user_id for fast conversation lookups by user
-- Query pattern: SELECT * FROM conversations WHERE user_id = ?
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);

-- Create index on created_at for time-based ordering
-- Query pattern: SELECT * FROM conversations WHERE user_id = ? ORDER BY created_at DESC
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at DESC);

-- Comments for documentation
COMMENT ON TABLE conversations IS 'Chat sessions between users and the AI assistant';
COMMENT ON COLUMN conversations.id IS 'Unique conversation identifier (auto-increment)';
COMMENT ON COLUMN conversations.user_id IS 'Foreign key to users.id (owner of conversation)';
COMMENT ON COLUMN conversations.created_at IS 'Conversation creation timestamp (UTC, immutable)';
COMMENT ON COLUMN conversations.updated_at IS 'Last message timestamp (UTC, auto-updated)';
