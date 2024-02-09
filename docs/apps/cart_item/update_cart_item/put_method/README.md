## Update Cart item by PUT

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrators and cart owner only`

```
  PUT https://api.sakurassweets.asion.dev/cart-items/{id}/
```

`PUT` method enforce you to send all **required** fields even if you don't change them.

**Fields that can be updated:**

| Parameter  | Type      | Description                                                                 |
| :--------- | :-------- | :-------------------------------------------------------------------------- |
| `cart`     | `id`      | **Required**. ForeignKey to cart in which item is stored. Specify the id.   |
| `product`  | `id`      | **Required**. ForeignKey to product which is added to cart. Specify the id. |
| `quantity` | `integer` | **Required**. Quantity, how many of product added to cart.                  |

**Response:**

In response you get all fields. For example:

**Sent:**

```json
{
  "product": 1,
  "quantity": 20,
  "cart": 1
}
```

**Got:**

```json
{
  "id": 47,
  "product_url": "https://api.sakurassweets.asion.dev/cart-items/products/1/",
  "cart_item_url": "https://api.sakurassweets.asion.dev/cart-items/cart-items/47/",
  "quantity": 20,
  "cart": 1,
  "product": "\"Мармелад Японський\""
}
```

**CODES:**

- `200` (OK)
- `400` (Bad request)
- `403` (Forbidden)
- `405` (Method now Allowed)

## Cart item updating validation rules

**Rules:**

- You can't manage items that not in your cart.
- You can't "move" items from you'r cart to another.
