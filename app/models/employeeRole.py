from sqlalchemy import Enum, Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.enum import Role

from app.database import Base

class EmployeeRole(Base):
    __tablename__ = "employee_roles"
    
    id = Column (Integer, primary_key = True)
    employeeId = Column (Integer, ForeignKey('employees.id'))
    role = Column(Enum(Role), nullable = False)