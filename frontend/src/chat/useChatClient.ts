/**
 * Chat API Client Hook
 *
 * Provides API client for chat operations with JWT authentication.
 * Handles message sending, conversation management, and error handling.
 */

'use client';

import { useState, useCallback } from 'react';
import { ApiError } from '@/lib/api-client';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Chat message types
 */
export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string | null;
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  task_action?: string | null;
}

/**
 * Get JWT token from storage
 */
function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('auth_token');
}

/**
 * Custom hook for chat API operations
 */
export function useChatClient() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Send a message to the chat API
   */
  const sendMessage = useCallback(async (
    message: string,
    conversationId?: string | null
  ): Promise<ChatResponse | null> => {
    setIsLoading(true);
    setError(null);

    try {
      const token = getToken();

      if (!token) {
        throw new ApiError(
          'Authentication required. Please sign in.',
          401,
          'UNAUTHORIZED'
        );
      }

      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          message,
          conversation_id: conversationId || null,
        } as ChatRequest),
      });

      if (!response.ok) {
        // Handle different error status codes
        if (response.status === 401) {
          throw new ApiError(
            'Your session has expired. Please refresh the page and sign in again.',
            401,
            'UNAUTHORIZED'
          );
        }

        if (response.status === 400) {
          const errorData = await response.json().catch(() => ({}));
          throw new ApiError(
            errorData.detail || 'Invalid message. Please try again.',
            400,
            'BAD_REQUEST'
          );
        }

        if (response.status >= 500) {
          throw new ApiError(
            'The chat service is temporarily unavailable. Please try again in a moment.',
            response.status,
            'SERVER_ERROR'
          );
        }

        throw new ApiError(
          'Something went wrong. Please try again.',
          response.status,
          'UNKNOWN_ERROR'
        );
      }

      const data: ChatResponse = await response.json();
      return data;

    } catch (err) {
      const errorMessage = err instanceof ApiError
        ? err.message
        : 'Failed to send message. Please check your connection and try again.';

      setError(errorMessage);
      console.error('Chat API error:', err);
      return null;

    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Clear error state
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    sendMessage,
    isLoading,
    error,
    clearError,
  };
}

/**
 * Hook for managing chat conversation state
 */
export function useChatConversation() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);

  /**
   * Add a user message to the conversation
   */
  const addUserMessage = useCallback((content: string) => {
    setMessages(prev => [
      ...prev,
      {
        role: 'user',
        content,
        timestamp: new Date().toISOString(),
      },
    ]);
  }, []);

  /**
   * Add an assistant message to the conversation
   */
  const addAssistantMessage = useCallback((content: string) => {
    setMessages(prev => [
      ...prev,
      {
        role: 'assistant',
        content,
        timestamp: new Date().toISOString(),
      },
    ]);
  }, []);

  /**
   * Set the conversation ID
   */
  const setConversation = useCallback((id: string) => {
    setConversationId(id);
  }, []);

  /**
   * Clear all messages and conversation
   */
  const clearConversation = useCallback(() => {
    setMessages([]);
    setConversationId(null);
  }, []);

  return {
    messages,
    conversationId,
    addUserMessage,
    addAssistantMessage,
    setConversation,
    clearConversation,
  };
}
