import jwt
from fastapi import Request, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.services.user_service import get_user_by_email
from app.core.security import SECRET_KEY, ALGORITHM

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    try:
        token = token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except jwt.PyJWTError:
        return None

    return get_user_by_email(db, email=email)