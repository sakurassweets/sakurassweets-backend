## Retrieve Product

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  GET https://api.sakurassweets.asion.dev/products/{id}/
```

**Response:**

```json
{
  "id": 1,
  "product_url": "https://api.sakurassweets.asion.dev/products/1/",
  "product_type": "Мармелад",
  "price_currency": "UAH",
  "images": [
    {
      "image": "https://api.sakurassweets.asion.dev/media/product_1/jk-placeholder-image.jpg"
    }
  ],
  "title": "\"Мармелад Японський\"",
  "price": "123.00",
  "description": "фівфівфівіф",
  "quantity_in_stock": 100,
  "product_quantity": "40 грам",
  "discount": "0 %",
  "rating": 4.5,
  "components": "фівфівфівф",
  "price_currency_symbol": "₴"
}
```

**CODES:**

- `200` (OK)
