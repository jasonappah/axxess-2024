from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from api.database import get_session
from datetime import datetime
from api.config import settings
from api.public.user.models import ChatMessageBase, ChatSessionRead, Prescription, User, UserCreate, UserRole, ChatMessage, ChatSession
from api.utils.logger import logger_config

logger = logger_config(__name__)


def read_patients(db: Session = Depends(get_session)):
    patients = db.exec(select(User).where(User.role == UserRole.PATIENT)).all()
    return patients


def read_user_by_id(user_id: str, db: Session = Depends(get_session)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with id: {user_id}",
        )
    return user


def insert_user(user_create: UserCreate, db: Session = Depends(get_session)):
    user = User(**user_create.model_dump(exclude={"prescriptions",}))
    for p in user_create.prescriptions:
        prescription = Prescription(**p)
        user.prescriptions.append(prescription)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def read_messages_by_user(user_id: str, db: Session = Depends(get_session)):
    messages = db.exec(select(ChatMessage).where(User.id == user_id)).all()
    return messages


def find_session_by_time_and_user(user_id: str, dt = datetime.now(),
                                  db: Session = Depends(get_session)) -> ChatSessionRead:
    time_limit = dt - settings.CREATE_NEW_CHAT_SESSION_AFTER
    session = db.exec(
        select(ChatSessionRead).where(
            (ChatSessionRead.user_id == user_id) & (ChatSessionRead.created_at > time_limit)
        )
    ).one_or_none()
    if session:
        return session

    logger.info(f"Creating new chat session for user: {user_id}")
    s = ChatSession(user_id=user_id)
    db.add(s)
    db.commit()
    db.refresh(s)
    return find_session_by_time_and_user(user_id, dt, db)

def find_session_by_id(session_id: str, db: Session = Depends(get_session)):
    session = db.get(ChatSessionRead, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat session not found with id: {session_id}",
        )
    return session

def insert_message(msg: ChatMessageBase, db: Session = Depends(get_session)):
    if not msg.chat_session_id:
        chat_session = find_session_by_time_and_user(msg.user_id, db=db)
        msg.chat_session_id = chat_session.id
    else:
        chat_session = find_session_by_id(msg.chat_session_id, db)
    db.add(msg)
    db.commit()
    db.refresh(chat_session)
    db.refresh(msg)
    return msg

