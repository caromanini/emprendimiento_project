from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    title = Column(String, index=True)
    instruction = Column(String)
    is_active = Column(Boolean, default=True)

    contact = relationship("Contact", back_populates="topics")
