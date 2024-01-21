## Product model information

## Product model fields

| Field      | Field Type             | Description                               | Parameters                         |
| :--------- | :--------------------- | :---------------------------------------- | ---------------------------------- |
| `cart`     | `ForeignKey`           | ForeignKey to cart that item is listed in | `null=True, blank=False`           |
| `product`  | `ForeignKey`           | ForeignKey of product that listed in cart | `null=True, blank=False`           |
| `quantity` | `PositiveIntegerField` | Quantity of product in cart               | `default=1, null=True, blank=True` |

## Other information

Cart item title displays like "this" or this only. There's formatting to avoid double or more quotes.

By default ordering is `"-id"` (first one is the newest).
