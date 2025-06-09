from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from ..auth import utils,models,main
from jose import JWTError


oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/auth/signin")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(main.get_db)):
 try: 
    payload = utils.decode_token(token) 
    if payload is None: 
        raise HTTPException(status_code=401, detail="Invalid token") 
    user = db.query(models.User).filter(models.User.email == payload.get("sub")).first() 
    if not user: 
        raise HTTPException(status_code=404, detail="User not found") 
    return user 
 
 except JWTError:
    raise HTTPException(status_code=404,detail="Invalid Token.")
 

 from fastapi import Security 
def require_admin(current_user: models.User = Depends(get_current_user)): 
    if current_user.role != "admin": 
        raise HTTPException(status_code=403, detail="Admins only") 
    return current_user 
def require_user(current_user: models.User = Depends(get_current_user)): 
    if current_user.role != "user": 
        raise HTTPException(status_code=403, detail="Users only") 
    return current_user