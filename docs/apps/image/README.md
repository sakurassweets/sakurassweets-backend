## Image model information

## Image model fields

| Parameter    | Type           | Description                                                                      |
| :----------- | :------------- | :------------------------------------------------------------------------------- |
| `image`      | `ImageField`   | Image field that stores a link (path) to image                                   |
| `main_image` | `BooleanField` | Says if image is main for product or not. Can be only one main image for product |
| `related_to` | `ForeignKey`   | ForeignKey to `Product` model. Says to which product image is related            |

## Other information

By default ordering is `"-id"` (first one is the newest).
