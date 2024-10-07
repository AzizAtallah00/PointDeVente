from sqlalchemy import Column, ForeignKey, Integer, DateTime
from ..database import Base
# from datetime import datetime


class Order (Base):
     __tablename__ = "orders"
     
     id = Column (Integer, primary_key = True)
     date_order = Column (DateTime, nullable = False)
     receipt_number = Column (Integer, nullable=False)
     total_price = Column (Integer, nullable=False)
     employee_id = Column (Integer, ForeignKey('employees.id'))
     customer_id = Column (Integer, ForeignKey('customers.id'))
     session_id = Column (Integer, ForeignKey('sessions.id'))
     pricelist_id = Column (Integer, ForeignKey('pricelists.id'))
     