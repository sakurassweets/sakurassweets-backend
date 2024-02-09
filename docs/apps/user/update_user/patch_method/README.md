## Update user by PATCH

**Allow:** `GET, PUT, PATCH, DELETE, HEAD, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Administrator or user itself`

```
  PATCH https://api.sakurassweets.asion.dev/users/{id}/
```

`PATCH` method allows you to change fields by sending only field that you wanna change and new value. For example:

```json
{
  "email": "new_email@gmail.com"
}
```

**Fields that can be updated:**

**!!! To update password, you should send `new_password` in request body**

| Parameter      | Type       | Description       | Permission           |
| :------------- | :--------- | :---------------- | -------------------- |
| `email`        | `string`   | User email        | User itself or admin |
| `password`     | `string`   | User password     | User itself or admin |
| `last_login`   | `DateTime` | last login time   | Admin or staff       |
| `is_superuser` | `boolean`  | super user status | Admin                |
| `is_staff`     | `boolean`  | staff status      | Admin                |
| `is_active`    | `boolean`  | activity status   | Admin or staff       |

> currently permissions isn't working properly, but this will be fixed

**Response:**

In response you get data about changed fields. For example:

**Sent:**

```json
{
  "new_password": "912459512jaSBDas"
}
```

**Got:**

```json
{
  "data": {
    "new_password": "argon2$argon2id$v=19$m=102400,t=2,p=8$MW1Zdk1jUUxSN2FQMnJxMExBSFhhSg$C740Naw0dRGoWpnwTvWbbrvZ3Pkn8eS87rL+CR2o0v0"
  }
}
```

**CODES:**

- `200` (OK)
- `400` (Bad request)
- `403` (Forbidden)

## User updating validation rules

- Validates that you have permission to update user. Permission have only administrators and users itself.
- Validates you didn't send any empty field
- Validates you sent atleast anything in request

**New password validation:**

- Validates you'r password not the same as old one
- Password length validation:
  - Min value: 8 characters
  - Max value: 40 characters
- Password should not contain spacebars
- Password should contain only latin characters
- Password should have atleast 1 digit
- Password can't be too similar to any of other fields (max similarity is 55%)
- Password should contain atleast 1 lowercase and 1 uppercase letters

**New email validation:**

**Notes:**

- Validates you'r email not the same as old one
- Allowed special characters list: `-`, `_`, `.`
- Allowed all latin letters and digits
- Email parts (Structure: `<email_name>@<domain_name>.<domain_address>`):
  - email name
  - email domain
    - domain name
    - domain address

**Rules:**

**General email:**

- Email should have one and only one '@' symbol
- Email should not contain any of unallowed characters in any of it parts
- Validates email parts that:
  - part didn't start or end with special characters
  - part have at least one non-digit character
  - part didn't have 2 or more special characters in a row

**Email domain:**

- Domain contains domain name and domain address splitted by dot
- Domain should not contain any special characters
- Domain should not contain any digits
- Domain address can be minimum of 2 digits and maximum of 6
- Domain should not contain underscore
