from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import utils
from app.auth import models
from app.auth import schemas
from app.auth import utils
from datetime import datetime, timedelta, timezone
from app.core.logging_config import logger


def get_user_by_email(db : Session, email : str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = utils.hash_password(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login(db : Session,user: schemas.UserLogin):
    user_db = db.query(models.User).filter(models.User.email == user.email).first()
    access_token = utils.create_access_token({"sub":user.email,"role":user_db.role})
    refresh_token = utils.create_refresh_token({"sub":user.email,"role":user_db.role})
    logger.info(f"Login requested by {user.email}")
    return {"access_token": access_token,"refresh_token":refresh_token,"type":"bearer"}

def reset_pass(data: dict, db: Session):
    payload = utils.decode_token(data.token)

    if payload is None:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")

    email = payload["sub"]

    reset_entry = db.query(models.PasswordToken).filter(models.PasswordToken.token == data.token).first()
    if not reset_entry:
        raise HTTPException(status_code=404, detail="Reset token not found.")

    if reset_entry.used:
        raise HTTPException(status_code=400, detail="Token already used.")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.hashed_password = utils.hash_password(data.new_password)
    reset_entry.used = True 

    db.commit()

    return {"message": "Password changed successfully!"}
