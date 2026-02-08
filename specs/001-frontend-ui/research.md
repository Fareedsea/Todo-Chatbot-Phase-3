# Research: Frontend UI Technology Decisions

**Feature**: Frontend UI for Phase II Todo Web Application
**Date**: 2026-02-04
**Status**: Complete

## Purpose

This document consolidates all technology research and decisions for the frontend implementation. All "NEEDS CLARIFICATION" items from the Technical Context have been resolved through research and architectural analysis.

## Research Findings

### 1. Next.js 16+ App Router Implementation

**Decision**: Use Next.js 16+ App Router with route groups for authentication and protected dashboard sections.

**Rationale**:
- App Router is the recommended and future-forward approach for Next.js 16+
- Route groups `(auth)` and `(dashboard)` provide clean separation without URL nesting
- Built-in layouts enable shared components (NavBar) for protected routes
- Server Components reduce client bundle size (though we start with Client Components for simplicity)
- Better code splitting and lazy loading capabilities

**Alternatives Considered**:
- **Pages Router**: Deprecated in Next.js 16+, lacks modern features
- **Other React frameworks** (Remix, Vite + React Router): Violates constitutional requirement for Next.js

**References**:
- Next.js 16 App Router documentation
- Community best practices for auth with App Router

---

### 2. Better Auth Integration Strategy

**Decision**: Integrate Better Auth using React hooks, store JWT in httpOnly cookies (preferred) with localStorage fallback.

**Rationale**:
- httpOnly cookies prevent XSS attacks (JavaScript cannot access)
- Better Auth handles token refresh automatically
- Constitutional requirement mandates Better Auth
- Hooks provide clean integration with React components
- SameSite cookie attribute provides CSRF protection

**Alternatives Considered**:
- **localStorage only**: Vulnerable to XSS attacks, not recommended for sensitive tokens
- **Manual JWT handling**: Error-prone, reinventing the wheel
- **Session-based auth**: Doesn't align with JWT requirement

**Implementation Notes**:
- Configure Better Auth in `lib/auth.ts`
- Use `useAuth()` hook for auth state
- Middleware intercepts protected routes
- Auto-refresh tokens before expiration

**References**:
- Better Auth documentation
- OWASP JWT security best practices

---

### 3. State Management Architecture

**Decision**: Use React Context for auth state, local component state for UI, React Query for server state caching.

**Rationale**:
- Minimal dependencies (React Context is native)
- React Query handles server state caching, refetching, and background updates
- Avoids over-engineering with Redux or other complex state libraries
- Leverages React 19's useOptimistic for optimistic UI
- Clear separation: auth (Context), UI (local), server (React Query)

**Alternatives Considered**:
- **Redux**: Overkill for this application size, adds complexity
- **Zustand**: Unnecessary dependency, Context sufficient
- **MobX**: Non-standard, learning curve
- **No state management**: Would require prop drilling and duplicated logic

**State Responsibilities**:
| State Type | Solution | Responsibility |
|------------|----------|----------------|
| Authentication | React Context | User auth state, JWT token |
| UI State | Local useState | Modal visibility, form state |
| Server State | React Query | Tasks from API, caching, refetching |
| Form State | React Hook Form | Form inputs, validation |

**References**:
- React Context API documentation
- React Query documentation

---

### 4. Form Validation Strategy

**Decision**: Use React Hook Form + Zod for schema-based validation.

**Rationale**:
- Type-safe validation with TypeScript integration
- Minimal re-renders (React Hook Form uses uncontrolled components)
- Zod provides runtime type checking and schema validation
- Excellent developer experience with autocompletion
- Industry-standard combination

**Alternatives Considered**:
- **Formik**: Heavier bundle size, more boilerplate
- **Manual validation**: Error-prone, duplicated code
- **Yup**: Less TypeScript-first than Zod

**Implementation Pattern**:
```typescript
const schema = z.object({
  email: z.string().email("Invalid email format"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(schema)
});
```

**References**:
- React Hook Form documentation
- Zod documentation

---

### 5. API Client Architecture

**Decision**: Centralized fetch wrapper with JWT interceptor, error handling, retry logic, and timeout.

