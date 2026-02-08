# Environment Variables

Complete guide to all environment variables used in the Todo Web App frontend.

## Required Variables

### `NEXT_PUBLIC_API_URL`

**Description**: Base URL for the backend API server.

**Type**: `string` (URL)

**Required**: Yes

**Default**: `http://localhost:8000`

**Usage**: Used by the API client to make all HTTP requests to the backend.

**Examples**:
```bash
# Development
NEXT_PUBLIC_API_URL=http://localhost:8000

# Staging
NEXT_PUBLIC_API_URL=https://api-staging.todoapp.com

# Production
NEXT_PUBLIC_API_URL=https://api.todoapp.com
```

**Notes**:
- Must start with `http://` or `https://`
- No trailing slash
- Must be prefixed with `NEXT_PUBLIC_` to be accessible in the browser
- Should use HTTPS in production

---

## Optional Variables

### `NODE_ENV`

**Description**: Environment mode for Node.js and Next.js.

**Type**: `"development" | "production" | "test"`

**Required**: No (automatically set by Next.js)

**Default**: `"development"`

**Usage**: Controls build optimizations, debugging features, and error reporting.

**Examples**:
```bash
# Development (set automatically by `npm run dev`)
NODE_ENV=development

# Production (set automatically by `npm run build` and `npm start`)
NODE_ENV=production

# Testing (set by test runner)
NODE_ENV=test
```

**Notes**:
- Automatically set by Next.js commands
- Affects ErrorBoundary behavior (shows stack traces in development)
- Controls various optimizations and debugging features

---

## Setup Instructions

### Development Environment

1. Copy the example environment file:
   ```bash
   cp .env.local.example .env.local
   ```

2. Edit `.env.local` and set your values:
   ```bash
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. Restart the development server:
   ```bash
   npm run dev
   ```

### Production Environment

Set environment variables in your hosting platform:

#### Vercel
1. Go to Project Settings → Environment Variables
2. Add `NEXT_PUBLIC_API_URL` with your production API URL
3. Set for "Production" environment
4. Redeploy

#### Docker
Create a `.env.production` file or pass via docker-compose:
```yaml
services:
  frontend:
    environment:
      - NEXT_PUBLIC_API_URL=https://api.todoapp.com
```

#### Environment Variables in CI/CD
Add to GitHub Actions secrets or your CI provider:
```yaml
env:
  NEXT_PUBLIC_API_URL: ${{ secrets.API_URL }}
```

---

## Environment File Priority

Next.js loads environment variables in this order (highest priority first):

1. `.env.local` - Local overrides (gitignored)
2. `.env.production` or `.env.development` - Environment-specific
3. `.env` - Default values (committed to git)

**Never commit sensitive values**: Use `.env.local` for secrets.

---

## Validation

The application validates environment variables at startup:

- `NEXT_PUBLIC_API_URL` must be a valid URL
- If missing or invalid, the app will use the default `http://localhost:8000`

---

## Troubleshooting

### Environment variable not updating

**Solution**: Restart the dev server after changing `.env.local`:
```bash
# Stop the server (Ctrl+C)
npm run dev
```

### Environment variable undefined in browser

**Cause**: Missing `NEXT_PUBLIC_` prefix

**Solution**: Rename the variable:
```bash
# Wrong
API_URL=http://localhost:8000

# Correct
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Different values in development vs production

**Solution**: Use environment-specific files:
```bash
# .env.development
NEXT_PUBLIC_API_URL=http://localhost:8000

# .env.production
NEXT_PUBLIC_API_URL=https://api.todoapp.com
```

---

## Security Best Practices

1. **Never commit `.env.local`** - Add to `.gitignore`
2. **Use `NEXT_PUBLIC_` only for non-sensitive values** - These are exposed to the browser
3. **Server-side secrets** - Use regular env vars (without `NEXT_PUBLIC_`) for API keys, secrets
4. **Rotate credentials regularly** - Update tokens and API keys periodically
5. **Use HTTPS in production** - Always use `https://` URLs for production APIs

---

## Example Files

### `.env.local.example`
```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### `.env.development`
```bash
# Development environment
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### `.env.production`
```bash
# Production environment
NEXT_PUBLIC_API_URL=https://api.todoapp.com
```
