from datetime import datetime
from uuid import uuid4 as uuid

id_factory = lambda: str(uuid())
now_factory = lambda: datetime.now()