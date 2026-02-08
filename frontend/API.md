# API Integration Guide

Complete guide for integrating with the Todo Web App backend API.

## Table of Contents

- [Overview](#overview)
- [API Client](#api-client)
- [Authentication](#authentication)
- [Task Management](#task-management)
- [Error Handling](#error-handling)
- [Testing](#testing)

---

## Overview

The frontend communicates with the backend through a centralized API client that automatically handles:
- JWT token injection
- Request/response validation
- Error handling and retry logic
- Type safety with TypeScript

**Base URL**: Configured via `NEXT_PUBLIC_API_URL` environment variable

**API Version**: v1 (implicitly included in all endpoints)

---

## API Client

### Location
`frontend/src/lib/api-client.ts`

### Architecture

The API client is a singleton that provides type-safe methods for all backend endpoints:

```typescript
import { apiClient } from '@/lib/api-client';

// All requests automatically include JWT token if available
const tasks = await apiClient.tasks.getAll();
```

### Key Features

1. **Automatic JWT Injection**: Reads token from localStorage and adds to Authorization header
2. **Type Safety**: All requests/responses are typed with TypeScript interfaces
3. **Error Handling**: Converts HTTP errors to typed ApiError instances
4. **Network Error Detection**: Distinguishes between server and network errors

### Token Management

```typescript
import { setToken, removeToken } from '@/lib/api-client';

// Store token after successful authentication
setToken(response.token);

// Remove token on logout
removeToken();
```

---

## Authentication

### Endpoints

#### POST /api/auth/register

Register a new user account.

**Request**:
```typescript
{
  email: string;      // Valid email format
  password: string;   // Min 8 chars, uppercase, lowercase, number
}
```

**Response** (201 Created):
```typescript
{
  user: {
    id: string;
    email: string;
    createdAt: string;  // ISO 8601
  };
  token: string;        // JWT token
}
```

**Errors**:
- `400` - Validation error (invalid email/password)
- `409` - Email already exists
- `500` - Server error

**Example**:
```typescript
import { apiClient } from '@/lib/api-client';
import { setToken } from '@/lib/api-client';

try {
  const response = await apiClient.auth.register(
    'user@example.com',
    'SecurePass123'
  );

  setToken(response.token);
  console.log('User created:', response.user);
} catch (error) {
  if (error instanceof ApiError) {
    if (error.code === 'EMAIL_EXISTS') {
      console.error('Email already registered');
    }
  }
}
```

#### POST /api/auth/login

Authenticate an existing user.

**Request**:
```typescript
{
  email: string;
  password: string;
}
```

**Response** (200 OK):
```typescript
{
  user: {
    id: string;
    email: string;
    createdAt: string;
  };
  token: string;
}
```

**Errors**:
- `400` - Validation error
- `401` - Invalid credentials
- `500` - Server error

**Example**:
```typescript
try {
  const response = await apiClient.auth.login(
    'user@example.com',
    'SecurePass123'
  );

  setToken(response.token);
  // Redirect to dashboard
} catch (error) {
  if (error instanceof ApiError && error.code === 'INVALID_CREDENTIALS') {
    console.error('Wrong email or password');
  }
}
```

#### POST /api/auth/logout

Invalidate the current session (optional backend implementation).

**Request**: None (token in header)

**Response** (200 OK):
```typescript
{
  message: string;
}
```

**Example**:
```typescript
import { removeToken } from '@/lib/api-client';

try {
  await apiClient.auth.logout();
} finally {
  removeToken();
  // Redirect to sign-in page
}
```

---

## Task Management

All task endpoints require authentication (JWT token in Authorization header).

### Endpoints

#### GET /api/tasks

Retrieve all tasks for the authenticated user.

**Request**: None (token in header)

**Response** (200 OK):
```typescript
Task[] // Array of task objects
```

**Task Schema**:
```typescript
{
  id: string;
  title: string;
  description: string | null;
  dueDate: string | null;     // ISO 8601 or null
  isCompleted: boolean;
  userId: string;
  createdAt: string;           // ISO 8601
  updatedAt: string;           // ISO 8601
}
```

**Errors**:
- `401` - Unauthorized (missing/invalid token)
- `500` - Server error

**Example**:
```typescript
import { useTasks } from '@/hooks/useTasks';

function TaskListComponent() {
  const { data: tasks, isLoading, error } = useTasks();

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return <TaskList tasks={tasks} />;
}
```

#### GET /api/tasks/:id

Retrieve a single task by ID.

**Request**: None (token in header, id in URL)

**Response** (200 OK):
```typescript
Task // Single task object
```

**Errors**:
- `401` - Unauthorized
- `404` - Task not found or not owned by user
- `500` - Server error

**Example**:
```typescript
import { useTask } from '@/hooks/useTasks';

function TaskDetailComponent({ taskId }: { taskId: string }) {
  const { data: task, isLoading } = useTask(taskId);

  if (isLoading) return <LoadingSpinner />;

  return <TaskCard task={task} />;
}
```

#### POST /api/tasks

Create a new task.

**Request**:
```typescript
{
  title: string;                    // Required, max 200 chars
  description?: string | null;      // Optional, max 1000 chars
  dueDate?: string | null;          // Optional, ISO 8601
  isCompleted?: boolean;            // Optional, default false
}
```

**Response** (201 Created):
```typescript
Task // Newly created task with id
```

**Errors**:
- `400` - Validation error (missing title, invalid format)
- `401` - Unauthorized
- `500` - Server error

**Example**:
```typescript
import { useCreateTask } from '@/hooks/useTasks';

function CreateTaskForm() {
  const { mutateAsync: createTask, isPending } = useCreateTask();

  const handleSubmit = async (data: TaskCreateInput) => {
    try {
      const newTask = await createTask({
        title: data.title,
        description: data.description || null,
        dueDate: data.dueDate || null,
        isCompleted: false,
      });

      console.log('Task created:', newTask);
    } catch (error) {
      console.error('Failed to create task:', error);
    }
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

#### PUT /api/tasks/:id

Update an existing task.

**Request**:
```typescript
{
  title?: string;               // Optional, max 200 chars
  description?: string | null;  // Optional, max 1000 chars
  dueDate?: string | null;      // Optional, ISO 8601
  isCompleted?: boolean;        // Optional
}
```

**Response** (200 OK):
```typescript
Task // Updated task
```

**Errors**:
- `400` - Validation error
- `401` - Unauthorized
- `404` - Task not found or not owned by user
- `500` - Server error

**Example**:
```typescript
import { useUpdateTask } from '@/hooks/useTasks';

function EditTaskForm({ task }: { task: Task }) {
  const { mutateAsync: updateTask, isPending } = useUpdateTask();

  const handleSubmit = async (data: TaskUpdateInput) => {
    try {
      const updatedTask = await updateTask({
        id: task.id,
        data: {
          title: data.title,
          description: data.description,
          isCompleted: data.isCompleted,
        },
      });

      console.log('Task updated:', updatedTask);
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

#### DELETE /api/tasks/:id

Delete a task.

**Request**: None (token in header, id in URL)

**Response** (200 OK):
```typescript
{
  message: string;  // Success message
}
```

**Errors**:
- `401` - Unauthorized
- `404` - Task not found or not owned by user
- `500` - Server error

**Example**:
```typescript
import { useDeleteTask } from '@/hooks/useTasks';

function DeleteTaskButton({ taskId }: { taskId: string }) {
  const { mutateAsync: deleteTask, isPending } = useDeleteTask();

  const handleDelete = async () => {
    try {
      await deleteTask(taskId);
      console.log('Task deleted');
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  return (
    <button onClick={handleDelete} disabled={isPending}>
      Delete
    </button>
  );
}
```

---

## Error Handling

### Error Types

The API client throws typed `ApiError` instances:

```typescript
class ApiError extends Error {
  status: number;        // HTTP status code
  code: string;          // Error code constant
  details?: Record<string, string>;  // Validation errors
}
```

### Error Codes

```typescript
enum ApiErrorCode {
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  AUTHENTICATION_ERROR = 'AUTHENTICATION_ERROR',
  AUTHORIZATION_ERROR = 'AUTHORIZATION_ERROR',
  RESOURCE_NOT_FOUND = 'RESOURCE_NOT_FOUND',
  DUPLICATE_RESOURCE = 'DUPLICATE_RESOURCE',
  RATE_LIMIT_ERROR = 'RATE_LIMIT_ERROR',
  SERVER_ERROR = 'SERVER_ERROR',
  NETWORK_ERROR = 'NETWORK_ERROR',
}
```

### Error Handling Examples

```typescript
import { ApiError } from '@/lib/api-client';
import { handleError } from '@/lib/error-handler';

try {
  await apiClient.tasks.create({ title: 'My Task' });
} catch (error) {
  if (error instanceof ApiError) {
    switch (error.code) {
      case 'AUTHENTICATION_ERROR':
        // Redirect to login
        router.push('/sign-in');
        break;

      case 'VALIDATION_ERROR':
        // Show validation errors
        if (error.details) {
          Object.entries(error.details).forEach(([field, message]) => {
            console.error(`${field}: ${message}`);
          });
        }
        break;

      case 'NETWORK_ERROR':
        // Show network error message
        alert('Please check your internet connection');
        break;

      default:
        // Generic error handling
        const result = handleError(error);
        alert(result.message);
    }
  }
}
```

### Global Error Handler

Use the `handleError` utility for consistent error messages:

```typescript
import { handleError, logError } from '@/lib/error-handler';

try {
  await apiClient.tasks.delete(taskId);
} catch (error) {
  const { message, shouldRetry, shouldRedirect } = handleError(error);

  // Log error (can be extended to send to logging service)
  logError(error, 'Delete Task');

  // Show user-friendly message
  setErrorMessage(message);

  // Handle redirect if needed
  if (shouldRedirect) {
    router.push(shouldRedirect);
  }

  // Retry if applicable
  if (shouldRetry) {
    // Show retry button
  }
}
```

---

## Testing

### Manual Testing with curl

#### Register
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123"}'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123"}'
```

#### Get Tasks (with token)
```bash
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

#### Create Task
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Task","description":"Task description"}'
```

### Testing with Frontend

The React Query DevTools are enabled in development mode for debugging API calls:

1. Open the app in development mode
2. Look for the React Query DevTools icon (bottom-left corner)
3. Inspect queries, mutations, and cache state

### Common Issues

#### 401 Unauthorized
**Cause**: Missing or invalid JWT token

**Solution**:
- Check localStorage for `auth_token`
- Verify token is being sent in Authorization header
- Try logging out and logging in again

#### CORS Errors
**Cause**: Backend not allowing requests from frontend origin

**Solution**:
- Ensure backend CORS is configured to allow `http://localhost:3000`
- Check `Access-Control-Allow-Origin` header in backend response

#### Network Errors
**Cause**: Backend not running or wrong API URL

**Solution**:
- Verify backend is running: `curl http://localhost:8000/health`
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Restart frontend dev server after changing env vars

---

## Best Practices

1. **Always use hooks for data fetching**: Use `useTasks`, `useCreateTask`, etc. instead of calling apiClient directly in components
2. **Handle loading and error states**: Always render LoadingSpinner and error messages
3. **Use optimistic updates**: Hooks automatically handle optimistic UI updates
4. **Type everything**: Use TypeScript types for all API requests and responses
5. **Centralize API logic**: Don't make fetch calls directly in components
6. **Log errors properly**: Use `logError` for consistent error logging

---

## Additional Resources

- [React Query Documentation](https://tanstack.com/query/latest)
- [Next.js API Routes](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
