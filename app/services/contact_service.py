from sqlalchemy.orm import Session
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate

def get_contact_by_id(db: Session, contact_id: str, user_id: int):
    return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user_id).first()

def get_user_contacts(db: Session, user_id: int):
    return db.query(Contact).filter(Contact.user_id == user_id).all()

def create_contact(db: Session, contact: ContactCreate, user_id: int):
    db_contact = Contact(**contact.model_dump(), user_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, user_id: int, contact_data: ContactUpdate):
    db_contact = get_contact_by_id(db, contact_id, user_id)
    
    if db_contact:
        db_contact.full_name = contact_data.full_name
        db_contact.phone_number = contact_data.phone_number
        db.commit()
        db.refresh(db_contact)
        
    return db_contact

def delete_contact(db: Session, contact_id: int, user_id: int):
    db_contact = get_contact_by_id(db, contact_id, user_id)

    if db_contact:
        db.delete(db_contact)
        db.commit()
    
    return db_contact