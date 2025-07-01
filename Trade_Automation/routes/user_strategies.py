# routers/user_strategies.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from core.database import get_db
from models import User
from schemas.user_strategies import GetUserStrategiesResponse, UserStrategyOut, UserStrategyUpdate
from services.user_strategies import get_user_strategies_for_user, update_user_strategy_status
from core.security import get_current_user

router = APIRouter(prefix="/strategies", tags=["User Strategies"])

@router.get("/", response_model=GetUserStrategiesResponse)
async def get_user_strategies(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategies = await get_user_strategies_for_user(current_user.user_id, db)
    return GetUserStrategiesResponse(user_id=current_user.user_id, strategies=strategies)


@router.patch("/{strategy_id}/status", response_model=UserStrategyOut)
async def update_strategy_status(
    strategy_id: UUID,
    status_update: UserStrategyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_strategy = await update_user_strategy_status(
        current_user.user_id, strategy_id, status_update, db
    )
    return updated_strategy
