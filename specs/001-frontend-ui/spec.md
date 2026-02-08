# Feature Specification: Frontend UI for Phase II Todo Web Application

**Feature Branch**: `001-frontend-ui`
**Created**: 2026-02-04
**Status**: Draft
**Input**: User description: "Create complete frontend UI specifications for Phase II Todo Web Application"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Authentication Flow (Priority: P1)

A new user visits the application and needs to create an account, then sign in to access their personal task list. Returning users should be able to sign in quickly and securely.

**Why this priority**: Authentication is the foundation for multi-user support and data isolation. Without authentication, no other features can function properly.

**Independent Test**: Can be fully tested by creating an account, signing out, and signing back in. Success means the user can access a protected dashboard after authentication.

**Acceptance Scenarios**:

1. **Given** a new user visits the application, **When** they navigate to the sign-up page and provide valid credentials (email, password), **Then** their account is created and they are redirected to the dashboard
2. **Given** an existing user on the sign-in page, **When** they enter correct credentials, **Then** they are authenticated and redirected to their dashboard
3. **Given** a user on the sign-in page, **When** they enter incorrect credentials, **Then** they see a clear error message and remain on the sign-in page
4. **Given** an authenticated user, **When** they click the logout button, **Then** they are signed out and redirected to the sign-in page
5. **Given** an unauthenticated user, **When** they attempt to access the dashboard directly, **Then** they are redirected to the sign-in page

---

### User Story 2 - Task List Management (Priority: P2)

An authenticated user needs to view all their tasks in an organized, scannable list with clear visual hierarchy. They should quickly understand task status, priority, and due dates at a glance.

**Why this priority**: The task list is the primary interface for the application. Users need to see their tasks before they can create, edit, or delete them.

**Independent Test**: Can be fully tested by signing in and viewing the task list. Success means tasks are displayed in a clear, organized manner with appropriate visual feedback for different states.

**Acceptance Scenarios**:

1. **Given** an authenticated user with existing tasks, **When** they view the dashboard, **Then** they see all their tasks displayed in a list format
2. **Given** an authenticated user with no tasks, **When** they view the dashboard, **Then** they see an empty state with guidance to create their first task
3. **Given** an authenticated user viewing the task list, **When** a task is marked as completed, **Then** the visual appearance updates to reflect completed status
4. **Given** an authenticated user viewing the task list, **When** they hover over a task card, **Then** visual feedback indicates interactivity
5. **Given** an authenticated user on mobile, **When** they view the task list, **Then** tasks are displayed in a single column with appropriate spacing

---

### User Story 3 - Task Creation (Priority: P3)

An authenticated user needs to quickly create new tasks with a title, description, due date, and completion status. The creation process should be intuitive and provide immediate feedback.

**Why this priority**: Task creation is essential functionality but depends on authentication and the task list view being in place first.

**Independent Test**: Can be fully tested by clicking a "Create Task" button, filling in task details, and submitting. Success means the new task appears in the task list immediately.

**Acceptance Scenarios**:

1. **Given** an authenticated user on the dashboard, **When** they click the "Create Task" button, **Then** a task creation form appears
2. **Given** a user in the task creation form, **When** they provide a title and submit, **Then** a new task is created and appears in the task list
3. **Given** a user in the task creation form, **When** they submit without a title, **Then** they see a validation error and the form is not submitted
4. **Given** a user creating a task, **When** the API request is in progress, **Then** they see a loading indicator and the submit button is disabled
5. **Given** a user creating a task, **When** the API request fails, **Then** they see an error message and can retry

---

### User Story 4 - Task Editing (Priority: P4)

An authenticated user needs to update existing tasks to reflect changes in priority, status, description, or due dates. The editing experience should be seamless and provide clear feedback.

**Why this priority**: Task editing is important but can wait until core creation and viewing functionality is complete.

**Independent Test**: Can be fully tested by clicking on an existing task, modifying its details, and saving. Success means the updated task reflects the changes in the task list.

