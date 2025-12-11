from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from .services import RAGService
from .session_manager import session_manager, ChatMessage
from .rate_limiter import rate_limiter, RATE_LIMITS
from .validation import ValidatedChatRequest, ValidatedSearchRequest, ValidatedFeedbackRequest
import uuid
from datetime import datetime

router = APIRouter()

# Pydantic models for request/response
# Using validated models
ChatRequest = ValidatedChatRequest

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]
    session_id: str
    timestamp: datetime

class SessionRequest(BaseModel):
    user_id: Optional[str] = None
    initial_message: str

class SessionResponse(BaseModel):
    session_id: str
    created_at: datetime
    initial_response: str

class HistoryResponse(BaseModel):
    session_id: str
    messages: List[Dict[str, Any]]

# Using validated model
SearchRequest = ValidatedSearchRequest

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]

# Using validated model
FeedbackRequest = ValidatedFeedbackRequest

class FeedbackResponse(BaseModel):
    status: str
    timestamp: datetime

# Initialize RAG service
rag_service = RAGService()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest, request: Request):
    try:
        # Rate limiting: Get client IP for unauthenticated requests
        client_ip = request.client.host
        user_id = chat_request.session_id or client_ip  # Use session ID if available, otherwise IP

        # Check if the request is allowed based on rate limits
        if not rate_limiter.is_allowed(
            user_id,
            RATE_LIMITS["unauthenticated"]["limit"],
            RATE_LIMITS["unauthenticated"]["window"]
        ):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        # Get or create session
        if chat_request.session_id:
            session = session_manager.get_session(chat_request.session_id)
            if not session:
                # If session doesn't exist, create a new one
                session = session_manager.create_session()
        else:
            session = session_manager.create_session()

        # Add user message to session
        user_message = ChatMessage(
            id=str(uuid.uuid4()),
            role="user",
            content=chat_request.message,
            timestamp=datetime.utcnow().timestamp()
        )
        session_manager.add_message_to_session(session.id, user_message)

        # Process the query with RAG service
        result = rag_service.process_query(
            query=chat_request.message,
            current_page=chat_request.context.get("current_page") if chat_request.context else None
        )

        # Add assistant message to session
        assistant_message = ChatMessage(
            id=str(uuid.uuid4()),
            role="assistant",
            content=result["response"],
            timestamp=datetime.utcnow().timestamp(),
            sources=result["sources"]
        )
        session_manager.add_message_to_session(session.id, assistant_message)

        return ChatResponse(
            response=result["response"],
            sources=result["sources"],
            session_id=session.id,
            timestamp=datetime.utcnow()
        )
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@router.post("/chat/session", response_model=SessionResponse)
async def create_session(session_request: SessionRequest):
    try:
        # Create a new session with the initial message
        session = session_manager.create_session(
            user_id=session_request.user_id,
            initial_message=session_request.initial_message
        )

        # Process the initial message
        result = rag_service.process_query(
            query=session_request.initial_message
        )

        # Add initial messages to the session
        user_message = ChatMessage(
            id=str(uuid.uuid4()),
            role="user",
            content=session_request.initial_message,
            timestamp=datetime.utcnow().timestamp()
        )
        session_manager.add_message_to_session(session.id, user_message)

        assistant_message = ChatMessage(
            id=str(uuid.uuid4()),
            role="assistant",
            content=result["response"],
            timestamp=datetime.utcnow().timestamp(),
            sources=result["sources"]
        )
        session_manager.add_message_to_session(session.id, assistant_message)

        return SessionResponse(
            session_id=session.id,
            created_at=datetime.fromtimestamp(session.created_at),
            initial_response=result["response"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")

@router.get("/chat/session/{session_id}/history", response_model=HistoryResponse)
async def get_chat_history(session_id: str, limit: int = 10, offset: int = 0):
    try:
        # Get the session
        session = session_manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Get messages from the session
        messages = session_manager.get_session_history(session_id, limit, offset)
        if messages is None:
            messages = []

        # Format messages for response
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "timestamp": datetime.fromtimestamp(msg.timestamp).isoformat(),
                "sources": msg.sources
            })

        return HistoryResponse(
            session_id=session_id,
            messages=formatted_messages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chat history: {str(e)}")

@router.post("/search", response_model=SearchResponse)
async def search_endpoint(search_request: SearchRequest, request: Request):
    try:
        # Rate limiting for search endpoint
        client_ip = request.client.host
        user_id = client_ip  # Use IP for rate limiting on search

        # Check if the request is allowed based on search rate limits
        if not rate_limiter.is_allowed(
            user_id,
            RATE_LIMITS["search"]["limit"],
            RATE_LIMITS["search"]["window"]
        ):
            raise HTTPException(status_code=429, detail="Search rate limit exceeded")

        # Use RAG service to search documents
        results = rag_service.search_documents(
            query=search_request.query,
            limit=search_request.limit
        )

        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result["metadata"].get("title", "Unknown"),
                "content": result["content"][:300] + "..." if len(result["content"]) > 300 else result["content"],  # Truncate for display
                "url": result["metadata"].get("url", ""),
                "relevance_score": result["score"]
            })

        return SearchResponse(results=formatted_results)
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing search: {str(e)}")

@router.post("/feedback", response_model=FeedbackResponse)
async def feedback_endpoint(feedback_request: FeedbackRequest, request: Request):
    try:
        # Rate limiting for feedback endpoint
        client_ip = request.client.host
        user_id = feedback_request.session_id or client_ip  # Use session ID if available, otherwise IP

        # Apply a moderate rate limit for feedback
        if not rate_limiter.is_allowed(user_id, 50, 3600):  # 50 feedbacks per hour
            raise HTTPException(status_code=429, detail="Feedback rate limit exceeded")

        # In a real implementation, this would store feedback in a database
        # For now, just return a success response
        return FeedbackResponse(
            status="feedback recorded",
            timestamp=datetime.utcnow()
        )
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recording feedback: {str(e)}")