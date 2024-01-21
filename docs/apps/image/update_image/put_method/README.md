## Update image by PUT

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrator and Staff only`

```
  PUT https://api.sakurassweets.asion.tk/images/{id}/
```

**This method is not recommended to use with Image model right now**

`PUT` method enforce you to send all **required** fields even if you don't change them.

**Fields that can be updated:**

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
"main_image": "False",
"related_to": 3
```

**Got:**

```json
{
  "id": 1,
  "image_url": "https://api.sakurassweets.asion.tk/images/1/",
  "image": "https://api.sakurassweets.asion.tk/media/product_3/jk-placeholder-image_VvPgMwp.jpg",
  "main_image": false,
  "related_to": 3
}
```

**CODES:**

- `200` (OK)
- `400` (Bad request)
- `403` (Forbidden)
