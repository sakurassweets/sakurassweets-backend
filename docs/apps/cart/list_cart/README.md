## List carts

**Allow:** `GET, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  GET https://api.sakurassweets.asion.dev/carts/
```

**Response:**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 3,
      "items": [],
      "cart_url": "https://api.sakurassweets.asion.dev/carts/3/",
      "cart_owner": 2
    },
    {
      "id": 1,
      "items": [
        {
          "product": "\"Мармелад Японський\"",
          "product_url": "https://api.sakurassweets.asion.dev/products/1/",
          "cart_item_url": "https://api.sakurassweets.asion.dev/cart-items/47/"
        },
        {
          "product": "123123122233asd222",
          "product_url": "https://api.sakurassweets.asion.dev/products/3/",
          "cart_item_url": "https://api.sakurassweets.asion.dev/cart-items/45/"
        }
      ],
      "cart_url": "https://api.sakurassweets.asion.dev/carts/1/",
      "cart_owner": 1
    }
  ]
}
```

**CODES:**

- `200` (OK)
