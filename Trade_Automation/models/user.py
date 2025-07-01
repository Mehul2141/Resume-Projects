from sqlalchemy import (
    Column, String, Integer, ForeignKey, DateTime, Text, DECIMAL, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from core.database import Base
import datetime
import uuid


class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String)
    mobile = Column(String)
    password = Column(String)
    email = Column(String, unique=True)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    brokers = relationship("UserBroker", back_populates="user")
    trades = relationship("Trade", back_populates="user")
    funds = relationship("UserFund", back_populates="user", uselist=False)
    logs = relationship("AuditLog", back_populates="user")
    subscriptions = relationship("UserSubscription", back_populates="user")
    strategies = relationship("UserStrategy", back_populates="user")