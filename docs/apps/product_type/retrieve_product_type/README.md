## Retrieve product type

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  GET https://api.sakurassweets.asion.tk/product-types/{id}/
```

**Response:**

```json
{
  "id": 1,
  "product_type_url": "https://api.sakurassweets.asion.tk/product-types/1/",
  "title": "Мармелад"
}
```

**CODES:**

- `200` (OK)
