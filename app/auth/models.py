from app.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from enum import Enum
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone


class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(RoleEnum), default=RoleEnum.user)

    reset_tokens = relationship("PasswordToken", back_populates="user")
    cart = relationship("Cart", back_populates="user")
    orders = relationship("Orders", back_populates="user")
    product = relationship("Products", back_populates="user")


class PasswordToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    expiration_time = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc) + timedelta(minutes=30))
    used = Column(Boolean, default=False)
    user = relationship("User", back_populates="reset_tokens")
