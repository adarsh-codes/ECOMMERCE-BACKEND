from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from . import utils
from app.auth import models
from app.auth import schemas
from app.core.logging_config import logger
from app.core.custom_exceptions import UserAlreadyExists, InvalidCredentials, PasswordPattern
import re
from . import email_service


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise UserAlreadyExists(f"Email {user.email} already exists.")

    logger.info(f"[CREATE_USER] Creating user: {user.email}")

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&]).*$'

    if not re.match(pattern, user.password):
        raise PasswordPattern("Password should be of 8 characters and must include atleast 1 uppercase, 1 lowercase, 1 digit and 1 symbol.")
    hashed_pw = utils.hash_password(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def login(db: AsyncSession, user: schemas.UserLogin):
    logger.info(f"Login requested by {user.email}")
    existing_user = await get_user_by_email(db, user.email)
    if not existing_user or not utils.verify_password(user.password, existing_user.hashed_password):
        raise InvalidCredentials("Invalid Credentials! Please check the details input.")

    access_token = utils.create_access_token({"sub": user.email, "role": existing_user.role})
    refresh_token = utils.create_refresh_token({"sub": user.email, "role": existing_user.role})
    logger.info(f"Login Successful by {user.email}")
    return {"access_token": access_token, "refresh_token": refresh_token, "type": "bearer"}


async def store_reset_token(user_id: int, token: str, db: AsyncSession):
    pass_db = models.PasswordToken(user_id=user_id, token=token, used=False)
    db.add(pass_db)
    await db.commit()
    await db.refresh(pass_db)


async def reset_pass(data: dict, db: AsyncSession):
    payload = utils.decode_token(data.token)

    if payload is None:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")

    email = payload["sub"]

    result = await db.execute(select(models.PasswordToken).where(models.PasswordToken.token == data.token))
    reset_entry = result.scalar_one_or_none()
    if not reset_entry:
        raise HTTPException(status_code=404, detail="Reset token not found.")

    if reset_entry.used:
        raise HTTPException(status_code=400, detail="Token already used.")

    res = await db.execute(select(models.User).where(models.User.email == email))
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&]).*$'

    if not re.match(pattern, data.new_password):
        raise PasswordPattern("Password should be of 8 characters and must include atleast 1 uppercase, 1 lowercase, 1 digit and 1 symbol.")

    user.hashed_password = utils.hash_password(data.new_password)
    reset_entry.used = True
    db.add(user)
    db.add(reset_entry)
    await db.commit()
    return {"message": "Password changed successfully!"}


async def send_mail(data: dict, db: AsyncSession):
    res_token = utils.reset_token({"sub": data.email})
    user = await get_user_by_email(db=db, email=data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    email_service.send_reset_email(to_email=data.email, token=res_token)
    await store_reset_token(user_id=user.id, token=res_token, db=db)
    return {"reset_token": res_token, "message": "Reset token stored In DB."}