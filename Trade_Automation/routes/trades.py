from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.security import get_current_user
from schemas.trade import TradeResponse
from models import User
from services.trades import get_trades

router = APIRouter(prefix="/trades", tags=["Trades"])

@router.get("/", response_model=List[TradeResponse])
async def get_user_trades(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trades = await get_trades(current_user.user_id, db)
    return trades

