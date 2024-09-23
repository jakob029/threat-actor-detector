

# How to communicate with ollama server


```
curl http://10.245.115.5:11434/api/generate -d '{
  "model": "llama3.1",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

* Prompt is what you want to ask it.
* Stream false means that we want the entire generated answer from llama to be in one JSON response. Set true if you want to recive one response per word.
