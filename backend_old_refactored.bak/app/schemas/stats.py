"""
Pydantic schemas for stats endpoints
"""

from pydantic import BaseModel


class StatsResponse(BaseModel):
    model_accuracy: float
    champions_analyzed: int
    training_matches: int
