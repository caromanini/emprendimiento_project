from datetime import datetime, time
from sqlalchemy.orm import Session
from app.models.message import Message


def get_todays_messages(db: Session, contact_id: int, source: str = None):
    today = datetime.now().date()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)

    q = db.query(Message).filter(
        Message.contact_id == contact_id,
        Message.created_at >= start_of_day,
        Message.created_at <= end_of_day
    )
    if source:
        q = q.filter(Message.source == source)
    return q.order_by(Message.created_at.asc()).all()


def create_message(db: Session, contact_id: int, role: str, content: str, source: str = 'simulator'):
    db_message = Message(contact_id=contact_id, role=role, content=content, source=source)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_latest_messages(db: Session, contact_id: int, limit: int = 20, source: str = None):
    q = db.query(Message).filter(Message.contact_id == contact_id)
    if source:
        q = q.filter(Message.source == source)
    messages = q.order_by(Message.created_at.desc()).limit(limit).all()
    return list(reversed(messages))


def get_messages_before(db: Session, contact_id: int, before_id: int, limit: int = 20, source: str = None):
    q = db.query(Message).filter(
        Message.contact_id == contact_id,
        Message.id < before_id
    )
    if source:
        q = q.filter(Message.source == source)
    messages = q.order_by(Message.created_at.desc()).limit(limit).all()
    return list(reversed(messages))


def has_messages_before(db: Session, contact_id: int, before_id: int, source: str = None) -> bool:
    q = db.query(Message).filter(
        Message.contact_id == contact_id,
        Message.id < before_id
    )
    if source:
        q = q.filter(Message.source == source)
    return q.first() is not None
