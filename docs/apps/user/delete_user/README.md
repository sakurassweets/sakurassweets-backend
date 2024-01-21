## Delete user

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrator or user itself`

```
  DELETE https://api.sakurassweets.asion.tk/users/{id}/
```

**Response:**

```
<empty response>
```

**CODES:**

- `204` (No content)
- `400` (Bad Request)
- `403` (Forbidden)
- `405` (Method now Allowed)