## List users reference

## List users

**Allow:** `GET, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```http
  GET https://api.sakurassweets.asion.tk/users/
```

**Response:**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "user_url": "http://api.sakurassweets.asion.tk/users/2/",
      "email": "testuser2@mail.com",
      "last_login": "2024-01-13T16:12:04.199075+02:00",
      "is_staff": true,
      "is_active": true
    }
        {
      "id": 1,
      "user_url": "http://api.sakurassweets.asion.tk/users/1/",
      "email": "testuser1@mail.com",
      "last_login": "2024-01-13T16:12:04.199075+02:00",
      "is_staff": false,
      "is_active": true
    }
  ]
}
```

**CODES:**

- `200` (OK)

**Notes:**

- Administrators will have extended list of fields. Administrators additionally can see fields `created_at`, `updated_at` and `is_superuser`
