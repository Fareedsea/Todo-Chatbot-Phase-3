# API Contract: Task Endpoints

**API Version**: 1.0
**Base URL**: `/api/tasks`
**Format**: JSON
**Authentication**: JWT (Bearer token) - Required for all endpoints

---

## GET /api/tasks

Fetch all tasks for authenticated user.

### Request

**Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Query Parameters**: None

### Response

**Status**: 200 OK

```json
{
  "tasks": [
    {
      "id": "task-uuid-1",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "dueDate": "2026-02-10",
      "isCompleted": false,
      "createdAt": "2026-02-04T10:00:00Z",
      "updatedAt": "2026-02-04T10:00:00Z",
      "userId": "user-uuid-123"
    },
    {
      "id": "task-uuid-2",
      "title": "Completed task",
      "description": null,
      "dueDate": null,
      "isCompleted": true,
      "createdAt": "2026-02-01T08:30:00Z",
      "updatedAt": "2026-02-02T15:45:00Z",
      "userId": "user-uuid-123"
    }
  ]
}
```

### Empty Response

**Status**: 200 OK

```json
{
  "tasks": []
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

## POST /api/tasks

Create new task.

### Request

**Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Body**:
```json
{
  "title": "New task",
  "description": "Optional description",
  "dueDate": "2026-02-15",
  "isCompleted": false
}
```

**Field Requirements**:
- `title` (required): 1-200 characters
- `description` (optional): null or string, max 1000 chars
- `dueDate` (optional): null or ISO date string (YYYY-MM-DD)
- `isCompleted` (optional): boolean, defaults to false

### Response

**Status**: 201 Created

```json
{
  "task": {
    "id": "task-uuid-new",
    "title": "New task",
    "description": "Optional description",
    "dueDate": "2026-02-15",
    "isCompleted": false,
    "createdAt": "2026-02-04T11:30:00Z",
    "updatedAt": "2026-02-04T11:30:00Z",
    "userId": "user-uuid-123"
  }
}
```

### Errors

**400 Bad Request** - Invalid input
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Title is required"
}
```

**401 Unauthorized** - Invalid token
```json
{
  "error": "UNAUTHORIZED",
  "message": "Missing or invalid authentication token"
}
```

**422 Unprocessable Entity** - Validation failure
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Validation failed",
  "details": {
    "title": "Title must be between 1 and 200 characters",
    "description": "Description cannot exceed 1000 characters"
  }
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

## GET /api/tasks/:id

Fetch specific task by ID.

### Request

**Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**URL Parameters**:
- `:id` (string) - Task ID

### Response

**Status**: 200 OK

```json
{
  "task": {
    "id": "task-uuid-1",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "dueDate": "2026-02-10",
    "isCompleted": false,
    "createdAt": "2026-02-04T10:00:00Z",
    "updatedAt": "2026-02-04T10:00:00Z",
    "userId": "user-uuid-123"
  }
}
```

### Errors

**401 Unauthorized** - Invalid token
```json
{
  "error": "UNAUTHORIZED",
  "message": "Missing or invalid authentication token"
}
```

**403 Forbidden** - Task belongs to different user
```json
{
  "error": "FORBIDDEN",
  "message": "Access denied"
}
```

**404 Not Found** - Task doesn't exist
```json
{
  "error": "NOT_FOUND",
  "message": "Task not found"
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

## PUT /api/tasks/:id

Update existing task.

### Request

**Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**URL Parameters**:
- `:id` (string) - Task ID

**Body** (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "dueDate": "2026-02-20",
  "isCompleted": true
}
```

**Partial Updates**: Only include fields to update
```json
{
  "isCompleted": true
}
```

### Response

**Status**: 200 OK

```json
{
  "task": {
    "id": "task-uuid-1",
    "title": "Updated title",
    "description": "Updated description",
    "dueDate": "2026-02-20",
    "isCompleted": true,
    "createdAt": "2026-02-04T10:00:00Z",
    "updatedAt": "2026-02-04T12:15:00Z",
    "userId": "user-uuid-123"
  }
}
```

