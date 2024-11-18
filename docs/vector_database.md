# Vector database instructions

The Vector database is based on Chroma DB, running the all-mpnet-base-v2 inference model.

Example usage:
```python
collection.query(
query_texts=["crime group that has stolen payment card"],
n_results=20,
include=["distances"]
)
```

Where the distance is the lenght of the vector for the given index.
