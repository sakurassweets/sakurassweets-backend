## List images

**Allow:** `GET, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  GET https://api.sakurassweets.asion.dev/images/
```

**Response:**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 7,
      "image_url": "https://api.sakurassweets.asion.dev/images/7/",
      "image": "https://api.sakurassweets.asion.dev/media/product_3/jk-placeholder-image_LOB0DLt.jpg",
      "main_image": true,
      "related_to": 3
    },
    {
      "id": 1,
      "image_url": "https://api.sakurassweets.asion.dev/images/1/",
      "image": "https://api.sakurassweets.asion.dev/media/product_1/jk-placeholder-image.jpg",
      "main_image": true,
      "related_to": 1
    }
  ]
}
```

**CODES:**

- `200` (OK)
