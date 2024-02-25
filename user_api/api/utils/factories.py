from datetime import datetime
from uuid import uuid4 as uuid

def id_factory():
    return str(uuid())

def now_factory():
    return datetime.now()