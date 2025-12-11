# Physical AI & Humanoid Robotics Textbook

## Overview

This is an educational resource for learning Physical AI and Humanoid Robotics. It includes comprehensive textbook content with 10-12 chapters covering fundamental to advanced topics, and an integrated RAG (Retrieval Augmented Generation) chatbot that can answer questions about the content.

## Features

- Comprehensive textbook on Physical AI & Humanoid Robotics
- Interactive RAG chatbot for answering questions about the content
- Responsive design for all device types
- User authentication and personalization
- Content translation (Urdu and other languages)
- Progress tracking and recommendations

## Tech Stack

- **Frontend**: Docusaurus (React-based static site generator)
- **Backend**: FastAPI (Python web framework)
- **Database**: PostgreSQL
- **Vector Database**: Qdrant
- **LLM Integration**: OpenAI API
- **Authentication**: JWT-based
- **Deployment**: Docker, GitHub Pages (frontend), cloud platform (backend)

## Installation & Setup

### Prerequisites

- Node.js v18.x or higher
- Python 3.11 or higher
- Docker (optional, for containerized deployment)

### Frontend Setup

1. Install dependencies:
   ```bash
   cd [project-root]
   npm install
   ```

2. Run the development server:
   ```bash
   npm run start
   ```

### Backend Setup

1. Create a Python virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. Initialize the RAG content:
   ```bash
   python initialize_content.py
   ```

5. Run the backend server:
   ```bash
   uvicorn src.main:app --reload
   ```

## Deployment

### Frontend (Docusaurus)

The frontend can be built and deployed to GitHub Pages or any static hosting service:

```bash
npm run build
```

This creates a `build/` directory with the static site that can be deployed.

### Backend (FastAPI)

The backend can be deployed using various cloud platforms. A Dockerfile is provided for containerized deployment:

```bash
# Build the Docker image
docker build -t textbook-backend .

# Run the container
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here textbook-backend
```

## Environment Variables

The application requires the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key for LLM functionality
- `QDRANT_URL`: URL for your Qdrant vector database instance
- `DATABASE_URL`: Connection string for PostgreSQL database
- `SECRET_KEY`: Secret key for JWT token generation

## API Endpoints

### RAG Chatbot API

- `POST /api/chat` - Submit a message to the chatbot
- `POST /api/chat/session` - Start a new chat session
- `GET /api/chat/session/{session_id}/history` - Get chat history
- `POST /api/search` - Search textbook content
- `POST /api/feedback` - Submit feedback about responses

### Authentication API

- `POST /api/token` - Login and get access token
- `GET /api/users/me` - Get current user info

### Bonus Features API

- `POST /api/preferences` - Set user preferences
- `GET /api/recommendations` - Get personalized recommendations
- `POST /api/translate` - Translate content

## Architecture

The application follows a micro-frontend architecture:

- **Frontend**: Docusaurus-based static site with interactive components
- **Backend**: FastAPI-based API server handling RAG functionality, user management, and other services
- **Data**: PostgreSQL for structured data, Qdrant for vector storage of textbook content

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.