## Create price currency

**Allow:** `GET, POST, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrators and Staff only`

```
  POST https://api.sakurassweets.asion.dev/price-currencies/
```

| Parameter         | Type     | Description                                               |
| :---------------- | :------- | :-------------------------------------------------------- |
| `currency_symbol` | `string` | **Required**. Currency symbol (e.g. "$")                  |
| `currency`        | `string` | **Required**. Currency name (e.g. "USD")                  |
| `country`         | `string` | **Required**. Country where currency is used (e.g. "USA") |

**Response:**

**Sent:**

```json
{
  "currency_symbol": "T",
  "currency": "test",
  "country": "Country"
}
```

**Got:**

```json
{
  "id": 7,
  "price_currency_url": "https://api.sakurassweets.asion.dev/price-currencies/7/",
  "currency_symbol": "T",
  "currency": "test",
  "country": "Country"
}
```

**CODES:**

- `201` (Created)
- `400` (Bad Request)
- `403` (Forbidden)
- `405` (Method now Allowed)
