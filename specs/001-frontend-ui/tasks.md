---
description: "Task list for frontend UI implementation"
---

# Tasks: Frontend UI for Phase II Todo Web Application

**Input**: Design documents from `/specs/001-frontend-ui/`
**Prerequisites**: plan.md (✅), spec.md (✅), research.md (✅), data-model.md (✅), contracts/ (✅)

**Tests**: No tests requested - focus on implementation
**Organization**: Tasks grouped by user story to enable independent implementation and testing of each story

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/src/`
- Root layouts: `frontend/src/app/`
- Components: `frontend/src/components/`
- Utilities: `frontend/src/lib/`
- Hooks: `frontend/src/hooks/`
- Types: `frontend/src/types/`
- Tests: `frontend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Initialize Next.js 16+ project with TypeScript and Tailwind CSS configuration
- [ ] T002 [P] Install and configure primary dependencies (React Hook Form, Zod, React Query, Better Auth)
- [ ] T003 [P] Configure TypeScript compiler with strict mode and path aliases in `frontend/tsconfig.json`
- [ ] T004 [P] Configure Tailwind CSS with responsive breakpoints (sm, md, lg) in `frontend/tailwind.config.ts`
- [ ] T005 [P] Setup ESLint and Prettier for code quality and formatting in `frontend/`
- [ ] T006 [P] Configure environment variables template in `frontend/.env.local.example`
- [ ] T007 Configure Next.js middleware for route protection in `frontend/src/middleware.ts`
- [ ] T008 Setup testing infrastructure (Vitest, React Testing Library, Playwright) with config files
- [ ] T009 Create base project structure (app/, components/, lib/, hooks/, types/, tests/ directories)
- [ ] T010 Setup git ignore for frontend dependencies and build artifacts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T011 [P] Create API client with JWT interceptor in `frontend/src/lib/api-client.ts`
- [ ] T012 [P] Setup error handling and response validation with Zod in `frontend/src/lib/api-client.ts`
- [ ] T013 [P] Create TypeScript types for API requests/responses in `frontend/src/types/api.ts`
- [ ] T014 [P] Create TypeScript types for Task entity in `frontend/src/types/task.ts`
- [ ] T015 [P] Create TypeScript types for Auth entities in `frontend/src/types/auth.ts`
- [ ] T016 [P] Setup Better Auth configuration in `frontend/src/lib/auth.ts`
- [ ] T017 [P] Create root layout with providers (AuthContext, QueryClientProvider) in `frontend/src/app/layout.tsx`
- [ ] T018 [P] Create Error Boundary component in `frontend/src/components/ui/ErrorBoundary.tsx`
- [ ] T019 [P] Create global error handler utility in `frontend/src/lib/error-handler.ts`
- [ ] T020 [P] Create base UI components:
  - [ ] Button component in `frontend/src/components/ui/Button.tsx`
  - [ ] Input component in `frontend/src/components/ui/Input.tsx`
  - [ ] Modal/Dialog component in `frontend/src/components/ui/Modal.tsx`
  - [ ] LoadingSpinner component in `frontend/src/components/ui/LoadingSpinner.tsx`
  - [ ] EmptyState component in `frontend/src/components/ui/EmptyState.tsx`
- [ ] T021 [P] Create utility functions (cn for class merging, formatDate, etc.) in `frontend/src/lib/utils.ts`
- [ ] T022 Setup React Query hooks in `frontend/src/lib/query-client.ts`
- [ ] T023 Create mock API handlers for development in `frontend/src/mocks/handlers.ts`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication Flow (Priority: P1) 🎯 MVP

**Goal**: Enable users to register, sign in, and access protected dashboard with JWT authentication

**Independent Test**: User can sign up with email/password, sign in, and be redirected to dashboard. Sign out redirects to sign-in page.

### Tests for User Story 1 (NONE REQUESTED)

### Implementation for User Story 1

