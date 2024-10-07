from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func, Float
from ..database import Base

class Product (Base):
    __tablename__ = "products"
    
    id = Column (Integer, primary_key = True)
    name = Column (String, nullable = False)
    description = Column (String)
    price = Column (Float, nullable=False)
    image_link = Column (String, nullable = False)
    quantity = Column (Integer, nullable = False)
    category_id = Column (Integer, ForeignKey('categories.id'))
    created_on = Column (DateTime, nullable = False, server_default = func.now())    