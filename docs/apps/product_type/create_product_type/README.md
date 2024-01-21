## Create product type

**Allow:** `GET, POST, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrators and Staff only`

```
  POST https://api.sakurassweets.asion.tk/product-types/
```

| Parameter | Type     | Description                         |
| :-------- | :------- | :---------------------------------- |
| `title`   | `string` | **Required**. Title of product type |

**Response:**

**Sent:**

```json
{
  "title": "Шоколад"
}
```

**Got:**

```json
{
  "id": 2,
  "product_type_url": "https://api.sakurassweets.asion.tk/product-types/2/",
  "title": "Шоколад"
}
```

**CODES:**

- `201` (Created)
- `400` (Bad Request)
- `403` (Forbidden)
- `405` (Method now Allowed)