- [ ] T024 [P] [US1] Create Authentication Context and Provider in `frontend/src/lib/auth-context.tsx`
- [ ] T025 [P] [US1] Create useAuth custom hook in `frontend/src/hooks/useAuth.ts`
- [ ] T026 [P] [US1] Create sign-up form component with React Hook Form validation in `frontend/src/components/auth/SignUpForm.tsx`
- [ ] T027 [P] [US1] Create sign-in form component with React Hook Form validation in `frontend/src/components/auth/SignInForm.tsx`
- [ ] T028 [US1] Create /sign-up page with SignUpForm component in `frontend/src/app/(auth)/sign-up/page.tsx`
- [ ] T029 [US1] Create /sign-in page with SignInForm component in `frontend/src/app/(auth)/sign-in/page.tsx`
- [ ] T030 [US1] Implement auth middleware to redirect authenticated users from auth pages in `frontend/src/middleware.ts`
- [ ] T031 [US1] Implement protected routes middleware to redirect unauthenticated users in `frontend/src/middleware.ts`
- [ ] T032 [P] [US1] Create NavBar component with logout functionality in `frontend/src/components/layout/NavBar.tsx`
- [ ] T033 [US1] Create dashboard layout with NavBar in `frontend/src/app/(dashboard)/layout.tsx`
- [ ] T034 [US1] Handle auth errors (401, invalid credentials, duplicate email) with user-friendly messages
- [ ] T035 [US1] Implement session expiration handling (redirect to sign-in)
- [ ] T036 [US1] Create unit tests for auth hooks in `frontend/tests/unit/hooks/useAuth.test.ts`
- [ ] T037 [US1] Create E2E test for complete sign-up/sign-in flow in `frontend/tests/e2e/auth.spec.ts`

**Checkpoint**: User Story 1 complete - authentication fully functional, all subsequent stories unblocked

---

## Phase 4: User Story 2 - Task List Management (Priority: P2)

**Goal**: Display all user tasks in an organized, responsive list with visual feedback for states

**Independent Test**: Authenticated user sees all their tasks in a list. Empty state shows when no tasks. Task completion status updates visually.

### Tests for User Story 2 (NONE REQUESTED)

### Implementation for User Story 2

- [ ] T038 [P] [US2] Create useTasks custom hook for fetching tasks in `frontend/src/hooks/useTasks.ts`
- [ ] T039 [P] [US2] Create Task entity types and Zod validation schema in `frontend/src/types/task.ts`
- [ ] T040 [P] [US2] Create TaskCard component displaying task details in `frontend/src/components/tasks/TaskCard.tsx`
- [ ] T041 [P] [US2] Create TaskList component rendering array of TaskCards in `frontend/src/components/tasks/TaskList.tsx`
- [ ] T042 [US2] Create dashboard page fetching and displaying tasks in `frontend/src/app/(dashboard)/page.tsx`
- [ ] T043 [US2] Implement empty state component when user has no tasks
- [ ] T044 [US2] Implement error state component when task fetching fails
- [ ] T045 [US2] Implement loading skeleton/spinner while tasks are being fetched
- [ ] T046 [US2] Add hover and interaction states to TaskCard component (visual feedback)
- [ ] T047 [P] [US2] Implement responsive layout for mobile (375px), tablet (768px), desktop (1024px)
- [ ] T048 [US2] Handle API errors (500, network errors) with retry button
- [ ] T049 [US2] Create unit tests for TaskCard and TaskList in `frontend/tests/unit/components/`
- [ ] T050 [US2] Create E2E test for task list display in `frontend/tests/e2e/tasks.spec.ts`

**Checkpoint**: User Story 2 complete - users can view their task list with full responsiveness

---

## Phase 5: User Story 3 - Task Creation (Priority: P3)

**Goal**: Enable users to create new tasks with title, description, due date, and instant UI feedback

**Independent Test**: User clicks "Create Task", fills form, submits. New task appears in list immediately (optimistic UI). Validation errors display inline.

### Tests for User Story 3 (NONE REQUESTED)

### Implementation for User Story 3

- [ ] T051 [P] [US3] Create TaskCreateModal component with form in `frontend/src/components/tasks/TaskCreateModal.tsx`
- [ ] T052 [P] [US3] Create task creation form with React Hook Form and Zod validation in `frontend/src/components/tasks/TaskCreateModal.tsx`
- [ ] T053 [P] [US3] Implement character counters for title (max 200) and description (max 1000) fields
- [ ] T054 [US3] Create useCreateTask hook with optimistic UI update in `frontend/src/hooks/useTasks.ts`
- [ ] T055 [US3] Implement optimistic task creation (add to list immediately, rollback on error)
- [ ] T056 [US3] Add "Create Task" button to dashboard page
- [ ] T057 [US3] Wire TaskCreateModal to dashboard with open/close state
- [ ] T058 [US3] Handle task creation errors (400, 422, 500) with rollback and error message
- [ ] T059 [US3] Display success feedback after task creation
- [ ] T060 [US3] Implement form validation error display inline below each field
- [ ] T061 [P] [US3] Add loading indicator on submit button during API request
- [ ] T062 [US3] Implement cancel button to close modal without saving
- [ ] T063 [US3] Create unit tests for task creation form in `frontend/tests/unit/components/`
- [ ] T064 [US3] Create E2E test for complete task creation flow in `frontend/tests/e2e/tasks.spec.ts`