**Acceptance Scenarios**:

1. **Given** an authenticated user viewing a task, **When** they click the edit button, **Then** an edit form appears pre-filled with current task data
2. **Given** a user editing a task, **When** they modify fields and save, **Then** the task is updated and changes are reflected in the task list
3. **Given** a user editing a task, **When** they click cancel, **Then** the edit form closes without saving changes
4. **Given** a user editing a task, **When** the API request fails, **Then** they see an error message and can retry

---

### User Story 5 - Task Deletion (Priority: P5)

An authenticated user needs to remove tasks that are no longer relevant. The deletion process should include confirmation to prevent accidental deletions.

**Why this priority**: Deletion is a destructive action that should be implemented last, after all other CRUD operations are stable.

**Independent Test**: Can be fully tested by deleting a task and confirming it no longer appears in the task list. Success means the task is permanently removed with appropriate confirmation.

**Acceptance Scenarios**:

1. **Given** an authenticated user viewing a task, **When** they click the delete button, **Then** they see a confirmation dialog
2. **Given** a user in the delete confirmation dialog, **When** they confirm deletion, **Then** the task is removed from the task list
3. **Given** a user in the delete confirmation dialog, **When** they cancel, **Then** the dialog closes and the task remains
4. **Given** a user deleting a task, **When** the API request fails, **Then** they see an error message and the task remains visible

---

### Edge Cases

- What happens when a user's session expires while they're viewing or editing a task?
- How does the system handle slow network connections during task creation or updates?
- What happens when a user navigates away from an unsaved task creation or edit form?
- How does the system handle concurrent edits (user edits a task in two browser tabs)?
- What happens when the API returns a 500 error during any operation?
- How does the system handle extremely long task titles or descriptions?
- What happens when a user has hundreds of tasks (pagination/infinite scroll)?
- How does the system handle date validation for past due dates?

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication & Navigation

- **FR-001**: System MUST provide a sign-up page accessible to unauthenticated users
- **FR-002**: System MUST provide a sign-in page accessible to unauthenticated users
- **FR-003**: System MUST validate email format and password requirements on the client side before submission
- **FR-004**: System MUST display clear error messages for authentication failures (invalid credentials, network errors)
- **FR-005**: System MUST redirect authenticated users from auth pages to the dashboard
- **FR-006**: System MUST redirect unauthenticated users from protected pages to the sign-in page
- **FR-007**: System MUST provide a logout mechanism accessible from the dashboard
- **FR-008**: System MUST persist authentication state across page refreshes using JWT tokens
- **FR-009**: System MUST provide a navigation bar visible to authenticated users on all application pages

#### Task Display & Organization

- **FR-010**: System MUST display all tasks belonging to the authenticated user in a list format
- **FR-011**: System MUST display task title, description, due date, and completion status for each task
- **FR-012**: System MUST provide visual differentiation between completed and incomplete tasks
- **FR-013**: System MUST display an empty state with helpful guidance when the user has no tasks
- **FR-014**: System MUST display a loading state while fetching tasks from the API
- **FR-015**: System MUST display an error state when task fetching fails
- **FR-016**: System MUST support responsive layout for mobile, tablet, and desktop screen sizes

#### Task Creation

- **FR-017**: System MUST provide a task creation interface accessible from the dashboard
- **FR-018**: System MUST require a task title (minimum length: 1 character)
- **FR-019**: System MUST allow optional task description, due date, and completion status
- **FR-020**: System MUST validate required fields before allowing form submission
- **FR-021**: System MUST display a loading indicator during task creation API requests
- **FR-022**: System MUST display success feedback when a task is created successfully
- **FR-023**: System MUST display error feedback when task creation fails
- **FR-024**: System MUST add newly created tasks to the task list immediately (optimistic UI)

#### Task Editing

