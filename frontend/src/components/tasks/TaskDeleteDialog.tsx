// T077: TaskDeleteDialog component with confirmation

'use client';

import React, { useState } from 'react';
import Modal from '@/components/ui/Modal';
import Button from '@/components/ui/Button';
import { useDeleteTask } from '@/hooks/useTasks';
import { Task } from '@/types/task';

interface TaskDeleteDialogProps {
  task: Task | null;
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

const TaskDeleteDialog: React.FC<TaskDeleteDialogProps> = ({
  task,
  isOpen,
  onClose,
  onSuccess,
}) => {
  const { mutateAsync: deleteTask, isPending } = useDeleteTask();
  const [serverError, setServerError] = useState<string | null>(null);

  const handleDelete = async () => {
    if (!task) return;

    setServerError(null);

    try {
      await deleteTask(task.id);
      onClose();
      onSuccess?.();
    } catch (error) {
      if (error instanceof Error) {
        setServerError(error.message);
      } else {
        setServerError('Failed to delete task. Please try again.');
      }
    }
  };

  const handleClose = () => {
    setServerError(null);
    onClose();
  };

  if (!task) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="Delete Task"
      size="sm"
      showCloseButton={false}
    >
      <div className="space-y-4">
        {serverError && (
          <div
            className="p-3 bg-error-50 border border-error-200 rounded-lg"
            role="alert"
          >
            <p className="text-sm text-error-700">{serverError}</p>
          </div>
        )}

        <div className="flex items-start gap-3">
          <div className="flex-shrink-0">
            <svg
              className="h-6 w-6 text-error-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-medium text-gray-900">
              Are you sure?
            </h3>
            <p className="mt-2 text-sm text-gray-600">
              This will permanently delete the task:{' '}
              <span className="font-medium">{task.title}</span>. This action
              cannot be undone.
            </p>
          </div>
        </div>

        <div className="flex gap-3 pt-4">
          <Button
            type="button"
            onClick={handleClose}
            variant="secondary"
            className="flex-1"
            disabled={isPending}
          >
            Cancel
          </Button>
          <Button
            type="button"
            onClick={handleDelete}
            variant="danger"
            className="flex-1"
            isLoading={isPending}
            disabled={isPending}
          >
            Delete
          </Button>
        </div>
      </div>
    </Modal>
  );
};

export default TaskDeleteDialog;
