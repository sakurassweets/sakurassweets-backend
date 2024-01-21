## Update cart by PUT/PATCH

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrators and Staff only`

```
  PUT/PATCH https://api.sakurassweets.asion.tk/carts/{id}/
```

Since crat has only one field and it's **required**, there's no sense to split PUT and PATCH methods. But recommended to choose proper method for you because changes in fields of product type can affect your requests.

**Fields that can be updated:**

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
  "id": 1,
  "items": [
    {
      "product": "\"Мармелад Японський\"",
      "product_url": "https://api.sakurassweets.asion.tk/products/1/",
      "cart_item_url": "https://api.sakurassweets.asion.tk/cart-items/47/"
    },
    {
      "product": "123123122233asd222",
      "product_url": "https://api.sakurassweets.asion.tk/products/3/",
      "cart_item_url": "https://api.sakurassweets.asion.tk/cart-items/45/"
    }
  ],
  "cart_url": "https://api.sakurassweets.asion.tk/carts/1/",
  "cart_owner": 12
}
```

**CODES:**

- `200` (OK)
- `400` (Bad request)
- `403` (Forbidden)
