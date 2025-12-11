from pydantic import BaseModel, validator
from typing import Optional
import re

class ValidatedChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    context: Optional[dict] = None
    
    @validator('message')
    def validate_message(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Message cannot be empty')
        if len(v) > 1000:  # Limit message length
            raise ValueError('Message too long, must be under 1000 characters')
        return v.strip()
    
    @validator('session_id', pre=True)
    def validate_session_id(cls, v):
        if v is None:
            return v
        # Basic validation for session ID format
        if not re.match(r'^[a-zA-Z0-9-_]+$', v):
            raise ValueError('Invalid session ID format')
        return v

class ValidatedSearchRequest(BaseModel):
    query: str
    filters: Optional[dict] = None
    limit: int = 5
    
    @validator('query')
    def validate_query(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Query cannot be empty')
        if len(v) > 500:  # Limit query length
            raise ValueError('Query too long, must be under 500 characters')
        return v.strip()
    
    @validator('limit')
    def validate_limit(cls, v):
        if v < 1:
            raise ValueError('Limit must be at least 1')
        if v > 50:  # Maximum limit
            raise ValueError('Limit cannot exceed 50')
        return v

class ValidatedFeedbackRequest(BaseModel):
    session_id: str
    message_id: str
    rating: int  # 1 for positive, -1 for negative, 0 for neutral
    comment: Optional[str] = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if v not in [-1, 0, 1]:
            raise ValueError('Rating must be -1, 0, or 1')
        return v
    
    @validator('session_id', 'message_id')
    def validate_ids(cls, v):
        if not re.match(r'^[a-zA-Z0-9-_]+$', v):
            raise ValueError('Invalid ID format')
        return v