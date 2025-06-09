from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.core.database import Base, SessionLocal, engine
from . import schemas, email_service
from .models import User
from . import crud,utils
from typing import List


router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/signup', response_model=schemas.UserOut)
def add_user(user : schemas.UserCreate, db : Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.create_user(db, user)
    return new_user


@router.post('/signin',response_model=schemas.Token)
def user_login(user : schemas.UserLogin, db : Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db=db,email=user.email)
    if not existing_user or not utils.verify_password(user.password,existing_user.hashed_password):
        return HTTPException(status_code=404,detail="Invalid Credentials! Please check the details input.")
    return crud.login(user=user,db=db)
    
@router.post("/refresh",response_model=schemas.Token)
def refresh(data : schemas.Refresh, db : Session = Depends(get_db)):
    return utils.refresh_token(data=data)
 
'''

EK LOGOUT WALA FEATURE YAAD RKHNA

'''

@router.post('/forgot-password')
def send_email(data : schemas.ForgotPassword, db:Session = Depends(get_db)):
    res_token = utils.reset_token({"sub":data.email})
    email_service.send_reset_email(to_email=data.email,token=res_token)
    return {"message":"EMAIL SENT!"}

@router.post('/reset-password')
def reset_password(data : schemas.ChangePassword,db : Session = Depends(get_db)):
    return crud.reset_pass(data=data,db=db)
@router.get('/users',response_model=List[schemas.UserOut])
def get_users(db : Session = Depends(get_db), skip : int = 0, limit : int = 10):
    return db.query(User).all()

