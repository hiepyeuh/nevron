# Llama Integration

The agent supports local inference using Meta's Llama models (8B, 70B, and 405B parameters) for scenarios requiring on-premise or self-hosted language models.

## Setup

1. Download Llama Model
   - Obtain access to Meta's Llama models through [Meta's AI website](https://ai.meta.com/llama/)
   - Download your preferred model size:
     - Llama-8B (16GB minimum RAM)
     - Llama-70B (140GB minimum RAM)
     - Llama-405B (780GB minimum RAM)

2. Install Dependencies
   ```bash
   pip install torch>=2.2.0 transformers>=4.38.0
   ```

3. Configure Environment Variables
   Add these to your `.env` file:
   ```bash
   LLAMA_MODEL_PATH=/path/to/your/llama/model
   LLM_PROVIDER=llama
   ```

### Basic Setup
```python
from src.llm.llm import LLM

# Initialize LLM with Llama backend
llm = LLM()  # Will use Llama if LLM_PROVIDER=llama

# Generate a response
response = await llm.generate_response([
    {"role": "user", "content": "Explain quantum computing"}
])
```

## Model Selection

Choose the appropriate model size based on your requirements:

### Llama-8B
- Minimum Requirements:
  - 16GB RAM
  - 20GB disk space
- Best for:
  - Basic text generation
  - Simple chat interactions
  - Resource-constrained environments

### Llama-70B
- Minimum Requirements:
  - 140GB RAM
  - 140GB disk space
- Best for:
  - Complex reasoning
  - Code generation
  - Advanced chat applications

### Llama-405B
- Minimum Requirements:
  - 780GB RAM
  - 800GB disk space
- Best for:
  - Research applications
  - Maximum model capability
  - Enterprise-scale deployments

## Advanced Configuration

### Memory Management
The agent automatically manages model loading based on available resources:
```python
# Override default device mapping
response = await llm.generate_response(
    messages=[{"role": "user", "content": "Hello"}],
    device_map="cpu"  # Force CPU inference
)

# Control memory usage
response = await llm.generate_response(
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=512,  # Limit response length
    torch_dtype="auto"  # Automatic precision selection
)
```

### Generation Parameters
Customize response generation:
```python
# Creative writing
response = await llm.generate_response(
    messages=[{"role": "user", "content": "Write a story"}],
    temperature=0.9,  # More creative
    top_p=0.95
)

# Factual responses
response = await llm.generate_response(
    messages=[{"role": "user", "content": "Explain TCP/IP"}],
    temperature=0.2,  # More focused
    top_p=0.1
)
```

## Example Use Cases

### Chat Application
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]
response = await llm.generate_response(messages)
```

### Code Generation
```python
messages = [
    {"role": "system", "content": "You are a Python expert."},
    {"role": "user", "content": "Write a function to calculate Fibonacci numbers."}
]
response = await llm.generate_response(
    messages,
    temperature=0.2  # Lower temperature for code generation
)
```

## Best Practices

1. **Resource Management**
   - Monitor system memory usage
   - Use appropriate model size for your hardware
   - Consider CPU fallback for large models

2. **Performance Optimization**
   - Use GPU acceleration when available
   - Adjust batch sizes based on memory constraints
   - Cache frequently used responses

3. **Error Handling**
   - Implement proper validation of model files
   - Handle out-of-memory scenarios gracefully
   - Monitor model performance and errors

## Troubleshooting

Common issues and solutions:

1. **Out of Memory Errors**
   - Switch to a smaller model
   - Use CPU fallback
   - Reduce batch size or context length

2. **Missing Model Files**
   - Verify model path in environment variables
   - Check file permissions
   - Ensure all required model files are present

3. **Poor Performance**
   - Check GPU utilization
   - Monitor system resources
   - Adjust generation parameters

## Reference
For implementation details, see: `src/llm/providers/llama.py`

For more information, refer to:
- [Llama Model Documentation](https://ai.meta.com/llama/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- [PyTorch Documentation](https://pytorch.org/docs/)