- **FR-025**: System MUST provide a task editing interface accessible from each task in the list
- **FR-026**: System MUST pre-populate the edit form with current task data
- **FR-027**: System MUST allow users to modify title, description, due date, and completion status
- **FR-028**: System MUST validate required fields before allowing form submission
- **FR-029**: System MUST provide a cancel action that discards unsaved changes
- **FR-030**: System MUST display a loading indicator during task update API requests
- **FR-031**: System MUST display success feedback when a task is updated successfully
- **FR-032**: System MUST display error feedback when task update fails
- **FR-033**: System MUST update the task in the task list immediately (optimistic UI)

#### Task Deletion

- **FR-034**: System MUST provide a task deletion action accessible from each task
- **FR-035**: System MUST display a confirmation dialog before deleting a task
- **FR-036**: System MUST allow users to cancel the deletion action
- **FR-037**: System MUST display a loading indicator during task deletion API requests
- **FR-038**: System MUST display success feedback when a task is deleted successfully
- **FR-039**: System MUST display error feedback when task deletion fails
- **FR-040**: System MUST remove the deleted task from the task list immediately (optimistic UI)

#### UI/UX Requirements

- **FR-041**: System MUST use a consistent color scheme across all pages (neutral, professional palette)
- **FR-042**: System MUST use a consistent typography hierarchy (headings, body, meta text)
- **FR-043**: System MUST provide visual feedback for all interactive elements (hover, focus, active states)
- **FR-044**: System MUST use consistent spacing and alignment across all components
- **FR-045**: System MUST provide accessible labels and ARIA attributes for screen readers
- **FR-046**: System MUST support keyboard navigation for all interactive elements
- **FR-047**: System MUST display form validation errors inline, next to the relevant field
- **FR-048**: System MUST use loading skeletons or spinners during data fetching operations

### Key Entities

- **User**: Represents an authenticated user with email, authentication token, and associated tasks
- **Task**: Represents a todo item with title, optional description, optional due date, completion status, and owner (user)
- **UI State**: Represents the current state of the UI including loading states, error states, modal visibility, and form data

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete the sign-up process in under 60 seconds
- **SC-002**: Users can sign in and view their task list in under 3 seconds (excluding network latency)
- **SC-003**: Users can create a new task in under 30 seconds
- **SC-004**: Users can edit an existing task in under 45 seconds
- **SC-005**: Users can delete a task in under 10 seconds (including confirmation)
- **SC-006**: 95% of users successfully complete their first task creation without errors
- **SC-007**: The UI remains responsive and usable on mobile devices (screen width 375px and above)
- **SC-008**: All interactive elements are accessible via keyboard navigation
- **SC-009**: The application displays appropriate feedback for all loading and error states
- **SC-010**: Users can distinguish between completed and incomplete tasks at a glance

### User Experience Goals

- **SC-011**: The UI feels clean, minimal, and professional
- **SC-012**: Users understand how to navigate the application without external documentation
- **SC-013**: Form validation provides clear, actionable guidance when errors occur
- **SC-014**: The application works consistently across modern browsers (Chrome, Firefox, Safari, Edge)

## UI Design Principles *(optional)*

### Layout Philosophy

- **Spacing**: Use consistent 4px/8px grid system for all spacing (margins, padding, gaps)
- **Alignment**: Left-align text content, center-align form elements and modals
- **Hierarchy**: Use size, weight, and color to establish clear visual hierarchy
- **Whitespace**: Embrace generous whitespace to reduce visual clutter and improve scannability
- **Containers**: Use max-width containers (640px for forms, 1024px for content) to prevent excessive line lengths

### Color Palette

- **Background**: Light neutral (white, gray-50) for main backgrounds
- **Foreground**: Dark neutral (gray-900, gray-800) for primary text
- **Accent**: Blue-600 for primary actions and links
- **Success**: Green-600 for success states and completed tasks
- **Error**: Red-600 for error states and validation messages
- **Warning**: Yellow-600 for warning states
- **Borders**: Gray-300 for subtle borders and dividers

### Typography Hierarchy

