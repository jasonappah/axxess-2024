from datetime import datetime
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel
from uuid import uuid4 as uuid
from api.utils.factories import id_factory, now_factory
from api.public.user.models import User

class ChatRole(str, Enum):
    USER = "USER"
    SYSTEM = "SYSTEM"
    ASSISTANT = "ASSISTANT"


class ChatSession(SQLModel, table=True):
    id: str | None = Field(default_factory=id_factory, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="chat_sessions")
    created_at: datetime | None = Field(default_factory=now_factory)
    chat_messages: list["ChatMessage"] = Relationship(back_populates="chat_session")

class ChatSessionRead(SQLModel):
    id: str
    created_at: datetime

class ChatMessageBase(SQLModel):
    id: str | None = Field(default_factory=id_factory, primary_key=True)
    chat_session_id: str = Field(foreign_key="chat_session.id")
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime | None = Field(default_factory=now_factory)
    chat_role: ChatRole
    message: str


class ChatMessage(ChatMessageBase, table=True):
    user: User = Relationship(back_populates="chat_messages")
    chat_session: ChatSession = Relationship(back_populates="chat_messages")


