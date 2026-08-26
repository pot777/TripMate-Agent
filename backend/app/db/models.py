from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, JSON, String, Text
from sqlalchemy.orm import relationship

from .database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(128), primary_key=True)
    title = Column(String(200), nullable=False, default="新旅行")
    preview = Column(String(500), nullable=False, default="")
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )
    travel_state = relationship(
        "TravelStateRecord",
        back_populates="conversation",
        cascade="all, delete-orphan",
        uselist=False
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(
        String(128),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False
    )
    role = Column(String(32), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)

    conversation = relationship("Conversation", back_populates="messages")

    __table_args__ = (
        Index("ix_messages_conversation_created", "conversation_id", "created_at", "id"),
    )


class TravelStateRecord(Base):
    __tablename__ = "travel_states"

    conversation_id = Column(
        String(128),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        primary_key=True
    )
    state_json = Column(JSON, nullable=False, default=dict)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)

    conversation = relationship("Conversation", back_populates="travel_state")
