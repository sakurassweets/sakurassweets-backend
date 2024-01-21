## Update Product by PATCH

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrators and Staff only`

```
  PATCH https://api.sakurassweets.asion.tk/products/{id}/
```

`PATCH` method allows you to change fields by sending only field that you wanna change and new value. For example:

```json
{
  "title": "New title of Product"
}
```

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

In response you get all fields (will be fixed later). For example:

**Sent:**

```json
{
  "title": "New Title"
}
```

**Got:**

```json
{
  "id": 8,
  "product_url": "https://api.sakurassweets.asion.tk/products/8/",
  "product_type": "Мармелад",
  "price_currency": "USD",
  "images": [],
  "title": "New Title",
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

- `200` (OK)
- `400` (Bad request)
- `403` (Forbidden)
- `405` (Method now Allowed)
