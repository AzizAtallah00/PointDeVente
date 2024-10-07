from sqlalchemy import Column, Integer, String
from ..database import Base


class Pricelist (Base):
    __tablename__ = "pricelists"
    
    id = Column (Integer, primary_key = True)
    name = Column (String, nullable = False)
    description = Column (String, nullable = False)
    