## Cart model information

## Cart model fields

| Field        | Field Type   | Description              | Parameters                                          |
| :----------- | :----------- | :----------------------- | --------------------------------------------------- |
| `cart_owner` | `ForeignKey` | ForeignKey to user model | `on_delete=models.SET_NULL, null=True, blank=False` |

## Other information

By default ordering is `"-id"` (first one is the newest).
