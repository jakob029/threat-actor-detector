# API

The vector database API allows for interactions with the chromaDB based vector database.

It also contains functionality four gathering descriptions for certain APT groups using the group analyzer endpoint.

## Requests

<details>

<summary>GroupDescriptor</summary>

### POST

Retrieve a dictionary containing descriptions for given APT groups.
(Group names shall be separated by ':')

#### Request

```json
{
    "groups": "<GROUP_NAMES>",
}
```

#### Response
```json
{
    "descriptor": {
        "<GROUP_NAME>": "<DESCRIPTION>"
    },
}
```


</details>

<details>

<summary>GroupAnalyzer</summary>

### GET

Retrieve an analyzed response of APT groups and vector database distances sourced from database based on given prompt.

#### Request

```json
{
    "prompt": "<VECTOR_DB_PROMPT>",
}
```

#### Response
```json
{
    "response": "<VECTOR_DB_RESPONSE>"
}
```