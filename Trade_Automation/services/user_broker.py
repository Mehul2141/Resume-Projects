from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserBroker, Broker
import uuid

async def save_user_broker(
    db: AsyncSession,
    user_id: uuid.UUID,
    broker_name: str,
    client_code: str,
    jwt_token: str,
    refresh_token: str,
    feed_token: str,
    expires_at,
    created_at,
):
    # Get broker id from broker_name
    result = await db.execute(select(Broker).where(Broker.name == broker_name))
    broker = result.scalar_one_or_none()

    if not broker:
        # Optionally create broker if not found, or raise error
        raise ValueError(f"Broker '{broker_name}' not found")

    # Check if UserBroker already exists for this user and broker
    result = await db.execute(
        select(UserBroker).where(
            (UserBroker.user_id == user_id) & (UserBroker.broker_id == broker.broker_id)
        )
    )
    user_broker = result.scalar_one_or_none()

    if user_broker:
        # Update existing tokens and expiry
        user_broker.client_code = client_code
        user_broker.jwt_token = jwt_token
        user_broker.refresh_token = refresh_token
        user_broker.feed_token = feed_token
        user_broker.expires_at = expires_at
        user_broker.created_at = created_at
    else:
        # Create new UserBroker entry
        user_broker = UserBroker(
            user_id=user_id,
            broker_id=broker.broker_id,
            client_code=client_code,
            jwt_token=jwt_token,
            refresh_token=refresh_token,
            feed_token=feed_token,
            expires_at=expires_at,
            created_at=created_at,
        )
        db.add(user_broker)

    await db.commit()
    await db.refresh(user_broker)

    return user_broker

