## List Product

**Allow:** `GET, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  GET https://api.sakurassweets.asion.dev/products/
```

**Filters:**

- **Default filter:**

  - **Filter fields:** `product_type`, `price_currency`, `price`, `quantity_in_stock`, `rating`, `price_currency_symbol`
  - **Usage:**

  ```
  GET https://api.sakurassweets.asion.dev/products/?rating=5
  ```

  > will add in future ability to search by gt, gte, lt, lte (greater/lower than | or equal)

- **Search filter:**

  - **Search type:** `icontains`. That means that filter search for any field that contains query value (mochi in this case)
  - **Search fields:** `title`, `description`, `components`
  - **Usage:**

  ```
  GET https://api.sakurassweets.asion.dev/products/?search=mochi
  ```

- **Greater/lower than equals filter:**
  - Filtering by greater/lower than equals method.
  - **Filter fields:** `price`, `rating`, `quantity_in_stock`
  - **Usage:** `{field}__lte` (lower than equals) or `{field}__gte` (greater than equals)

  ```
  GET https://api.sakurassweets.asion.dev/products/?price__lte=2000
  ```

- **Ordering filter:**

  - **Ordering fields:** `id`, `price`, `quantity_in_stock`, `rating`, `discount`, `title`
  - **Usage:**

  ```
  GET https://api.sakurassweets.asion.dev/products/?ordering=-rating
  ```

  - All field can be searched like `id` or `-id`. `-` means in reverse order. For exaple: in `id` case - from newer to older, in `price` case - from higher to lower

**Response:**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "product_url": "https://api.sakurassweets.asion.dev/products/2/",
      "product_type": "Мармелад",
      "price_currency": "UAH",
      "images": [
        {
          "image": "https://api.sakurassweets.asion.dev/media/product_2/jk-placeholder-image.jpg"
        }
      ],
      "title": "123123122233asd222",
      "price": "123.00",
      "description": "asfassa",
      "quantity_in_stock": 108,
      "product_quantity": "asdfa",
      "discount": "0 %",
      "rating": 2.0,
      "components": "sagassgasga",
      "price_currency_symbol": "₴"
    },
    {
      "id": 1,
      "product_url": "https://api.sakurassweets.asion.dev/products/1/",
      "product_type": "Мармелад",
      "price_currency": "UAH",
      "images": [
        {
          "image": "https://api.sakurassweets.asion.dev/media/product_1/jk-placeholder-image.jpg"
        }
      ],
      "title": "\"Мармелад Японський\"",
      "price": "123.00",
      "description": "фівфівфівіф",
      "quantity_in_stock": 100,
      "product_quantity": "40 грам",
      "discount": "0 %",
      "rating": 4.5,
      "components": "фівфівфівф",
      "price_currency_symbol": "₴"
    }
  ]
}
```

**CODES:**

- `200` (OK)
