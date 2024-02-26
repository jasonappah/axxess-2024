from sqlmodel import Session, select

from api.database import engine
from api.public.user.models import User, Prescription, UserRole, FrequencyUnit
from api.utils.logger import logger_config

logger = logger_config(__name__)


def create_demo_data():
    with Session(engine) as session:
        logger.info("=========== CREATING MOCK DATA ===========")
        if session.exec(select(User).where(User.name == "Caretaker Amy")).first():
            logger.info("=========== MOCK DATA ALREADY EXISTS ===========")
            return
        
        caretaker = User(
            name="Caretaker Amy",
            role=UserRole.CARETAKER,
        )

        patient1 = User(
            name="Bob Whitaker",
            role=UserRole.PATIENT,
        )

        patient2 = User(
            name="John Doe",
            role=UserRole.PATIENT,
        )
        session.add(caretaker)
        session.add(patient1)
        session.add(patient2)
        session.commit()
        session.refresh(caretaker)
        session.refresh(patient1)
        session.refresh(patient2)

        # mainly for type checking
        assert patient1.id is not None
        assert patient2.id is not None
        
        prescription1 = Prescription(
            medication_name="Aspirin 100mg",
            user_id=patient1.id,
            frequency_number=1,
            frequency_unit_number=1,
            frequency_unit=FrequencyUnit.MIN,
        )

        prescription2 = Prescription(
            medication_name="Tylenol 500mg",
            user_id=patient1.id,
            frequency_number=3,
            frequency_unit_number=6,
            frequency_unit=FrequencyUnit.HOUR,
        )

        prescription3 = Prescription(
            medication_name="Aspirin 100mg",
            user_id=patient2.id,
            frequency_number=1,
            frequency_unit_number=1,
            frequency_unit=FrequencyUnit.DAY,
        )

        prescription4 = Prescription(
            medication_name="Tylenol 500mg",
            user_id=patient2.id,
            frequency_number=2,
            frequency_unit_number=6,
            frequency_unit=FrequencyUnit.HOUR,
        )

        session.add(prescription1)
        session.add(prescription2)
        session.add(prescription3)
        session.add(prescription4)
        session.commit()
        session.refresh(prescription1)
        session.refresh(prescription2)
        session.refresh(prescription3)
        session.refresh(prescription4)


        logger.info("=========== MOCK DATA CREATED ===========")
