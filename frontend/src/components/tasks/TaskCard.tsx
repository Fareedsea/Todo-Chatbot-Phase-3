// T040: TaskCard component displaying task details

'use client';

import React from 'react';
import { Task } from '@/types/task';
import { cn } from '@/lib/utils';
import Button from '@/components/ui/Button';

interface TaskCardProps {
  task: Task;
  onEdit?: (task: Task) => void;
  onDelete?: (task: Task) => void;
  onToggleComplete?: (task: Task) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({
  task,
  onEdit,
  onDelete,
  onToggleComplete,
}) => {
  const formatDate = (dateString: string | null) => {
    if (!dateString) return null;

    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    } catch {
      return null;
    }
  };

  const isOverdue = (dueDate: string | null) => {
    if (!dueDate || task.isCompleted) return false;
    return new Date(dueDate) < new Date();
  };

  return (
    <div
      className={cn(
        'bg-white rounded-lg shadow-sm border p-4',
        'transition-all duration-200',
        'hover:shadow-md hover:border-gray-300',
        task.isCompleted ? 'border-gray-200 opacity-75' : 'border-gray-200'
      )}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <button
          onClick={() => onToggleComplete?.(task)}
          className={cn(
            'mt-1 flex-shrink-0 w-5 h-5 rounded border-2',
            'transition-colors duration-200',
            'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
            task.isCompleted
              ? 'bg-primary-600 border-primary-600'
              : 'border-gray-300 hover:border-primary-400'
          )}
          aria-label={task.isCompleted ? 'Mark as incomplete' : 'Mark as complete'}
        >
          {task.isCompleted && (
            <svg
              className="w-full h-full text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={3}
                d="M5 13l4 4L19 7"
              />
            </svg>
          )}
        </button>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <h3
            className={cn(
              'text-base font-medium',
              task.isCompleted
                ? 'text-gray-500 line-through'
                : 'text-gray-900'
            )}
          >
            {task.title}
          </h3>

          {task.description && (
            <p
              className={cn(
                'mt-1 text-sm',
                task.isCompleted ? 'text-gray-400' : 'text-gray-600'
              )}
            >
              {task.description}
            </p>
          )}

          {task.dueDate && (
            <div className="mt-2 flex items-center gap-1 text-xs">
              <svg
                className="w-4 h-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
              <span
                className={cn(
                  'font-medium',
                  isOverdue(task.dueDate)
                    ? 'text-error-600'
                    : task.isCompleted
                    ? 'text-gray-400'
                    : 'text-gray-600'
                )}
              >
                {formatDate(task.dueDate)}
                {isOverdue(task.dueDate) && ' (Overdue)'}
              </span>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-2">
          {onEdit && (
            <Button
              onClick={() => onEdit(task)}
              variant="ghost"
              size="sm"
              aria-label="Edit task"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                />
              </svg>
            </Button>
          )}

          {onDelete && (
            <Button
              onClick={() => onDelete(task)}
              variant="ghost"
              size="sm"
              aria-label="Delete task"
            >
              <svg
                className="w-4 h-4 text-error-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};

export default TaskCard;
