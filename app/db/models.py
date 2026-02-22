from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.db.session import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    source_chat_id = Column(String, index=True)
    source_message_id = Column(String, index=True)

    date_utc = Column(DateTime)
    text = Column(Text)
    raw_json = Column(JSON)

    content_hash = Column(String, index=True)

    status = Column(String, default="INGESTED")
    category_key = Column(String, nullable=True)
    score = Column(Integer, nullable=True)

    error = Column(Text, nullable=True)
    retries = Column(Integer, default=0)

    posted_chat_id = Column(String, nullable=True)
    posted_message_id = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())