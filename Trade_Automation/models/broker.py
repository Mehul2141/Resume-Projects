from sqlalchemy import (
    Column, String, Integer, ForeignKey, DateTime, Text, DECIMAL, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from core.database import Base
import datetime
import uuid

class Broker(Base):
    __tablename__ = 'brokers'

    broker_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    broker_name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    users = relationship("UserBroker", back_populates="broker")