// T013: TypeScript types for API requests/responses

import { Task } from './task';
import { User } from './auth';

// Error response from API
export interface ErrorResponse {
  error: string;
  message: string;
  details?: Record<string, string>;
  status: number;
}

// Auth API responses
export interface AuthResponse {
  user: User;
  token: string;
}

// Task API responses
export interface GetTasksResponse {
  tasks: Task[];
}

export interface GetTaskResponse {
  task: Task;
}

export interface CreateTaskRequest {
  title: string;
  description?: string | null;
  dueDate?: string | null;
  isCompleted?: boolean;
}

export interface CreateTaskResponse {
  task: Task;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string | null;
  dueDate?: string | null;
  isCompleted?: boolean;
}

export interface UpdateTaskResponse {
  task: Task;
}

export interface DeleteTaskResponse {
  message: string;
}

// HTTP Status codes enum
export enum HttpStatus {
  OK = 200,
  CREATED = 201,
  BAD_REQUEST = 400,
  UNAUTHORIZED = 401,
  FORBIDDEN = 403,
  NOT_FOUND = 404,
  CONFLICT = 409,
  UNPROCESSABLE_ENTITY = 422,
  INTERNAL_SERVER_ERROR = 500,
}

// API Error codes
export enum ApiErrorCode {
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  AUTHENTICATION_ERROR = 'AUTHENTICATION_ERROR',
  AUTHORIZATION_ERROR = 'AUTHORIZATION_ERROR',
  UNAUTHORIZED = 'UNAUTHORIZED',
  FORBIDDEN = 'FORBIDDEN',
  RESOURCE_NOT_FOUND = 'RESOURCE_NOT_FOUND',
  NOT_FOUND = 'NOT_FOUND',
  DUPLICATE_RESOURCE = 'DUPLICATE_RESOURCE',
  EMAIL_EXISTS = 'EMAIL_EXISTS',
  INVALID_CREDENTIALS = 'INVALID_CREDENTIALS',
  RATE_LIMIT_ERROR = 'RATE_LIMIT_ERROR',
  SERVER_ERROR = 'SERVER_ERROR',
  NETWORK_ERROR = 'NETWORK_ERROR',
}
