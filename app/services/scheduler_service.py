import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.db.database import SessionLocal
from app.models.contact import Contact
from app.services.report_service import process_daily_report_for_contact

logger = logging.getLogger(__name__)

def scheduled_report_job():
    db = SessionLocal()
    try:
        contacts = db.query(Contact).all()
        for contact in contacts:
            process_daily_report_for_contact(db, contact.id)

            time.sleep(10) 
    
    except Exception as e:
        logger.exception(f"Error in scheduled job: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()

    trigger = CronTrigger(hour=20, minute=00)
    scheduler.add_job(
        scheduled_report_job, 
        trigger=trigger, 
        id='daily_report_job', 
        replace_existing=True
    )
    
    scheduler.start()    
    return scheduler