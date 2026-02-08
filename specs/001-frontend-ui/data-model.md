# Data Model: Frontend UI State

**Feature**: Frontend UI for Phase II Todo Web Application
**Date**: 2026-02-04
**Status**: Complete

## Overview

This document defines all data models used by the frontend UI, including client-side state, types, and their relationships to backend entities.

## Client-Side State Model

### 1. Authentication State (React Context)

```typescript
interface User {
  id: string;           // From JWT sub claim
  email: string;        // User's email address
  token: string;        // JWT token (stored in httpOnly cookie)
  isAuthenticated: boolean;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  signUp: (email: string, password: string) => Promise<void>;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  clearError: () => void;
}
```

**Storage**: httpOnly cookie (preferred) or localStorage (fallback)
**Lifecycle**: Initialized on app load, persisted across page refreshes
**JWT Payload Expected**:
```json
{
  "sub": "user-id",
  "email": "user@example.com",
  "iat": 1704067200,
  "exp": 1704153600
}
```

---

### 2. Task State (Server State via React Query)

```typescript
interface Task {
  id: string;                    // Unique task ID from backend
  title: string;                 // Task title (1-200 chars)
  description: string | null;    // Optional description (max 1000 chars)
  dueDate: ISO8601Date | null;   // Optional due date (ISO format)
  isCompleted: boolean;          // Completion status
  createdAt: ISO8601DateTime;    // Creation timestamp
  updatedAt: ISO8601DateTime;    // Last update timestamp
  userId: string;                // Owner (for validation only, not displayed)
}

interface TasksQueryState {
  data: Task[];                  // Array of user's tasks
  isLoading: boolean;            // Initial fetch in progress
  isFetching: boolean;           // Background refetch in progress
  isError: boolean;              // Fetch failed
  error: Error | null;           // Error details
  refetch: () => void;           // Manual refetch trigger
}

interface TaskMutationState {
  isPending: boolean;            // Mutation in progress
  error: string | null;          // Mutation error message
  data: Task | null;             // Returned task (for create/update)
}
```

**Storage**: React Query cache (in-memory, TTL-based)
**Validation**: Zod schema validates all incoming tasks
**Ownership**: Backend enforces, frontend displays only returned tasks
**Sort Order**: Display in creation order (createdAt ascending)

---

### 3. UI State (Local Component State)

```typescript
interface UIState {
  // Modal visibility
  isCreateModalOpen: boolean;
  isEditModalOpen: boolean;
  isDeleteDialogOpen: boolean;

  // Form interaction
  selectedTaskId: string | null;
  isSubmitting: boolean;

  // Navigation
  currentPage: 'sign-in' | 'sign-up' | 'dashboard';

  // Error handling
  globalError: string | null;
  fieldErrors: Record<string, string>;
}
```

**Storage**: Local useState (lost on page refresh)
**Scope**: Component-level, no global UI state machine
**Responsibilities**: Modal visibility, form submission states, error display

---

### 4. Form State (React Hook Form)

#### Sign-Up Form
```typescript
interface SignUpFormData {
  email: string;           // Must be valid email
  password: string;        // Min 8 chars
  confirmPassword: string; // Must match password
}

// Zod Schema
const SignUpSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Password must contain uppercase letter")
    .regex(/[0-9]/, "Password must contain number"),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});
```

#### Sign-In Form
```typescript
interface SignInFormData {
  email: string;    // Must be valid email
  password: string; // Required
}

// Zod Schema
const SignInSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(1, "Password required"),
});
```

#### Task Create/Edit Form
```typescript
interface TaskFormData {
  title: string;              // Required, 1-200 chars
  description: string | null; // Optional, max 1000 chars
  dueDate: Date | null;       // Optional ISO date
  isCompleted: boolean;       // Optional, defaults to false
}

// Zod Schema
const TaskSchema = z.object({
  title: z.string()
    .min(1, "Title is required")
    .max(200, "Title must be under 200 characters"),
  description: z.string()
    .max(1000, "Description must be under 1000 characters")
    .nullable(),
  dueDate: z.coerce.date().nullable(),
  isCompleted: z.boolean().default(false),
});
```

---

### 5. API Request/Response Types

#### Authentication API
```typescript
// POST /api/auth/register
interface RegisterRequest {
  email: string;
  password: string;
}

interface AuthResponse {
  user: {
    id: string;
    email: string;
  };
  token: string;
}

// POST /api/auth/login
interface LoginRequest {
  email: string;
  password: string;
}

// POST /api/auth/logout
interface LogoutResponse {
  message: string;
}
```

