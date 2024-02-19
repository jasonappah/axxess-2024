from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session, select

from api.database import Session, get_session
from api.public.user.crud import get_newest_pill_dispense_id, get_newest_user_id, mark_dispense_as_consumed, read_user_by_id, read_patients, insert_user, read_user_if_user_is_due_for_dispense, update_user, delete_user
from api.public.user.models import PillDispenseEvent, Prescription, UserCreate, UserReadWithPrescriptions
from api.utils.logger import logger_config
from api.config import settings

router = APIRouter()
logger = logger_config(__name__)

lol = 2

# @router.get(
#     "/{user_id}/due_for_dispense",
#     response_model=list[UserReadWithPrescriptions],
#     status_code=status.HTTP_200_OK,
# )
# def get_user_due_for_dispense(user_id: str = settings.SHOULD_GET_LATEST_RECORD_FROM_DB, db: Session = Depends(get_session)):
#     user_id = get_newest_user_id(db) if user_id == settings.SHOULD_GET_LATEST_RECORD_FROM_DB else user_id
#     return read_user_if_user_is_due_for_dispense(user_id=user_id, db=db)

@router.post(
    "/set_num",
    status_code=status.HTTP_200_OK,
)
def set_num(num: int):
    global lol
    lol = num
    return num

@router.get(
    "/due_for_dispense",
    # response_model=list[UserReadWithPrescriptions],
    status_code=status.HTTP_200_OK,
)
def get_user_due_for_dispense_default(user_id: Annotated[str, Query(min_length=0)] = settings.SHOULD_GET_LATEST_RECORD_FROM_DB, db: Session = Depends(get_session)):
    global lol
    return lol
    # if user_id == settings.SHOULD_GET_LATEST_RECORD_FROM_DB:
    #     user_id = get_newest_user_id(db)
    # return read_user_if_user_is_due_for_dispense(user_id=user_id, db=db)


# @router.post(
#     "/{pill_dispense_id}/consume",
#     status_code=status.HTTP_200_OK,
# )
# def user_consumed_pill_dispense_event(pill_dispense_id: str = settings.SHOULD_GET_LATEST_RECORD_FROM_DB, db: Session = Depends(get_session)):
#     if pill_dispense_id == settings.SHOULD_GET_LATEST_RECORD_FROM_DB:
#         pill_dispense_id = get_newest_pill_dispense_id(db)
#     return mark_dispense_as_consumed(pill_dispense_id=pill_dispense_id, db=db)

@router.get(
    "/consume",
    status_code=status.HTTP_200_OK,
)
def user_consumed_pill_dispense_event_default(pill_dispense_id: Annotated[str, Query(min_length=0)] = settings.SHOULD_GET_LATEST_RECORD_FROM_DB, db: Session = Depends(get_session)):
    global lol
    lol = 0
    return PillDispenseEvent(prescription_id=db.exec(select(Prescription)).first().id, consumed_time=datetime.now(), dispense_count=lol)


    # if pill_dispense_id == settings.SHOULD_GET_LATEST_RECORD_FROM_DB:
    #     pill_dispense_id = get_newest_pill_dispense_id(db)
    # return mark_dispense_as_consumed(pill_dispense_id=pill_dispense_id, db=db)


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