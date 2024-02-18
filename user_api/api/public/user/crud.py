from datetime import datetime
from fastapi import HTTPException, status
from pydantic import BaseModel

from sqlmodel import Session, select, desc
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


def get_newest_user_id(db: Session):
    user = db.exec(select(User).order_by(desc(User.created_at))).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user found",
        )
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has no id",
        )
    return user.id

def get_newest_pill_dispense_id(db: Session):
    pill_dispense = db.exec(select(PillDispenseEvent).order_by(desc(PillDispenseEvent.dispense_time))).first()
    if not pill_dispense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pill dispense found",
        )
    if pill_dispense.id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pill dispense has no id",
        )
    return pill_dispense.id
