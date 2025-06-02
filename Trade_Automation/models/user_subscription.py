from sqlalchemy import (
    Column, String, Integer, ForeignKey, DateTime, Text, DECIMAL, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from core.database import Base
import datetime
import uuid

class UserSubscription(Base):
    __tablename__ = 'user_subscriptions'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), primary_key=True)
    plan_id = Column(UUID(as_uuid=True), ForeignKey('subscription_plans.plan_id'), primary_key=True)
    subscribed_at = Column(DateTime)
    expires_at = Column(DateTime)

    user = relationship("User", back_populates="subscriptions")
    plan = relationship("SubscriptionPlan", back_populates="subscriptions")