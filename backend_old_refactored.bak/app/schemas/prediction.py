"""
Pydantic schemas for prediction endpoints
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class ChampionMatchupRequest(BaseModel):
    blue_champions: List[str] = Field(..., min_items=1, max_items=5, example=["MissFortune", "Lux", "Braum", "Renekton", "Fizz"])
    red_champions: List[str] = Field(..., min_items=1, max_items=5, example=["Caitlyn", "Morgana", "Leona", "Darius", "Zed"])


class GameStateRequest(BaseModel):
    game_duration: int = Field(..., ge=1, le=60, example=20)
    blue_kills: int = Field(..., ge=0, example=15)
    blue_deaths: int = Field(..., ge=0, example=10)
    blue_assists: int = Field(..., ge=0, example=25)
    blue_gold: int = Field(..., ge=0, example=35000)
    blue_towers: int = Field(..., ge=0, le=11, example=4)
    blue_dragons: int = Field(..., ge=0, le=4, example=2)
    blue_barons: int = Field(..., ge=0, le=2, example=0)
    blue_vision_score: int = Field(..., ge=0, example=90)
    red_kills: int = Field(..., ge=0, example=10)
    red_deaths: int = Field(..., ge=0, example=15)
    red_assists: int = Field(..., ge=0, example=18)
    red_gold: int = Field(..., ge=0, example=30000)
    red_towers: int = Field(..., ge=0, le=11, example=2)
    red_dragons: int = Field(..., ge=0, le=4, example=1)
    red_barons: int = Field(..., ge=0, le=2, example=0)
    red_vision_score: int = Field(..., ge=0, example=75)


class GameStateV2Request(BaseModel):
    """Request model for the new Game State Predictor (79.28% accuracy)"""
    blue_gold: int = Field(..., ge=0, example=35000)
    red_gold: int = Field(..., ge=0, example=30000)
    blue_xp: int = Field(..., ge=0, example=45000)
    red_xp: int = Field(..., ge=0, example=42000)
    blue_level: int = Field(..., ge=1, le=18, example=12)
    red_level: int = Field(..., ge=1, le=18, example=11)
    blue_cs: int = Field(..., ge=0, example=350)
    red_cs: int = Field(..., ge=0, example=320)
    blue_kills: int = Field(..., ge=0, example=15)
    red_kills: int = Field(..., ge=0, example=10)
    blue_dragons: int = Field(0, ge=0, le=4, example=2)
    red_dragons: int = Field(0, ge=0, le=4, example=1)
    blue_barons: int = Field(0, ge=0, le=2, example=0)
    red_barons: int = Field(0, ge=0, le=2, example=0)
    blue_towers: int = Field(0, ge=0, le=11, example=4)
    red_towers: int = Field(0, ge=0, le=11, example=2)


class PredictionResponse(BaseModel):
    blue_win_probability: float
    red_win_probability: float
    prediction: str
    confidence: str
    details: Optional[Dict] = None
