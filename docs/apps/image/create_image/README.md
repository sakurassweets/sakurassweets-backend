## Upload image

**Allow:** `GET, POST, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrators and Staff only`

```
  POST https://api.sakurassweets.asion.dev/images/
```

| Parameter    | Type                         | Description                                                                             |
| :----------- | :--------------------------- | :-------------------------------------------------------------------------------------- |
| `image`      | `file (multipart/form-data)` | **Required**. Image file                                                                |
| `main_image` | `bool`                       | **Required**. Main image always displays as first image and can be only one for product |
| `related_to` | `id`                         | **Required**. ForeignKey to `Product` that image is related to                          |

**Response:**

**Sent:**

```
(form-data)

"image": "image_file",
"main_image": "true",
"related_to": 3
```

**Got:**

```json
{
  "id": 7,
  "image_url": "https://api.sakurassweets.asion.dev/images/7/",
  "image": "https://api.sakurassweets.asion.dev/media/product_3/jk-placeholder-image_LOB0DLt.jpg",
  "main_image": true,
  "related_to": 3
}
```

**CODES:**

- `201` (Created)
- `400` (Bad Request)
- `403` (Forbidden)
- `405` (Method now Allowed)

## Image uploading validation rules

**Rules:**

- Main image for product can be only one.
