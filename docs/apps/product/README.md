## Product model information

## Product model fields

| Field               | Field Type                  | Description                            | Parameters                                                |
| :------------------ | :-------------------------- | :------------------------------------- | --------------------------------------------------------- |
| `title`             | `CharField`                 | Product title                          | `max_length=255, blank=False, null=False`                 |
| `price`             | `DecimalField`              | Product price                          | `max_digits=8, decimal_places=2, blank=False, null=False` |
| `price_currency`    | `ForeignKey`                | ForeignKey to `PriceCurrency` model    | `on_delete=models.SET_NULL, blank=False, null=True`       |
| `product_type`      | `ForeignKey`                | ForeignKey to `ProductType` model      | `on_delete=models.SET_NULL, blank=False, null=True`       |
| `description`       | `TextField`                 |                                        | `max_length=6000, default='', blank=True, null=False`     |
| `quantity_in_stock` | `PositiveIntegerField`      | Quantity of product in stock           | `blank=False, null=False`                                 |
| `product_quantity`  | `CharField`                 | Quantity of product (e.g. 100g, 12pcs) | `max_length=255, blank=False, null=False`                 |
| `discount`          | `PositiveSmallIntegerField` | Product discount (from 0 to 99)        | `default=0, blank=True, null=True`                        |
| `rating`            | `FloatField`                | Product rating (from 0 to 5.0)         | `default=0, blank=True, null=True`                        |
| `components`        | `TextField`                 | List of product components             | `default='', blank=True, null=True`                       |

## Other information

Product title displays like "this" or this only. There's formatting to avoid double or more quotes.

By default ordering is `"-id"` (first one is the newest).
