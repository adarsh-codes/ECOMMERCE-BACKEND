from app.core.database import Base
from sqlalchemy import Column,Integer,String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    name = Column(String,index=True)
    email = Column(String,unique=True,index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