#### Task API
```typescript
// GET /api/tasks
interface GetTasksResponse {
  tasks: Task[];
}

// POST /api/tasks
interface CreateTaskRequest {
  title: string;
  description?: string;
  dueDate?: string;  // ISO format
  isCompleted?: boolean;
}

interface CreateTaskResponse {
  task: Task;
}

// GET /api/tasks/:id
interface GetTaskResponse {
  task: Task;
}

// PUT /api/tasks/:id
interface UpdateTaskRequest {
  title?: string;
  description?: string;
  dueDate?: string;
  isCompleted?: boolean;
}

interface UpdateTaskResponse {
  task: Task;
}

// DELETE /api/tasks/:id
interface DeleteTaskResponse {
  message: string;
}
```

#### Error Response
```typescript
interface ErrorResponse {
  error: string;
  message: string;
  details?: Record<string, string>;  // Field errors for 422
  status: number;
}
```

---

## State Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    App Root Component                        │
│  - AuthContext Provider (manages User state)                 │
│  - QueryClientProvider (manages Task state)                  │
│  - ErrorBoundary (catches component errors)                  │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
  ┌──────────────┐      ┌──────────────┐
  │ Auth Routes  │      │ Dashboard    │
  │ (Sign-In/Up) │      │ (Task List)  │
  └──────────────┘      └──────┬───────┘
        │                      │
        │                      ├─ NavBar (uses AuthContext.user)
        │                      ├─ TaskList (uses React Query)
        │                      ├─ TaskCard (local state for hover)
        │                      ├─ TaskCreateModal (form state)
        │                      ├─ TaskEditModal (form state)
        │                      └─ TaskDeleteDialog (confirmation)
        │
    useAuth() hook
    │
    └─> AuthContext.user

    useTasks() hook
    │
    └─> React Query cache

    useForm() hook
    │
    └─> React Hook Form state
```

---

## Data Validation Rules

### Client-Side Validation

| Field | Rules | Error Message |
|-------|-------|---------------|
| Email | Valid format (RFC 5322) | "Invalid email address" |
| Password (Sign-Up) | Min 8 chars, uppercase, number | "Password must be at least 8 characters with uppercase and number" |
| Password (Sign-In) | Min 1 char | "Password required" |
| Confirm Password | Matches password | "Passwords don't match" |
| Task Title | Min 1, Max 200 chars | "Title is required" / "Title must be under 200 characters" |
| Task Description | Max 1000 chars | "Description must be under 1000 characters" |
| Task Due Date | Valid date | "Invalid date" |

### Server-Side Validation (Expected)

- Email uniqueness (409 Conflict if exists)
- Password hashing/validation
- Task title non-empty
- User ownership verification (backend enforces 403)
- Task existence before update/delete (404 Not Found)

---

## Type Definition Files

### types/api.ts
- API request/response interfaces
- Error response types
- Status code enums

### types/task.ts
- Task entity interface
- Task form data interface
- Task query state types

### types/auth.ts
- User interface
- Auth context interface
- Auth form data interfaces

---

## State Management Patterns

### Authentication Flow
```
Initial Load → Check localStorage/cookie
    ↓
Token exists? → YES → Validate with backend (optional)
    ↓ NO
Show Sign-In/Sign-Up
    ↓
User submits → API call
    ↓
Success → Store token, redirect to dashboard
    ↓
Error → Display error message, keep on auth page
```

### Task Management Flow
```
User accesses dashboard → useEffect triggers useTasks()
    ↓
React Query checks cache
    ↓
Cache hit? → Return cached tasks (instant)
    ↓ Cache miss or stale
Fetch from API with JWT
    ↓
Show loading state
    ↓
Success → Update cache, render tasks
    ↓
Error → Show error state, offer retry
```

### Optimistic Update Flow
```
User clicks "Create Task"
    ↓
useOptimistic adds task to local list (instant)
    ↓
Send API request in background
    ↓
Success → API response replaces optimistic task
    ↓
Error → Revert to previous state, show error
```

---

## Constraints & Assumptions

- All dates stored as ISO 8601 format (YYYY-MM-DDTHH:mm:ssZ)
- Task IDs are strings (UUIDs or server-generated)
- User can only see their own tasks (backend enforces via JWT)
- No pagination in MVP (<100 tasks per user)
- No sorting/filtering in MVP (display creation order)
- Timestamps are in UTC (server responsibility)
- Token expiration handled by Better Auth (auto-refresh)

---

**Data Model Status**: ✅ Complete
**TypeScript Coverage**: ✅ Full type safety
**Ready for**: Implementation phase (use these types in all components)
