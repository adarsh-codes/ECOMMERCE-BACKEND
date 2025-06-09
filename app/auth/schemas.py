from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name : str
    email : str

class UserCreate(UserBase):
    password : str
    role : str = "user"

class UserLogin(BaseModel):
    email : str
    password : str

class ForgotPassword(BaseModel):
    email : str

class ChangePassword(BaseModel):
    token : str
    new_password : str

class Token(BaseModel):
    access_token : str
    refresh_token : str
    type : str

class Refresh(BaseModel):
    refresh_token : str

class UserOut(UserBase):
    id : int
    
    model_config = ConfigDict(from_attributes=True)