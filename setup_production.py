#!/bin/bash
# setup_production.py - Script to set up the application for production

import os
import sys
from pathlib import Path

def setup_production():
    print("Setting up Physical AI & Humanoid Robotics Textbook for production...")
    
    # Create necessary directories if they don't exist
    required_dirs = [
        "logs",
        "data", 
        "temp"
    ]
    
    for directory in required_dirs:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {directory}")
    
    # Check for environment variables
    required_env_vars = [
        "OPENAI_API_KEY",
        "QDRANT_URL", 
        "DATABASE_URL",
        "SECRET_KEY"
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Warning: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these in your environment or .env file before running the application.")
    
    # Initialize the content for the RAG system
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        from backend.initialize_content import initialize_rag_content
        print("Initializing RAG content...")
        initialize_rag_content()
        print("RAG content initialized successfully.")
    except ImportError as e:
        print(f"Could not import initialization module: {e}")
        print("Make sure all dependencies are installed.")
    except Exception as e:
        print(f"Error initializing RAG content: {e}")
    
    print("Production setup complete!")

if __name__ == "__main__":
    setup_production()