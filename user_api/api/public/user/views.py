from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from api.database import Session, get_session
from api.public.user.crud import get_newest_pill_dispense_id, get_newest_user_id, mark_dispense_as_consumed, read_user_by_id, read_patients, insert_user, read_user_if_user_is_due_for_dispense
from api.public.user.models import UserCreate, UserReadWithPrescriptions
from api.utils.logger import logger_config
from api.config import settings

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


@router.get(
    "/{user_id}/due_for_dispense",
    response_model=list[UserReadWithPrescriptions],
    status_code=status.HTTP_200_OK,
)
def get_user_due_for_dispense(user_id: str = settings.SHOULD_GET_LATEST_RECORD_FROM_DB, db: Session = Depends(get_session)):
    user_id = get_newest_user_id(db) if user_id == settings.SHOULD_GET_LATEST_RECORD_FROM_DB else user_id
    return read_user_if_user_is_due_for_dispense(user_id=user_id, db=db)


@router.post(
    "/{pill_dispense_id}/consume",
    status_code=status.HTTP_200_OK,
)
def user_consumed_pill_dispense_event(pill_dispense_id: str = settings.SHOULD_GET_LATEST_RECORD_FROM_DB, db: Session = Depends(get_session)):
    if pill_dispense_id == settings.SHOULD_GET_LATEST_RECORD_FROM_DB:
        pill_dispense_id = get_newest_pill_dispense_id(db)
    return mark_dispense_as_consumed(pill_dispense_id=pill_dispense_id, db=db)