from pydantic import BaseModel, ConfigDict, EmailStr, Field
from .models import RoleEnum


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=20)
    email: EmailStr = Field(..., description="Give a valid email address")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=40,
                          description="Password must be 8-40 characters and include upper, lower, digit, special char.")
    role: RoleEnum = RoleEnum.admin


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Give a valid email address")
    password: str = Field(..., min_length=8, max_length=40)


class ForgotPassword(BaseModel):
    email: EmailStr = Field(..., description="Give a valid email address")


class ChangePassword(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=40,
                              description="Password must be 8-40 characters and include upper, lower, digit, special char.")


class Token(BaseModel):
    access_token: str
    refresh_token: str
    type: str


class ResetTokenResponse(BaseModel):
    reset_token: str
    message: str


class MessageResponse(BaseModel):
    message: str


class Refresh(BaseModel):
    refresh_token: str


class UserOut(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
