from sqlalchemy import Column, ForeignKey, Integer
from ..database import Base

class OrderLigne (Base):
    __tablename__ = "order_lignes"
    
    id = Column (Integer, primary_key = True)
    product_id = Column (Integer, ForeignKey('products.id'))
    quantity = Column (Integer, nullable=False)
    unit_price = Column (Integer, nullable=False)
    total_price = Column (Integer)
    order_id = Column (Integer, ForeignKey('orders.id'))
    