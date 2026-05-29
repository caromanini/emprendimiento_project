from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    phone_number = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    guardian = relationship("User", back_populates="contacts")
    messages = relationship(
        "Message", back_populates="contact", cascade="all, delete-orphan"
    )
    topics = relationship(
        "Topic", back_populates="contact", cascade="all, delete-orphan"
    )
    daily_reports = relationship(
        "DailyReport", back_populates="contact", cascade="all, delete-orphan"
    )
