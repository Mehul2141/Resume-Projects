from sqlalchemy import (
    Column, String, Integer, ForeignKey, DateTime, Text, DECIMAL, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from core.database import Base
import datetime
import uuid

class UserFund(Base):
    __tablename__ = 'user_funds'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), primary_key=True)
    margin_used = Column(DECIMAL)
    funds_available = Column(DECIMAL)
    last_updated = Column(DateTime)

    user = relationship("User", back_populates="funds")