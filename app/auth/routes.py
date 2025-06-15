from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from . import controllers, schemas
from . import utils
from app.core.logging_config import logger
from app.core.custom_exceptions import UserAlreadyExists, InvalidCredentials, PasswordPattern


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post('/signup', response_model=schemas.UserOut, status_code=201, description="USER SIGN UP")
async def add_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)) -> schemas.UserCreate:
    """
    Register a new user in the system.

    Args:
        user (schemas.UserCreate): The data for the new user to be created.
        db (AsyncSession): The database session, injected by FastAPI. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the email is already registered (status 400).
        HTTPException: If the password does not meet the required pattern (status 400).
        HTTPException: For any other unexpected server errors (status 500).

    Returns:
        schemas.UserOut: The created user data (excluding sensitive information like password).
    """
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


@router.post('/signin', response_model=schemas.Token, description="USER LOG IN")
async def user_login(user: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Authenticates a user and returns an access and refresh token.

    Args:
        user (schemas.UserLogin): User login credentials containing email and password.
        db (AsyncSession): Database session for querying the user data.

    Raises:
        HTTPException: If the credentials are invalid.
        HTTPException: For unexpected internal server errors.

    Returns:
        schemas.Token: A token response including access token, refresh token, and token type.
    """
    try:
        return await controllers.login(user=user, db=db)
    except InvalidCredentials as e:
        logger.warning(f"{e}")
        raise HTTPException(status_code=404, detail="Invalid Credentials.")
    except Exception as e:
        logger.error(f"[SIGNIN] Internal server error: {e}")
        raise HTTPException(status_code=500, detail="Failed to sign in user.")


@router.post("/refresh", response_model=schemas.Token, description="REFRESH TOKEN")
async def refresh(data: schemas.Refresh, db: AsyncSession = Depends(get_db)):
    """
    Refresh the user's access token using a valid refresh token.

    Args:
        data (schemas.Refresh): Object containing the refresh token.
        db (AsyncSession): Database session dependency.

    Raises:
        HTTPException: If the token is invalid or server error occurs.

    Returns:
        schemas.Token: A new access token and the existing refresh token.
    """
    try:
        return utils.refresh_token(data=data)
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(status_code=500, detail="Failed to refresh token.")


@router.post('/forgot-password', response_model=schemas.ResetTokenResponse, description="Forgot Password?")
async def send_email(data: schemas.ForgotPassword, db: AsyncSession = Depends(get_db)):
    """
    Sends a password reset email to the user with a reset token.

    Args:
        data (schemas.ForgotPassword): User email data to send reset password link.
        db (AsyncSession): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: Raises 500 if sending email fails due to server error.

    Returns:
        schemas.ResetTokenResponse: Contains the reset token sent to the user.
    """
    try:
        return await controllers.send_mail(data=data, db=db)
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(status_code=500, detail="Failed to send mail to user.")


@router.post('/reset-password', response_model=schemas.MessageResponse, description="Reset your password!")
async def reset_password(data: schemas.ChangePassword, db: AsyncSession = Depends(get_db)):
    try:
        return await controllers.reset_pass(data=data, db=db)
    except PasswordPattern as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise HTTPException(status_code=500, detail="Failed to change password.")
