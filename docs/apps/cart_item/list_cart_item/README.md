## List Cart items

**Allow:** `GET, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  GET https://api.sakurassweets.asion.tk/cart-items/
```

**Response:**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 49,
      "product_url": "https://api.sakurassweets.asion.tk/products/1/",
      "cart_item_url": "https://api.sakurassweets.asion.tk/cart-items/49/",
      "quantity": 100,
      "cart": 3,
      "product": "\"Мармелад Японський\""
    },
    {
      "id": 45,
      "product_url": "https://api.sakurassweets.asion.tk/products/3/",
      "cart_item_url": "https://api.sakurassweets.asion.tk/cart-items/45/",
      "quantity": 12,
      "cart": 1,
      "product": "Test"
    }
  ]
}
```

**CODES:**

- `200` (OK)
