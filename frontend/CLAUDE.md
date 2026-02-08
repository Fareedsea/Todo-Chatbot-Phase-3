# Frontend Development Guide for Claude Code

This document provides frontend-specific guidance for the Todo Web App Next.js application.

## Project Context

This is a production-ready Next.js 16+ frontend implementing a todo application with JWT authentication, built following spec-driven development principles.

**Tech Stack**: Next.js 16 (App Router) · TypeScript · Tailwind CSS · React Query · Better Auth

---

## Architecture Principles

### 1. Server-First Architecture

**Default to Server Components**: Use server components unless you need client-side interactivity.

```typescript
// ✅ GOOD: Server component (default)
export default function TaskListPage() {
  // Can fetch data server-side
  return <TaskList />;
}

// ❌ BAD: Unnecessary client component
'use client';
export default function TaskListPage() {
  return <TaskList />;
}
```

**Use Client Components Only When Needed**:
- Form submission and validation
- onClick, onChange, onSubmit handlers
- useState, useEffect, useContext
- Browser APIs (localStorage, navigator)
- Third-party libraries requiring client-side execution

```typescript
// ✅ GOOD: Client component for interactivity
'use client';
export function TaskCreateModal() {
  const [isOpen, setIsOpen] = useState(false);
  // Client-side state and handlers
}
```

### 2. Centralized API Client

**NEVER make fetch calls directly in components**. Always use the centralized API client:

```typescript
// ❌ BAD: Direct fetch in component
async function getTasks() {
  const response = await fetch('/api/tasks', {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.json();
}

// ✅ GOOD: Use centralized API client
import { apiClient } from '@/lib/api-client';

const tasks = await apiClient.tasks.getAll();
// JWT token automatically injected
```

**Benefits**:
- Automatic JWT token injection
- Consistent error handling
- Type safety
- Retry logic
- Request/response validation

### 3. Data Fetching with React Query

**Use custom hooks for all data operations**:

```typescript
// ✅ GOOD: Use custom hooks
import { useTasks, useCreateTask } from '@/hooks/useTasks';

function Dashboard() {
  const { data: tasks, isLoading } = useTasks();
  const { mutateAsync: createTask } = useCreateTask();

  if (isLoading) return <LoadingSpinner />;
  return <TaskList tasks={tasks} />;
}

// ❌ BAD: Direct apiClient calls in components
function Dashboard() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    apiClient.tasks.getAll().then(setTasks);
  }, []);
}
```

**Custom Hooks Provide**:
- Automatic caching and revalidation
- Loading and error states
- Optimistic UI updates with rollback
- Automatic retry on network errors

### 4. Type Safety

**No `any` types allowed**. Use explicit types everywhere:

```typescript
// ❌ BAD: Using any
function handleSubmit(data: any) {
  apiClient.tasks.create(data);
}

// ✅ GOOD: Explicit types
import { TaskCreateInput } from '@/types/task';

function handleSubmit(data: TaskCreateInput) {
  apiClient.tasks.create(data);
}
```

**Import types from `/types` directory**:
- `@/types/api` - API request/response types
- `@/types/auth` - Authentication types
- `@/types/task` - Task entity types

### 5. Responsive Design

**Mobile-first approach with Tailwind breakpoints**:

```typescript
// ✅ GOOD: Mobile-first responsive
<div className="px-4 sm:px-6 lg:px-8">
  <h1 className="text-2xl sm:text-3xl lg:text-4xl">
    My Tasks
  </h1>
</div>

// ❌ BAD: Desktop-first
<div className="lg:px-8 sm:px-6 px-4">
```

**Breakpoints**:
- `xs`: 375px (mobile)
- `sm`: 640px (large mobile)
- `md`: 768px (tablet)
- `lg`: 1024px (desktop)
- `xl`: 1280px (large desktop)

**Test at minimum width**: Always verify UI works at 375px width.

---

## Component Patterns

### UI Components (`/components/ui`)

Reusable, presentational components with no business logic:

```typescript
// Button, Input, Modal, LoadingSpinner, EmptyState, ErrorBoundary

// ✅ GOOD: Pure UI component
export function Button({ onClick, children, variant = 'primary' }) {
  return (
    <button
      onClick={onClick}
      className={cn('btn', variantStyles[variant])}
    >
      {children}
    </button>
  );
}

// ❌ BAD: UI component with API calls
export function Button({ onClick }) {
  const { mutate: createTask } = useCreateTask();
  // Don't fetch data in UI components
}
```

### Feature Components (`/components/tasks`, `/components/auth`)

Domain-specific components with business logic:

```typescript
// TaskCard, TaskList, TaskCreateModal, SignInForm, etc.

// ✅ GOOD: Feature component with hooks
'use client';
export function TaskCreateModal({ isOpen, onClose }) {
  const { mutateAsync: createTask } = useCreateTask();
  const { handleSubmit, register } = useForm();

  return <Modal isOpen={isOpen}>...</Modal>;
}
```

