import os
from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import OpenAI
from dotenv import load_dotenv
from .models import Document
from sqlalchemy.orm import Session
from .translation import initialize_translation_service

load_dotenv()

class RAGService:
    def __init__(self):
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL", "http://localhost:6333")
        )

        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Create collection in Qdrant if it doesn't exist
        try:
            self.qdrant_client.get_collection("textbook_content")
        except:
            self.qdrant_client.create_collection(
                collection_name="textbook_content",
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )

        # Initialize translation service
        initialize_translation_service(self)
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embeddings for text using OpenAI"""
        response = self.openai_client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding
    
    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any]):
        """Add a document to the vector database"""
        embedding = self.embed_text(content)
        
        self.qdrant_client.upsert(
            collection_name="textbook_content",
            points=[
                models.PointStruct(
                    id=doc_id,
                    vector=embedding,
                    payload={
                        "content": content,
                        "metadata": metadata
                    }
                )
            ]
        )
    
    def search_documents(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant documents based on query"""
        query_embedding = self.embed_text(query)
        
        search_results = self.qdrant_client.search(
            collection_name="textbook_content",
            query_vector=query_embedding,
            limit=limit
        )
        
        results = []
        for result in search_results:
            results.append({
                "id": result.id,
                "content": result.payload["content"],
                "metadata": result.payload["metadata"],
                "score": result.score
            })
        
        return results
    
    def generate_response(self, query: str, context: List[Dict[str, Any]], current_page: Optional[str] = None) -> str:
        """Generate a response using OpenAI with the provided context"""
        # Format context for the LLM
        context_text = "\n\n".join([doc["content"] for doc in context])
        
        # Create a prompt with the context
        prompt = f"""
        You are an assistant for the Physical AI & Humanoid Robotics Textbook. 
        Answer the user's question based on the provided context from the textbook.
        If the answer is not available in the provided context, inform the user that 
        the information is not in the current context.
        
        Context:
        {context_text}
        
        User's question: {query}
        
        Please provide an accurate answer based on the context provided.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # or gpt-4 if preferred
            messages=[
                {"role": "system", "content": "You are an educational assistant for the Physical AI & Humanoid Robotics Textbook. Provide accurate, helpful answers based only on the context provided."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def process_query(self, query: str, current_page: Optional[str] = None, limit: int = 5) -> Dict[str, Any]:
        """Process a user query and return response with sources"""
        # Search for relevant documents
        search_results = self.search_documents(query, limit)
        
        # Generate response based on context
        response = self.generate_response(query, search_results, current_page)
        
        # Format sources
        sources = []
        for result in search_results:
            sources.append({
                "title": result["metadata"].get("title", "Unknown"),
                "url": result["metadata"].get("url", ""),
                "relevance_score": result["score"]
            })
        
        return {
            "response": response,
            "sources": sources,
            "context_used": [r["content"] for r in search_results]
        }

class ContentService:
    def __init__(self, db: Session):
        self.db = db
    
    def load_textbook_content(self) -> List[Document]:
        """Load all textbook content from the database"""
        # This would load from the actual textbook content
        # In a real implementation, this would read from the /docs directory
        # and potentially store in the Document table
        return []
    
    def process_textbook_for_rag(self, rag_service: RAGService):
        """Process textbook content and add to RAG system"""
        # For now, just a placeholder for how this would work
        # In reality, this would load all textbook content and add it to the RAG system
        pass