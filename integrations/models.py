from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func
from app.database import Base

class OutreachLog(Base):
    __tablename__ = "outreach_logs"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, index=True)
    outreach_type = Column(String)  # email, sms, call
    message = Column(String)
    status = Column(String, default="pending")  # pending, sent, opened, clicked, replied
    response = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class VoiceSession(Base):
    __tablename__ = "voice_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True)
    command = Column(String)
    response = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
