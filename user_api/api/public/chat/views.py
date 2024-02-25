from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from api.database import Session, get_session
from api.public.chat.crud import ChatMessageResponse, find_session_by_id, message
from api.public.chat.models import (
    ChatMessageBase,
    ChatSession,
)
from api.utils.logger import logger_config

router = APIRouter()
logger = logger_config(__name__)


@router.get(
    "/sessions/{session_id}",
    response_model=ChatSession,
    status_code=status.HTTP_200_OK,
)
def get_session_by_id(session_id: str, db: Session = Depends(get_session)):
    return find_session_by_id(session_id=session_id, db=db)


@router.get(
    "/sessions",
    response_model=list[ChatSession],
    status_code=status.HTTP_200_OK,
)
def get_sessions(db: Session = Depends(get_session)):
    return db.exec(select(ChatSession)).all()


@router.post(
    "/message",
    response_model=ChatMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    m: ChatMessageBase,
    user_id: str,
    db: Session = Depends(get_session),
):
    return message(m, user_id, db)
