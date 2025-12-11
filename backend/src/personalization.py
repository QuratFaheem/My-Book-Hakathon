from typing import Dict, List, Optional
from pydantic import BaseModel
import random

class UserPreferences(BaseModel):
    background: str  # "beginner", "intermediate", "expert"
    interests: List[str]
    preferred_language: str = "en"
    accessibility_needs: List[str] = []

class PersonalizationService:
    def __init__(self):
        self.user_preferences: Dict[str, UserPreferences] = {}
    
    def set_user_preferences(self, user_id: str, preferences: UserPreferences):
        """Set user preferences for personalization"""
        self.user_preferences[user_id] = preferences
    
    def get_user_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """Get user preferences"""
        return self.user_preferences.get(user_id)
    
    def adjust_content_for_user(self, user_id: str, content: str) -> str:
        """Adjust content based on user preferences"""
        preferences = self.get_user_preferences(user_id)
        if not preferences:
            return content
        
        # Adjust content based on background level
        if preferences.background == "beginner":
            # Add more explanations for beginners
            content += "\n\n*Beginner tip: Take your time to understand each concept before moving on.*"
        elif preferences.background == "expert":
            # Add advanced notes for experts
            content += "\n\n*Expert insight: Consider the implications of this concept in advanced applications.*"
        
        return content
    
    def get_personalized_recommendations(self, user_id: str, current_topic: str) -> List[Dict[str, str]]:
        """Get personalized content recommendations"""
        preferences = self.get_user_preferences(user_id)
        if not preferences:
            # Default recommendations
            return [
                {"title": "Next Chapter", "url": "/docs/next-chapter", "reason": "Sequential learning"},
                {"title": "Related Concepts", "url": "/docs/related-concepts", "reason": "Foundational knowledge"}
            ]
        
        # Generate recommendations based on user interests
        recommendations = []
        
        if "programming" in preferences.interests:
            recommendations.append({
                "title": "Programming Examples",
                "url": "/docs/programming-examples",
                "reason": "Based on your interest in programming"
            })
        
        if "hardware" in preferences.interests:
            recommendations.append({
                "title": "Hardware Implementation",
                "url": "/docs/hardware-implementation", 
                "reason": "Based on your interest in hardware"
            })
        
        # Add a default recommendation if no specific interests match
        if not recommendations:
            recommendations.append({
                "title": "Next Chapter",
                "url": "/docs/next-chapter",
                "reason": "Sequential learning"
            })
        
        return recommendations[:2]  # Limit to 2 recommendations

# Global instance
personalization_service = PersonalizationService()