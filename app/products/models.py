from app.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.auth.models import User


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    stock = Column(Integer, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    image_url = Column(String, nullable=True, index=True)

    user = relationship("User", back_populates="product")
    cart = relationship("Cart", back_populates="product")
    items = relationship("OrderItems", back_populates="products")
