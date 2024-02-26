from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from api.database import get_session
from api.public.user.crud import DispensationStatus, mark_dispense_as_consumed, read_user_by_id, read_patients, insert_user, read_user_if_user_is_due_for_dispense, update_user, delete_user
from api.public.user.models import PillDispenseEvent, UserCreate, UserReadWithPrescriptions
from api.utils.logger import logger_config

router = APIRouter()
logger = logger_config(__name__)

@router.get(
    "/{user_id}/due_for_dispense",
    response_model=DispensationStatus,
    status_code=status.HTTP_200_OK,
)
def get_user_due_for_dispense(user_id: str, db: Session = Depends(get_session)):
    return read_user_if_user_is_due_for_dispense(user_id=user_id, db=db)

@router.post(
    "/{pill_dispense_id}/consume",
    response_model=PillDispenseEvent,
    status_code=status.HTTP_200_OK,
)
def user_consumed_pill_dispense_event(pill_dispense_id: str, db: Session = Depends(get_session)):
    return mark_dispense_as_consumed(pill_dispense_id=pill_dispense_id, db=db)

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

@router.post(
    "/update/{user_id}",
    response_model=UserReadWithPrescriptions,
    status_code=status.HTTP_200_OK,
)
def update_usr(user_id: str, user_create: UserCreate, db: Session = Depends(get_session)):
    return update_user(user_id=user_id, user=user_create, db=db)

@router.post(
    "/delete/{user_id}",
    status_code=status.HTTP_200_OK,
)
def delete_usr(user_id: str, db: Session = Depends(get_session)):
    return delete_user(user_id=user_id, db=db)