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


def read_patients(db: Session = Depends(get_session)):
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


def insert_user(user_create: UserCreate, db: Session = Depends(get_session)):
    user = User(**user_create.model_dump(exclude={"prescriptions",}))
    for p in user_create.prescriptions:
        prescription = Prescription(**p)
        user.prescriptions.append(prescription)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


