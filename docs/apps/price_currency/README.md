## Price currency model information

## Price currency model fields

| Field             | Field Type  | Description                                   | Parameters                                             |
| :---------------- | :---------- | :-------------------------------------------- | ------------------------------------------------------ |
| `currency_symbol` | `CharField` | Symbol of currency (e.g. "$")                 | `unique=True, max_length=10, blank=False, null=False`  |
| `currency`        | `CharField` | Currency name (e.g. "USD")                    | `unique=True, max_length=255, blank=False, null=False` |
| `country`         | `CharField` | Country where this currency used (e.g. "USA") | `max_length=255, blank=False, null=False`              |

## Other information

By default ordering is `"-id"` (first one is the newest).
