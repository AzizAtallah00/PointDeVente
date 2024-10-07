# from enum import Enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from ..database import Base
# from datetime import datetime
from ..enum import SessionStatus
from . import Employee
class Session (Base):
    __tablename__ = "sessions"
    
    id = Column (Integer, primary_key = True)
    employee_id = Column (Integer, ForeignKey('employees.id'))
    opened_at = Column (DateTime, nullable = False)
    closed_at = Column (DateTime)
    session_status = Column (Enum(SessionStatus), nullable = False, default = SessionStatus.OPEN)
    employee = relationship("Employee")