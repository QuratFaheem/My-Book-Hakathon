import os
import re
from pathlib import Path
from typing import List, Dict, Any
from .models import Document
from .services import RAGService

class ContentLoader:
    def __init__(self, docs_path: str, rag_service: RAGService):
        self.docs_path = Path(docs_path)
        self.rag_service = rag_service
    
    def extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extract frontmatter from markdown content"""
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            # Simple parsing of frontmatter (in real app, use proper YAML parser)
            result = {}
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    result[key.strip()] = value.strip().strip('"\'')
            return result
        return {}
    
    def load_documents(self) -> List[Dict[str, Any]]:
        """Load all markdown documents from the docs directory"""
        documents = []
        
        for md_file in self.docs_path.rglob("*.md"):
            relative_path = md_file.relative_to(self.docs_path)
            url_path = f"/docs/{relative_path.parent}/{relative_path.stem}"
            
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract frontmatter if present
            frontmatter = self.extract_frontmatter(content)
            
            # Remove frontmatter from content
            content_without_frontmatter = re.sub(r'^---\n(.*?)\n---', '', content, 1, re.DOTALL).strip()
            
            # Create document metadata
            doc_metadata = {
                "title": frontmatter.get('title', relative_path.stem.replace('-', ' ').title()),
                "url": url_path,
                "source_file": str(md_file),
                "relative_path": str(relative_path)
            }
            
            documents.append({
                "id": str(md_file),
                "content": content_without_frontmatter,
                "metadata": doc_metadata
            })
        
        return documents
    
    def process_and_store(self):
        """Process all documents and store in the RAG system"""
        documents = self.load_documents()
        
        for doc in documents:
            self.rag_service.add_document(
                doc_id=doc["id"],
                content=doc["content"],
                metadata=doc["metadata"]
            )
        
        print(f"Processed and stored {len(documents)} documents in the RAG system.")

# Example usage
if __name__ == "__main__":
    rag_service = RAGService()
    loader = ContentLoader("../../docs", rag_service)
    loader.process_and_store()