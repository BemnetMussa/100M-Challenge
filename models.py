from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, index=True)
    user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True)
    properties = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
