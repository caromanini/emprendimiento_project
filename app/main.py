from fastapi import FastAPI
from app.db.database import engine, Base

import app.models.user
import app.models.contact
import app.models.message
import app.models.topic
from app.routers import users, dashboard, contacts, topics, chat, reports

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(contacts.router)
app.include_router(topics.router)
app.include_router(chat.router)
app.include_router(reports.router)
