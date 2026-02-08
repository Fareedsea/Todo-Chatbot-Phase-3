# Quickstart: Frontend UI Development Setup

**Feature**: Frontend UI for Phase II Todo Web Application
**Date**: 2026-02-04
**Status**: Complete

## Prerequisites

- **Node.js**: 20.x LTS (or higher)
- **Package Manager**: npm 10+, pnpm 8+, or yarn 4+
- **Git**: Latest version
- **Backend API**: Running on `http://localhost:8000` (for integration testing)
- **Better Auth**: Configuration details (secret, URL)

### Verify Prerequisites

```bash
# Check Node.js version
node --version  # Should output v20.x.x or higher

# Check npm version
npm --version   # Should output 10.x.x or higher

# Check git
git --version   # Should output git version X.Y.Z
```

---

## Project Setup

### 1. Clone or Navigate to Project

```bash
# If starting fresh
git clone <repo-url>
cd todo-web-app-Phase-2

# Navigate to frontend directory
cd frontend
```

### 2. Install Dependencies

```bash
# Using npm
npm install

# Or using pnpm (faster)
pnpm install

# Or using yarn
yarn install
```

**Expected Output**:
```
added XXX packages, and audited YYY packages in Zs
```

### 3. Environment Configuration

#### Create `.env.local` File

```bash
# Copy example file
cp .env.local.example .env.local
```

#### Configure Environment Variables

Edit `.env.local`:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=30000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-key-here-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# Optional: Enable debug mode during development
DEBUG=*:frontend:*
```

**Configuration Notes**:
- `NEXT_PUBLIC_API_URL`: Backend API URL (must be accessible from browser)
- `BETTER_AUTH_SECRET`: Min 32 characters, keep secure
- `BETTER_AUTH_URL`: Frontend URL for callback redirects

### 4. Verify Setup

```bash
# Check that TypeScript compiles
npm run type-check

# Expected output: no errors
```

---

## Development Workflow

### Start Development Server

```bash
npm run dev
```

**Output**:
```
  ▲ Next.js 16.x.x
  - Local:        http://localhost:3000
  - Environments: .env.local

✓ Ready in 1234ms
```

**Access Application**: Open `http://localhost:3000` in your browser

### Common Development Tasks

#### Hot Module Reload (HMR)
- Edit any `.tsx` file and save
- Browser automatically reloads with changes
- TypeScript errors show in browser and terminal

#### TypeScript Type Checking
```bash
# Check types without building
npm run type-check

# Watch mode (continuous checking)
npm run type-check -- --watch
```

#### Code Formatting & Linting
```bash
# Check code style
npm run lint

# Auto-fix code style
npm run lint -- --fix

# Format with Prettier
npm run format

# Check formatting
npm run format:check
```

#### Run Tests

```bash
# Unit and integration tests
npm run test

# Watch mode (re-runs on file changes)
npm run test -- --watch

# Coverage report
npm run test:coverage

# E2E tests (requires app running)
npm run test:e2e

# E2E tests in debug mode
npm run test:e2e -- --debug
```

---

## API Integration

### Backend API Requirements

The frontend expects a backend API running at `NEXT_PUBLIC_API_URL` with these endpoints:

#### Authentication Endpoints
- `POST /api/auth/register` - Create new account
- `POST /api/auth/login` - Sign in
- `POST /api/auth/logout` - Sign out

#### Task Endpoints
- `GET /api/tasks` - Fetch all tasks for user
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/:id` - Update existing task
- `DELETE /api/tasks/:id` - Delete task

### Testing with Mock API

For frontend-only development without a backend:

```bash
# Start mock API server (MSW - Mock Service Worker)
npm run dev

