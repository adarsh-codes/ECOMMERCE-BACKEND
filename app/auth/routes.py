from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from . import controllers, schemas
from . import utils
from app.core.logging_config import logger
from app.core.custom_exceptions import UserAlreadyExists, InvalidCredentials, PasswordPattern


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post('/signup', response_model=schemas.UserOut)
async def add_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"[SIGNUP] Attempt from {user.email}")

    try:
        return await controllers.create_user(db, user)

    except UserAlreadyExists as e:
        logger.warning(f"[SIGNUP] User already exists: {e}")
        raise HTTPException(status_code=400, detail="Email already registered. Please login.")
    except PasswordPattern as e:
        logger.warning(f"[SIGNUP]: {e}")
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        logger.error(f"[SIGNUP] Internal server error: {e}")
        raise HTTPException(status_code=500, detail=f"{e}")


@router.post('/signin', response_model=schemas.Token)
async def user_login(user: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        return await controllers.login(user=user, db=db)

    except InvalidCredentials as e:
        logger.warning(f"{e}")
        raise HTTPException(status_code=404, detail="Invalid Credentials.")
    except Exception as e:
        logger.error(f"[SIGNIN] Internal server error: {e}")
        raise HTTPException(status_code=500, detail="Failed to sign in user.")


@router.post("/refresh", response_model=schemas.Token)
async def refresh(data: schemas.Refresh, db: AsyncSession = Depends(get_db)):
    try:
        return utils.refresh_token(data=data)
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(status_code=500, detail="Failed to refresh token.")


'''

EK LOGOUT WALA FEATURE YAAD RKHNA

'''


@router.post('/forgot-password')
async def send_email(data: schemas.ForgotPassword, db: AsyncSession = Depends(get_db)):
    try:
        return await controllers.send_mail(data=data, db=db)
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(status_code=500, detail="Failed to send mail to user.")


@router.post('/reset-password')
async def reset_password(data: schemas.ChangePassword, db: AsyncSession = Depends(get_db)):
    try:
        return await controllers.reset_pass(data=data, db=db)
    except PasswordPattern as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(status_code=500, detail="Failed to change password.")
