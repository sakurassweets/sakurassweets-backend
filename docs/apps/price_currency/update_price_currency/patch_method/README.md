## Update price currency by PATCH

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrators and Staff only`

```
  PATCH https://api.sakurassweets.asion.tk/price-currencies/{id}/
```

`PATCH` method allows you to change fields by sending only field that you wanna change and new value. For example:

```json
{
  "country": "Ukraine"
}
```

**Fields that can be updated:**

| Parameter         | Type     | Description                                 |
| :---------------- | :------- | :------------------------------------------ |
| `currency_symbol` | `string` | Currency symbol (e.g. "$")                  |
| `currency`        | `string` | Currency name (e.g. "USD")                  |
| `country`         | `string` | Country where currency is used (e.g. "USA") |

**Response:**

In response you get data about all fields. For example:

**Sent:**

```json
{
  "country": "Ukraine"
}
```

**Got:**

```json
{
  "id": 1,
  "price_currency_url": "http://127.0.0.1:8000/price-currencies/1/",
  "currency_symbol": "₴",
  "currency": "UAH",
  "country": "Ukraine"
}
```

**CODES:**

- `200` (OK)
- `400` (Bad request)
- `403` (Forbidden)
