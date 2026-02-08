# Todo Web App - Frontend

Modern, responsive Next.js frontend for the Todo Web Application with JWT authentication and optimistic UI updates.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [Contributing](#contributing)

---

## Features

### Core Functionality
- User authentication (sign-up, sign-in, sign-out) with JWT
- Complete task CRUD operations (create, read, update, delete)
- Task completion toggle with visual feedback
- Due date management with overdue indicators
- Empty states for zero-data scenarios

### User Experience
- Optimistic UI updates for instant feedback
- Automatic error rollback on failed operations
- Loading states for all async operations
- Comprehensive error messages
- Responsive design (mobile-first, 375px minimum)

### Technical Features
- TypeScript strict mode for complete type safety
- Tailwind CSS for utility-first styling
- React Query for intelligent data caching
- Form validation with React Hook Form and Zod
- Route protection with Next.js middleware
- Global error boundary for graceful error handling

---

## Tech Stack

- **Framework**: [Next.js 16.1.6](https://nextjs.org) (App Router with Turbopack)
- **Language**: [TypeScript 5.x](https://www.typescriptlang.org) (strict mode)
- **Styling**: [Tailwind CSS 4.x](https://tailwindcss.com)
- **State Management**: [React Query 5.x](https://tanstack.com/query/latest)
- **Forms**: [React Hook Form](https://react-hook-form.com) + [Zod](https://zod.dev)
- **Authentication**: [Better Auth](https://better-auth.com) (JWT)
- **Testing**: [Vitest](https://vitest.dev), [React Testing Library](https://testing-library.com/react), [Playwright](https://playwright.dev)

---

## Getting Started

### Prerequisites

- **Node.js**: 18.x or higher
- **npm**: 9.x or higher
- **Backend API**: Must be running (see `/backend/README.md`)

### Installation

1. Clone the repository and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment configuration:
   ```bash
   cp .env.local.example .env.local
   ```

4. Update `.env.local` with your backend API URL:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

### Running the Development Server

```bash
npm run dev
```

The application will be available at [http://localhost:3000](http://localhost:3000)

**Hot Reload**: The page automatically updates as you edit files.

### Building for Production

```bash
npm run build
```

This creates an optimized production build in the `.next` directory.

### Running in Production Mode

```bash
npm start
```

Serves the production build on [http://localhost:3000](http://localhost:3000)

---

## Project Structure

```
frontend/
├── src/
│   ├── app/                      # Next.js App Router
│   │   ├── (auth)/              # Auth route group (sign-in, sign-up)
│   │   ├── (dashboard)/         # Protected routes (dashboard)
│   │   ├── layout.tsx           # Root layout with providers
│   │   ├── page.tsx             # Landing page (redirects)
│   │   └── globals.css          # Global styles
│   ├── components/
│   │   ├── ui/                  # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── LoadingSpinner.tsx
│   │   │   ├── EmptyState.tsx
│   │   │   └── ErrorBoundary.tsx
│   │   ├── auth/                # Authentication components
│   │   │   ├── SignInForm.tsx
│   │   │   └── SignUpForm.tsx
│   │   ├── tasks/               # Task management components
│   │   │   ├── TaskCard.tsx
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskCreateModal.tsx
│   │   │   ├── TaskEditModal.tsx
│   │   │   └── TaskDeleteDialog.tsx
│   │   ├── layout/              # Layout components
│   │   │   └── NavBar.tsx
│   │   └── providers/           # Context providers
│   │       └── Providers.tsx
│   ├── hooks/                   # Custom React hooks
│   │   ├── useAuth.ts          # Authentication hook
│   │   └── useTasks.ts         # Task operations hooks
│   ├── lib/                     # Utilities and configurations
│   │   ├── api-client.ts       # Centralized API client
│   │   ├── auth-context.tsx    # Auth context provider
│   │   ├── auth.ts             # Better Auth configuration
│   │   ├── error-handler.ts    # Error handling utilities
│   │   ├── query-client.ts     # React Query configuration
│   │   └── utils.ts            # General utilities (cn, formatDate)
│   ├── types/                   # TypeScript type definitions
│   │   ├── api.ts              # API types and error codes
│   │   ├── auth.ts             # Authentication types
│   │   └── task.ts             # Task entity types
│   └── middleware.ts            # Route protection middleware
├── tests/                       # Test files
│   ├── unit/                   # Unit tests (Vitest)
│   ├── e2e/                    # E2E tests (Playwright)
│   └── setup.ts                # Test configuration
├── public/                      # Static assets
├── .env.local.example          # Environment variables template
├── tailwind.config.ts          # Tailwind CSS configuration
├── tsconfig.json               # TypeScript configuration
├── next.config.ts              # Next.js configuration
├── playwright.config.ts        # Playwright configuration
├── vitest.config.ts            # Vitest configuration
├── package.json                # Dependencies and scripts
├── README.md                   # This file
├── CLAUDE.md                   # Development guide for Claude Code
├── API.md                      # API integration guide
└── ENV.md                      # Environment variables guide
```

---

## Development Workflow

### Available Scripts

```bash
# Development
npm run dev              # Start development server with hot reload

# Building
npm run build            # Create production build
npm start                # Run production build locally

# Code Quality
npm run lint             # Run ESLint
npm run type-check       # Run TypeScript type checking

# Testing
npm run test             # Run unit tests (Vitest)
npm run test:watch       # Run tests in watch mode
npm run test:e2e         # Run E2E tests (Playwright)
npm run test:e2e:ui      # Run E2E tests with UI
```

### Code Style

- **ESLint**: Configured with Next.js recommended rules
- **Prettier**: Configured for consistent formatting
- **TypeScript**: Strict mode enabled, no `any` types

### Git Workflow

1. Create a feature branch from `main`
2. Make changes with clear, atomic commits
3. Ensure build passes: `npm run build`
4. Ensure tests pass: `npm run test`
5. Submit PR with descriptive title and body

---

## Testing

### Unit Tests (Vitest)

Test individual functions and hooks:

```bash
npm run test
```

**Example**:
```typescript
import { describe, it, expect } from 'vitest';
import { cn } from '@/lib/utils';

describe('cn utility', () => {
  it('merges classnames', () => {
    expect(cn('btn', 'btn-primary')).toBe('btn btn-primary');
  });
});
```

### Component Tests (React Testing Library)

Test component behavior:

```bash
npm run test
```

**Example**:
```typescript
import { render, screen } from '@testing-library/react';
import { Button } from '@/components/ui/Button';

test('renders button with children', () => {
  render(<Button>Click me</Button>);
  expect(screen.getByText('Click me')).toBeInTheDocument();
});
```

### E2E Tests (Playwright)

Test complete user flows:

```bash
npm run test:e2e
```

**Example**:
```typescript
import { test, expect } from '@playwright/test';

test('user can create a task', async ({ page }) => {
  await page.goto('/dashboard');
  await page.click('text=Create Task');
  await page.fill('input[name="title"]', 'Buy groceries');
  await page.click('button[type="submit"]');

  await expect(page.locator('text=Buy groceries')).toBeVisible();
});
```

### Test Coverage

Run tests with coverage:

```bash
npm run test -- --coverage
```

---

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel dashboard
3. Add environment variable:
   - `NEXT_PUBLIC_API_URL`: Your production API URL
4. Deploy

Vercel automatically:
- Builds on every push
- Provides preview deployments for PRs
- Serves via global CDN

### Docker

Build and run with Docker:

```bash
# Build image
docker build -t todo-frontend .

# Run container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=https://api.todoapp.com \
  todo-frontend
```

### Static Export

For static hosting (Netlify, S3, etc.):

```bash
npm run build
npm run export
```

Serve the `out/` directory.

**Note**: Static export doesn't support:
- Server-side rendering
- API routes
- Dynamic routes with `getServerSideProps`

---

## Documentation

- **[CLAUDE.md](./CLAUDE.md)**: Development guide for Claude Code agent
- **[API.md](./API.md)**: Complete API integration guide with examples
- **[ENV.md](./ENV.md)**: Environment variables documentation
- **[Specification](/specs/001-frontend-ui/spec.md)**: Full feature specification
- **[Plan](/specs/001-frontend-ui/plan.md)**: Architecture and design decisions

---

## Architecture Highlights

### Server-First Approach

Components are server components by default. Client components (`'use client'`) are used only when necessary:
- Form submission and validation
- Interactive UI (onClick, onChange)
- Browser APIs (localStorage, navigator)
- State management (useState, useContext)

### Centralized API Client

All API calls go through a single client (`lib/api-client.ts`) that:
- Automatically injects JWT tokens
- Validates requests/responses
- Handles errors consistently
- Provides retry logic

### Optimistic UI Updates

Task operations use optimistic updates for instant feedback:
- UI updates immediately
- API request sent in background
- Automatic rollback on error

### Type Safety

- TypeScript strict mode enabled
- No `any` types anywhere
- Complete type coverage for API contracts
- Zod for runtime validation

---

## Security

### Authentication
- JWT tokens stored in localStorage (development)
- Tokens automatically attached to all authenticated requests
- Middleware protects dashboard routes
- Automatic redirect to sign-in on 401 errors

### Input Validation
- Client-side validation with Zod schemas
- Backend validates again (defense in depth)
- XSS protection via React's JSX escaping

### Best Practices
- No sensitive data in localStorage (only auth token)
- HTTPS required in production
- SameSite cookies for CSRF protection
- No hardcoded secrets or API keys

---

## Performance

### Optimizations Implemented
- **Code Splitting**: Modals lazy-loaded with Next.js dynamic imports
- **React Query Caching**: 5-minute stale time, 10-minute cache time
- **Optimistic Updates**: Instant UI feedback, reduced perceived latency
- **Image Optimization**: Next.js Image component for automatic optimization
- **Bundle Size**: ~200KB gzipped (initial load)

### Lighthouse Scores (Target)
- Performance: 90+
- Accessibility: 100
- Best Practices: 100
- SEO: 100

---

## Accessibility

- **ARIA Labels**: All interactive elements properly labeled
- **Keyboard Navigation**: Full keyboard support (Tab, Enter, Escape)
- **Focus Management**: Visible focus indicators, auto-focus on modal open
- **Semantic HTML**: Proper heading hierarchy, landmark regions
- **Color Contrast**: 4.5:1 minimum for normal text, 3:1 for large text
- **Screen Reader Support**: Tested with NVDA and VoiceOver

---

## Browser Support

- **Chrome**: 90+
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

**Mobile**:
- iOS Safari 14+
- Android Chrome 90+

---

## Troubleshooting

### Environment variable not updating
**Solution**: Restart the dev server after changing `.env.local`

### Build fails with type errors
**Solution**: Run `npm run type-check` to see all errors

### Auth not persisting on refresh
**Solution**: Check `auth_token` in localStorage, ensure `setToken()` is called

### CORS errors
**Solution**: Verify backend allows requests from `http://localhost:3000`

### Port 3000 already in use
**Solution**: Kill the process or use a different port:
```bash
PORT=3001 npm run dev
```

---

## Contributing

1. Review [CLAUDE.md](./CLAUDE.md) for development guidelines
2. Follow the established code style and patterns
3. Add tests for new features
4. Update documentation as needed
5. Ensure build passes before submitting PR

### Code Review Checklist
- [ ] No `any` types
- [ ] No `console.log` statements
- [ ] Loading states for async operations
- [ ] Error handling for API calls
- [ ] Responsive design tested
- [ ] Accessibility attributes included
- [ ] TypeScript builds without errors
- [ ] Tests added/updated

---

## License

Private - Hackathon Project

---

## Support

For questions or issues:
1. Check [CLAUDE.md](./CLAUDE.md) for development guidance
2. Review [API.md](./API.md) for API integration help
3. Check [ENV.md](./ENV.md) for environment setup
4. Review specification files in `/specs/001-frontend-ui/`

---

**Built with Next.js, TypeScript, and Tailwind CSS**
