# **Memory Module**

## Overview

The Memory Module is a critical component designed to store and retrieve structured memory entries for the agent. It leverages vector embedding and similarity search to maintain a contextual memory, allowing the agent to make decisions based on historical events and outcomes. This module supports flexible backends to meet different scalability and performance needs.

The Memory Module is implemented in `src/memory/memory_module.py` and integrates with vector storage systems like Qdrant and ChromaDB.

---

## How It Works

The Memory Module operates as follows:

1. **Embedding Generation**: Converts textual data into vector embeddings using OpenAI's embedding models.

2. **Memory Storage**: Stores embeddings and associated metadata in a vector store backend.

3. **Memory Retrieval**: Performs similarity searches to retrieve related memories based on a query.

4. **Backend Flexibility**: Supports multiple backends, such as Qdrant and ChromaDB, to accommodate various storage and performance requirements.

---

## Technical Features

### 1. **Embedding Generation**
The module uses an `EmbeddingGenerator` to convert textual descriptions (e.g., events, actions, outcomes) into vector embeddings. These embeddings form the basis for similarity searches.

#### Key Features:
- Supports asynchronous embedding generation using OpenAI models.
- Combines event, action, and outcome data to create meaningful embeddings.

#### Example:
```python
embedding = await embedding_generator.get_embedding("event action outcome")
```

---

### 2. **Memory Storage**
The `store` method saves memory entries in the vector store backend.

#### Features:
- Combines textual data and embeddings for efficient storage.
- Includes metadata for additional context.

#### Implementation:
```python
await memory_module.store(
    event="User Login",
    action="Verify Credentials",
    outcome="Success",
    metadata={"user_id": 1234}
)
```

---

### 3. **Memory Search**
The `search` method retrieves similar memory entries by performing a vector similarity search.

#### Features:
- Asynchronous search capability.
- Configurable `top_k` parameter to control the number of results.

#### Example:
```python
results = await memory_module.search(query="User Login", top_k=5)
```

---

### 4. **Backend Flexibility**
The module supports multiple backends for vector storage (by default Chroma):

- **Chroma**:
    - Local & lightweight vector store.
    - Uses persistent storage on disk.

- **Qdrant**:
    - High-performance distributed vector store.
    - Requires configuration for host, port, and vector size.

#### Backend Initialization:
```python
backend = QdrantBackend(
    collection_name="memory_collection",
    host="localhost",
    port=6333,
    vector_size=512
)
```

**Please note**: If you want to use Qdrant as a memory backend, you need to have Docker installed for running the Qdrant container. Install this software first (follow the official documentation).

---

## Example Workflow

1. **Store Memory**:
   ```python
   await memory_module.store(
       event="User Registration",
       action="Send Confirmation Email",
       outcome="Email Sent",
       metadata={"user_email": "example@example.com"}
   )
   ```

2. **Search Memory**:
   ```python
   similar_memories = await memory_module.search(
       query="User Registration",
       top_k=3
   )
   ```

3. **Backend Initialization**:
   ```python
   memory_module = get_memory_module(
       backend_type="qdrant"
   )
   ```

---

## Best Practices

1. **Consistent Data Structure**:
   Ensure all memory entries follow a standardized structure for consistency.

2. **Choose the Right Backend**:
   Use Qdrant for distributed, scalable setups and ChromaDB for lightweight, local use cases.

3. **Asynchronous Operations**:
   Take advantage of asynchronous methods for efficient execution.

---

If you have any questions or need further assistance, please refer to the [GitHub Discussions](https://github.com/axioma-ai-labs/nevron/discussions).

