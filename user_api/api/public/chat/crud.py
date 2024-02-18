from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select
from api.database import get_session
from datetime import datetime
from api.config import settings
from api.public.chat.models import (
    ChatMessage,
    ChatMessageBase,
    ChatRole,
    ChatSession,
    ChatSession,
)
from api.utils.logger import logger_config
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


client = OpenAI(base_url=settings.OPENAI_BASE_URL, api_key=settings.OPENAI_API_KEY)


logger = logger_config(__name__)

# TODO: experiment with different system messages
SYSTEM_MESSAGE = "You are a helpful assistant."


def find_session_by_time_and_user(
    user_id: str, db: Session, dt=datetime.now(), 
) -> ChatSession:
    time_limit = dt - settings.CREATE_NEW_CHAT_SESSION_IF_LAST_MSG_OLDER_THAN
    session = db.exec(
        select(ChatSession).where(
            (ChatSession.user_id == user_id) & (ChatSession.created_at > time_limit)
        )
    ).one_or_none()
    if session:
        return session

    logger.info(f"Creating new chat session for user: {user_id}")
    s = ChatSession(user_id=user_id)
    if not s.id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate a chat session id.",
        )
    system_msg = ChatMessage(
        chat_session_id=s.id,
        chat_role=ChatRole.SYSTEM,
        message=SYSTEM_MESSAGE,
    )
    db.add(s)
    s.chat_messages.append(system_msg)
    db.commit()
    db.refresh(s)
    return find_session_by_time_and_user(user_id, db, dt)


def find_session_by_id(session_id: str, db: Session):
    session = db.get(ChatSession, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat session not found with id: {session_id}",
        )
    return session


def insert_message(msg: ChatMessageBase, user_id: str, db: Session):
    if not msg.chat_session_id:
        chat_session = find_session_by_time_and_user(user_id, db=db)
        msg.chat_session_id = chat_session.id
    else:
        chat_session = find_session_by_id(msg.chat_session_id, db)
    r = ChatMessage(**msg.model_dump())
    db.add(r)
    db.commit()
    db.refresh(chat_session)
    db.refresh(r)
    return chat_session


def chat_session_to_oai_format(
    session: ChatSession,
) -> list[ChatCompletionMessageParam]:
    role_to_name = {
        ChatRole.USER: session.user.name.split(" ")[0],
        ChatRole.SYSTEM: "Caretaker",
        ChatRole.ASSISTANT: "Gia",
    }
    messages = []
    for msg in session.chat_messages:
        messages.append(
            {
                "role": msg.chat_role,
                "content": msg.message,
                "name": role_to_name[msg.chat_role],
            }
        )
    return messages


def create_chat_completion(
    chat_session: ChatSession, db: Session
) -> ChatMessage:
    if chat_session.id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chat session does not exist (????). this should never happen haha ;))",
        )
    if chat_session.chat_messages[-1].chat_role == ChatRole.ASSISTANT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assistant has already responded to the last message in this chat session.",
        )

    messages = chat_session_to_oai_format(chat_session)
    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL_ID,
        messages=messages,
    )

    if (content := response.choices[0].message.content) is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OpenAI failed to generate a response. :(",
        )

    msg = ChatMessage(
        chat_session_id=chat_session.id,
        chat_role=ChatRole.ASSISTANT,
        message=content,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    db.refresh(chat_session)
    return msg

class ChatMessageResponse(BaseModel):
    chat_session: ChatSession
    chat_message: ChatMessage

def message(msg: ChatMessageBase, user_id: str, db: Session):
    s = insert_message(msg, user_id, db)
    response = create_chat_completion(s, db)
    return ChatMessageResponse(chat_session=s, chat_message=response)
