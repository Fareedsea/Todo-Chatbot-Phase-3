// T042, T098: Dashboard page with lazy-loaded modals for performance

'use client';

import React, { useState } from 'react';
import dynamic from 'next/dynamic';
import { useTasks, useUpdateTask } from '@/hooks/useTasks';
import TaskList from '@/components/tasks/TaskList';
import Button from '@/components/ui/Button';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import { Task } from '@/types/task';

// Lazy load modals - only load when needed (T098: Code splitting)
const TaskCreateModal = dynamic(() => import('@/components/tasks/TaskCreateModal'), {
  loading: () => <LoadingSpinner size="md" />,
});

const TaskEditModal = dynamic(() => import('@/components/tasks/TaskEditModal'), {
  loading: () => <LoadingSpinner size="md" />,
});

const TaskDeleteDialog = dynamic(() => import('@/components/tasks/TaskDeleteDialog'), {
  loading: () => <LoadingSpinner size="md" />,
});

export default function DashboardPage() {
  const { data: tasks, isLoading, isError, error, refetch } = useTasks();
  const { mutateAsync: updateTask } = useUpdateTask();

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deletingTask, setDeletingTask] = useState<Task | null>(null);

  const handleToggleComplete = async (task: Task) => {
    try {
      await updateTask({
        id: task.id,
        data: { isCompleted: !task.isCompleted },
      });
    } catch (error) {
      console.error('Failed to toggle task completion:', error);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
  };

  const handleDeleteTask = (task: Task) => {
    setDeletingTask(task);
  };

  // Loading state
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner size="lg" label="Loading your tasks..." />
      </div>
    );
  }

  // Error state
  if (isError) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-sm border border-error-200 p-6">
          <div className="flex items-start gap-3">
            <svg
              className="h-6 w-6 text-error-600 flex-shrink-0 mt-0.5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <div className="flex-1">
              <h3 className="text-lg font-medium text-gray-900 mb-1">
                Failed to load tasks
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                {error instanceof Error
                  ? error.message
                  : 'An unexpected error occurred. Please try again.'}
              </p>
              <Button onClick={() => refetch()} variant="primary" size="sm">
                Try Again
              </Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Empty state
  if (!tasks || tasks.length === 0) {
    return (
      <div className="max-w-2xl mx-auto">
        <EmptyState
          icon={
            <svg
              className="h-16 w-16"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
          }
          title="No tasks yet"
          description="Get started by creating your first task. Stay organized and track your progress."
          action={{
            label: 'Create Your First Task',
            onClick: () => setIsCreateModalOpen(true),
          }}
        />

        <TaskCreateModal
          isOpen={isCreateModalOpen}
          onClose={() => setIsCreateModalOpen(false)}
        />
      </div>
    );
  }

  // Task list with data
  const incompleteTasks = tasks.filter((task) => !task.isCompleted);
  const completedTasks = tasks.filter((task) => task.isCompleted);

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header with Create Button */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
          <p className="mt-1 text-sm text-gray-600">
            {incompleteTasks.length} active,{' '}
            {completedTasks.length} completed
          </p>
        </div>
        <Button
          onClick={() => setIsCreateModalOpen(true)}
          variant="primary"
          size="md"
          leftIcon={
            <svg
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4v16m8-8H4"
              />
            </svg>
          }
        >
          <span className="hidden sm:inline">Create Task</span>
          <span className="sm:hidden">New</span>
        </Button>
      </div>

      {/* Task Lists */}
      <div className="space-y-8">
        {/* Active Tasks */}
        {incompleteTasks.length > 0 && (
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-3">
              Active Tasks
            </h2>
            <TaskList
              tasks={incompleteTasks}
              onEditTask={handleEditTask}
              onDeleteTask={handleDeleteTask}
              onToggleComplete={handleToggleComplete}
            />
          </div>
        )}

        {/* Completed Tasks */}
        {completedTasks.length > 0 && (
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-3">
              Completed Tasks
            </h2>
            <TaskList
              tasks={completedTasks}
              onEditTask={handleEditTask}
              onDeleteTask={handleDeleteTask}
              onToggleComplete={handleToggleComplete}
            />
          </div>
        )}
      </div>

      {/* Modals */}
      <TaskCreateModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
      />

      <TaskEditModal
        task={editingTask}
        isOpen={!!editingTask}
        onClose={() => setEditingTask(null)}
      />

      <TaskDeleteDialog
        task={deletingTask}
        isOpen={!!deletingTask}
        onClose={() => setDeletingTask(null)}
      />
    </div>
  );
}
