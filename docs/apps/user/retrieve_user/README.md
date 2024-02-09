## Retrieve user

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  GET https://api.sakurassweets.asion.dev/users/{id}/
```

**Response:**

```json
{
  "id": 2,
  "user_url": "http://api.sakurassweets.asion.dev/users/2/",
  "email": "testuser2@mail.com",
  "last_login": "2024-01-13T16:12:04.199075+02:00",
  "is_staff": true,
  "is_active": true
}
```

**CODES:**

- `200` (OK)

**Notes:**

- Administrators will have extended list of fields. Administrators additionally can see fields `created_at`, `updated_at` and `is_superuser`
