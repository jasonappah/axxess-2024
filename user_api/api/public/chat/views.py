from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from api.database import Session, get_session
from api.public.chat.crud import find_session_by_id
from api.public.chat.models import ChatSession, ChatSessionRead
from api.utils.logger import logger_config

router = APIRouter()
logger = logger_config(__name__)


@router.get(
    "/session/{session_id}",
    response_model=ChatSessionRead,
    status_code=status.HTTP_200_OK,
)
def get_session_by_id(session_id: str, db: Session = Depends(get_session)):
    return find_session_by_id(session_id=session_id, db=db)


@router.get(
    "/sessions",
    response_model=list[ChatSessionRead],
    status_code=status.HTTP_200_OK,
)
def get_sessions(db: Session = Depends(get_session)):
    return db.exec(select(ChatSession)).all()
