## User model information

## User model fields

| Field          | Field Type      | Description                      | Parameters                                                   |
| :------------- | :-------------- | :------------------------------- | ------------------------------------------------------------ |
| `email`        | `CharField`     | User email                       | `unique=True`                                                |
| `password`     | `CharField`     | User password                    | `max_length=128` in DB since it's hashed. For user it's `40` |
| `created_at`   | `DateTimeField` | When user created at             | `auto_now_add=True` (sets only when created)                 |
| `updated_at`   | `DateTimeField` | User password                    | `auto_now=True` (sets every time when updated)               |
| `is_superuser` | `BooleanField`  | Highest permissions class        | `default=False`                                              |
| `is_staff`     | `BooleanField`  | Moderator level permission class | `default=False`                                              |
| `is_active`    | `BooleanField`  | User activity status             | `default=True`                                               |

## Other information

By default ordering is `"-id"` (first one is the newest).
