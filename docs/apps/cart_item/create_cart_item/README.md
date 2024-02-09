## Create cart item

**Allow:** `GET, POST, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Authenticated only`

```
  POST https://api.sakurassweets.asion.dev/products/
```

| Parameter  | Type      | Description                                                                 |
| :--------- | :-------- | :-------------------------------------------------------------------------- |
| `cart`     | `id`      | **Required**. ForeignKey to cart in which item is stored. Specify the id.   |
| `product`  | `id`      | **Required**. ForeignKey to product which is added to cart. Specify the id. |
| `quantity` | `integer` | **Required**. Quantity, how many of product added to cart.                  |

**Response:**

**Sent:**

```json
{
  "quantity": 100,
  "cart": 3,
  "product": 1
}
```

**Got:**

```json
{
  "id": 49,
  "product_url": "https://api.sakurassweets.asion.dev/products/1/",
  "cart_item_url": "https://api.sakurassweets.asion.dev/cart-items/49/",
  "quantity": 100,
  "cart": 3,
  "product": "\"Мармелад Японський\""
}
```

**CODES:**

- `201` (Created)
- `400` (Bad Request)
- `403` (Forbidden)
- `405` (Method now Allowed)

## Cart item creating validation rules

**Rules:**

- `quantity` should be positive integer number, float of negative number unallowed. You can't add amount of product in cart that bigger then product's quantity in stock.
- `cart` should exist and don't have this product in it already.
- `product` should exist.
- `User` should be owner of the cart in which cart item is adding.
