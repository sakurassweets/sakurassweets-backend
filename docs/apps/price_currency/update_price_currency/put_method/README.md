## Update price currency by PUT

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrators and Staff only`

```
  PUT https://api.sakurassweets.asion.tk/price-currencies/{id}/
```

`PUT` method enforce you to send all **required** fields even if you don't change them.

**Fields that can be updated:**

| Parameter         | Type     | Description                                               |
| :---------------- | :------- | :-------------------------------------------------------- |
| `currency_symbol` | `string` | **Required**. Currency symbol (e.g. "$")                  |
| `currency`        | `string` | **Required**. Currency name (e.g. "USD")                  |
| `country`         | `string` | **Required**. Country where currency is used (e.g. "USA") |

**Response:**

In response you get data about all fields. For example:

**Sent:**

```json
{
  "country": "USA",
  "currency_symbol": "$",
  "currency": "Test USD"
}
```

**Got:**

```json
{
  "id": 6,
  "price_currency_url": "http://127.0.0.1:8000/price-currencies/6/",
  "currency_symbol": "$",
  "currency": "Test USD",
  "country": "USA"
}
```

**CODES:**

- `200` (OK)
- `400` (Bad request)
- `403` (Forbidden)
