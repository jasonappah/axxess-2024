from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from api.database import Session, get_session
from api.public.user.crud import read_user_by_id, read_patients, insert_user
from api.public.user.models import User
from api.utils.logger import logger_config

router = APIRouter()
logger = logger_config(__name__)


@router.get(
    "/patients",
    response_model=list[User],
    status_code=status.HTTP_200_OK,
)
def get_patients(db: Session = Depends(get_session)):
    return read_patients(db=db)


@router.get(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
def get_user_by_id(user_id: str, db: Session = Depends(get_session)):
    return read_user_by_id(user_id=user_id, db=db)

@router.post(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
def create_user(user: User, db: Session = Depends(get_session)):
    return insert_user(user=user, db=db)