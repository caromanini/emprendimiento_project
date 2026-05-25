from fastapi import FastAPI
from app.routers import users, dashboard, contacts
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(contacts.router)
