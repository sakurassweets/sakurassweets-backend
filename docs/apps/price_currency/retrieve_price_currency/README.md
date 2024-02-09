## Retrieve price currency

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  GET https://api.sakurassweets.asion.dev/price-currencies/{id}/
```

**Response:**

```json
{
  "id": 1,
  "price_currency_url": "https://api.sakurassweets.asion.dev/price-currencies/1/",
  "currency_symbol": "₴",
  "currency": "UAH",
  "country": "ukraine"
}
```

**CODES:**

- `200` (OK)
