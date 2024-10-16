# API

## Requests

<details>

<summary>Analysis request</summary>

### Analysis

sends a question to the llm and gives the llm response as a response.

> URL http://127.0.0.1:5000/analysis

**Request body**

```json
{
    "question": <question>
}
```

**Response body**

```json
{
    "response": {
        "model": <model name>,
        "created_at": <reasuest time (YYYY-MM-DDTHH:MM:SS)>,
        "message": {
            "role": "assistant",
            "content": <llm response>
        }
    }    
}
```
</details>
