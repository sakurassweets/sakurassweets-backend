## Update image by PATCH

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrator and Staff only`

```
  PATCH https://api.sakurassweets.asion.tk/images/{id}/
```

`PATCH` method allows you to change fields by sending only field that you wanna change and new value. For example:

```json
{
  "related_to": 6
}
```

**Fields that can be updated:**

| Parameter    | Type                         | Description                                                               |
| :----------- | :--------------------------- | :------------------------------------------------------------------------ |
| `image`      | `file (multipart/form-data)` | Image file                                                                |
| `main_image` | `bool`                       | Main image always displays as first image and can be only one for product |
| `related_to` | `id`                         | ForeignKey to `Product` that image is related to                          |

**Response:**

In response you get data about changed fields. For example:

**Sent:**

```json
{
  "related_to": 6
}
```

**Got:**

```json
{
  "id": 1,
  "image_url": "https://api.sakurassweets.asion.tk/images/1/",
  "image": "https://api.sakurassweets.asion.tk/media/product_1/jk-placeholder-image.jpg",
  "main_image": true,
  "related_to": 6
}
```

**CODES:**

- `200` (OK)
- `400` (Bad request)
- `403` (Forbidden)
