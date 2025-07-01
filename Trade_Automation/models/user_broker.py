from sqlalchemy import (
    Column, String, Integer, ForeignKey, DateTime, Text, DECIMAL, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from core.database import Base
import datetime
import uuid

class UserBroker(Base):
    __tablename__ = 'user_brokers'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), primary_key=True)
    broker_id = Column(UUID(as_uuid=True), ForeignKey('brokers.broker_id'), primary_key=True)
    client_code = Column(String,unique=True)
    feed_token = Column(Text)
    jwt_token = Column(Text)
    refresh_token = Column(Text)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="brokers")
    broker = relationship("Broker", back_populates="users")