- **Page Titles**: 2xl (24px), semi-bold, gray-900
- **Section Headings**: xl (20px), semi-bold, gray-900
- **Body Text**: base (16px), regular, gray-800
- **Meta Text**: sm (14px), regular, gray-600
- **Labels**: sm (14px), medium, gray-700
- **Buttons**: base (16px), medium, contextual color

### Accessibility

- **Color Contrast**: Minimum 4.5:1 ratio for normal text, 3:1 for large text
- **Focus Indicators**: Visible focus ring (2px blue-500 outline) on all interactive elements
- **Keyboard Navigation**: Full keyboard support with logical tab order
- **Screen Readers**: Meaningful labels, ARIA attributes, and semantic HTML
- **Touch Targets**: Minimum 44x44px for all interactive elements on mobile

### Responsive Design

- **Mobile First**: Design for mobile (375px) first, then enhance for larger screens
- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px)
- **Mobile**: Single column layout, full-width cards, collapsible navigation
- **Tablet**: Two-column layout where appropriate, persistent navigation
- **Desktop**: Multi-column layout, hover states, expanded navigation

## Page Specifications *(optional)*

### Authentication Pages

#### Sign-Up Page

**Purpose**: Allow new users to create an account

**Layout Structure**:
- Centered vertical layout with max-width 400px
- Logo/app name at top
- Heading: "Create your account"
- Form with email and password fields
- Submit button
- Link to sign-in page ("Already have an account? Sign in")

**UI Elements**:
- Email input (type=email, required)
- Password input (type=password, required, minimum 8 characters)
- Confirm password input (type=password, required, must match password)
- "Create Account" button (full-width, primary style)
- Client-side validation indicators (checkmark for valid, X for invalid)

**Validation Behavior**:
- Email: Must be valid email format
- Password: Minimum 8 characters, show strength indicator
- Confirm Password: Must match password field
- Display inline error messages below each field
- Disable submit button until all validations pass

**Loading States**:
- Show spinner on submit button during API request
- Disable all form fields during submission

**Error States**:
- Display API errors (e.g., "Email already exists") above form
- Maintain form values so user doesn't need to re-enter
- Re-enable form for retry

---

#### Sign-In Page

**Purpose**: Allow existing users to authenticate

**Layout Structure**:
- Centered vertical layout with max-width 400px
- Logo/app name at top
- Heading: "Sign in to your account"
- Form with email and password fields
- Submit button
- Link to sign-up page ("Don't have an account? Sign up")

**UI Elements**:
- Email input (type=email, required)
- Password input (type=password, required)
- "Sign In" button (full-width, primary style)

**Validation Behavior**:
- Email: Must be valid email format
- Password: Required, no minimum length on sign-in
- Display inline error messages below each field
- Disable submit button until both fields are filled

**Loading States**:
- Show spinner on submit button during API request
- Disable all form fields during submission

**Error States**:
- Display authentication errors (e.g., "Invalid credentials") above form
- Clear password field on error for security
- Maintain email value
- Re-enable form for retry

---

### Application Pages

#### Dashboard / Task List Page

**Purpose**: Display all user tasks and provide access to task management functions

**Layout Structure**:
- Navigation bar at top (fixed)
- Page heading: "My Tasks"
- "Create Task" button (top-right of heading section)
- Task list container (scrollable, full remaining height)
- Each task rendered as a card component

**Component Composition**:
- NavBar component
- Page heading with create button
- TaskList component containing multiple TaskCard components
- Empty state component (when no tasks)
- Loading state component (while fetching)
- Error state component (when fetch fails)

**User Interactions**:
- Click "Create Task" → Open task creation modal/view
- Click task card → Open task edit modal/view
- Click task checkbox → Toggle completion status (optimistic update)
- Click delete icon → Open delete confirmation dialog

**Visual Hierarchy**:
- Navigation bar: highest priority, always visible
- Page heading and create button: secondary priority
- Task cards: tertiary priority, scannable list
- Completed tasks: reduced visual weight (gray text, strikethrough)

