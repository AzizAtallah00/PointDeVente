from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from app.enum import TokenStatus

from app.database import Base

class ChangePassword (Base):
    __tablename__ = "change_password"
    id = Column (Integer, primary_key = True) 
    token = Column (String)
    email = Column (String)
    employeeId = Column (Integer, ForeignKey("employees.id"))
    status = Column (Enum(TokenStatus), nullable = False)
    created_on = Column (DateTime, nullable=False, server_default = func.now())
