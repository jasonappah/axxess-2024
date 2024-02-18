from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from api.database import get_session
from api.public.user.models import User, UserRole
from api.utils.logger import logger_config

logger = logger_config(__name__)


def read_patients(db: Session = Depends(get_session)):
    patients = db.exec(select(User).where(User.role == UserRole.PATIENT)).all()
    return patients


def read_user_by_id(user_id: str, db: Session = Depends(get_session)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with id: {user_id}",
        )
    return user


def insert_user(user: User, db: Session = Depends(get_session)):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
