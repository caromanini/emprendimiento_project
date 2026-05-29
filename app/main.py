from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.database import engine, Base
import app.models.user
import app.models.contact
import app.models.message
import app.models.topic
import app.models.daily_report

from app.routers import users, dashboard, contacts, topics, chat, reports
from app.services.scheduler_service import start_scheduler

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(contacts.router)
app.include_router(topics.router)
app.include_router(chat.router)
app.include_router(reports.router)
