// T014: TypeScript types for Task entity

export interface Task {
  id: string;
  title: string;
  description: string | null;
  dueDate: string | null; // ISO 8601 format
  isCompleted: boolean;
  createdAt: string; // ISO 8601 format
  updatedAt: string; // ISO 8601 format
  userId: string;
}

export interface TaskFormData {
  title: string;
  description?: string | null;
  dueDate?: string | null;
  isCompleted?: boolean;
}

export interface TasksQueryState {
  data: Task[];
  isLoading: boolean;
  isFetching: boolean;
  isError: boolean;
  error: Error | null;
  refetch: () => void;
}

export interface TaskMutationState {
  isPending: boolean;
  error: string | null;
  data: Task | null;
}

export interface TaskCreateInput {
  title: string;
  description?: string | null;
  dueDate?: string | null;
  isCompleted?: boolean;
}

export interface TaskUpdateInput {
  title?: string;
  description?: string | null;
  dueDate?: string | null;
  isCompleted?: boolean;
}
