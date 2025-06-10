from app.core.database import Base
from sqlalchemy import Column, Integer, String


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False, index=True)
    price = Column(Integer, nullable=False, index=True)
    stock = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    image_url = Column(String, nullable=True, index=True)
