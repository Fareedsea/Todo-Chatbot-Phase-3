// T038, T054, T067, T078: useTasks hook for all task operations with optimistic UI

'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { queryKeys } from '@/lib/query-client';
import { Task, TaskCreateInput, TaskUpdateInput } from '@/types/task';
import { handleError, logError } from '@/lib/error-handler';

// Fetch all tasks
export const useTasks = () => {
  return useQuery<Task[]>({
    queryKey: queryKeys.tasks.lists(),
    queryFn: async () => {
      const response = await apiClient.tasks.getAll();
      // API returns { tasks: Task[] }, extract the array
      const data = response as { tasks: Task[] };
      return data.tasks || [];
    },
  });
};

// Fetch single task
export const useTask = (id: string) => {
  return useQuery<Task>({
    queryKey: queryKeys.tasks.detail(id),
    queryFn: async () => {
      const response = await apiClient.tasks.getOne(id);
      return response as Task;
    },
    enabled: !!id,
  });
};

// Create task with optimistic UI
export const useCreateTask = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: TaskCreateInput) => {
      const response = await apiClient.tasks.create(data);
      // API returns { task: Task }, extract the task
      const result = response as { task: Task };
      return result.task;
    },
    onMutate: async (newTask) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: queryKeys.tasks.lists() });

      // Snapshot previous value
      const previousTasks = queryClient.getQueryData<Task[]>(
        queryKeys.tasks.lists()
      );

      // Optimistically update to the new value
      const optimisticTask: Task = {
        id: `temp-${Date.now()}`,
        title: newTask.title,
        description: newTask.description || null,
        dueDate: newTask.dueDate || null,
        isCompleted: newTask.isCompleted || false,
        userId: '', // Will be set by server
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      queryClient.setQueryData<Task[]>(
        queryKeys.tasks.lists(),
        (old = []) => [...old, optimisticTask]
      );

      return { previousTasks, optimisticTask };
    },
    onError: (error, _newTask, context) => {
      // Rollback to previous value
      if (context?.previousTasks) {
        queryClient.setQueryData(queryKeys.tasks.lists(), context.previousTasks);
      }
      logError(error, 'Create Task');
    },
    onSuccess: (data, _variables, context) => {
      // Replace optimistic task with real task
      queryClient.setQueryData<Task[]>(
        queryKeys.tasks.lists(),
        (old = []) => {
          return old.map((task) =>
            task.id === context?.optimisticTask.id ? data : task
          );
        }
      );
    },
    onSettled: () => {
      // Always refetch after error or success
      queryClient.invalidateQueries({ queryKey: queryKeys.tasks.lists() });
    },
  });
};

// Update task with optimistic UI
export const useUpdateTask = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: TaskUpdateInput }) => {
      const response = await apiClient.tasks.update(id, data);
      // API returns { task: Task }, extract the task
      const result = response as { task: Task };
      return result.task;
    },
    onMutate: async ({ id, data }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: queryKeys.tasks.lists() });

      // Snapshot previous value
      const previousTasks = queryClient.getQueryData<Task[]>(
        queryKeys.tasks.lists()
      );

      // Optimistically update
      queryClient.setQueryData<Task[]>(
        queryKeys.tasks.lists(),
        (old = []) => {
          return old.map((task) =>
            task.id === id
              ? { ...task, ...data, updatedAt: new Date().toISOString() }
              : task
          );
        }
      );

      return { previousTasks };
    },
    onError: (error, _variables, context) => {
      // Rollback to previous value
      if (context?.previousTasks) {
        queryClient.setQueryData(queryKeys.tasks.lists(), context.previousTasks);
      }
      logError(error, 'Update Task');
    },
    onSettled: () => {
      // Always refetch after error or success
      queryClient.invalidateQueries({ queryKey: queryKeys.tasks.lists() });
    },
  });
};

// Delete task with optimistic UI
export const useDeleteTask = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      await apiClient.tasks.delete(id);
      return id;
    },
    onMutate: async (id) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: queryKeys.tasks.lists() });

      // Snapshot previous value
      const previousTasks = queryClient.getQueryData<Task[]>(
        queryKeys.tasks.lists()
      );

      // Optimistically remove from list
      queryClient.setQueryData<Task[]>(
        queryKeys.tasks.lists(),
        (old = []) => old.filter((task) => task.id !== id)
      );

      return { previousTasks };
    },
    onError: (error, _id, context) => {
      // Rollback to previous value
      if (context?.previousTasks) {
        queryClient.setQueryData(queryKeys.tasks.lists(), context.previousTasks);
      }
      logError(error, 'Delete Task');
    },
    onSettled: () => {
      // Always refetch after error or success
      queryClient.invalidateQueries({ queryKey: queryKeys.tasks.lists() });
    },
  });
};
