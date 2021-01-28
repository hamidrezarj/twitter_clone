# Create Account

Register an Account

**URL** : `/api/register/`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None

**Data constraints**

Provide name, password, email of Account to be created.

```json
{
    "username": "[unicode 64 chars max]",
    "password": "[string]",
    "password2": "[string that should be the same as 'password']",
    "email": "[valid email address]"
}
```

**Data example** All fields must be sent.

```json
{
    "username": "testUser",
    "password": "abcd1234",
    "password2": "abcd1234",
    "email": "testUser@gmail.com"
}
```

## Success Response
Redirects to Home

**Condition** : If everything is OK and an Account didn't exist for this User.

**Code** : `201 CREATED`

**Content** ```{}```
```

## Error Responses

**Condition** : If Account already exists for User.

**Content example**

```json
{
    "error_message": true, 
    "username": "[username]"
}
```

### Or

**Condition** : Passwords don't match!

**Content example**

```json
{
    "pass_error": true
}
```