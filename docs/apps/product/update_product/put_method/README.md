## Update Product by PUT

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrators and Staff only`

```
  PUT https://api.sakurassweets.asion.dev/products/{id}/
```

`PUT` method enforce you to send all **required** fields even if you don't change them.

**Fields that can be updated:**

| Parameter           | Type      | Description                                          |
| :------------------ | :-------- | :--------------------------------------------------- |
| `title`             | `string`  | Title of product                                     |
| `price`             | `integer` | Product price                                        |
| `price_currency`    | `id`      | Price currency                                       |
| `product_type`      | `id`      | Product type                                         |
| `description`       | `string`  | Product description.                                 |
| `quantity_in_stock` | `integer` | Quantity of product in stock.                        |
| `product_quantity`  | `string`  | Product quantity means like 500 mg or 10pcs          |
| `discount`          | `integer` | Product discout.                                     |
| `rating`            | `float`   | Product rating.                                      |
| `components`        | `string`  | Product components (will be deleted later probably). |

**Response:**

In response you get data about all fields. For example:

**Sent:**

```json
{
  "title": "New Title",
  "product_type": 1,
  "price": 2100,
  "price_currency": 6,
  "quantity_in_stock": 1000,
  "product_quantity": "100 g"
}
```

**Got:**

```json
{
  "id": 8,
  "product_url": "http://127.0.0.1:8000/products/8/",
  "product_type": "Мармелад",
  "price_currency": "USD",
  "images": [],
  "title": "New Title",
  "price": "2100.00",
  "description": "",
  "quantity_in_stock": 1000,
  "product_quantity": "100 g",
  "discount": "0 %",
  "rating": 0.0,
  "components": "",
  "price_currency_symbol": "$"
}
```

**CODES:**

- `200` (OK)
- `400` (Bad request)
- `403` (Forbidden)
- `405` (Method now Allowed)
