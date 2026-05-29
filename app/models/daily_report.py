from sqlalchemy import Column, Integer, Text, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class DailyReport(Base):
    __tablename__ = "daily_reports"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    content = Column(Text)
    date = Column(Date, server_default=func.current_date(), index=True)

    contact = relationship("Contact", back_populates="daily_reports")