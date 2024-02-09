## Create Product

**Allow:** `GET, POST, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrators and Staff only`

```
  POST https://api.sakurassweets.asion.dev/products/
```

| Parameter           | Type      | Description                                                         |
| :------------------ | :-------- | :------------------------------------------------------------------ |
| `title`             | `string`  | **Required**. Title of product                                      |
| `price`             | `integer` | **Required**. Product price                                         |
| `price_currency`    | `id`      | **Required**. Price currency                                        |
| `product_type`      | `id`      | **Required**. Product type                                          |
| `description`       | `string`  | Product description. `Default = ''`                                 |
| `quantity_in_stock` | `integer` | **Required**. Quantity of product in stock.                         |
| `product_quantity`  | `string`  | **Required**. Product quantity means like 500 mg or 10pcs           |
| `discount`          | `integer` | Product discout. `Default = 0`                                      |
| `rating`            | `float`   | Product rating. `Default = 0`                                       |
| `components`        | `string`  | Product components (will be deleted later probably). `Default = ''` |

**Response:**

**Sent:**

```json
{
  "title": "Testing Title",
  "price": "210",
  "price_currency": 6,
  "product_type": 1,
  "quantity_in_stock": 5000,
  "product_quantity": "12pcs"
}
```

**Got:**

```json
{
  "id": 6,
  "product_url": "https://api.sakurassweets.asion.dev/products/6/",
  "product_type": "Мармелад",
  "price_currency": "USD",
  "images": [],
  "title": "Testing Title",
  "price": "210.00",
  "description": "",
  "quantity_in_stock": 5000,
  "product_quantity": "12pcs",
  "discount": "0 %",
  "rating": 0.0,
  "components": "",
  "price_currency_symbol": "$"
}
```

**CODES:**

- `201` (Created)
- `400` (Bad Request)
- `403` (Forbidden)
- `405` (Method now Allowed)
