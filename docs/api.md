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

