from sqlalchemy import (
    Column, String, Integer, ForeignKey, DateTime, Text, DECIMAL, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from core.database import Base
import datetime
import uuid

class Strategy(Base):
    __tablename__ = 'strategies'

    strategy_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_name = Column(String)
    description = Column(Text)
    win_rate = Column(DECIMAL)
    risk_to_reward = Column(DECIMAL)
    minimum_capital = Column(DECIMAL)
    plan_id = Column(UUID(as_uuid=True), ForeignKey('subscription_plans.plan_id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    plan = relationship("SubscriptionPlan", back_populates="strategies")
    users = relationship("UserStrategy", back_populates="strategy")