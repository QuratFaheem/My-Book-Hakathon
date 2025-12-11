import time
from typing import Dict
from collections import defaultdict
from fastapi import HTTPException

class RateLimiter:
    def __init__(self):
        # Store request times for each identifier (IP or user ID)
        self.requests: Dict[str, list] = defaultdict(list)
        
    def is_allowed(self, identifier: str, limit: int, window: int) -> bool:
        """
        Check if a request is allowed based on rate limits
        :param identifier: Unique identifier (IP address or user ID)
        :param limit: Max number of requests
        :param window: Time window in seconds
        :return: True if allowed, False otherwise
        """
        current_time = time.time()
        
        # Remove requests older than the time window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if current_time - req_time < window
        ]
        
        # Check if we're under the limit
        if len(self.requests[identifier]) < limit:
            self.requests[identifier].append(current_time)
            return True
        
        return False

# Predefined rate limits
RATE_LIMITS = {
    "unauthenticated": {"limit": 10, "window": 60},  # 10 requests per minute
    "authenticated": {"limit": 100, "window": 60},   # 100 requests per minute
    "search": {"limit": 20, "window": 60}            # 20 search requests per minute
}

# Global rate limiter instance
rate_limiter = RateLimiter()