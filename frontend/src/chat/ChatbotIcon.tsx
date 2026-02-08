/**
 * Chatbot Icon Component
 *
 * Floating action button that toggles the chat window.
 * Always visible in bottom-right corner for authenticated users.
 */

'use client';

import { useState } from 'react';
import ChatWindow from './ChatWindow';

export default function ChatbotIcon() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      {/* Floating Chat Button */}
      <button
        onClick={toggleChat}
        className={`
          fixed bottom-6 right-6 z-50
          w-14 h-14 rounded-full
          bg-blue-600 hover:bg-blue-700
          text-white shadow-lg hover:shadow-xl
          transition-all duration-200 ease-in-out
          flex items-center justify-center
          focus:outline-none focus:ring-4 focus:ring-blue-300
          ${isOpen ? 'scale-0' : 'scale-100'}
        `}
        aria-label="Open chat"
        title="Chat with AI Assistant"
      >
        {/* Chat Icon (speech bubble) */}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={2}
          stroke="currentColor"
          className="w-6 h-6"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z"
          />
        </svg>

        {/* Notification Badge (optional - for unread messages) */}
        {/* <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full text-xs flex items-center justify-center">
          1
        </span> */}
      </button>

      {/* Chat Window Modal */}
      {isOpen && (
        <ChatWindow
          isOpen={isOpen}
          onClose={() => setIsOpen(false)}
        />
      )}
    </>
  );
}
