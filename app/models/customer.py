from sqlalchemy import Column, Integer, String, ForeignKey
from ..database import Base

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column (Integer, primary_key = True)
    name = Column (String, nullable = False)
    email = Column (String, nullable = False)
    pricelist_id = Column (Integer, ForeignKey('pricelists.id'))