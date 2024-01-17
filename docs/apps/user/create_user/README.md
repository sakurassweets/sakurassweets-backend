## Create user reference

## Create user

**Allow:** `POST, OPTIONS`

**Content-Type:** `application/json`

**Vary:** `Accept`

**Permissions required**: `Allowed Anyone`

```
  POST https://api.sakurassweets.asion.tk/register/
```

| Parameter  | Type     | Description                 |
| :--------- | :------- | :-------------------------- |
| `email`    | `string` | **Required**. User email    |
| `password` | `string` | **Required**. User password |

If all data is correct you will get JSON response:

```json
{
  "access": "access_token_here",
  "refresh": "refresh_token_here"
}
```

**CODES:**

- `201` (Created)
- `400` (Bad Request)
- `405` (Method now Allowed)

## User creating context

- Sending welcome email after user creating
- Password always hashes
- Password and email validates

## User creating validation rules

**Password validation:**

- Password length validation:
  - Min value: 8 characters
  - Max value: 40 characters
- Password should not contain spacebars
- Password should contain only latin characters
- Password should have atleast 1 digit
- Password can't be too similar to any of other fields (max similarity is 55%)
- Password should contain atleast 1 lowercase and 1 uppercase letters

**Email validation:**

**Notes:**

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
