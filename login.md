# Login

Used to collect a Token for a registered User.

**URL** : `/api/login/`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
    "username": "[registered username]",
    "password": "[password in plain text]"
}
```

**Data example**

```json
{
    "username": "testUser",
    "password": "abcd1234"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "token": "..."
}
```

## Error Response

**Condition** : If 'username' and 'password' combination is wrong.

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "wrong_pass": "Wrong password for this username!",
    "error_message": "This user has not registered yet!"
}
```