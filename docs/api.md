# API

## Requests

<details>

<summary>Analysis</summary>

sends a question to the llm and gives the llm response as a response.

**URL** GET

    http://127.0.0.1:5000/analyzis

**Request body**

```json
{
    "prompt": <prompt>
}
```

**Response body**

```json
{
    "response": <llm response>
    "message": "Success"
}
```

**Failed**

```json
{
    "message": <error message>
} 
```

</details>
<details>

<summary>Authentication</summary>

**URL** POST

    http://127.0.0.1:5000/user/login

**Request body**

```json
{
    "username": <username>,
    "password": <password>
}
```

**Response body**

```json
{
    "message": "success",
    "uid": <user id>
}
```

**Failed**

```json
{
    "message": <error message>
}
```


</details>
<details>

<summary>Registration</summary>

**URL** POST

    http://127.0.0.1:5000/user/register

**Request body**

```json
{
    "username": <username>,
    "password": <password>
}
```

**Response body**

```json
{
    "message": "User registered."
}
```

**Failed**

No error implemented.

</details>

## Functions



