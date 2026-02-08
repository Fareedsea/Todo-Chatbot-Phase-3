# API Contract: Authentication Endpoints

**API Version**: 1.0
**Base URL**: `/api/auth`
**Format**: JSON
**Authentication**: JWT (Bearer token) for logout endpoint

---

## POST /api/auth/register

Create a new user account.

### Request

```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Content-Type**: `application/json`

**Field Validation**:
- `email`: Valid email format (RFC 5322)
- `password`: Minimum 8 characters

### Response

**Status**: 201 Created

```json
{
  "user": {
    "id": "user-uuid-123",
    "email": "user@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Errors

**400 Bad Request** - Invalid input
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Invalid email format",
  "details": {
    "email": "must be valid email"
  }
}
```

**409 Conflict** - Email already exists
```json
{
  "error": "EMAIL_EXISTS",
  "message": "Email already registered"
}
```

**500 Internal Server Error**
```json
{
  "error": "SERVER_ERROR",
  "message": "Something went wrong"
}
```

---

## POST /api/auth/login

Authenticate existing user and receive JWT token.

### Request

```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Content-Type**: `application/json`

### Response

**Status**: 200 OK

```json
{
  "user": {
    "id": "user-uuid-123",
    "email": "user@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**JWT Claims**:
```json
{
  "sub": "user-uuid-123",
  "email": "user@example.com",
  "iat": 1704067200,
  "exp": 1704153600
}
```

### Errors

**401 Unauthorized** - Invalid credentials
```json
{
  "error": "INVALID_CREDENTIALS",
  "message": "Invalid email or password"
}
```

**400 Bad Request** - Malformed input
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Missing required fields"
}
```

**500 Internal Server Error**
```json
{
  "error": "SERVER_ERROR",
  "message": "Something went wrong"
}
```

---

## POST /api/auth/logout

Sign out user and invalidate session.

### Request

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Body**: Empty or `{}`

### Response

**Status**: 200 OK

```json
{
  "message": "Logged out successfully"
}
```

### Errors

**401 Unauthorized** - Missing or invalid token
```json
{
  "error": "UNAUTHORIZED",
  "message": "Missing or invalid authentication token"
}
```

**500 Internal Server Error**
```json
{
  "error": "SERVER_ERROR",
  "message": "Something went wrong"
}
```

---

## JWT Token Details

### Token Storage
- **Preferred**: httpOnly cookie (`X-Auth-Token`)
- **Fallback**: localStorage (`auth_token`)
- **SameSite**: Strict (CSRF protection)
- **Secure**: True (HTTPS only in production)

### Token Refresh
- Backend should return new token before expiration
- Better Auth handles automatic refresh
- Token expires after 24 hours (configurable)

### Token Usage
All protected endpoints require:
```
Authorization: Bearer <token>
```

---

## Error Handling

### Status Code Mapping

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 201 | Created | Process response |
| 400 | Bad Request | Display validation errors |
| 401 | Unauthorized | Redirect to sign-in |
| 409 | Conflict | Display "email exists" error |
| 500 | Server Error | Display generic error, retry |

### Frontend Error Display

```typescript
// Map backend errors to user-friendly messages
const errorMessages: Record<string, string> = {
  'VALIDATION_ERROR': 'Invalid input. Please check your details.',
  'EMAIL_EXISTS': 'Email is already registered. Please sign in instead.',
  'INVALID_CREDENTIALS': 'Invalid email or password.',
  'UNAUTHORIZED': 'Your session expired. Please sign in again.',
  'SERVER_ERROR': 'Something went wrong. Please try again.'
};
```

---

## Rate Limiting

**Expected**: Rate limiting on sign-up and login
- Recommended: 5 requests per minute per IP
- Frontend: Show helpful message if rate limited

---

## Security Considerations

1. **Password**: Never log passwords, only send in request
2. **Token**: Store securely (httpOnly cookie), never expose in URL
3. **CORS**: Backend must allow requests from frontend origin
4. **HTTPS**: Always use HTTPS in production
5. **Secrets**: Never commit API secrets to version control

---

**Contract Status**: ✅ Complete
**Version**: 1.0
**Last Updated**: 2026-02-04
