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

Signs the user in and returns their UID.

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

Registers a new user.

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

## Packages

- **backend_connectors**: Package containing everything related to backend connections.
    - **.database_connector**: Module holding all the database related functions.
    - **.ollama_connector**: Module holding all Ollama related functions.

- **endpoints**: Package containing all endpoints.
    - **.ollama_endpoint**: Module holding all ollama related endpoints.
    - **.user_endpoint**: Module holding all user related enpoints.

- **handlers**: Package containing all internal modules.
    - **.user_handler**: Internal user handler, between endpoint and connector.
 
## Environment variables

- `LLM_MODEL` which modle to user, default: `llama3.2`
- `LLM_ADDRESS` full address to llm host, default: `http://100.77.88.10`
- `LLM_PREPROPT_PATH` path to file containing the preprompt, default: `./preprompt`