### Layout Components (`/components/layout`)

Page structure and navigation:

```typescript
// NavBar, Sidebar, Footer

// ✅ GOOD: Layout component
'use client';
export function NavBar() {
  const { logout } = useAuth();
  return <nav>...</nav>;
}
```

---

## State Management

### Authentication State

Use `useAuth` hook from AuthContext:

```typescript
import { useAuth } from '@/hooks/useAuth';

function Component() {
  const { user, isAuthenticated, login, logout } = useAuth();

  // Don't access localStorage directly for auth state
}
```

### Task State

Use React Query hooks from `useTasks.ts`:

```typescript
import { useTasks, useCreateTask, useUpdateTask, useDeleteTask } from '@/hooks/useTasks';

function TaskManager() {
  const { data: tasks, isLoading } = useTasks();
  const { mutateAsync: createTask } = useCreateTask();
  const { mutateAsync: updateTask } = useUpdateTask();
  const { mutateAsync: deleteTask } = useDeleteTask();

  // All mutations include optimistic updates
}
```

### Local Component State

Use `useState` for UI-only state:

```typescript
'use client';
export function TaskModal() {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedTab, setSelectedTab] = useState('details');

  // UI state only - not persisted
}
```

---

## Form Handling

**Use React Hook Form with Zod validation**:

```typescript
'use client';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  title: z.string().min(1, 'Required').max(200, 'Too long'),
  description: z.string().max(1000).optional(),
});

type FormData = z.infer<typeof schema>;

export function TaskForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    // Submit validated data
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Input
        {...register('title')}
        error={errors.title?.message}
      />
    </form>
  );
}
```

**Benefits**:
- Client-side validation before API call
- Type-safe form data
- Automatic error handling
- Accessible error messages

---

## Error Handling

### Component Level

Always handle loading and error states:

```typescript
function TaskList() {
  const { data: tasks, isLoading, error } = useTasks();

  if (isLoading) return <LoadingSpinner />;

  if (error) {
    return (
      <div className="error">
        <p>{error.message}</p>
        <button onClick={() => refetch()}>Retry</button>
      </div>
    );
  }

  return <div>{tasks.map(task => <TaskCard key={task.id} task={task} />)}</div>;
}
```

### Global Error Handling

Use `handleError` utility for consistent messaging:

```typescript
import { handleError, logError } from '@/lib/error-handler';

try {
  await createTask(data);
} catch (error) {
  const { message, shouldRetry, shouldRedirect } = handleError(error);

  logError(error, 'Create Task');
  setErrorMessage(message);

  if (shouldRedirect) {
    router.push(shouldRedirect);
  }
}
```

### ErrorBoundary

Already implemented at root layout - catches unhandled React errors.

---

## Security Guidelines

### JWT Token Management

**DO**:
- Use `setToken()` and `removeToken()` helpers
- Let API client handle token injection automatically
- Clear token on logout

**DON'T**:
- Store passwords in localStorage
- Store sensitive user data in localStorage
- Share tokens between users
- Hardcode tokens or API keys

### Input Validation

**Always validate on both client and server**:

```typescript
// Client-side validation (Zod)
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

// Server validates again (backend)
```

### XSS Prevention

React automatically escapes JSX content. Be careful with:

```typescript
// ✅ SAFE: React escapes automatically
<div>{userInput}</div>

// ⚠️ DANGEROUS: dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{ __html: userInput }} />
// Only use if absolutely necessary and sanitize input
```

---

## Performance Optimization

### Code Splitting

Use Next.js dynamic imports for heavy components:

```typescript
import dynamic from 'next/dynamic';

const TaskEditModal = dynamic(() => import('@/components/tasks/TaskEditModal'), {
  loading: () => <LoadingSpinner />,
});

// Modal only loaded when needed
```

### Image Optimization

Use Next.js Image component:

```typescript
import Image from 'next/image';

<Image
  src="/logo.png"
  alt="Logo"
  width={200}
  height={100}
  priority // for above-the-fold images
/>
```

### React Query Caching

Already configured with optimal defaults:
- Stale time: 5 minutes
- Cache time: 10 minutes
- Automatic refetch on window focus disabled

---

## Testing Guidelines

### Unit Tests (Vitest)

Test hooks and utility functions:

```typescript
import { describe, it, expect } from 'vitest';
import { formatDate } from '@/lib/utils';

describe('formatDate', () => {
  it('formats ISO date correctly', () => {
    expect(formatDate('2024-01-01')).toBe('Jan 1, 2024');
  });
});
```

### Component Tests (React Testing Library)

Test user interactions:

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { TaskCard } from '@/components/tasks/TaskCard';

test('completes task on checkbox click', async () => {
  const task = { id: '1', title: 'Test', isCompleted: false };
  const onToggle = vi.fn();

  render(<TaskCard task={task} onToggleComplete={onToggle} />);

  fireEvent.click(screen.getByRole('checkbox'));

  expect(onToggle).toHaveBeenCalledWith(task);
});
```

### E2E Tests (Playwright)

Test complete user flows:

```typescript
import { test, expect } from '@playwright/test';

