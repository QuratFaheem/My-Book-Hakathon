import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

@dataclass
class ChatMessage:
    id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: float
    sources: Optional[List[Dict[str, Any]]] = None

@dataclass
class ChatSession:
    id: str
    user_id: Optional[str]
    created_at: float
    updated_at: float
    title: str
    messages: List[ChatMessage]
    
    def add_message(self, message: ChatMessage):
        self.messages.append(message)
        self.updated_at = time.time()

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, ChatSession] = {}
        # In a real implementation, this would connect to a database
    
    def create_session(self, user_id: Optional[str] = None, initial_message: Optional[str] = None) -> ChatSession:
        session_id = str(int(time.time() * 1000000))  # Use microsecond timestamp as ID
        title = initial_message[:50] + "..." if initial_message and len(initial_message) > 50 else "New Chat Session"
        
        session = ChatSession(
            id=session_id,
            user_id=user_id,
            created_at=time.time(),
            updated_at=time.time(),
            title=title,
            messages=[]
        )
        
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        # Clean up expired sessions (older than 24 hours)
        self._cleanup_expired_sessions()
        
        return self.sessions.get(session_id)
    
    def add_message_to_session(self, session_id: str, message: ChatMessage):
        session = self.get_session(session_id)
        if session:
            session.add_message(message)
            return session
        return None
    
    def get_session_history(self, session_id: str, limit: int = 10, offset: int = 0) -> Optional[List[ChatMessage]]:
        session = self.get_session(session_id)
        if session:
            # Return messages in reverse chronological order (most recent first)
            all_messages = session.messages
            start_idx = min(offset, len(all_messages))
            end_idx = min(offset + limit, len(all_messages))
            
            return all_messages[start_idx:end_idx]
        return None
    
    def _cleanup_expired_sessions(self):
        """Remove sessions older than 24 hours to manage memory"""
        current_time = time.time()
        expired_sessions = [
            session_id for session_id, session in self.sessions.items()
            if current_time - session.updated_at > 24 * 3600  # 24 hours in seconds
        ]
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
    
    def save_session(self, session_id: str):
        """In a real implementation, this would save to a database"""
        # Placeholder for database saving logic
        pass

# Global session manager instance
session_manager = SessionManager()