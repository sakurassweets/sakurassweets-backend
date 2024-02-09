## Create cart

**Allow:** `POST, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Authenticated only`

```
  POST https://api.sakurassweets.asion.dev/carts/
```

| Parameter    | Type | Description                                           |
| :----------- | :--- | :---------------------------------------------------- |
| `cart_owner` | `id` | **Required**. ForeignKey to user. Specify the user id |

**Response:**

**Sent:**

```json
{
  "cart_owner": 12
}
```

**Got:**

```json
{
  "id": 8,
  "items": [],
  "cart_url": "https://api.sakurassweets.asion.dev/carts/8/",
  "cart_owner": 12
}
```

**CODES:**

- `201` (Created)
- `400` (Bad Request)
- `405` (Method now Allowed)

## Cart creating validation rules

**Rules:**

- User could have only one cart, throw excpetion if user already have cart.
- Cart owner should be an existing user.
