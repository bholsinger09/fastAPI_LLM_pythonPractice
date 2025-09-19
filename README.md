# FastAPI + LLM Python Practice

A comprehensive FastAPI application integrated with Large Language Models (LLMs) for learning and experimentation purposes.

## 🚀 Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **OpenAI Integration**: Chat completions, text generation, and streaming responses
- **Rate Limiting**: Built-in rate limiting to prevent API abuse
- **Error Handling**: Comprehensive error handling and validation
- **Advanced Endpoints**: Text summarization, translation, and streaming responses
- **CORS Support**: Cross-origin resource sharing enabled
- **Environment Configuration**: Secure API key management with environment variables

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key (get from [OpenAI Platform](https://platform.openai.com/api-keys))

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bholsinger09/fastAPI_LLM_pythonPractice.git
   cd fastAPI_LLM_pythonPractice
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_actual_api_key_here
   ```

## 🚀 Running the Application

Start the development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📖 API Endpoints

### Basic Endpoints

#### Health Check
- **GET** `/` - Root endpoint
- **GET** `/health` - Health check

#### Chat Completions
- **POST** `/chat` - Simple chat completion
- **POST** `/text` - Text completion (legacy models)
- **POST** `/conversation` - Chat with conversation history

### Advanced Endpoints

#### Streaming
- **POST** `/advanced/stream` - Streaming chat responses

#### Text Processing
- **POST** `/advanced/summarize` - Text summarization
- **POST** `/advanced/translate` - Language translation

#### Utility
- **GET** `/advanced/models` - List available models

## 💡 Usage Examples

### Simple Chat Completion

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! How are you today?",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 150
  }'
```

**Response**:
```json
{
  "response": "Hello! I'm doing well, thank you for asking. How are you doing today?",
  "model": "gpt-3.5-turbo",
  "tokens_used": 23
}
```

### Conversation with History

```bash
curl -X POST "http://localhost:8000/conversation" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What did I just ask you?",
    "conversation_history": [
      {"role": "user", "content": "Hello! How are you today?"},
      {"role": "assistant", "content": "Hello! I'\''m doing well, thank you for asking. How are you doing today?"}
    ],
    "model": "gpt-3.5-turbo"
  }'
```

### Text Summarization

```bash
curl -X POST "http://localhost:8000/advanced/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. It was created by Sebastian Ramirez and first released in 2018. FastAPI is built on top of Starlette for the web parts and Pydantic for the data parts.",
    "model": "gpt-3.5-turbo",
    "max_tokens": 100
  }'
```

### Language Translation

```bash
curl -X POST "http://localhost:8000/advanced/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you?",
    "source_language": "English",
    "target_language": "Spanish",
    "model": "gpt-3.5-turbo"
  }'
```

### Streaming Response

```bash
curl -X POST "http://localhost:8000/advanced/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me a short story",
    "model": "gpt-3.5-turbo",
    "max_tokens": 200
  }' \
  --no-buffer
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Optional |
| `API_HOST` | Server host | `0.0.0.0` |
| `API_PORT` | Server port | `8000` |
| `RATE_LIMIT` | Requests per minute | `60` |

### Model Parameters

| Parameter | Description | Range | Default |
|-----------|-------------|-------|---------|
| `temperature` | Sampling randomness | 0.0 - 2.0 | 0.7 |
| `max_tokens` | Maximum response length | 1 - 4000 | 150 |
| `model` | LLM model to use | See `/advanced/models` | `gpt-3.5-turbo` |

## 🛡️ Rate Limiting

The API includes built-in rate limiting:
- **Default**: 60 requests per minute per IP
- **Headers**: Rate limit info in response headers
- **Status Code**: 429 when limit exceeded

## 🚨 Error Handling

The API provides detailed error responses:

```json
{
  "error": "Validation Error",
  "message": "Temperature must be between 0.0 and 2.0",
  "detail": "Invalid temperature value: 3.0"
}
```

## 🏗️ Project Structure

```
fastAPI_LLM_python/
├── main.py                 # Main FastAPI application
├── llm_client.py           # LLM client implementation
├── advanced_endpoints.py   # Advanced API endpoints
├── middleware.py           # Rate limiting and error handling
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🧪 Testing

Test the API endpoints using the interactive documentation at http://localhost:8000/docs or use curl commands as shown in the examples above.

## 🔐 Security Considerations

- **API Keys**: Never commit API keys to version control
- **Rate Limiting**: Implement proper rate limiting in production
- **CORS**: Configure CORS origins for production use
- **Input Validation**: All inputs are validated using Pydantic models
- **Error Handling**: Errors don't expose sensitive information

## 🚀 Deployment

For production deployment, consider:

1. **Use a production ASGI server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   ```

2. **Set environment-specific configurations**
3. **Implement proper logging and monitoring**
4. **Use a reverse proxy (nginx)**
5. **Set up SSL/TLS certificates**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
2. Review [OpenAI API documentation](https://platform.openai.com/docs/)
3. Open an issue on GitHub

## 🎯 Learning Goals

This project helps you learn:

- FastAPI framework fundamentals
- API design and documentation
- LLM integration patterns
- Error handling and validation
- Rate limiting and middleware
- Environment configuration
- Streaming responses
- Pydantic data validation

Happy coding! 🚀