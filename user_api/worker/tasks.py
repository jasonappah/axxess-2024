from celery import Celery
from api.database import get_session
from api.public.user.crud import read_prescriptions

app = Celery('tasks')
app.config_from_object('worker.celeryconfig')

@app.task
def create_scheduled_dispenses():
    db = next(get_session())
    prescriptions = read_prescriptions(db)
    
    updates = [prescription.handle_dispense() for prescription in prescriptions]
    
    if any(updates):
        db.commit()
    return updates
    
