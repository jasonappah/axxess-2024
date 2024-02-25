from datetime import datetime
from fastapi import HTTPException, status
from pydantic import BaseModel

from sqlmodel import Session, select
from api.public.user.models import (
    PillDispenseEvent,
    Prescription,
    User,
    UserCreate,
    UserRole,
)
from api.utils.logger import logger_config

logger = logger_config(__name__)


def read_patients(db: Session):
    patients = db.exec(select(User).where(User.role == UserRole.PATIENT)).all()
    return patients


def read_user_by_id(user_id: str, db: Session):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with id: {user_id}",
        )
    return user


def insert_user(user_create: UserCreate, db: Session):
    user = User(
        **user_create.model_dump(
            exclude={
                "prescriptions",
            }
        )
    )
    for p in user_create.prescriptions:
        prescription = Prescription(**p)
        user.prescriptions.append(prescription)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


class DispensationStatus(BaseModel):
    needs_dispense: bool
    events: list[PillDispenseEvent]


def read_user_if_user_is_due_for_dispense(user_id: str, db: Session):
    user = read_user_by_id(user_id, db)
    pill_dispenses: list[PillDispenseEvent] = []
    for prescription in user.prescriptions:
        if prescription.pill_dispenses == []:
            continue
        latest_dispense = prescription.pill_dispenses[-1]
        if latest_dispense.consumed_time is None:
            pill_dispenses.append(latest_dispense)

    return DispensationStatus(
        needs_dispense=len(pill_dispenses) > 0, events=pill_dispenses
    )


def mark_dispense_as_consumed(pill_dispense_id: str, db: Session):
    pill_dispense = db.get(PillDispenseEvent, pill_dispense_id)
    if not pill_dispense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pill dispense not found with id: {pill_dispense_id}",
        )
    pill_dispense.consumed_time = datetime.now()
    db.commit()
    db.refresh(pill_dispense)
    return pill_dispense




def update_user(user_id: str, user: UserCreate, db: Session):
    user2 = read_user_by_id(user_id, db)
    user2.name = user.name
    user2.prescriptions = []
    for p in user.prescriptions:
        prescription = Prescription(**p)
        user2.prescriptions.append(prescription)
    db.commit()
    db.refresh(user2)
    return user2

def delete_user(user_id: str, db: Session):
    user = read_user_by_id(user_id, db)
    db.delete(user)
    db.commit()
    return user