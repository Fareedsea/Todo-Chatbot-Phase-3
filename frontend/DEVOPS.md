# DevOps Guide

Complete guide for CI/CD pipeline and development automation.

---

## Table of Contents

- [CI/CD Pipeline](#cicd-pipeline)
- [Pre-commit Hooks](#pre-commit-hooks)
- [Deployment](#deployment)
- [Monitoring](#monitoring)

---

## CI/CD Pipeline (T109)

### Overview

Automated pipeline using GitHub Actions for continuous integration and deployment.

**Location**: `.github/workflows/frontend-ci.yml`

### Pipeline Stages

```
┌─────────────────────────────────────────────────────┐
│              Lint & Type Check (Parallel)            │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼──────┐     ┌────────▼────────┐
│    Build     │     │      Test       │
└───────┬──────┘     └────────┬────────┘
        │                     │
        │            ┌────────▼────────┐
        │            │   E2E Tests     │
        │            └────────┬────────┘
        │                     │
        └─────────┬───────────┘
                  │
         ┌────────▼────────┐
         │  Security Audit  │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │ Deployment Check │
         └─────────────────┘
```

### Jobs

#### 1. Lint and Type Check

**Runs**: On every push and pull request
**Purpose**: Catch syntax and type errors early

```yaml
- Run ESLint
- Run TypeScript type check
```

**Duration**: ~30 seconds

#### 2. Build

**Runs**: After lint/typecheck passes
**Purpose**: Verify production build works

```yaml
- Install dependencies
- Build Next.js production bundle
- Upload build artifacts
```

**Duration**: ~1-2 minutes

#### 3. Test

**Runs**: In parallel with build
**Purpose**: Run unit and component tests

```yaml
- Run Vitest with coverage
- Upload coverage to Codecov
```

**Duration**: ~30-60 seconds

#### 4. E2E Tests

**Runs**: After build completes
**Purpose**: Test complete user flows

```yaml
- Install Playwright browsers
- Build application
- Run E2E tests
- Upload test reports
```

**Duration**: ~2-3 minutes

#### 5. Security Audit

**Runs**: On every push
**Purpose**: Check for dependency vulnerabilities

```yaml
- Run npm audit
- Fail on high-severity issues
```

**Duration**: ~10 seconds

#### 6. Deployment Check

**Runs**: Only on main/master branch
**Purpose**: Signal ready for deployment

```yaml
- Verify all checks passed
- Display deployment readiness
```

### Triggering the Pipeline

**Automatic Triggers**:
- Push to `main`, `master`, or `develop` branches
- Push to any branch ending with `-frontend-ui`
- Pull requests to `main`, `master`, or `develop`

**Manual Trigger**:
```bash
# Push to trigger CI
git push origin feature-branch

# Create PR to trigger full pipeline
gh pr create --title "Feature: New feature"
```

### Environment Variables

Set in GitHub repository settings:

**Required**:
- `NEXT_PUBLIC_API_URL`: Production API URL

**Optional**:
- `CODECOV_TOKEN`: For coverage reports
- `SLACK_WEBHOOK`: For notifications

### Viewing Pipeline Status

**GitHub UI**:
1. Go to repository
2. Click "Actions" tab
3. Select workflow run

**CLI**:
```bash
gh run list --workflow=frontend-ci.yml
gh run view <run-id>
```

### Pipeline Badges

Add to README.md:

```markdown
![CI Status](https://github.com/your-org/todo-app/workflows/Frontend%20CI/badge.svg)
```

---

## Pre-commit Hooks (T110)

### Overview

Automated checks before each commit to maintain code quality.

**Location**: `.husky/pre-commit`

### Setup

#### 1. Install Husky

```bash
cd frontend

# Install husky
npm install --save-dev husky

# Initialize husky
npx husky init
```

#### 2. Create Pre-commit Hook

Already created in `.husky/pre-commit`

#### 3. Make Hook Executable (Unix/Mac)

```bash
chmod +x .husky/pre-commit
```

#### 4. Test Hook

```bash
# Make a change and commit
git add .
git commit -m "Test commit"

# Hook will run automatically
```

### What Gets Checked

```
🔍 Running pre-commit checks...
├─ 📝 ESLint (code quality)
├─ 🔧 TypeScript (type safety)
└─ ✅ All checks passed!
```

**Duration**: ~10-20 seconds

### Checks Performed

1. **ESLint**:
   - Code style
   - Best practices
   - Potential bugs
   - Unused variables

2. **TypeScript**:
   - Type errors
   - Missing types
   - Type mismatches
   - `any` usage (if configured)

### Bypassing Hooks (Not Recommended)

**Only use for emergencies**:

```bash
# Skip pre-commit hooks
git commit --no-verify -m "Emergency fix"
```

**Warning**: Bypassing hooks may cause CI failures.

### Troubleshooting

#### Hook Not Running

**Solution**:
```bash
# Reinstall hooks
npx husky install

# Check hook exists
ls -la .husky/pre-commit
```

#### Hook Fails Unexpectedly

**Solution**:
```bash
# Run checks manually
npm run lint
npm run type-check

# Fix errors and retry commit
```

#### Slow Hook

**Optimization**:
```bash
# Use lint-staged for faster checks
npm install --save-dev lint-staged

# Update package.json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "tsc --noEmit"]
  }
}
```

---

## Deployment

### Vercel (Recommended)

**Automatic Deployment**:
1. Connect repository to Vercel
2. Set environment variables in Vercel dashboard
3. Push to `main` branch
4. Vercel automatically deploys

**Environment Variables** (Vercel):
```
NEXT_PUBLIC_API_URL=https://api.todoapp.com
```

**Custom Domain**:
1. Add domain in Vercel dashboard
2. Update DNS records
3. SSL automatically provisioned

### Docker

**Build Image**:
```bash
cd frontend

# Build production image
docker build -t todo-frontend:latest .

# Run container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=https://api.todoapp.com \
  todo-frontend:latest
```

**Docker Compose**:
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=https://api.todoapp.com
    restart: unless-stopped
```

### Manual Deployment

**Build and Export**:
```bash
cd frontend

# Build production version
npm run build

# Start production server
npm start

# Or export static files
npm run export
# Serve the 'out/' directory
```

---

## Monitoring

### Application Monitoring

**Recommended Tools**:
- **Vercel Analytics**: Built-in with Vercel
- **Sentry**: Error tracking
- **LogRocket**: Session replay

**Setup Sentry**:
```bash
npm install @sentry/nextjs

# Initialize
npx @sentry/wizard@latest -i nextjs
```

### Performance Monitoring

**Real User Monitoring (RUM)**:
```typescript
// pages/_app.tsx
import { useEffect } from 'react';
import { reportWebVitals } from 'next/web-vitals';

export function reportWebVitals(metric) {
  // Send to analytics
  console.log(metric);
}
```

**Lighthouse CI**:
```yaml
# .github/workflows/lighthouse.yml
- name: Run Lighthouse CI
  uses: treosh/lighthouse-ci-action@v9
  with:
    urls: |
      https://todoapp.com
      https://todoapp.com/dashboard
    uploadArtifacts: true
```

### Health Checks

**Health Endpoint**:
```typescript
// app/api/health/route.ts
export async function GET() {
  return Response.json({ status: 'ok', timestamp: Date.now() });
}
```

**Monitoring Script**:
```bash
#!/bin/bash
# check-health.sh

curl -f https://todoapp.com/api/health || exit 1
echo "✅ Frontend healthy"
```

---

## Continuous Deployment

### Deployment Workflow

```
1. Developer pushes to feature branch
   ↓
2. CI pipeline runs (lint, test, build)
   ↓
3. Developer creates PR
   ↓
4. Code review + CI checks
   ↓
5. PR merged to main
   ↓
6. Automatic deployment to staging
   ↓
7. Manual promotion to production
```

### Deployment Checklist

**Before Deployment**:
- [ ] All CI checks passed
- [ ] Code reviewed and approved
- [ ] Environment variables set
- [ ] Database migrations ready (if any)
- [ ] Rollback plan prepared

**After Deployment**:
- [ ] Smoke tests passed
- [ ] Health check returns 200
- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Verify new features work

### Rollback Procedure

**Vercel**:
```bash
# List deployments
vercel ls

# Rollback to previous
vercel rollback <deployment-url>
```

**Docker**:
```bash
# Revert to previous image
docker pull todo-frontend:previous
docker stop todo-frontend
docker rm todo-frontend
docker run -d --name todo-frontend todo-frontend:previous
```

---

## Best Practices

### 1. Commit Often

```bash
# Small, focused commits
git commit -m "feat: Add task creation modal"
git commit -m "fix: Correct validation error message"
```

### 2. Keep CI Fast

- Use caching for dependencies
- Run tests in parallel
- Skip unnecessary steps

### 3. Monitor Pipeline Health

```bash
# Check recent pipeline runs
gh run list --limit 10

# View failed runs
gh run list --status=failure
```

### 4. Automate Everything

- Linting: Pre-commit hooks
- Testing: CI pipeline
- Deployment: Automatic on merge
- Rollback: One-click revert

### 5. Document Changes

```bash
# Good commit messages
git commit -m "feat(auth): Add JWT token refresh

- Implement token refresh endpoint
- Add automatic retry on 401
- Update auth context to handle refresh
- Add tests for refresh flow

Closes #123"
```

---

## Troubleshooting

### CI Pipeline Failures

**Lint Errors**:
```bash
# Run locally
npm run lint

# Fix automatically
npm run lint -- --fix
```

**Type Errors**:
```bash
# Run type check
npm run type-check

# Check specific file
npx tsc --noEmit src/components/MyComponent.tsx
```

**Build Errors**:
```bash
# Clean and rebuild
rm -rf .next
npm run build
```

**Test Failures**:
```bash
# Run tests locally
npm run test

# Run specific test
npm run test -- TaskCard.test.tsx
```

### Deployment Issues

**Environment Variables Not Set**:
```bash
# Verify env vars
echo $NEXT_PUBLIC_API_URL

# Set for current session
export NEXT_PUBLIC_API_URL=https://api.todoapp.com
```

**Build Timeout**:
```bash
# Increase timeout (Vercel)
# In vercel.json:
{
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next",
      "config": { "maxDuration": 300 }
    }
  ]
}
```

---

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Husky Documentation](https://typicode.github.io/husky/)
- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

---

**Maintained By**: Development Team
**Last Updated**: 2026-02-04
