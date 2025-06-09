from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import utils
from app.auth.models import User
from app.auth import schemas
from app.auth import utils


def get_user_by_email(db : Session, email : str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = utils.hash_password(user.password)
    db_user = User(
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
    access_token = utils.create_access_token({"sub":user.email})
    refresh_token = utils.create_refresh_token({"sub":user.email})
    return {"access_token": access_token,"refresh_token":refresh_token,"type":"bearer"}

def reset_pass(data:dict,db:Session):
    payload = utils.decode_token(data.token)

    if payload is None:
        raise HTTPException(status_code=404,detail="Invalid Token.")
    
    email = payload["sub"]
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404,detail="User not found! Try again.")
    user.hashed_password = utils.hash_password(data.new_password)
    return {"message" : "Password changed Succesfully!"}