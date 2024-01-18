## Delete Product reference

## Delete Product

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrators and Staff only`

```
  DELETE https://api.sakurassweets.asion.tk/products/{id}/
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
