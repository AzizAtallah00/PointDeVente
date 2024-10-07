from sqlalchemy import Column, DateTime, Integer, String, func
from ..database import Base

class Category (Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column (String, nullable=False)
    description = Column (String)
    icon = Column (String, nullable=False)
    created_on = Column (DateTime, nullable=False, server_default = func.now())