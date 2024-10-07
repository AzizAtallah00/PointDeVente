from datetime import UTC
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
from app.enum import TokenStatus
from app.database import Base

class AccountActivation (Base):
    __tablename__ = "account_activations"
    
    id = Column (Integer, primary_key = True)
    email = Column (String, nullable = False)
    token = Column (String)
    employeeId = Column (Integer, ForeignKey("employees.id"))
    status = Column (Enum(TokenStatus), nullable = False)
    created_on = Column (DateTime, nullable=False, server_default = func.now())
    