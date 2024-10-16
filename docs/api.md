# API

## Requests

<details>

<summary>Tests</summary>

sends a question to the llm and gives the llm response as a response.

    URL http://127.0.0.1:5000/test

**Response body**

```json
{
    "messages": [
        {
            'role': 'user',
            'content': 'what is a rock?'
        }, {
            'role': 'assistant',
            'content': <llm response 1>
        }, {
            'role': 'user',
            'content': 'can you write a song about it?'
        }, {
            'role': 'assistant',
            'content': <llm response 2>
        }
    ]
}
```

**Failed**

```json
{
    "message": <messgae>
} 
```

</details>

<details>

<summary>Analysis</summary>

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