**Checkpoint**: User Story 3 complete - users can create tasks with instant feedback

---

## Phase 6: User Story 4 - Task Editing (Priority: P4)

**Goal**: Enable users to update existing task details with seamless editing and instant feedback

**Independent Test**: User clicks edit on a task, modifies fields, saves. Changes appear in list immediately. Cancel discards changes.

### Tests for User Story 4 (NONE REQUESTED)

### Implementation for User Story 4

- [ ] T065 [P] [US4] Create TaskEditModal component in `frontend/src/components/tasks/TaskEditModal.tsx`
- [ ] T066 [P] [US4] Create task edit form with pre-populated current values in `frontend/src/components/tasks/TaskEditModal.tsx`
- [ ] T067 [P] [US4] Implement useUpdateTask hook with optimistic UI in `frontend/src/hooks/useTasks.ts`
- [ ] T068 [US4] Add edit button to TaskCard component
- [ ] T069 [US4] Wire TaskEditModal to TaskCard with state management
- [ ] T070 [US4] Implement optimistic task update (update list immediately, rollback on error)
- [ ] T071 [US4] Handle task update errors (404, 403, 422, 500) with rollback and message
- [ ] T072 [US4] Implement cancel button to close modal without saving
- [ ] T073 [US4] Display success feedback after task update
- [ ] T074 [P] [US4] Add loading indicator during update
- [ ] T075 [US4] Create unit tests for task edit form in `frontend/tests/unit/components/`
- [ ] T076 [US4] Create E2E test for complete task editing flow in `frontend/tests/e2e/tasks.spec.ts`

**Checkpoint**: User Story 4 complete - users can edit existing tasks

---

## Phase 7: User Story 5 - Task Deletion (Priority: P5)

**Goal**: Enable users to delete tasks with confirmation and instant UI feedback

**Independent Test**: User clicks delete, confirms in dialog. Task removed from list immediately. Undo option available on error.

### Tests for User Story 5 (NONE REQUESTED)

### Implementation for User Story 5

- [ ] T077 [P] [US5] Create TaskDeleteDialog component with confirmation in `frontend/src/components/tasks/TaskDeleteDialog.tsx`
- [ ] T078 [P] [US5] Implement useDeleteTask hook with optimistic UI in `frontend/src/hooks/useTasks.ts`
- [ ] T079 [US5] Add delete button to TaskCard component
- [ ] T080 [US5] Wire TaskDeleteDialog to TaskCard with state management
- [ ] T081 [US5] Implement optimistic task deletion (remove from list immediately, rollback on error)
- [ ] T082 [US5] Handle task deletion errors (404, 403, 500) with rollback and error message
- [ ] T083 [US5] Display success feedback after task deletion
- [ ] T084 [P] [US5] Add loading indicator during deletion
- [ ] T085 [US5] Implement cancel button in confirmation dialog
- [ ] T086 [US5] Create E2E test for complete task deletion flow in `frontend/tests/e2e/tasks.spec.ts`

