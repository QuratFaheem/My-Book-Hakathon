from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from .personalization import personalization_service, UserPreferences
from .translation import translation_service

router = APIRouter()

class SetPreferencesRequest(BaseModel):
    background: str  # "beginner", "intermediate", "expert"
    interests: List[str]
    preferred_language: str = "en"
    accessibility_needs: List[str] = []

class GetRecommendationsRequest(BaseModel):
    current_topic: str

class Recommendation(BaseModel):
    title: str
    url: str
    reason: str

class TranslateRequest(BaseModel):
    content: str
    target_language: str = "ur"

class TranslateResponse(BaseModel):
    translated_content: str

@router.post("/preferences")
async def set_user_preferences(
    user_id: str,  # In a real app, this would come from authentication
    preferences: SetPreferencesRequest
):
    """Set user preferences for personalization"""
    user_prefs = UserPreferences(
        background=preferences.background,
        interests=preferences.interests,
        preferred_language=preferences.preferred_language,
        accessibility_needs=preferences.accessibility_needs
    )
    
    personalization_service.set_user_preferences(user_id, user_prefs)
    return {"status": "success", "message": "Preferences updated successfully"}

@router.get("/recommendations", response_model=List[Recommendation])
async def get_recommendations(
    user_id: str,  # In a real app, this would come from authentication
    current_topic: str
):
    """Get personalized content recommendations"""
    recommendations = personalization_service.get_personalized_recommendations(
        user_id, 
        current_topic
    )
    return recommendations

@router.post("/translate", response_model=TranslateResponse)
async def translate_content(translate_request: TranslateRequest):
    """Translate content to the requested language"""
    if not translation_service:
        raise HTTPException(
            status_code=500, 
            detail="Translation service not initialized. Check API keys."
        )
    
    try:
        translated_content = translation_service.translate_text(
            translate_request.content,
            translate_request.target_language
        )
        return TranslateResponse(translated_content=translated_content)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Translation failed: {str(e)}"
        )