### Errors

**400 Bad Request** - Invalid input
```json
{
  "error": "VALIDATION_ERROR",
  "message": "At least one field required"
}
```

**401 Unauthorized** - Invalid token
```json
{
  "error": "UNAUTHORIZED",
  "message": "Missing or invalid authentication token"
}
```

**403 Forbidden** - Task belongs to different user
```json
{
  "error": "FORBIDDEN",
  "message": "Access denied"
}
```

**404 Not Found** - Task doesn't exist
```json
{
  "error": "NOT_FOUND",
  "message": "Task not found"
}
```

**422 Unprocessable Entity** - Validation failure
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Validation failed",
  "details": {
    "title": "Title must be between 1 and 200 characters"
  }
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

## DELETE /api/tasks/:id

Delete task permanently.

### Request

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**URL Parameters**:
- `:id` (string) - Task ID

### Response

**Status**: 200 OK

```json
{
  "message": "Task deleted successfully"
}
```

### Errors

**401 Unauthorized** - Invalid token
```json
{
  "error": "UNAUTHORIZED",
  "message": "Missing or invalid authentication token"
}
```

**403 Forbidden** - Task belongs to different user
```json
{
  "error": "FORBIDDEN",
  "message": "Access denied"
}
```

**404 Not Found** - Task doesn't exist
```json
{
  "error": "NOT_FOUND",
  "message": "Task not found"
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

## Task Entity Schema

```typescript
interface Task {
  id: string;                    // UUID, immutable
  title: string;                 // 1-200 characters, required
  description: string | null;    // 0-1000 characters, nullable
  dueDate: string | null;        // ISO date (YYYY-MM-DD), nullable
  isCompleted: boolean;          // true/false, defaults to false
  createdAt: ISO8601DateTime;    // Server timestamp, immutable
  updatedAt: ISO8601DateTime;    // Server timestamp, auto-updated
  userId: string;                // Owner ID, for validation only
}
```

---

## Response Timestamps

All timestamps use ISO 8601 format in UTC:
- Format: `2026-02-04T11:30:00Z`
- Timezone: UTC (Z suffix)
- Precision: Seconds

Frontend should parse as:
```typescript
const date = new Date("2026-02-04T11:30:00Z");
```

---

## Error Handling

### Status Code Mapping

| Code | Meaning | Frontend Action |
|------|---------|-----------------|
| 200 | Success | Update state with response |
| 201 | Created | Add to task list |
| 400 | Bad Request | Show validation errors |
| 401 | Unauthorized | Redirect to sign-in |
| 403 | Forbidden | Show "Access denied" |
| 404 | Not Found | Refresh list, remove task |
| 422 | Validation Error | Show field errors |
| 500 | Server Error | Show generic error, retry |

### Error Message Display

```typescript
const displayError = (error: ErrorResponse) => {
  if (error.status === 422 && error.details) {
    // Show field-level errors
    Object.entries(error.details).forEach(([field, message]) => {
      showFieldError(field, message);
    });
  } else {
    // Show generic error
    showToast(error.message || 'Something went wrong');
  }
};
```

---

## Rate Limiting

**Expected**: Rate limiting on all endpoints
- Recommended: 100 requests per minute per user
- Frontend: Implement exponential backoff on retries

---

## Security & User Isolation

1. **JWT Required**: All requests must include valid JWT
2. **User Validation**: Backend verifies task belongs to authenticated user
3. **Data Isolation**: User can only access their own tasks (403 if not owner)
4. **Timestamps**: Server-generated, immutable (frontend cannot change)

---

## Pagination (Future)

**Not in MVP**: All tasks returned in single response
**Future Enhancement**: Implement cursor-based pagination
```json
{
  "tasks": [...],
  "pagination": {
    "cursor": "next-cursor-token",
    "hasMore": true
  }
}
```

---

**Contract Status**: ✅ Complete
**Version**: 1.0
**Last Updated**: 2026-02-04