**Checkpoint**: User Story 5 complete - users can delete tasks with confirmation

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T087 [P] Implement global error boundary wrapping entire app
- [ ] T088 [P] Add accessibility improvements (ARIA labels, semantic HTML, keyboard navigation)
- [ ] T089 [P] Implement keyboard navigation for all interactive elements (Tab, Enter, Escape)
- [ ] T090 [P] Add focus management and visible focus indicators (blue outline)
- [ ] T091 [P] Implement keyboard shortcuts (Escape to close modals)
- [ ] T092 [P] Add ARIA labels to all form inputs, buttons, and landmarks
- [ ] T093 [P] Test color contrast ratios (4.5:1 minimum for normal text)
- [ ] T094 [P] Test responsive design on actual mobile devices (375px minimum)
- [ ] T095 [P] Add loading states with proper visual feedback for all async operations
- [ ] T096 [P] Implement form validation error messages with clear guidance
- [ ] T097 [P] Add toast notifications for success/error feedback (optional: consider removing for MVP)
- [ ] T098 [P] Performance optimization: code splitting with Next.js dynamic imports
- [ ] T099 [P] Performance optimization: image optimization with Next.js Image component
- [ ] T100 [P] Performance optimization: lazy load modals and non-critical components
- [ ] T101 [P] Performance audit with Lighthouse in browser DevTools
- [ ] T102 [P] Cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] T103 [P] Security audit: verify no sensitive data in localStorage
- [ ] T104 [P] Security audit: verify HTTPS-only in production, SameSite cookies
- [ ] T105 [P] Documentation: Create comprehensive README in `frontend/README.md`
- [ ] T106 [P] Documentation: Update CLAUDE.md with frontend-specific guidance in `frontend/CLAUDE.md`
- [ ] T107 [P] Documentation: Environment variable documentation in `frontend/ENV.md`
- [ ] T108 [P] Documentation: API integration guide in `frontend/API.md`
- [ ] T109 [P] Setup CI/CD pipeline (GitHub Actions or similar)
- [ ] T110 [P] Add pre-commit hooks for linting and type checking
- [ ] T111 Run full test suite to verify all user stories work end-to-end
- [ ] T112 Validate spec compliance: all 5 user stories implemented
- [ ] T113 Validate spec compliance: all 48 functional requirements met
- [ ] T114 Validate spec compliance: all 14 success criteria verified
- [ ] T115 Final code review and refactoring

**Checkpoint**: Application meets all success criteria and quality standards

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) and US1 complete - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) and US2 complete - Depends on task list UI
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) and US2 complete - Depends on task list UI
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) and US2 complete - Depends on task list UI

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- UI components before page integration
- Hooks/state management before component implementation
- Core implementation before error handling and loading states
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes:
  - All base UI components (T020) can be built in parallel
  - Auth pages (T026, T027) can be built in parallel
  - API client (T011-T016) can be built in parallel
- Once US1 (Auth) complete:
  - US2, US3, US4, US5 can start in parallel (if team capacity allows)
- Task creation (T051-T054) can build in parallel
- Task edit (T065-T067) can build in parallel
- Task delete (T077-T078) can build in parallel

---

## Parallel Example: User Story 1 (Auth)

```bash
# Phase 2 Foundational (can run in parallel):
Task: "Create API client with JWT interceptor" (T011)
Task: "Create TypeScript types for API" (T013-T015)
Task: "Setup Better Auth configuration" (T016)
Task: "Create root layout with providers" (T017)
Task: "Create base UI components" (T020)

# Phase 3 Auth (can run in parallel after Phase 2):
Task: "Create Auth Context" (T024)
Task: "Create useAuth hook" (T025)
Task: "Create sign-up form component" (T026)
Task: "Create sign-in form component" (T027)
Task: "Create NavBar component" (T032)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Auth)
4. **STOP and VALIDATE**: Test auth flow end-to-end
5. Deploy/demo if ready

### Incremental Delivery (All Stories)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Auth)
   - Developer B: User Story 2 (Task List)
   - Developer C: User Story 3 (Create)
   - Developer D: User Story 4 (Edit)
   - Developer E: User Story 5 (Delete)
3. Stories complete and integrate independently
4. Team collaborates on Polish phase

---

## Notes

- [P] tasks = different files, no interdependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD encouraged)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

**Task Generation Status**: ✅ Complete
**Total Tasks**: 115
**Task Count by Phase**:
- Phase 1 (Setup): 10 tasks
- Phase 2 (Foundational): 13 tasks
- Phase 3 (US1 - Auth): 14 tasks
- Phase 4 (US2 - Task List): 13 tasks
- Phase 5 (US3 - Create): 14 tasks
- Phase 6 (US4 - Edit): 12 tasks
- Phase 7 (US5 - Delete): 10 tasks
- Phase 8 (Polish): 29 tasks

**Independent Test Criteria** (Each story can be tested alone):
- US1 (Auth): User signs up, signs in, signs out successfully
- US2 (Task List): User views all tasks in list, sees empty state, sees completed status
- US3 (Create): User creates task, sees in list immediately, validation works
- US4 (Edit): User edits task, changes appear in list immediately
- US5 (Delete): User deletes task with confirmation, removed from list

**Suggested MVP Scope**: Complete Phase 1 + Phase 2 + Phase 3 (just User Story 1 - Auth)
This delivers a working authentication system ready for integration with task management features.

**Ready for**: Implementation phase - Begin with Phase 1 (Setup) tasks
