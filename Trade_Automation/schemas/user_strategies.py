from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class StrategyBase(BaseModel):
    strategy_id: UUID
    strategy_name: str
    description: Optional[str]
    win_rate: Optional[int]
    risk_to_reward: Optional[int]
    minimum_capital: int

    class Config:
        from_attributes = True

class UserStrategyOut(BaseModel):
    user_id: UUID
    strategy_status: str
    strategy: StrategyBase

    class Config:
        from_attributes = True

class GetUserStrategiesResponse(BaseModel):
    user_id: UUID
    strategies: List[UserStrategyOut]

class UserStrategyUpdate(BaseModel):
    enable: bool