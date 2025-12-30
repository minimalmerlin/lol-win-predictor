"""
Pydantic schemas for item recommendation endpoints
"""

from pydantic import BaseModel, Field
from typing import List, Dict


class ItemRecommendationRequest(BaseModel):
    champion: str = Field(..., example="MissFortune")
    enemy_team: List[str] = Field(..., min_items=1, max_items=5, example=["Zed", "Malphite", "Leona", "Caitlyn", "Lux"])
    top_n: int = Field(5, ge=1, le=10, example=5)


class ItemRecommendationResponse(BaseModel):
    champion: str
    recommended_items: List[Dict]
    popular_builds: List[Dict]


class DynamicBuildRequest(BaseModel):
    user_champion: str
    user_role: str  # Top, Jungle, Mid, ADC, Support
    ally_champions: List[str] = Field(..., min_length=4, max_length=4)
    ally_roles: List[str] = Field(..., min_length=4, max_length=4)
    enemy_champions: List[str] = Field(..., min_length=5, max_length=5)
    enemy_roles: List[str] = Field(..., min_length=5, max_length=5)
    game_state: str = Field(default="even", pattern="^(leading|even|losing)$")
