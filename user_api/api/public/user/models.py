from datetime import datetime
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel
from uuid import uuid4 as uuid


class UserRole(str, Enum):
    PATIENT = "PATIENT"
    CARETAKER = "CARETAKER"

id_factory = lambda: str(uuid())
now_factory = lambda: datetime.now()
class FrequencyUnit(str, Enum):
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"


class Prescription(SQLModel, table=True):
    id: str | None = Field(default_factory=id_factory, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="prescriptions")
    medication_name: str
    created_at: datetime | None = Field(default_factory=now_factory)

    # {frequency_number} times per {frequency_unit_number} {frequency_unit}
    # e.g. 2 pills per 1 DAY
    # e.g. 1 pill per 6 HOUR

    frequency_number: int
    frequency_unit_number: int
    frequency_unit: FrequencyUnit


class UserBase(SQLModel):
    role: UserRole
    name: str
    
class UserCreate(UserBase):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jane Good",
                "role": "PATIENT",
                "prescriptions": [
                    {
                        "medication_name": "Tylenol 500mg",
                        "frequency_number": 1,
                        "frequency_unit_number": 6,
                        "frequency_unit": "HOUR",
                    }
                ],
            }
        }
    prescriptions: list[dict] = []

class User(UserBase, table=True):
    prescriptions: list[Prescription] = Relationship(back_populates="user")
    id: str | None = Field(default_factory=id_factory, primary_key=True)
    created_at: datetime | None = Field(default_factory=now_factory)
    chat_messages: list["ChatMessage"] = Relationship(back_populates="user")


class UserReadWithPrescriptions(UserBase):
    prescriptions: list[Prescription] = []
    id: str

class ChatMessage(SQLModel, table=True):
    id: str | None = Field(default_factory=id_factory, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="chat_messages")
    message: str
    created_at: datetime | None = Field(default_factory=now_factory)
