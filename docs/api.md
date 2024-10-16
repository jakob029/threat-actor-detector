# API

## Requests

<details>

<summary>Analysis request</summary>

### Analysis

sends a question to the llm and gives the llm response as a response.

    URL http://127.0.0.1:5000/analysis

**Request body**

```json
{
    "question": <question>
}
```

**Response body**

```json
{
    "created": <Time request was created>,
    "content": <llm response>,
    "message": "Success"
}
```

**Failed**

```json
{
    "message": <messgae>
} 
```

</details>
