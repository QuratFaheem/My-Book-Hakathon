from typing import Dict
import openai
from .services import RAGService

class TranslationService:
    def __init__(self, openai_client: openai.OpenAI):
        self.openai_client = openai_client
        self.supported_languages = {
            "ur": "Urdu",
            "en": "English", 
            "es": "Spanish",
            "fr": "French",
            "de": "German"
        }
    
    def translate_text(self, text: str, target_language: str = "ur", source_language: str = "en") -> str:
        """
        Translate text to the target language
        For now, this is a placeholder - in a real implementation we would use a translation API
        """
        if target_language not in self.supported_languages:
            raise ValueError(f"Language {target_language} is not supported")
        
        if source_language == target_language:
            return text
        
        # For the demo, we'll use OpenAI to perform translation
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a professional translator. Translate the following text to {self.supported_languages[target_language]}. Maintain technical accuracy for robotics and AI terminology."},
                    {"role": "user", "content": f"Translate this to {self.supported_languages[target_language]}: {text}"}
                ],
                max_tokens=len(text) * 2,  # Allow for differences in text length between languages
                temperature=0.3
            )
            
            return response.choices[0].message.content
        except Exception as e:
            # If translation fails, return original text with error note
            return f"[TRANSLATION ERROR: {str(e)}] {text}"
    
    def translate_chapter(self, chapter_content: str, target_language: str = "ur") -> str:
        """
        Translate an entire chapter, preserving structure
        """
        # This is a simplified implementation
        # In a real implementation, we would need to parse the markdown structure
        # and translate content while preserving formatting
        return self.translate_text(chapter_content, target_language)

# Global instance - will be initialized with the RAG service's OpenAI client
translation_service = None

def initialize_translation_service(rag_service: RAGService):
    global translation_service
    translation_service = TranslationService(rag_service.openai_client)