# services/user_strategy.py

from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models import UserStrategy
from schemas.user_strategies import UserStrategyUpdate

async def get_user_strategies_for_user(user_id: UUID, db: AsyncSession):
    result = await db.execute(
        select(UserStrategy)
        .where(UserStrategy.user_id == user_id)
        .options(selectinload(UserStrategy.strategy))
    )
    return result.scalars().all()


async def update_user_strategy_status(
    user_id: UUID,
    strategy_id: UUID,
    status_update: UserStrategyUpdate,
    db: AsyncSession
):
    result = await db.execute(
        select(UserStrategy)
        .where(UserStrategy.user_id == user_id, UserStrategy.strategy_id == strategy_id)
        .options(selectinload(UserStrategy.strategy))
    )
    user_strategy = result.scalar_one_or_none()

    if not user_strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")

    user_strategy.strategy_status = "active" if status_update.enable else "inactive"
    await db.commit()
    await db.refresh(user_strategy)

    return user_strategy