**Responsive Behavior**:
- Mobile: Single column, full-width task cards, hamburger menu
- Tablet: Single column, constrained task cards (max 600px wide)
- Desktop: Single column, constrained task cards (max 800px wide), persistent navigation

---

#### Task Creation View

**Purpose**: Allow users to create new tasks with all relevant details

**Layout Structure**:
- Modal overlay with centered card (max-width 500px) OR inline form at top of task list
- Heading: "Create New Task"
- Form with all task fields
- Action buttons at bottom (Cancel, Create)

**UI Elements**:
- Title input (text, required, max 200 characters)
- Description textarea (optional, max 1000 characters)
- Due date input (date picker, optional)
- Completion status checkbox (optional, defaults to unchecked)
- Character count indicators below text fields
- "Cancel" button (secondary style)
- "Create Task" button (primary style)

**Validation Behavior**:
- Title: Required, minimum 1 character
- Description: Optional, show character count
- Due date: Optional, must be valid date
- Display inline error messages
- Disable create button until title is provided

**Loading States**:
- Show spinner on create button during API request
- Disable all form fields during submission

**Error States**:
- Display API errors above form
- Maintain all form values
- Re-enable form for retry

---

#### Task Edit View

**Purpose**: Allow users to modify existing task details

**Layout Structure**:
- Modal overlay with centered card (max-width 500px) OR inline edit form replacing task card
- Heading: "Edit Task"
- Form pre-filled with current task data
- Action buttons at bottom (Cancel, Save, Delete)

**UI Elements**:
- Title input (pre-filled with current title)
- Description textarea (pre-filled with current description)
- Due date input (pre-filled with current due date)
- Completion status checkbox (pre-filled with current status)
- Character count indicators
- "Cancel" button (secondary style)
- "Save Changes" button (primary style)
- "Delete" button (danger style, separated from other actions)

**Validation Behavior**:
- Same as creation view
- Highlight changed fields (optional)

**Loading States**:
- Show spinner on save button during API request
- Disable all form fields during submission

**Error States**:
- Display API errors above form
- Maintain all form values
- Re-enable form for retry

---

#### Empty State

**Purpose**: Provide guidance when user has no tasks

**Layout Structure**:
- Centered content (both vertically and horizontally)
- Illustration or icon
- Heading: "No tasks yet"
- Descriptive text: "Create your first task to get started"
- "Create Task" button (primary style)

**Visual Design**:
- Light, friendly illustration
- Muted text colors
- Prominent create button

---

#### Error State

**Purpose**: Inform users when data cannot be loaded

**Layout Structure**:
- Centered content
- Error icon (red)
- Heading: "Unable to load tasks"
- Descriptive text: "Please check your connection and try again"
- "Retry" button (primary style)

**Visual Design**:
- Error icon (clear but not alarming)
- Helpful error message
- Obvious retry action

## Component Specifications *(optional)*

### Navigation Bar (NavBar)

**Responsibility**: Provide site-wide navigation and user actions

**Props (Conceptual)**:
- User data (name, email)
- Current page indicator

**Visual Behavior**:
- Fixed position at top of viewport
- Full-width, white background, subtle bottom border
- Logo/app name on left
- User menu/logout button on right
- Height: 64px on desktop, 56px on mobile

**Interaction Behavior**:
- Click logo → Navigate to dashboard
- Click user menu → Show dropdown with profile and logout
- Click logout → Sign out and redirect to sign-in page

---

### Task Card

**Responsibility**: Display a single task with all relevant information and actions

**Props (Conceptual)**:
- Task data (title, description, due date, completion status)
- Event handlers (onEdit, onDelete, onToggleComplete)

**Visual Behavior**:
- White background with subtle border
- Rounded corners (8px)
- Padding: 16px
- Shadow on hover
- Strikethrough and gray text when completed
- Due date displayed with color coding (red if overdue, yellow if due soon)

**Interaction Behavior**:
- Click card → Open edit view
- Click checkbox → Toggle completion status
- Click delete icon → Open delete confirmation
- Hover → Show shadow and edit/delete icons

