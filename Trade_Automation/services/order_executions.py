from sqlalchemy import select
from core.database import get_db
from models import UserStrategy, UserBroker, Trade  # adjust import paths
from services.brokers.angelone import get_user_angelone_client, execute_order
import asyncio

# Optional: cap parallel executions to 100 users at a time
semaphore = asyncio.Semaphore(100)

async def handle_strategy_signals(strategy_id: str, signals: list):
    db = get_db()

    # fetch users who have enabled this strategy
    result = await db.execute(
        select(UserStrategy).where(
            UserStrategy.strategy_id == strategy_id,
            UserStrategy.strategy_status == True
        )
    )
    user_strategies = result.scalars().all()

    tasks = []
    for us in user_strategies:
        user_id = us.user_id
        for signal in signals:
            tasks.append(_execute_for_user(user_id, signal))

    await asyncio.gather(*tasks)


async def _execute_for_user(user_id: str, signal):
    async with semaphore:
        db = get_db()
        try:
            result = await db.execute(select(UserBroker).where(UserBroker.user_id == user_id))
            broker = result.scalar_one_or_none()
            if not broker:
                print(f"Broker not found for user {user_id}")
                return

            angel = await get_user_angelone_client(broker)

            res = execute_order(
                user_id=user_id,
                tradingsymbol="NIFTY",
                symboltoken="26009",
                Exchange="NSE",
                transaction_type=signal.side,
                ordertype="MARKET",
                quantity="1",
                producttype="INTRADAY",
                squareof="NO",
                stoploss=str(signal.sl),
                durantion="DAY",
                order_object=angel,
            )

            if res == "order placed successfully":
                order = Trade(
                    user_id=user_id,
                    order_type=signal.side,
                    entry_price=signal.price,
                    sl=signal.sl,
                    tp=signal.tp,
                    time=signal.candle_time,
                    symbol="NIFTY",
                    quantity=1,
                    status="Open"    
                )
                db.add(order)
                await db.commit()
        except Exception as e:
            print(f"Error executing for user {user_id}: {e}")