**Rationale**:
- Single source of truth for all API calls
- Consistent error handling across application
- Easy to test and mock
- No additional dependencies needed (native fetch)
- Can add request/response interceptors for JWT injection

**Alternatives Considered**:
- **Axios**: Unnecessary dependency, fetch is sufficient
- **Per-component fetch**: Duplicated logic, inconsistent error handling
- **GraphQL client**: Not using GraphQL (REST API requirement)

**API Client Features**:
- Automatic JWT token attachment
- Request timeout (30s default)
- Retry on network error (3 attempts)
- Response validation with Zod
- Error normalization (401, 403, 404, 422, 500, network)

**Implementation Location**: `lib/api-client.ts`

**References**:
- Fetch API documentation
- JWT best practices

---

### 6. Optimistic UI Implementation

**Decision**: Use React 19's `useOptimistic` hook wrapped in custom `useOptimistic` helper.

**Rationale**:
- Built-in React 19 support for optimistic updates
- Automatic rollback on error
- Improves perceived performance (instant feedback)
- Aligns with spec requirement for optimistic UI

**Alternatives Considered**:
- **Manual state tracking**: Complex, error-prone
- **No optimistic updates**: Poor user experience, feels slow
- **Third-party library**: Unnecessary when React provides built-in solution

**Optimistic UI Patterns**:
| Operation | Optimistic Behavior | Rollback Condition |
|-----------|---------------------|---------------------|
| Create Task | Add to list immediately | API returns error |
| Update Task | Update in list immediately | API returns error |
| Delete Task | Remove from list immediately | API returns error |
| Toggle Complete | Update visual state immediately | API returns error |

**References**:
- React 19 useOptimistic documentation

---

### 7. Responsive Design Strategy

**Decision**: Mobile-first Tailwind CSS with breakpoints at 640px (sm), 768px (md), 1024px (lg).

**Rationale**:
- Constitutional requirement to use Tailwind CSS
- Mobile-first approach matches spec requirement (375px+ support)
- Utility-first approach reduces custom CSS
- Consistent spacing with 4px/8px grid system
- Excellent developer experience with JIT compiler

**Alternatives Considered**:
- **CSS Modules**: More boilerplate, less utility-first
- **Styled-components**: Runtime cost, not constitutional requirement
- **Vanilla CSS**: More maintenance, no utility classes

**Breakpoint Strategy**:
| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| Mobile (default) | 375px+ | Single column, full-width cards, hamburger menu |
| Small (sm) | 640px+ | Slightly wider cards |
| Medium (md) | 768px+ | Constrained cards (max 600px), persistent nav |
| Large (lg) | 1024px+ | Wider cards (max 800px), hover states |

**References**:
- Tailwind CSS documentation
- Mobile-first design principles

---

### 8. Testing Strategy

**Decision**: Vitest for unit tests, React Testing Library for component tests, Playwright for E2E tests.

**Rationale**:
- Vitest is fast, Vite-native, and modern (replaces Jest)
- React Testing Library encourages accessibility and user-centric testing
- Playwright supports modern web features and cross-browser testing
- No Cypress (Playwright is more powerful and maintained)

**Alternatives Considered**:
- **Jest**: Slower, not Vite-native
- **Enzyme**: Deprecated, not maintained
- **Cypress**: Less powerful than Playwright for modern apps
- **Manual testing**: Unreliable, not repeatable

**Testing Pyramid**:
| Level | Tool | Focus | Coverage Target |
|-------|------|-------|-----------------|
| Unit | Vitest | Pure functions, utilities | 80%+ |
| Component | React Testing Library | Component behavior, a11y | 70%+ |
| Integration | Vitest + MSW | API client, hooks | 60%+ |
| E2E | Playwright | User flows, critical paths | 100% of user stories |

**References**:
- Vitest documentation
- React Testing Library documentation
- Playwright documentation

---

### 9. Error Boundary Strategy

**Decision**: React Error Boundaries for component errors, global error handler for API errors, toast notifications for user feedback.

**Rationale**:
- Prevents white screen of death (WSOD)
- Provides user-friendly error messages
- Separates component errors from API errors
- Allows graceful degradation

