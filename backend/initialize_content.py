import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.content_loader import ContentLoader
from src.services import RAGService

def initialize_rag_content():
    """Initialize RAG system with textbook content"""
    print("Initializing RAG system with textbook content...")
    
    # Initialize RAG service
    rag_service = RAGService()
    
    # Initialize content loader
    docs_path = os.path.join(os.path.dirname(__file__), '..', '..', 'docs')
    loader = ContentLoader(docs_path, rag_service)
    
    # Process and store all documents
    loader.process_and_store()
    
    print("RAG system initialization complete!")

if __name__ == "__main__":
    initialize_rag_content()