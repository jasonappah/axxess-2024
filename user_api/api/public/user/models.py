from enum import Enum
from typing import Literal
from sqlmodel import Field, SQLModel
from uuid import uuid4 as uuid

class UserRole(str, Enum):
    PATIENT = "PATIENT"
    CARETAKER = "CARETAKER"


class UserBase(SQLModel):
    role: UserRole
    name: str

class User(UserBase, table=True):
    id: str | None = Field(default_factory=lambda: str(uuid()), primary_key=True)