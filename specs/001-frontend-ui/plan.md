# Implementation Plan: Frontend UI for Phase II Todo Web Application

**Branch**: `001-frontend-ui` | **Date**: 2026-02-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-frontend-ui/spec.md`

## Summary

Implement a modern, professional frontend UI for the Phase II Todo Web Application using Next.js 16+ App Router, TypeScript, and Tailwind CSS. The implementation will provide a clean, minimal, responsive interface with five prioritized user stories: authentication flow (P1), task list management (P2), task creation (P3), task editing (P4), and task deletion (P5). The frontend will integrate with Better Auth for JWT-based authentication and communicate with a backend REST API for all data operations, including optimistic UI updates for enhanced user experience.

## Technical Context

**Language/Version**: TypeScript 5.x, Node.js 20.x LTS
**Primary Dependencies**: Next.js 16+, React 19+, Tailwind CSS 4.x, Better Auth (latest), React Hook Form, Zod (validation)
**Storage**: Browser localStorage/cookies for JWT tokens, no client-side data persistence
**Testing**: Vitest + React Testing Library for unit tests, Playwright for E2E tests
**Target Platform**: Modern web browsers (Chrome, Firefox, Safari, Edge), mobile-responsive (375px+)
**Project Type**: Web application (frontend only)
**Performance Goals**: <3s page load, <100ms UI interaction response, 60fps animations
**Constraints**: Client-side only (no SSR initially), must handle slow networks gracefully, WCAG 2.1 AA accessibility
**Scale/Scope**: Single-user sessions, <100 tasks per user (no pagination MVP), 7 pages, 9 reusable components

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase II Scope Compliance ✅
- ✅ Full-stack web application (frontend component)
- ✅ Multi-user support (authentication UI, user isolation via JWT)
- ✅ RESTful API integration (`/api/*` endpoints)
- ✅ Responsive frontend UI (mobile-first, 375px+)
- ✅ JWT-based authentication via Better Auth
- ❌ No AI features
- ❌ No chatbot functionality
- ❌ No Phase III features

### Technology Stack Compliance ✅
- ✅ Frontend: Next.js 16+ (App Router)
- ✅ TypeScript for type safety
- ✅ Tailwind CSS for styling
- ✅ Better Auth for JWT authentication
- ✅ Claude Code for implementation

### Security-First Architecture ✅
- ✅ JWT tokens attached to all API requests
- ✅ Frontend treats backend as authority (no client-side trust)
- ✅ Redirect unauthenticated users to sign-in
- ✅ Handle 401/403 responses appropriately
- ✅ No sensitive data stored client-side (tokens in httpOnly cookies preferred)

### API Contract Enforcement ✅
- ✅ All API calls use `/api/` prefix
- ✅ Expect JSON responses
- ✅ Handle proper HTTP status codes (400, 401, 403, 404, 422, 500)
- ✅ Display user-friendly error messages

### Agent Authority ✅
- ✅ Frontend Engineer Agent authority only
- ✅ Cannot modify backend or database
- ✅ Cannot modify API contracts (consume only)
- ✅ Spec-driven development followed

**GATE STATUS**: ✅ PASS - All constitutional requirements met

## Project Structure

### Documentation (this feature)

```text
specs/001-frontend-ui/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Approved feature specification
├── research.md          # Phase 0 output (technology decisions)
├── data-model.md        # Phase 1 output (client-side state model)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (API contracts from frontend perspective)
│   ├── auth-api.md
│   └── tasks-api.md
└── checklists/
    └── requirements.md  # Spec validation checklist
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── (auth)/            # Auth route group
│   │   │   ├── sign-in/
│   │   │   │   └── page.tsx
│   │   │   └── sign-up/
│   │   │       └── page.tsx
│   │   ├── (dashboard)/       # Protected route group
│   │   │   ├── layout.tsx     # Layout with NavBar
│   │   │   └── page.tsx       # Dashboard (task list)
│   │   ├── layout.tsx         # Root layout
│   │   └── globals.css        # Global styles + Tailwind
│   ├── components/            # Reusable UI components
│   │   ├── ui/                # Base UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── LoadingSpinner.tsx
│   │   │   └── EmptyState.tsx
│   │   ├── auth/              # Auth-specific components
│   │   │   ├── SignInForm.tsx
│   │   │   └── SignUpForm.tsx
│   │   ├── tasks/             # Task-specific components
│   │   │   ├── TaskCard.tsx
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskCreateModal.tsx
│   │   │   ├── TaskEditModal.tsx
│   │   │   └── TaskDeleteDialog.tsx
│   │   └── layout/            # Layout components
│   │       └── NavBar.tsx
│   ├── lib/                   # Utility functions & API client
│   │   ├── api-client.ts      # Centralized API client with JWT handling
│   │   ├── auth.ts            # Better Auth configuration
│   │   └── utils.ts           # Helper functions (cn, formatDate, etc.)
│   ├── hooks/                 # Custom React hooks
│   │   ├── useAuth.ts         # Auth state management
│   │   ├── useTasks.ts        # Task CRUD operations
│   │   └── useOptimistic.ts   # Optimistic UI helper
│   ├── types/                 # TypeScript type definitions
│   │   ├── api.ts             # API request/response types
│   │   └── task.ts            # Task entity types
│   └── middleware.ts          # Next.js middleware for auth protection
├── public/                    # Static assets
│   └── icons/
├── tests/
│   ├── unit/                  # Component unit tests
│   ├── integration/           # Integration tests
│   └── e2e/                   # End-to-end tests (Playwright)
├── .env.local.example         # Environment variable template
├── next.config.js             # Next.js configuration
├── tailwind.config.ts         # Tailwind configuration
├── tsconfig.json              # TypeScript configuration
├── package.json               # Dependencies
└── CLAUDE.md                  # Frontend-specific guidance
```

**Structure Decision**: Selected **Web application structure** (Option 2) as this is the frontend component of a full-stack web application. The structure uses Next.js 16+ App Router conventions with route groups for authentication and protected dashboard routes. Components are organized by feature (auth, tasks, layout, ui) to support independent development and testing. The `lib/` directory centralizes API interactions and utilities, while `hooks/` provides reusable state management logic. This structure enables clear separation of concerns and supports the five prioritized user stories.

## Complexity Tracking

> **No constitutional violations** - No justification required

## Phase 0: Research & Technology Decisions

### Research Tasks

1. **Next.js 16+ App Router Best Practices**
   - Decision: Use App Router with route groups for auth and dashboard
   - Rationale: App Router is the recommended approach for Next.js 16+, provides better code splitting and layouts
   - Alternatives: Pages Router (deprecated), other React frameworks (violates constitution)

2. **Better Auth Integration Strategy**
   - Decision: Use Better Auth React hooks with JWT stored in httpOnly cookies
   - Rationale: httpOnly cookies prevent XSS attacks, Better Auth handles refresh automatically
   - Alternatives: localStorage (vulnerable to XSS), manual JWT handling (error-prone)

3. **State Management Approach**
   - Decision: React Context + custom hooks for auth state, local component state for UI, React Query for server state
   - Rationale: Minimal dependencies, leverages React 19 features, avoids over-engineering
   - Alternatives: Redux (overkill), Zustand (unnecessary complexity), MobX (non-standard)

4. **Form Validation Strategy**
   - Decision: React Hook Form + Zod for schema validation
   - Rationale: Type-safe, performant, integrates well with TypeScript, minimal re-renders
   - Alternatives: Formik (heavier), manual validation (error-prone)

5. **API Client Architecture**
   - Decision: Centralized fetch wrapper with JWT interceptor, error handling, and retry logic
   - Rationale: Single source of truth for API calls, consistent error handling, easy to test
   - Alternatives: axios (unnecessary dependency), per-component fetch (duplicated logic)

6. **Optimistic UI Implementation**
   - Decision: Custom `useOptimistic` hook wrapping React 19's useOptimistic
   - Rationale: Built-in support in React 19, provides rollback on error, improves perceived performance
   - Alternatives: Manual state tracking (complex), no optimistic updates (poor UX)

7. **Responsive Design Strategy**
   - Decision: Mobile-first Tailwind breakpoints (sm:640px, md:768px, lg:1024px)
   - Rationale: Tailwind utility-first approach, mobile-first matches spec requirements
   - Alternatives: CSS modules (more boilerplate), styled-components (runtime cost)

8. **Testing Strategy**
   - Decision: Vitest + React Testing Library for unit tests, Playwright for E2E, no Cypress
   - Rationale: Vitest is fast and Vite-native, RTL encourages accessibility, Playwright handles modern web features
   - Alternatives: Jest (slower), Enzyme (deprecated), manual testing (unreliable)

9. **Error Boundary Strategy**
   - Decision: React Error Boundaries for component errors, global error handler for API errors
   - Rationale: Prevents white screen of death, provides user-friendly fallbacks
   - Alternatives: No error boundaries (poor UX), toast notifications only (incomplete)

10. **Accessibility Implementation**
    - Decision: Semantic HTML, ARIA labels, focus management, keyboard navigation
    - Rationale: WCAG 2.1 AA requirement from spec, improves UX for all users
    - Alternatives: Screen reader testing only (insufficient), no accessibility (constitutional violation)

### Technology Stack Summary

| Category | Technology | Version | Rationale |
|----------|-----------|---------|-----------|
| Framework | Next.js | 16+ | Constitutional requirement, App Router support |
| Language | TypeScript | 5.x | Type safety, better DX, spec assumption |
| Styling | Tailwind CSS | 4.x | Constitutional requirement, utility-first |
| Auth | Better Auth | Latest | Constitutional requirement, JWT handling |
| Forms | React Hook Form | Latest | Performance, type-safe validation |
| Validation | Zod | Latest | Runtime type checking, schema validation |
| HTTP Client | Fetch API | Native | Built-in, no extra dependencies needed |
| State (Server) | React Query | Latest | Server state caching, automatic refetching |
| State (Client) | React Context | Native | Auth state, minimal overhead |
| Testing (Unit) | Vitest | Latest | Fast, Vite-native, modern |
| Testing (Component) | React Testing Library | Latest | Accessibility-focused, best practices |
| Testing (E2E) | Playwright | Latest | Cross-browser, modern web support |

## Phase 1: Design & Contracts

### Data Model (Client-Side State)

See [data-model.md](./data-model.md) for complete definitions.

**Key Entities**:

1. **User** (Auth State)
   - `id`: string (from JWT)
   - `email`: string
   - `token`: string (JWT, stored in httpOnly cookie)
   - `isAuthenticated`: boolean

2. **Task** (Server Entity, mirrored client-side)
   - `id`: string
   - `title`: string (required, 1-200 chars)
   - `description`: string | null (optional, max 1000 chars)
   - `dueDate`: Date | null (optional)
   - `isCompleted`: boolean (default: false)
   - `createdAt`: Date
   - `updatedAt`: Date
   - `userId`: string (owner)

3. **UI State** (Component-Level)
   - Loading states: `isLoading`, `isSubmitting`, `isFetching`
   - Error states: `error: string | null`
   - Modal visibility: `isCreateModalOpen`, `isEditModalOpen`, `isDeleteDialogOpen`
   - Selected task: `selectedTask: Task | null`

4. **Form State** (React Hook Form)
   - Sign-up: `{ email, password, confirmPassword }`
   - Sign-in: `{ email, password }`
   - Task create/edit: `{ title, description, dueDate, isCompleted }`

### API Contracts (Frontend Perspective)

See [contracts/](./contracts/) directory for complete OpenAPI specs.

**Authentication Endpoints**:

1. **POST /api/auth/register**
   - Request: `{ email: string, password: string }`
   - Response: `{ user: User, token: string }` (201)
   - Errors: 400 (validation), 409 (email exists), 500

2. **POST /api/auth/login**
   - Request: `{ email: string, password: string }`
   - Response: `{ user: User, token: string }` (200)
   - Errors: 401 (invalid credentials), 500

3. **POST /api/auth/logout**
   - Request: None (JWT in header)
   - Response: `{ message: "Logged out successfully" }` (200)
   - Errors: 401 (invalid token), 500

**Task Endpoints**:

4. **GET /api/tasks**
   - Request: None (JWT in header)
   - Response: `{ tasks: Task[] }` (200)
   - Errors: 401, 500

5. **POST /api/tasks**
   - Request: `{ title, description?, dueDate?, isCompleted? }`
   - Response: `{ task: Task }` (201)
   - Errors: 400, 401, 422, 500

6. **GET /api/tasks/:id**
   - Request: None (JWT in header)
   - Response: `{ task: Task }` (200)
   - Errors: 401, 404, 500

7. **PUT /api/tasks/:id**
   - Request: `{ title, description?, dueDate?, isCompleted? }`
   - Response: `{ task: Task }` (200)
   - Errors: 400, 401, 404, 422, 500

8. **DELETE /api/tasks/:id**
   - Request: None (JWT in header)
   - Response: `{ message: "Task deleted" }` (200)
   - Errors: 401, 404, 500

### Quickstart Instructions

See [quickstart.md](./quickstart.md) for complete setup guide.

**Prerequisites**:
- Node.js 20.x LTS
- npm or pnpm
- Backend API running (for integration testing)

**Setup Steps**:
1. Navigate to `frontend/` directory
2. Copy `.env.local.example` to `.env.local`
3. Configure environment variables:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   BETTER_AUTH_SECRET=<secret-key>
   BETTER_AUTH_URL=http://localhost:3000
   ```
4. Install dependencies: `npm install`
5. Run development server: `npm run dev`
6. Open browser: `http://localhost:3000`

**Development Workflow**:
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run test` - Run unit tests
- `npm run test:e2e` - Run E2E tests
- `npm run lint` - Lint code
- `npm run type-check` - Type check

## Phase 2: Implementation Strategy

### Implementation Order (By User Story Priority)

**Phase 2.1: Foundation & Infrastructure** (No user story, but prerequisite)
- Task 1: Initialize Next.js project with TypeScript + Tailwind
- Task 2: Configure Better Auth client-side
- Task 3: Create API client with JWT interceptor
- Task 4: Setup middleware for route protection
- Task 5: Create base UI components (Button, Input, Modal, Loading, EmptyState)
- Task 6: Setup testing infrastructure (Vitest, RTL, Playwright)

**Phase 2.2: User Story 1 - Authentication Flow (P1)** 🎯 Critical Path
- Task 7: Create sign-up page with form validation
- Task 8: Create sign-in page with form validation
- Task 9: Implement auth context provider
- Task 10: Create useAuth hook for auth state management
- Task 11: Implement protected route middleware
- Task 12: Handle auth errors (401, invalid credentials)
- Task 13: Create NavBar with logout functionality
- Checkpoint: User can sign up, sign in, sign out, and be redirected appropriately

**Phase 2.3: User Story 2 - Task List Management (P2)**
- Task 14: Create dashboard layout with NavBar
- Task 15: Implement useTasks hook for fetching tasks
- Task 16: Create TaskCard component
- Task 17: Create TaskList component
- Task 18: Create EmptyState for no tasks
- Task 19: Create ErrorState for fetch failures
- Task 20: Implement loading skeletons for task list
- Task 21: Add hover and interaction states to task cards
- Task 22: Implement responsive layout (mobile, tablet, desktop)
- Checkpoint: Authenticated user can view their tasks in a responsive list

**Phase 2.4: User Story 3 - Task Creation (P3)**
- Task 23: Create TaskCreateModal component
- Task 24: Implement task creation form with React Hook Form + Zod
- Task 25: Add character counters for title/description
- Task 26: Implement optimistic UI for task creation
- Task 27: Handle creation errors and rollback
- Task 28: Add "Create Task" button to dashboard
- Task 29: Display success feedback on creation
- Checkpoint: User can create tasks with instant UI feedback

**Phase 2.5: User Story 4 - Task Editing (P4)**
- Task 30: Create TaskEditModal component
- Task 31: Pre-populate form with current task data
- Task 32: Implement optimistic UI for task updates
- Task 33: Handle update errors and rollback
- Task 34: Add edit button to TaskCard
- Task 35: Display success feedback on update
- Checkpoint: User can edit existing tasks with instant UI feedback

**Phase 2.6: User Story 5 - Task Deletion (P5)**
- Task 36: Create TaskDeleteDialog component (confirmation)
- Task 37: Implement optimistic UI for task deletion
- Task 38: Handle deletion errors and rollback
- Task 39: Add delete button to TaskCard and TaskEditModal
- Task 40: Display success feedback on deletion
- Checkpoint: User can delete tasks with confirmation and instant UI feedback

**Phase 2.7: Polish & Error Handling** (Cross-Cutting)
- Task 41: Implement global error boundary
- Task 42: Add session expiration handling
- Task 43: Improve form validation error messages
- Task 44: Add loading states for all async operations
- Task 45: Implement keyboard navigation for all interactive elements
- Task 46: Add ARIA labels and semantic HTML
- Task 47: Test and fix accessibility issues (WCAG 2.1 AA)
- Task 48: Add E2E tests for all user stories
- Task 49: Performance optimization (code splitting, lazy loading)
- Task 50: Cross-browser testing (Chrome, Firefox, Safari, Edge)
- Checkpoint: Application meets all success criteria and quality standards

### Critical Dependencies

1. **Better Auth Configuration** must be complete before auth UI implementation
2. **API Client** must be functional before any API-dependent features
3. **Base UI Components** must exist before page-specific components
4. **Authentication** (P1) blocks all other user stories (P2-P5)
5. **Task List** (P2) blocks Task Creation (P3), which blocks Edit (P4) and Delete (P5)

### Parallel Work Opportunities

- Base UI components can be built in parallel (Button, Input, Modal)
- Auth pages (sign-up, sign-in) can be built in parallel after auth infrastructure
- Task CRUD operations (create, edit, delete) can be built in parallel after task list
- Unit tests can be written alongside component implementation

## Frontend Integration Validation Plan

### JWT Token Verification
- ✅ All API requests include `Authorization: Bearer <token>` header
- ✅ Token is stored securely (httpOnly cookie preferred, localStorage fallback)
- ✅ Token refresh handled automatically by Better Auth
- ✅ Expired tokens trigger redirect to sign-in page

### Response Shape Validation
- ✅ All responses match API contract types (TypeScript validation)
- ✅ Unexpected response shapes trigger error states
- ✅ API responses are parsed and validated with Zod schemas

### Error Code Handling
- ✅ 401: Clear auth state, redirect to sign-in
- ✅ 403: Display "Access denied" message
- ✅ 404: Display "Task not found" error
- ✅ 422: Display validation errors inline on form
- ✅ 500: Display generic "Something went wrong" with retry button
- ✅ Network errors: Display "Connection failed" with retry button

### Empty & Edge Case Handling
- ✅ No tasks: Display empty state with "Create Task" CTA
- ✅ No network: Display offline message
- ✅ Slow network: Display loading indicators, don't block UI
- ✅ Session expiration: Detect and redirect before user action fails
- ✅ Concurrent edits: Use optimistic UI, handle conflicts gracefully

## Error & Edge Case Handling Plan

### Authentication Errors
1. **Missing Token**
   - Detection: Middleware checks for token before protected routes
   - Handling: Redirect to `/sign-in` with return URL preserved

2. **Invalid Token**
   - Detection: API returns 401
   - Handling: Clear auth state, redirect to `/sign-in`, show "Session expired"

3. **Expired Token**
   - Detection: Better Auth detects expiration before request
   - Handling: Attempt refresh, fallback to sign-in redirect

4. **Invalid Credentials (Sign-In)**
   - Detection: API returns 401 with error message
   - Handling: Display "Invalid email or password" inline, clear password field

5. **Duplicate Email (Sign-Up)**
   - Detection: API returns 409 with error message
   - Handling: Display "Email already exists" inline below email field

### Task Operation Errors
6. **Task Not Found**
   - Detection: API returns 404
   - Handling: Display "Task not found" toast, remove from client-side list

7. **Cross-User Access Attempt**
   - Detection: API returns 403
   - Handling: Display "Access denied" toast, refresh task list

8. **Validation Error**
   - Detection: API returns 422 with field errors
   - Handling: Display errors inline next to relevant form fields

9. **Network Error**
   - Detection: fetch() rejects or timeout
   - Handling: Display "Connection failed" toast with retry button

10. **Server Error (500)**
    - Detection: API returns 500
    - Handling: Display "Something went wrong" toast with retry button, log to error tracking

### UI Edge Cases
11. **Extremely Long Titles/Descriptions**
    - Prevention: Enforce character limits client-side (200/1000)
    - Display: Truncate with ellipsis, show full on hover or in edit mode

12. **Concurrent Edits (Multiple Tabs)**
    - Detection: Optimistic update succeeds locally but API returns 409
    - Handling: Show "Task was modified" message, offer to refresh or overwrite

13. **Empty Form Submission**
    - Prevention: Disable submit button until required fields valid
    - Fallback: Display validation errors if somehow submitted

14. **Navigation During Unsaved Changes**
    - Detection: React Hook Form dirty state + beforeunload event
    - Handling: Show confirmation dialog "Discard unsaved changes?"

15. **Slow Network / Hanging Requests**
    - Detection: Request timeout (30s)
    - Handling: Show loading indicator, allow user to cancel, retry on timeout

## Final Verification Checklist

### Spec Compliance
- [ ] All 5 user stories implemented per acceptance scenarios
- [ ] All 48 functional requirements met
- [ ] All 14 success criteria validated
- [ ] No out-of-scope features implemented
- [ ] 8 edge cases handled

### Security Requirements
- [ ] No authenticated access possible without valid JWT
- [ ] JWT attached to all API requests
- [ ] Sensitive data not stored in localStorage (tokens in httpOnly cookies)
- [ ] HTTPS enforced in production
- [ ] XSS prevention (React automatic escaping + CSP headers)
- [ ] CSRF protection (httpOnly cookies + SameSite attribute)

### User Isolation
- [ ] All tasks filtered by authenticated user (backend responsibility)
- [ ] Frontend displays only tasks returned by backend
- [ ] No client-side user ID manipulation possible
- [ ] Cross-user access attempts handled gracefully (403 errors)

### Performance
- [ ] Initial page load <3s
- [ ] UI interactions respond <100ms
- [ ] Animations run at 60fps
- [ ] Code splitting reduces bundle size
- [ ] Images optimized (Next.js Image component)

### Accessibility (WCAG 2.1 AA)
- [ ] All interactive elements keyboard navigable
- [ ] Focus indicators visible on all focusable elements
- [ ] ARIA labels on all form inputs
- [ ] Semantic HTML used throughout
- [ ] Color contrast ratios meet 4.5:1 (normal text) / 3:1 (large text)
- [ ] Screen reader tested
- [ ] Touch targets minimum 44x44px on mobile

### Responsive Design
- [ ] Mobile (375px): Single column, full-width cards, hamburger menu
- [ ] Tablet (768px): Constrained cards, persistent navigation
- [ ] Desktop (1024px+): Multi-column where appropriate, hover states
- [ ] All breakpoints tested

### Error Handling
- [ ] All error states display user-friendly messages
- [ ] Network errors show retry option
- [ ] Form validation errors displayed inline
- [ ] Global error boundary prevents white screen
- [ ] API errors logged for debugging

### Testing
- [ ] Unit tests for all components (>80% coverage)
- [ ] Integration tests for API client
- [ ] E2E tests for all 5 user stories
- [ ] Cross-browser tested (Chrome, Firefox, Safari, Edge)
- [ ] Accessibility tests pass (axe, Lighthouse)

### Documentation
- [ ] README with setup instructions
- [ ] CLAUDE.md with frontend-specific guidance
- [ ] Environment variable documentation
- [ ] API integration documentation
- [ ] Component Storybook (optional)

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Backend API not ready | High | Medium | Use mock API for development, define contracts upfront |
| Better Auth configuration complex | Medium | Low | Follow official docs, use community examples |
| Optimistic UI state management bugs | Medium | Medium | Extensive testing, graceful rollback on errors |
| Browser compatibility issues | Medium | Low | Use Babel for transpiling, test early on target browsers |
| Performance degradation with many tasks | Low | Low | Implement pagination if needed (out of scope for MVP) |
| Accessibility gaps | Medium | Medium | Use a11y linting, screen reader testing, ARIA guidelines |
| Token refresh edge cases | Medium | Medium | Thoroughly test token expiration scenarios |
| Responsive design inconsistencies | Low | Low | Use Tailwind breakpoints consistently, test on real devices |

## Next Steps

1. **Review & Approve Plan**: Stakeholder sign-off on implementation strategy
2. **Generate Tasks**: Run `/sp.tasks` to break down into executable tasks
3. **Setup Environment**: Initialize Next.js project, configure dependencies
4. **Begin Implementation**: Start with Phase 2.1 (Foundation), then P1 (Auth)
5. **Continuous Integration**: Setup CI/CD for automated testing
6. **Integration Testing**: Coordinate with backend team for API integration

---

**Plan Status**: ✅ Complete - Ready for task breakdown
**Constitutional Compliance**: ✅ Verified
**Next Command**: `/sp.tasks` to generate implementation tasks
