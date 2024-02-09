## Update product type by PUT/PATCH

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrators and Staff only`

```
  PUT/PATCH https://api.sakurassweets.asion.dev/product-types/{id}/
```

Since product type has only one field and it's **required**, there's no sense to split PUT and PATCH methods. But recommended to choose proper method for you because changes in fields of product type can affect your requests.

**Fields that can be updated:**

| Parameter | Type     | Description                         |
| :-------- | :------- | :---------------------------------- |
| `title`   | `string` | **Required**. Title of product type |

**Response:**

**Sent:**

```json
{
  "title": "Мочі"
}
```

**Got:**

```json
{
  "id": 2,
  "product_type_url": "http://127.0.0.1:8000/product-types/2/",
  "title": "Мочі"
}
```

**CODES:**

- `200` (OK)
- `400` (Bad request)
- `403` (Forbidden)
