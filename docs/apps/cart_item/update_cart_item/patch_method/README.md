## Update Cart item by PATCH

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrators and cart owner only`

```
  PATCH https://api.sakurassweets.asion.tk/cart-items/{id}/
```

`PATCH` method allows you to change fields by sending only field that you wanna change and new value. For example:

```json
{
  "quantity": 20
}
```

**Fields that can be updated:**

| Parameter  | Type      | Description                                                   |
| :--------- | :-------- | :------------------------------------------------------------ |
| `cart`     | `id`      | ForeignKey to cart in which item is stored. Specify the id.   |
| `product`  | `id`      | ForeignKey to product which is added to cart. Specify the id. |
| `quantity` | `integer` | Quantity, how many of product added to cart.                  |

**Response:**

In response you get all fields. For example:

**Sent:**

```json
{
  "quantity": 20
}
```

**Got:**

```json
{
  "id": 47,
  "product_url": "https://api.sakurassweets.asion.tk/cart-items/products/1/",
  "cart_item_url": "https://api.sakurassweets.asion.tk/cart-items/cart-items/47/",
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
