from fastapi import FastAPI
from dotenv import load_dotenv
from .routers import chat, auth, bonus_features
from .performance_monitor import perf_monitor
import time

# Load environment variables
load_dotenv()

# Initialize the FastAPI app
app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook API",
    description="RAG chatbot API for the Physical AI & Humanoid Robotics Textbook",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "Physical AI & Humanoid Robotics Textbook Backend API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(chat.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(bonus_features.router, prefix="/api")

# Middleware to track response times
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    # Record performance metric
    perf_monitor.record_response_time(request.url.path, process_time)

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)