---

### Task List

**Responsibility**: Render a collection of task cards with appropriate spacing

**Props (Conceptual)**:
- Array of tasks
- Event handlers for task actions

**Visual Behavior**:
- Vertical stack of task cards
- 12px gap between cards
- Scrollable if content exceeds viewport

**Interaction Behavior**:
- Pass events from individual cards to parent

---

### Button

**Responsibility**: Provide consistent interactive buttons across the application

**Props (Conceptual)**:
- Label text
- Style variant (primary, secondary, danger)
- Size (small, medium, large)
- Loading state
- Disabled state

**Visual Behavior**:
- Primary: Blue background, white text, hover darkens
- Secondary: White background, gray border, gray text, hover shows gray background
- Danger: Red background, white text, hover darkens
- Disabled: Gray background, gray text, no hover
- Loading: Show spinner, disable interaction

**Interaction Behavior**:
- Hover: Background color transition
- Active: Slight scale down
- Focus: Blue outline ring
- Disabled: Cursor not-allowed

---

### Input Field

**Responsibility**: Provide consistent text input with validation and feedback

**Props (Conceptual)**:
- Label text
- Placeholder text
- Input type (text, email, password, date)
- Required status
- Error message
- Value
- Change handler

**Visual Behavior**:
- Label above input (gray-700, semi-bold)
- Input: white background, gray border, rounded corners
- Focus: Blue border
- Error: Red border, red error text below
- Valid: Green checkmark icon (optional)

**Interaction Behavior**:
- Focus: Border color changes
- Blur: Trigger validation
- Type: Update value
- Invalid: Show error message

---

### Modal / Dialog

**Responsibility**: Display content in an overlay with backdrop

**Props (Conceptual)**:
- Title text
- Content (children)
- Close handler
- Visibility state

**Visual Behavior**:
- Semi-transparent dark backdrop
- White centered card with shadow
- Close icon in top-right corner
- Heading at top
- Content area
- Action buttons at bottom

**Interaction Behavior**:
- Click backdrop → Close modal (optional, configurable)
- Click close icon → Close modal
- Press Escape → Close modal
- Focus trap within modal

---

### Loading Indicator

**Responsibility**: Provide visual feedback during async operations

**Props (Conceptual)**:
- Size (small, medium, large)
- Color variant

**Visual Behavior**:
- Spinning circle or dots animation
- Blue color (default)
- Centered in container

**Interaction Behavior**:
- Continuous animation
- No user interaction

---

### Empty State Component

**Responsibility**: Provide helpful guidance when no data is available

**Props (Conceptual)**:
- Heading text
- Description text
- Action button (optional)

**Visual Behavior**:
- Centered vertically and horizontally
- Icon or illustration
- Muted text colors
- Optional call-to-action button

**Interaction Behavior**:
- Click action button → Trigger relevant action (e.g., create task)

## State & UX Behavior *(optional)*

### Loading States

- **Initial page load**: Display full-page loading spinner or skeleton screens
- **Task fetching**: Show skeleton task cards or loading indicator in task list area
- **Form submission**: Show spinner on submit button, disable form fields
- **Task actions**: Show inline loading indicator on affected task card

### Error States

- **Network errors**: Display error message with retry button
- **Validation errors**: Display inline error messages next to relevant fields
- **API errors**: Display error notification with descriptive message
- **Session expiration**: Redirect to sign-in page with message

### Empty Data States

- **No tasks**: Display empty state component with create action
- **Search no results**: Display "No tasks found" message (if search is implemented)

### Authenticated vs Unauthenticated

- **Unauthenticated**: Only show auth pages (sign-up, sign-in)
- **Authenticated**: Redirect auth pages to dashboard, show navigation bar, show task management pages

### Optimistic UI Behavior

- **Task creation**: Add task to list immediately, show loading indicator on card, rollback if API fails
- **Task update**: Update task in list immediately, show loading indicator, rollback if API fails
- **Task deletion**: Remove task from list immediately, show undo option, restore if API fails
- **Completion toggle**: Update visual state immediately, rollback if API fails

