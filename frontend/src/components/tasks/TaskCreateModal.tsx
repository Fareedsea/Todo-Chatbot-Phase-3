// T051, T052, T053: TaskCreateModal component with form and validation

'use client';

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import Modal from '@/components/ui/Modal';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import { useCreateTask } from '@/hooks/useTasks';
import { TaskCreateInput } from '@/types/task';

const taskCreateSchema = z.object({
  title: z
    .string()
    .min(1, 'Title is required')
    .max(200, 'Title must be 200 characters or less'),
  description: z
    .string()
    .max(1000, 'Description must be 1000 characters or less')
    .optional()
    .nullable(),
  dueDate: z
    .string()
    .optional()
    .nullable()
    .refine((date) => {
      if (!date) return true;
      const selectedDate = new Date(date);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      return selectedDate >= today;
    }, 'Due date cannot be in the past'),
});

type TaskCreateFormData = z.infer<typeof taskCreateSchema>;

interface TaskCreateModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

const TaskCreateModal: React.FC<TaskCreateModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
}) => {
  const { mutateAsync: createTask, isPending } = useCreateTask();
  const [serverError, setServerError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    watch,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<TaskCreateFormData>({
    resolver: zodResolver(taskCreateSchema),
    defaultValues: {
      title: '',
      description: '',
      dueDate: '',
    },
  });

  const titleLength = watch('title')?.length || 0;
  const descriptionLength = watch('description')?.length || 0;

  const onSubmit = async (data: TaskCreateFormData) => {
    setServerError(null);

    try {
      const input: TaskCreateInput = {
        title: data.title,
        description: data.description || null,
        dueDate: data.dueDate || null,
        isCompleted: false,
      };

      await createTask(input);
      reset();
      onClose();
      onSuccess?.();
    } catch (error) {
      if (error instanceof Error) {
        setServerError(error.message);
      } else {
        setServerError('Failed to create task. Please try again.');
      }
    }
  };

  const handleClose = () => {
    reset();
    setServerError(null);
    onClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="Create New Task"
      description="Add a new task to your list"
      size="md"
    >
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {serverError && (
          <div
            className="p-3 bg-error-50 border border-error-200 rounded-lg"
            role="alert"
          >
            <p className="text-sm text-error-700">{serverError}</p>
          </div>
        )}

        <div>
          <Input
            {...register('title')}
            label="Title"
            placeholder="Enter task title"
            error={errors.title?.message}
            required
            disabled={isSubmitting || isPending}
            maxLength={200}
          />
          <div className="mt-1 text-right">
            <span
              className={`text-xs ${
                titleLength > 180
                  ? 'text-error-600 font-medium'
                  : 'text-gray-500'
              }`}
            >
              {titleLength}/200
            </span>
          </div>
        </div>

        <div>
          <label
            htmlFor="description"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Description
          </label>
          <textarea
            {...register('description')}
            id="description"
            placeholder="Enter task description (optional)"
            disabled={isSubmitting || isPending}
            maxLength={1000}
            rows={4}
            className="w-full px-4 py-2 rounded-lg border border-gray-300 text-gray-900 placeholder-gray-400 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed disabled:text-gray-500"
          />
          {errors.description && (
            <p className="mt-1 text-sm text-error-500" role="alert">
              {errors.description.message}
            </p>
          )}
          <div className="mt-1 text-right">
            <span
              className={`text-xs ${
                descriptionLength > 900
                  ? 'text-error-600 font-medium'
                  : 'text-gray-500'
              }`}
            >
              {descriptionLength}/1000
            </span>
          </div>
        </div>

        <Input
          {...register('dueDate')}
          type="date"
          label="Due Date"
          error={errors.dueDate?.message}
          disabled={isSubmitting || isPending}
          min={new Date().toISOString().split('T')[0]}
        />

        <div className="flex gap-3 pt-4">
          <Button
            type="button"
            onClick={handleClose}
            variant="secondary"
            className="flex-1"
            disabled={isSubmitting || isPending}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            variant="primary"
            className="flex-1"
            isLoading={isSubmitting || isPending}
            disabled={isSubmitting || isPending}
          >
            Create Task
          </Button>
        </div>
      </form>
    </Modal>
  );
};

export default TaskCreateModal;
