# API

## Requests

<details>

<summary>Analysis</summary>

sends a question to the llm and gives the llm response as a response.

**URL** POST

    http://127.0.0.1:5000/analyzis

**Request body**

```json
{
    "prompt": "<prompt>"
}
```

**Response body**

```json
{
	"response": "<llm response>",
	"mesage": "<RESONSE_MESSAGE>",
	"data_points": {
		"ENTRY_2": "<FLOAT>",
		"ENRTY_1": "<FLOAT>"
	}
}
```

**Failed**

```json
{
    "mesage": "<RESONSE_MESSAGE>"
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
    "username": "<username>",
    "password": "<password>"
}
```

**Response body**

```json
{
    "mesage": "<RESONSE_MESSAGE>",
    "uid": "<user id>"
}
```

**Failed**

```json
{
    "mesage": "<RESONSE_MESSAGE>"
}
```


</details>
<<details>

<summary>Registration</summary>

Registers a new user.

**URL** POST

    http://127.0.0.1:5000/user/register

**Request body**

```json
{
    "username": "<username>",
    "password": "<password>"
}
```

**Response body**

```json
{
    "mesage": "<RESONSE_MESSAGE>"
}
```

**Failed**

No error implemented.

</details>

<details>

<summary>Create conversation</summary>

Create a new conversation.

**URL** POST

    http://127.0.0.1:5000/conversation

**Request body**

```json
{
    "uid": "<USER_ID>",
}
```

**Response body**

```json
{
    "mesage": "<RESONSE_MESSAGE>"
    "cid": "<CONVERSATION_ID>"
}
```

**Failed**

```json
{
    "mesage": "<ERROR_MESSAGE>"
}
```

</details>

<details>

<summary>Get conversations</summary>

Get all user conversations.

**URL** GET

    http://127.0.0.1:5000/conversation/<USER_ID>

**Response body**

```json
{
    "mesage": "<RESONSE_MESSAGE>"
    "conversations": {
        "<CONVERSATION_ID_1>": "<CONVERSATION_TITLE_1>",
        "<CONVERSATION_ID_2>": "<CONVERSATION_TITLE_2>"
    }
}
```

**Failed**

```json
{
    "mesage": "<ERROR_MESSAGE>"
}
```

</details>

<details>

<summary>Add message to conversation</summary>

Adds a message to an already existing conversation.

**URL** POST

    http://127.0.0.1:5000/messages

**Request body**

```json
{
    "cid": "<CONVERSATION_ID>",
    "text": "<TEXT>"
}
```

**Response body**

```json
{
    "mesage": "success"
}
```

**Failed**

```json
{
    "mesage": "<ERROR_MESSAGE>"
}
```

</details>

<details>

<summary>Get messages</summary>

Get all messages for a conversation.

**URL** GET

    http://127.0.0.1:5000/messages/<CONVERSATION_ID>

**Response body**

```json
{
    "mesage": "success"
    "conversation_history": [
        {
            "role": "<SENDER_ROLE_1>",
            "text": "<MESSAGE_TEXT_1>"
        },
        {
            "role": "<SENDER_ROLE_2>",
            "text": "<MESSAGE_TEXT_2>"
        }
    ]
}
```

**Failed**

```json
{
    "mesage": "<ERROR_MESSAGE>"
}
```

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
- `TAD_MYSQL_HOST` host ip to MySQL server.
- `TAD_MYSQL_USER` username of TAD managment account.
- `TAD_MYSQL_PASSWORD` user password.
- `TAD_MYSQL_DATABASE` database name.
