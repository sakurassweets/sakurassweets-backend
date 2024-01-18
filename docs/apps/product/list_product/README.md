## List Product reference

## List Product

**Allow:** `GET, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  GET https://api.sakurassweets.asion.tk/products/
```

**Response:**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "product_url": "https://api.sakurassweets.asion.tk/products/2/",
      "product_type": "Мармелад",
      "price_currency": "UAH",
      "images": [
        {
          "image": "https://api.sakurassweets.asion.tk/media/product_2/jk-placeholder-image.jpg"
        }
      ],
      "title": "123123122233asd222",
      "price": "123.00",
      "description": "asfassa",
      "quantity_in_stock": 108,
      "product_quantity": "asdfa",
      "discount": "0 %",
      "rating": 2.0,
      "components": "sagassgasga",
      "price_currency_symbol": "₴"
    },
    {
      "id": 1,
      "product_url": "https://api.sakurassweets.asion.tk/products/1/",
      "product_type": "Мармелад",
      "price_currency": "UAH",
      "images": [
        {
          "image": "https://api.sakurassweets.asion.tk/media/product_1/jk-placeholder-image.jpg"
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
  ]
}
```

**CODES:**

- `200` (OK)
