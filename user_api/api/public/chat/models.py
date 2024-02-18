from datetime import datetime
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel
from api.utils.factories import id_factory, now_factory

class ChatRole(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class ChatSession(SQLModel, table=True):
    id: str | None = Field(default_factory=id_factory, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="chat_sessions")
    created_at: datetime | None = Field(default_factory=now_factory)
    # TODO: need to have messages serializable on a session
    chat_messages: list["ChatMessage"] = Relationship(back_populates="chat_session")


class ChatMessageBase(SQLModel):
    id: str | None = Field(default_factory=id_factory, primary_key=True)
    chat_session_id: str | None = Field(foreign_key="chatsession.id", default=None)
    created_at: datetime | None = Field(default_factory=now_factory)
    chat_role: ChatRole
    message: str


class ChatMessage(ChatMessageBase, table=True):
    chat_session: ChatSession = Relationship(back_populates="chat_messages")
    


