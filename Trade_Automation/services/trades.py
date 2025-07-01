from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Trade
from typing import List

async def get_trades(user_id: str, db: AsyncSession) -> List[Trade]:
    result = await db.execute(select(Trade).filter(Trade.user_id == user_id))
    trades = result.scalars().all()
    return trades


# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select, func, case
# from typing import List

# from models import Trade  # your ORM trade model
# from schemas.trade import Trade, TradeStatsResponse, TradeListResponse

# async def get_user_trades(db: AsyncSession, user_id: int, limit: int, offset: int) -> List[Trade]:
#     query = select(Trade).where(Trade.user_id == user_id).order_by(Trade.trade_date.desc()).limit(limit).offset(offset)
#     result = await db.execute(query)
#     trades = result.scalars().all()
#     return trades

# async def get_trade_stats(db: AsyncSession, user_id: int) -> TradeStatsResponse:
#     # Aggregate stats from trades table for the user
#     total_trades_query = select(func.count(Trade.trade_id)).where(Trade.user_id == user_id)
#     total_trades_res = await db.execute(total_trades_query)
#     total_trades = total_trades_res.scalar() or 0

#     if total_trades == 0:
#         return TradeStatsResponse(
#             total_trades=0,
#             win_rate=0.0,
#             total_pnl=0.0,
#             avg_win=0.0,
#             avg_loss=0.0
#         )
    
#     # Win trades count
#     win_trades_query = select(func.count(Trade.trade_id)).where(Trade.user_id == user_id, Trade.profit_loss > 0, Trade.status == "Close")
#     win_trades_res = await db.execute(win_trades_query)
#     win_trades = win_trades_res.scalar() or 0

#     # Total pnl sum
#     total_pnl_query = select(func.sum(Trade.profit_loss)).where(Trade.user_id == user_id)
#     total_pnl_res = await db.execute(total_pnl_query)
#     total_pnl = total_pnl_res.scalar() or 0.0

#     # Avg win (avg pnl where pnl > 0)
#     avg_win_query = select(func.avg(Trade.profit_loss)).where(Trade.user_id == user_id, Trade.profit_loss > 0)
#     avg_win_res = await db.execute(avg_win_query)
#     avg_win = avg_win_res.scalar() or 0.0

#     # Avg loss (avg pnl where pnl < 0)
#     avg_loss_query = select(func.avg(Trade.pnl)).where(Trade.user_id == user_id, Trade.profit_loss < 0)
#     avg_loss_res = await db.execute(avg_loss_query)
#     avg_loss = avg_loss_res.scalar() or 0.0

#     win_rate = (win_trades / total_trades) * 100

#     return TradeStatsResponse(
#         total_trades=total_trades,
#         win_rate=round(win_rate, 2),
#         total_pnl=round(total_pnl, 2),
#         avg_win=round(avg_win, 2),
#         avg_loss=round(avg_loss, 2)
#     )

# async def get_user_trades_with_stats(db: AsyncSession, user_id: int, limit: int, offset: int) -> TradeListResponse:
#     trades = await get_user_trades(db, user_id, limit, offset)
#     stats = await get_trade_stats(db, user_id)
#     return TradeListResponse(
#         trades=trades,
#         stats=stats,
#         limit=limit,
#         offset=offset
#     )
