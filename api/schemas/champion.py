"""
Pydantic schemas for champion endpoints
"""

from pydantic import BaseModel
from typing import List, Dict


class ChampionStatsResponse(BaseModel):
    champions: List[Dict]
    total_champions: int