**Alternatives Considered**:
- **No error boundaries**: Poor UX, app crashes on errors
- **Toast notifications only**: Doesn't handle component errors
- **Full-page error**: Disrupts user flow

**Error Handling Layers**:
1. **Component Error Boundary**: Catches React component errors, shows fallback UI
2. **API Error Handler**: Normalizes API errors, shows toast notifications
3. **Global Error Handler**: Catches uncaught errors, logs to error tracking

**References**:
- React Error Boundaries documentation
- Error handling best practices

---

### 10. Accessibility Implementation

**Decision**: Semantic HTML, ARIA labels, focus management, keyboard navigation to achieve WCAG 2.1 Level AA compliance.

**Rationale**:
- Constitutional requirement (spec mandates WCAG 2.1 AA)
- Improves UX for all users, not just those with disabilities
- Required for government/enterprise clients
- Industry best practice

**Alternatives Considered**:
- **Screen reader testing only**: Insufficient, doesn't cover keyboard nav or color contrast
- **No accessibility**: Violates constitutional requirement
- **WCAG AAA**: Too strict for MVP, AA is sufficient

**Accessibility Checklist**:
- [ ] Semantic HTML (header, nav, main, footer)
- [ ] ARIA labels on all interactive elements
- [ ] Keyboard navigation (Tab, Enter, Escape, Arrow keys)
- [ ] Focus indicators (visible 2px blue outline)
- [ ] Color contrast 4.5:1 (normal text) / 3:1 (large text)
- [ ] Screen reader tested (NVDA, JAWS, VoiceOver)
- [ ] Touch targets 44x44px minimum on mobile

**Tools**:
- eslint-plugin-jsx-a11y for linting
- axe DevTools for testing
- Lighthouse for audits

**References**:
- WCAG 2.1 Guidelines
- Web Accessibility Initiative (WAI) documentation

---

## Technology Stack Summary

| Category | Technology | Version | Justification |
|----------|-----------|---------|---------------|
| Framework | Next.js | 16+ | Constitutional requirement, App Router support |
| Language | TypeScript | 5.x | Type safety, better developer experience |
| Styling | Tailwind CSS | 4.x | Constitutional requirement, utility-first approach |
| Auth | Better Auth | Latest | Constitutional requirement, JWT handling |
| Forms | React Hook Form | 7.x | Performance, minimal re-renders |
| Validation | Zod | 3.x | Runtime type checking, TypeScript-first |
| HTTP Client | Fetch API | Native | Built-in, no dependencies |
| State (Server) | React Query | 5.x | Server state caching, automatic refetching |
| State (Client) | React Context | Native | Auth state, minimal overhead |
| State (Optimistic) | React useOptimistic | Native (React 19) | Built-in support, automatic rollback |
| Testing (Unit) | Vitest | Latest | Fast, Vite-native |
| Testing (Component) | React Testing Library | Latest | Accessibility-focused |
| Testing (E2E) | Playwright | Latest | Cross-browser, modern web |
| Linting | ESLint | Latest | Code quality, a11y rules |
| Formatting | Prettier | Latest | Consistent code style |

---

## Resolved Questions

All "NEEDS CLARIFICATION" items from Technical Context have been resolved:

1. ✅ **Language/Version**: TypeScript 5.x, Node.js 20.x LTS
2. ✅ **Primary Dependencies**: Next.js 16+, React 19+, Tailwind CSS 4.x, Better Auth, React Hook Form, Zod, React Query
3. ✅ **Testing**: Vitest (unit), React Testing Library (component), Playwright (E2E)
4. ✅ **Performance Goals**: <3s load, <100ms interaction, 60fps animations
5. ✅ **Constraints**: Client-side rendering, WCAG 2.1 AA, handles slow networks
6. ✅ **Scale/Scope**: <100 tasks per user (no pagination MVP), 7 pages, 9 components

---

## Next Steps

1. Proceed to Phase 1: Design & Contracts (data-model.md, contracts/, quickstart.md)
2. Validate technology choices with team
3. Setup development environment with selected stack
4. Begin Phase 2: Implementation

---

**Research Status**: ✅ Complete - All technology decisions finalized
**Constitutional Compliance**: ✅ All choices align with Phase II Constitution
**Ready for**: Phase 1 (Design & Contracts)