## API Interaction *(optional)*

### Where API Calls Originate

- **API Client Layer**: Centralized API client module handles all HTTP requests
- **Component Level**: Components trigger API calls via event handlers or lifecycle hooks
- **State Management**: API calls update application state, which triggers UI updates

### API Endpoints Used (Frontend Perspective)

- **POST /api/auth/register**: Create new user account
- **POST /api/auth/login**: Authenticate existing user, receive JWT token
- **POST /api/auth/logout**: Invalidate user session
- **GET /api/tasks**: Fetch all tasks for authenticated user
- **POST /api/tasks**: Create new task
- **PUT /api/tasks/:id**: Update existing task
- **DELETE /api/tasks/:id**: Delete task

### JWT Token Handling

- **Storage**: Store JWT in httpOnly cookie or localStorage (based on Better Auth configuration)
- **Attachment**: Attach JWT to all API requests via Authorization header: `Bearer <token>`
- **Refresh**: Handle token refresh automatically when approaching expiration
- **Expiration**: Redirect to sign-in page when token expires, preserve intended destination

### Error Handling

- **401 Unauthorized**: Clear auth state, redirect to sign-in page
- **403 Forbidden**: Display error message, user lacks permission
- **404 Not Found**: Display "Task not found" error
- **422 Validation Error**: Display validation errors from API response
- **500 Server Error**: Display generic error message with retry option
- **Network Error**: Display connection error with retry option

### Request/Response Flow

1. User triggers action (e.g., create task)
2. UI displays loading state
3. API client sends request with JWT token
4. API responds with success or error
5. UI updates based on response (success: update state, error: display message)
6. Loading state removed

## Assumptions *(optional)*

- **Technology Stack**: Next.js 16+ with App Router, TypeScript, Tailwind CSS are confirmed
- **Authentication**: Better Auth handles JWT generation, validation, and refresh
- **API Contracts**: Backend REST API exists with endpoints matching the `/api/*` pattern
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge) with ES6+ support
- **User Behavior**: Users primarily access from desktop, but mobile support is required
- **Data Volume**: Users typically have fewer than 100 tasks (pagination not required for MVP)
- **Network**: Reasonable network speed assumed, but UI must handle slow connections gracefully
- **Accessibility**: WCAG 2.1 Level AA compliance is the target
- **Performance**: Client-side rendering is acceptable, no SSR requirements specified

## Constraints *(optional)*

- **No Implementation Details**: This spec intentionally avoids implementation details (components, hooks, state management libraries)
- **No Server-Side Rendering**: Not specified whether SSR/SSG is required
- **No Offline Support**: Offline functionality is out of scope for Phase II
- **No Advanced Features**: No search, filtering, sorting, categories, or tags in Phase II
- **No Internationalization**: English-only for Phase II
- **No Dark Mode**: Light theme only for Phase II
- **No Animations**: Minimal animations (transitions only) to keep implementation simple

## Dependencies *(optional)*

- **Backend API**: Frontend depends on backend API being implemented per `/specs/api/` specifications
- **Authentication Service**: Frontend depends on Better Auth being configured and operational
- **Database**: Indirectly depends on Neon PostgreSQL through backend API

## Out of Scope *(optional)*

- **Task Categories/Tags**: Not included in Phase II
- **Task Search/Filter**: Not included in Phase II
- **Task Sorting**: Not included in Phase II (display in creation order)
- **Task Priority Levels**: Not included in Phase II (only completion status)
- **Recurring Tasks**: Not included in Phase II
- **Task Sharing**: Not included in Phase II (single-user tasks only)
- **Notifications**: Not included in Phase II
- **Profile Management**: Not included in Phase II (no profile editing)
- **Password Reset**: Not included in Phase II
- **Email Verification**: Not included in Phase II
- **Social Authentication**: Not included in Phase II (email/password only)
