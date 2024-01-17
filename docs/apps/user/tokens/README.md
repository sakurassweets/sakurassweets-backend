## Tokens reference

## Get user Tokens

**Allow:** `POST, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  POST https://api.sakurassweets.asion.tk/login/
```

| Parameter  | Type     | Description                 |
| :--------- | :------- | :-------------------------- |
| `email`    | `string` | **Required**. User email    |
| `password` | `string` | **Required**. User password |

**Response:**

```json
{
  "refresh": "refresh_token_here",
  "access": "access_token_here"
}
```

**CODES:**

- `200` (OK)
- `400` (Bad Request)
- `401` (Unathorized)
- `405` (Method now Allowed)

## Refresh user Tokens

**Allow:** `POST, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  POST https://api.sakurassweets.asion.tk/refresh/
```

| Parameter | Type     | Description                      |
| :-------- | :------- | :------------------------------- |
| `refresh` | `string` | **Required**. User refresh token |

**Response:**

```json
{
  "access": "access_token_here",
  "refresh": "refresh_token_here"
}
```

**CODES:**

- `200` (OK)
- `400` (Bad Request)
- `401` (Unathorized)
- `405` (Method now Allowed)

## Notation

#### Also you can get tokens by creating user, but it's sligthly different from this documentation.

- #### Check [How to create user](https://github.com/sakurassweets/sakurassweets-backend/docs/apps/user/create_user/README.md)

#### This documentation show ways to manually use tokens.
