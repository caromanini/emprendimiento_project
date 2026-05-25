from datetime import datetime, time
from sqlalchemy.orm import Session
from app.models.message import Message

def get_todays_messages(db: Session, contact_id: int):
    today = datetime.now().date()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)
    
    return db.query(Message).filter(
        Message.contact_id == contact_id,
        Message.created_at >= start_of_day,
        Message.created_at <= end_of_day
    ).order_by(Message.created_at.asc()).all()

def create_message(db: Session, contact_id: int, role: str, content: str):
    db_message = Message(contact_id=contact_id, role=role, content=content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message