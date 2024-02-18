from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from api.database import Session, get_session
from api.public.user.crud import read_user_by_id, read_patients, insert_user
from api.public.user.models import UserCreate, UserReadWithPrescriptions
from api.utils.logger import logger_config

router = APIRouter()
logger = logger_config(__name__)


@router.get(
    "/patients",
    response_model=list[UserReadWithPrescriptions],
    status_code=status.HTTP_200_OK,
)
def get_patients(db: Session = Depends(get_session)):
    return read_patients(db=db)


@router.get(
    "/{user_id}",
    response_model=UserReadWithPrescriptions,
    status_code=status.HTTP_200_OK,
)
def get_user_by_id(user_id: str, db: Session = Depends(get_session)):
    return read_user_by_id(user_id=user_id, db=db)

@router.post(
    "/{user_id}",
    response_model=UserReadWithPrescriptions,
    status_code=status.HTTP_200_OK,
)
def create_user(user_create: UserCreate, db: Session = Depends(get_session)):
    return insert_user(user_create=user_create, db=db)