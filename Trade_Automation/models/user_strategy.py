from sqlalchemy import (
    Column, String, Integer, ForeignKey, DateTime, Text, DECIMAL, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from core.database import Base
import datetime
import uuid

class UserStrategy(Base):
    __tablename__ = 'user_strategies'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), primary_key=True)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('strategies.strategy_id'), primary_key=True)
    strategy_status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="strategies")
    strategy = relationship("Strategy", back_populates="users")