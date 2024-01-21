## List price currencies

**Allow:** `GET, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  GET https://api.sakurassweets.asion.tk/price-currencies/
```

**Response:**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 6,
      "price_currency_url": "https://api.sakurassweets.asion.tk/price-currencies/6/",
      "currency_symbol": "$",
      "currency": "USD",
      "country": "USA"
    },
    {
      "id": 1,
      "price_currency_url": "https://api.sakurassweets.asion.tk/price-currencies/1/",
      "currency_symbol": "₴",
      "currency": "UAH",
      "country": "ukraine"
    }
  ]
}
```

**CODES:**

- `200` (OK)
