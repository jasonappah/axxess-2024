from datetime import datetime
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel
from api.utils.factories import id_factory, now_factory
from api.public.chat.models import ChatSession


class UserRole(str, Enum):
    PATIENT = "PATIENT"
    CARETAKER = "CARETAKER"

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
    pill_dispenses: list["PillDispense"] = Relationship(back_populates="prescription")


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
    chat_sessions: list[ChatSession] = Relationship(back_populates="user")


class UserReadWithPrescriptions(UserBase):
    prescriptions: list[Prescription] = []
    id: str

class PillDispense(SQLModel, table=True):
    id: str | None = Field(default_factory=id_factory, primary_key=True)
    prescription_id: str = Field(foreign_key="prescription.id")
    prescription: "Prescription" = Relationship(back_populates="pill_dispenses")
    dispense_time: datetime | None = Field(default_factory=now_factory)
    dispense_count: int = 0
    consumed_time: datetime | None = None

"""
need to automatically create a pill dispense at the correct time for each prescription
e.g. if a prescription is created with frequency_number = 1, frequency_unit_number = 6, frequency_unit = "HOUR"
then we need to create a pill dispense every 6 hours
then we need to have an endpoint to mark a pill dispense as consumed

in real world:
- pills 'dispensing' means that the button on the dispenser to get the pills out is now active and will dispense the pills when pressed
- pills 'consumed' means that you actually took the pills, or at least pressed the button to get the pills out

need an endpoint to check for each user if they have any pills to dispense
need an endpoint to mark a pill dispense as consumed
endpoint to check if prescription is due for dispense is also nice but not 100% needed
"""