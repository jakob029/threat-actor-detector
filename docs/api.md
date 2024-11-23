# API

## Example usage

First create user with:

``` bash
curl \
-H 'Content-TYPE: application/json' \
-X POST \
-d '{"username": "jeppeboi2cool4u", "password": "Test123!"}' \
http://<HOST>:<PORT>/user/register
```

then, login to the newly created user:

``` bash
curl \
-H 'Content-TYPE: application/json' \
-X POST \
-d '{"username": "jeppeboi2cool4u", "password": "Test123!"}' \
http://<HOST>:<PORT>/user/login
```

which uppon success will return the *uid*, eg. 'a3921875-a9a2-11ef-b4c2-bc2411c91e6c'. Now a conversation can be created:

``` bash
curl \
-H 'Content-TYPE: application/json' \
-X POST \
-d '{"uid": "a3921875-a9a2-11ef-b4c2-bc2411c91e6c"}' \
http://<HOST>:<PORT>/conversation
```

which will return a *cid*, eg. 'ced239c1-a9a2-11ef-b4c2-bc2411c91e6c'. The *cid* will be used to handle the conversation, now we'll do an analyzis:

``` bash
curl \
-H 'Content-TYPE: application/json' \
-X POST \
-d '{"cid": "ced239c1-a9a2-11ef-b4c2-bc2411c91e6c", "prompt": "What APT is could be responsible for an attack that includes: Adversaries may encrypt data on target systems or on large numbers of systems in a network to interrupt availability to system and network resources."}' \
http://<HOST>:<PORT>/analyzis
```

This will give the llm response and some data points, which can be used for a graph.


## Requests

<details>

<summary>Analysis</summary>

sends a question to the llm and gives the llm response as a response.

**URL** POST

    http://<HOST>:<PORT>/analyzis

**Request body**

```json
{
    "prompt": "<PROMPT>",
    "cid": "<CONVERSATION_ID"
}
```

**Response body**

```json
{
	"response": "<LLM_RESPONSE>",
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

Get graph from previous analyzis call.

**URL** GET

    http://<HOST>:<PORT>/analyzis/<CONVERSATION_ID>

**Response body**

```json
{
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

    http://<HOST>:<PORT>/user/login

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
<details>

<summary>Registration</summary>

Registers a new user.

**URL** POST

    http://<HOST>:<PORT>/user/register

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

<summary>Conversations</summary>

Create a new conversation.

**URL** POST

    http://<HOST>:<PORT>/conversation

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

Get all user conversations.

**URL** GET

    http://<HOST>:<PORT>/conversation/<USER_ID>

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

<summary>Messages in conversations</summary>

Adds a message to an already existing conversation.

**URL** POST

    http://<HOST>:<PORT>/messages

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

Get all messages for a conversation.

**URL** GET

    http://<HOST>:<PORT>/messages/<CONVERSATION_ID>

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

Removes all messages and the graph for a conversation.

**URL** DELETE

    http://<HOST>:<PORT>/messages/<CONVERSATION_ID>

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



## Packages

- **backend_connectors**: Package containing everything related to backend connections.
    - **.database_connector**: Module holding all the database related functions.
    - **.ollama_connector**: Module holding all Ollama related functions.

- **endpoints**: Package containing all endpoints.
    - **.ollama_endpoint**: Module holding all ollama related endpoints.
    - **.user_endpoint**: Module holding all user related enpoints.
    - **.conversation_endpoint**: Module holding all conversation related enpoints.
    - **.message_endpoint**: Module holding all message related endpoints.

- **handlers**: Package containing all internal modules.
    - **.user_handler**: Internal user handler, between endpoint and connector.
    - **.conversation_handler**: Internal conversation handler, between endpoint and database.
 
## Environment variables

- `LLM_MODEL` which modle to user, default: `llama3.2`
- `LLM_ADDRESS` full address to llm host, default: `http://100.77.88.10`
- `LLM_PREPROPT_PATH` path to file containing the preprompt, default: `./preprompt`
- `TAD_MYSQL_HOST` host ip to MySQL server.
- `TAD_MYSQL_USER` username of TAD managment account.
- `TAD_MYSQL_PASSWORD` user password.
- `TAD_MYSQL_DATABASE` database name.
