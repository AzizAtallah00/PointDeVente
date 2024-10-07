from sqlalchemy import Column, Integer, String, ForeignKey, Date
from ..database import Base

class PricelistLigne (Base):
    __tablename__ = "pricelist_lignes"
     
    id = Column (Integer, primary_key = True)
    product_id = Column (Integer, ForeignKey('products.id'))
    price = Column (Integer, nullable=False)
    min_quantity = Column (Integer, nullable=False)
    start_date = Column (Date, nullable=False)
    end_date = Column (Date, nullable=False)
    pricelist_id = Column (Integer, ForeignKey('pricelists.id'))