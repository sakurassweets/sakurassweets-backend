## Retrieve image

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  GET https://api.sakurassweets.asion.tk/images/{id}/
```

**Response:**

```json
{
  "id": 1,
  "image_url": "https://api.sakurassweets.asion.tk/images/1/",
  "image": "https://api.sakurassweets.asion.tk/media/product_1/jk-placeholder-image.jpg",
  "main_image": true,
  "related_to": 1
}
```

**CODES:**

- `200` (OK)
