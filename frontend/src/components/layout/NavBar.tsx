// T032: NavBar component with logout functionality

'use client';

import React from 'react';
import Link from 'next/link';
import Button from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';

const NavBar: React.FC = () => {
  const { user, logout, isLoading } = useAuth();

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo/Brand */}
          <Link
            href="/dashboard"
            className="flex items-center gap-2 text-xl font-bold text-gray-900 hover:text-primary-600 transition-colors"
          >
            <svg
              className="h-8 w-8 text-primary-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
            <span>Todo App</span>
          </Link>

          {/* User Info & Actions */}
          <div className="flex items-center gap-4">
            {user && (
              <span className="text-sm text-gray-600 hidden sm:block">
                {user.email}
              </span>
            )}

            <Button
              onClick={logout}
              variant="ghost"
              size="sm"
              isLoading={isLoading}
              disabled={isLoading}
              aria-label="Sign out"
            >
              <svg
                className="h-5 w-5 mr-1"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                />
              </svg>
              <span className="hidden sm:inline">Sign Out</span>
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
