from datetime import datetime, timedelta
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel
from api.utils.factories import id_factory, now_factory
from api.public.chat.models import ChatSession


class UserRole(str, Enum):
    PATIENT = "PATIENT"
    CARETAKER = "CARETAKER"


# Months and years are more complex than initially anticipated since they do not always have fixed lengths.
# To avoid any ambiguity, prescription frequency units are limited to hours, days, and weeks.
class FrequencyUnit(str, Enum):
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    # for testing only
    MIN = "MIN"


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
    # TODO: need to have dispenses serializable on a prescription
    pill_dispenses: list["PillDispenseEvent"] = Relationship(
        back_populates="prescription",
         sa_relationship_kwargs=dict(cascade="all, delete-orphan")
    )

    def _delta_from_frequency(self):
        return timedelta(**{
            "hours": self.frequency_unit_number if self.frequency_unit == FrequencyUnit.HOUR else 0,
            "days": self.frequency_unit_number if self.frequency_unit == FrequencyUnit.DAY else 0,
            "weeks": self.frequency_unit_number if self.frequency_unit == FrequencyUnit.WEEK else 0,
        })

    def _should_dispense(self):
        # perform an immediate dispense if there are no dispenses
        if len(self.pill_dispenses) == 0:
            return True
        
        now = datetime.now()
        last_dispense = self.pill_dispenses[-1]
        consumed_time = last_dispense.consumed_time
        last_dispense_was_consumed = consumed_time is not None
        if last_dispense_was_consumed:
            return now - consumed_time > self._delta_from_frequency()
        else:
            return False
        
    def handle_dispense(self):
        should_dispense_now = self._should_dispense()
        if not should_dispense_now:
            return
        prescription_id = self.id
        if prescription_id is None:
            raise ValueError("Prescription must have an id")
        pill_dispense = PillDispenseEvent(prescription_id=prescription_id, dispense_count=self.frequency_number)
        self.pill_dispenses.append(pill_dispense)
        return pill_dispense
        


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
    prescriptions: list[Prescription] = Relationship(back_populates="user", sa_relationship_kwargs=dict(cascade="all, delete-orphan"))
    id: str | None = Field(default_factory=id_factory, primary_key=True)
    created_at: datetime | None = Field(default_factory=now_factory)
    chat_sessions: list[ChatSession] = Relationship(back_populates="user", sa_relationship_kwargs=dict(cascade="all, delete-orphan"))


class UserReadWithPrescriptions(UserBase):
    prescriptions: list[Prescription] = []
    id: str


"""
in real world:
- pills 'dispensing' means that the button on the dispenser to get the pills out is now active and will dispense the pills when pressed
- pills 'consumed' means that you actually took the pills, or at least pressed the button to get the pills out
"""
class PillDispenseEvent(SQLModel, table=True):
    id: str | None = Field(default_factory=id_factory, primary_key=True)
    prescription_id: str = Field(foreign_key="prescription.id")
    prescription: "Prescription" = Relationship(back_populates="pill_dispenses")
    dispense_time: datetime | None = Field(default_factory=now_factory)
    dispense_count: int = 0
    consumed_time: datetime | None = None


