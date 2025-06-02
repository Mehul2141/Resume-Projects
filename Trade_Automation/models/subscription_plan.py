from sqlalchemy import (
    Column, String, Integer, ForeignKey, DateTime, Text, DECIMAL, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from core.database import Base
import datetime
import uuid

class SubscriptionPlan(Base):
    __tablename__ = 'subscription_plans'

    plan_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_name = Column(String)
    description = Column(Text)
    pricing = Column(DECIMAL)

    subscriptions = relationship("UserSubscription", back_populates="plan")
    strategies = relationship("Strategy", back_populates="plan")