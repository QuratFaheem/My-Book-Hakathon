# Physical AI & Humanoid Robotics Textbook - Backend

This is the backend service for the Physical AI & Humanoid Robotics Textbook project. It provides a RAG (Retrieval Augmented Generation) chatbot that can answer questions about the textbook content.

## Features

- FastAPI-based REST API
- Qdrant vector database for content retrieval
- OpenAI integration for generating answers
- Session management for conversations
- Rate limiting for API protection

## Setup

1. Install Python dependencies:
   ```bash
   pip install poetry
   poetry install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. Run the development server:
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

## Endpoints

- `POST /api/chat` - Submit a message to the chatbot
- `POST /api/chat/session` - Start a new chat session
- `GET /api/chat/session/{session_id}/history` - Get chat history
- `POST /api/search` - Search textbook content
- `POST /api/feedback` - Submit feedback about responses

## Architecture

The backend follows a standard FastAPI project structure:

```
backend/
├── src/
│   ├── main.py             # Application entry point
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   └── api/                # API routers
├── database/               # Database configuration
├── routers/                # API route definitions
└── tests/                  # Unit and integration tests
```