test('creates a new task', async ({ page }) => {
  await page.goto('/dashboard');
  await page.click('text=Create Task');
  await page.fill('input[name="title"]', 'New Task');
  await page.click('button[type="submit"]');

  await expect(page.locator('text=New Task')).toBeVisible();
});
```

---

## Common Patterns

### Optimistic Updates

Already implemented in hooks - updates UI immediately, rolls back on error:

```typescript
const { mutateAsync: deleteTask } = useDeleteTask();

// UI updates immediately, rolls back if API fails
await deleteTask(taskId);
```

### Loading States

Show loading indicators during async operations:

```typescript
const { isPending } = useCreateTask();

<Button
  type="submit"
  isLoading={isPending}
  disabled={isPending}
>
  {isPending ? 'Creating...' : 'Create Task'}
</Button>
```

### Empty States

Show helpful empty states when no data:

```typescript
{tasks.length === 0 && (
  <EmptyState
    title="No tasks yet"
    description="Get started by creating your first task"
    action={{
      label: 'Create Task',
      onClick: () => setIsCreateModalOpen(true),
    }}
  />
)}
```

---

## File Organization

```
frontend/src/
├── app/                      # Next.js App Router
│   ├── (auth)/              # Auth route group (sign-in, sign-up)
│   ├── (dashboard)/         # Protected route group (dashboard)
│   ├── layout.tsx           # Root layout with providers
│   └── page.tsx             # Landing page
├── components/
│   ├── ui/                  # Reusable UI components
│   ├── auth/                # Authentication forms
│   ├── tasks/               # Task management components
│   ├── layout/              # Layout components
│   └── providers/           # Context providers
├── hooks/                   # Custom React hooks
│   ├── useAuth.ts          # Authentication hook
│   └── useTasks.ts         # Task operations hooks
├── lib/                     # Utilities and config
│   ├── api-client.ts       # Centralized API client
│   ├── auth-context.tsx    # Auth context provider
│   ├── error-handler.ts    # Error handling utilities
│   ├── query-client.ts     # React Query config
│   └── utils.ts            # General utilities
├── types/                   # TypeScript definitions
│   ├── api.ts              # API types
│   ├── auth.ts             # Auth types
│   └── task.ts             # Task types
└── middleware.ts            # Route protection middleware
```

---

## Troubleshooting

### "Cannot find module '@/...'"

**Solution**: Restart TypeScript server in VS Code:
- Cmd/Ctrl + Shift + P
- "TypeScript: Restart TS Server"

### Environment variable undefined

**Solution**: Restart dev server after changing `.env.local`:
```bash
npm run dev
```

### Auth not persisting on refresh

**Check**: Token in localStorage (`auth_token`)

**Solution**: Ensure `setToken()` called after successful login

### React Query not refetching

**Solution**: Manually invalidate queries:
```typescript
import { queryClient } from '@/lib/query-client';

queryClient.invalidateQueries({ queryKey: ['tasks'] });
```

### Build fails with type errors

**Solution**: Run type check locally:
```bash
npm run type-check
```

---

## Adding New Features

### Adding a New API Endpoint

1. **Add type definitions** in `src/types/`
2. **Add endpoint to API client** in `src/lib/api-client.ts`
3. **Create custom hook** in `src/hooks/` (if needed)
4. **Use in components**

### Adding a New Page

1. **Create route** in `src/app/`
2. **Use route group** if protected: `(dashboard)/new-page/page.tsx`
3. **Update middleware** if needed
4. **Add navigation link** in NavBar

### Adding a New Component

1. **Determine type**: UI, feature, or layout component
2. **Create in appropriate directory**: `components/ui`, `components/tasks`, etc.
3. **Export from index** (if needed)
4. **Add TypeScript props interface**
5. **Include accessibility attributes**

---

## Code Review Checklist

Before committing:

- [ ] No `any` types
- [ ] No console.log (use proper logging)
- [ ] No hardcoded API URLs or secrets
- [ ] Loading states for async operations
- [ ] Error handling for API calls
- [ ] Responsive design (test at 375px)
- [ ] Accessibility (ARIA labels, keyboard navigation)
- [ ] TypeScript builds without errors
- [ ] ESLint passes
- [ ] Meaningful commit message

---

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Query Documentation](https://tanstack.com/query/latest)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [React Hook Form Documentation](https://react-hook-form.com)
- [Zod Documentation](https://zod.dev)

---

## Getting Help

When stuck:

1. Check this CLAUDE.md
2. Review similar existing code
3. Check API.md for API integration
4. Check ENV.md for environment setup
5. Review spec files in `/specs/001-frontend-ui/`

**Remember**: This codebase follows spec-driven development. When unsure, refer to spec.md for requirements and plan.md for architecture decisions.
