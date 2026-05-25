from sqlalchemy.orm import Session
from app.models.topic import Topic
from app.schemas.topic import TopicCreate, TopicUpdate

def get_topic_by_id(db: Session, topic_id: str):
    return db.query(Topic).filter(Topic.id == topic_id).first()

def get_topics_by_contact(db: Session, contact_id: int):
    return db.query(Topic).filter(Topic.contact_id == contact_id).all()

def create_topic(db: Session, topic: TopicCreate, contact_id: int):
    db_topic = Topic(
        title=topic.title,
        instruction=topic.instruction,
        contact_id=contact_id
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def update_topic(db: Session, topic_id: int, topic_data: TopicUpdate):
    db_topic = get_topic_by_id(db, topic_id)

    if db_topic:
        db_topic.title = topic_data.title
        db_topic.instruction = topic_data.instruction
        db.commit()
        db.refresh(db_topic)
    
    return db_topic

def delete_topic(db: Session, topic_id: int):
    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if db_topic:
        db.delete(db_topic)
        db.commit()
