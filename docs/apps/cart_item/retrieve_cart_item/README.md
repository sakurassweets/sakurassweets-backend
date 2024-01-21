## Retrieve Cart item

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  GET https://api.sakurassweets.asion.tk/cart-items/{id}/
```

**Response:**

```json
{
  "id": 50,
  "product_url": "https://api.sakurassweets.asion.tk/products/1/",
  "cart_item_url": "https://api.sakurassweets.asion.tk/cart-items/50/",
  "quantity": 100,
  "cart": 13,
  "product": "\"Мармелад Японський\""
}
```

**CODES:**

- `200` (OK)
