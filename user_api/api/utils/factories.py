from datetime import datetime
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel
from uuid import uuid4 as uuid

id_factory = lambda: str(uuid())
now_factory = lambda: datetime.now()