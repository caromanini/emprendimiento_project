from datetime import date, datetime
from sqlalchemy.orm import Session

from app.models.daily_report import DailyReport
from app.services.message_service import get_todays_messages
from app.services.topic_service import get_topics_by_contact
from app.services.gemini_service import generate_daily_report

def get_report_by_date(db: Session, contact_id: int, report_date: date):
    return db.query(DailyReport).filter(
        DailyReport.contact_id == contact_id,
        DailyReport.date == report_date
    ).first()

def get_all_reports(db: Session, contact_id: int):
    return db.query(DailyReport).filter(
        DailyReport.contact_id == contact_id
    ).order_by(DailyReport.date.desc()).all()

def create_daily_report(db: Session, contact_id: int, content: str):
    db_report = DailyReport(contact_id=contact_id, content=content)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def process_daily_report_for_contact(db: Session, contact_id: int):
    todays_messages = get_todays_messages(db, contact_id)
            
    if not todays_messages:
        report_content = "ALERTA DE INACTIVIDAD:\n\nNo se ha registrado ninguna interacción del paciente con C.A.M.I. durante el día de hoy. Se recomienda contactar al adulto mayor directamente para verificar su estado de bienestar."
    else:
        topics = get_topics_by_contact(db, contact_id)
        report_content = generate_daily_report(todays_messages, topics)

    current_date = datetime.now().date()
    existing_report = get_report_by_date(db, contact_id, current_date)
            
    if existing_report:
        existing_report.content = report_content
        db.commit()
    else:
        create_daily_report(db, contact_id, report_content)