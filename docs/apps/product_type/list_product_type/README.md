## List product types

**Allow:** `GET, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  GET https://api.sakurassweets.asion.dev/product-types/
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
      "product_type_url": "https://api.sakurassweets.asion.dev/product-types/2/",
      "title": "Шоколад"
    },
    {
      "id": 1,
      "product_type_url": "https://api.sakurassweets.asion.dev/product-types/1/",
      "title": "Мармелад"
    }
  ]
}
```

**CODES:**

- `200` (OK)
