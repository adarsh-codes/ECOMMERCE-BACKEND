from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from fastapi import Depends, HTTPException, Security
from sqlalchemy import select
from app.auth import utils, models
from app.auth.routes import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = utils.decode_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        result = await db.execute(select(models.User).where(models.User.email == payload.get("sub")))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=404, detail="Invalid Token.")


def require_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user


def require_user(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Users only")
    return current_user
