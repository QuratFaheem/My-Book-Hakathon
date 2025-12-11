import time
from functools import wraps
from typing import Callable, Any
import logging

# Set up logging for performance monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitor_performance(func: Callable) -> Callable:
    """
    Decorator to monitor the execution time of functions
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
            
            # Log if the execution time exceeds the 1-second goal
            if execution_time > 1.0:
                logger.warning(f"{func.__name__} exceeded 1-second performance goal: {execution_time:.4f}s")
    
    return wrapper

class PerformanceMonitor:
    """
    A class to monitor and track performance metrics
    """
    def __init__(self):
        self.metrics = {}
    
    def record_response_time(self, endpoint: str, response_time: float):
        """
        Record the response time for an endpoint
        """
        if endpoint not in self.metrics:
            self.metrics[endpoint] = []
        
        self.metrics[endpoint].append(response_time)
        
        # Log if response time exceeds the 1-second goal
        if response_time > 1.0:
            logger.warning(f"Endpoint {endpoint} exceeded 1-second performance goal: {response_time:.4f}s")
    
    def get_average_response_time(self, endpoint: str) -> float:
        """
        Get the average response time for an endpoint
        """
        if endpoint in self.metrics and self.metrics[endpoint]:
            return sum(self.metrics[endpoint]) / len(self.metrics[endpoint])
        return 0.0
    
    def get_slowest_response_time(self, endpoint: str) -> float:
        """
        Get the slowest response time for an endpoint
        """
        if endpoint in self.metrics and self.metrics[endpoint]:
            return max(self.metrics[endpoint])
        return 0.0

# Global performance monitor instance
perf_monitor = PerformanceMonitor()