# MSW intercepts API calls and returns mock responses
# See src/mocks/handlers.ts for mock implementations
```

### Connecting to Real Backend

1. Ensure backend is running on configured `NEXT_PUBLIC_API_URL`
2. Update `.env.local` with correct API URL if different
3. Backend must return responses matching API contracts (see contracts/ directory)
4. Backend must include `Authorization: Bearer <token>` requirement for protected routes

---

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── (auth)/            # Auth route group
│   │   │   ├── sign-in/
│   │   │   │   └── page.tsx
│   │   │   └── sign-up/
│   │   │       └── page.tsx
│   │   ├── (dashboard)/       # Protected route group
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── layout.tsx         # Root layout
│   │   └── globals.css        # Global Tailwind CSS
│   ├── components/            # Reusable components
│   │   ├── ui/                # Base UI components
│   │   ├── auth/              # Auth-specific components
│   │   ├── tasks/             # Task-specific components
│   │   └── layout/            # Layout components
│   ├── lib/                   # Utilities and helpers
│   │   ├── api-client.ts      # API client with JWT
│   │   ├── auth.ts            # Better Auth config
│   │   └── utils.ts           # Helper functions
│   ├── hooks/                 # Custom React hooks
│   │   ├── useAuth.ts         # Auth state management
│   │   ├── useTasks.ts        # Task CRUD operations
│   │   └── useOptimistic.ts   # Optimistic UI helper
│   ├── types/                 # TypeScript definitions
│   │   ├── api.ts
│   │   ├── task.ts
│   │   └── auth.ts
│   ├── middleware.ts          # Next.js middleware
│   └── mocks/                 # Mock API for development
│       └── handlers.ts        # MSW handlers
├── tests/
│   ├── unit/                  # Component tests
│   ├── integration/           # API client tests
│   └── e2e/                   # Playwright tests
├── public/                    # Static assets
├── package.json               # Dependencies
├── tsconfig.json              # TypeScript config
├── tailwind.config.ts         # Tailwind config
├── next.config.js             # Next.js config
└── README.md                  # Project documentation
```

---

## Debugging

### Debug in Browser

```bash
# Development mode enables sourcemaps
npm run dev

# Open DevTools: F12 or Cmd+Option+I
# Sources tab shows original TypeScript code
```

### Debug in VSCode

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/next",
      "args": ["dev"],
      "console": "integratedTerminal",
      "internalConsoleOptions": "neverOpen"
    }
  ]
}
```

Then press F5 to start debugging.

### Enable Verbose Logging

```bash
# Set debug environment
DEBUG=* npm run dev

# Or be more specific
DEBUG=frontend:*,api:* npm run dev
```

---

## Production Build

### Create Production Build

```bash
npm run build

# Output shows build info and optimizations
```

### Preview Production Build

```bash
npm run start

# Opens production build locally for testing
# Typically available at http://localhost:3000
```

### Deploy

```bash
# Build outputs to .next/
# Deploy .next/ directory to your hosting platform
# (Vercel, Netlify, AWS, etc.)
```

---

## Troubleshooting

### Issue: Port 3000 Already in Use

```bash
# Kill process using port 3000
# macOS/Linux:
lsof -ti :3000 | xargs kill -9

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use different port:
PORT=3001 npm run dev
```

### Issue: Module Not Found Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Issue: TypeScript Errors After Environment Changes

```bash
# Restart dev server (Ctrl+C and run again)
npm run dev

# Or manually type-check
npm run type-check
```

### Issue: API Connection Errors

1. **Verify backend is running**: Check `NEXT_PUBLIC_API_URL` in `.env.local`
2. **Check CORS**: Backend must allow requests from `http://localhost:3000`
3. **Verify JWT configuration**: Better Auth settings must match backend
4. **Check browser console**: Look for network errors in DevTools

---

## Development Best Practices

### Code Organization
- Keep components focused (single responsibility)
- Place styles in component files using Tailwind utilities
- Use custom hooks for shared logic
- Centralize API calls in `api-client.ts`

### Type Safety
- Always use TypeScript types for props and state
- Define types in `types/` directory
- Use Zod for runtime validation

### Performance
- Use React.memo for pure components
- Implement code splitting with Next.js dynamic imports
- Optimize images with Next.js Image component
- Profile with DevTools Performance tab

### Testing
- Write tests alongside components
- Use React Testing Library for component tests
- Write E2E tests for critical user flows
- Aim for >80% code coverage

### Version Control
- Create feature branches: `feature/description`
- Commit frequently with clear messages
- Use conventional commits: `feat:`, `fix:`, `refactor:`, etc.
- Submit PRs for code review

---

## Next Steps

1. **Setup complete**: Run `npm run dev` to start development
2. **Review specs**: Read `/specs/001-frontend-ui/spec.md` for requirements
3. **Understand architecture**: Read `plan.md` for implementation strategy
4. **Start building**: Follow tasks in `/specs/001-frontend-ui/tasks.md`
5. **Test frequently**: Write tests as you build components

---

## Additional Resources

- [Next.js 16 Documentation](https://nextjs.org/docs)
- [React 19 Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Better Auth Documentation](https://better-auth.com/docs)
- [React Hook Form Documentation](https://react-hook-form.com)
- [Zod Documentation](https://zod.dev)
- [Playwright Documentation](https://playwright.dev)

---

**Quickstart Status**: ✅ Complete
**Ready to**: Begin frontend development
