from sqlalchemy import CheckConstraint, Column, Date, Enum, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
from app.enum import ContractType, Gender, AccountStatus 

class Employee(Base):
    __tablename__ = "employees"
     
    id = Column (Integer, primary_key=True)  
    first_name = Column (String)
    last_name = Column (String)
    number = Column (Integer)
    phone_number = Column (String)
    email = Column (String , unique = True)
    password = Column (String, nullable=False)
    birth_date = Column (Date) 
    cnss_number = Column (String)
    gender = Column (Enum(Gender), nullable= False)
    contract_type = Column (Enum(ContractType), nullable= False)
    account_status = Column (Enum(AccountStatus), nullable= False, default= AccountStatus.INACTIVE)
    created_on = Column (DateTime, nullable=False, server_default = func.now())
    
    __table_args__ = (
        CheckConstraint("(contract_type IN ('cdd','cdi') AND cnss_number IS NOT NULL AND cnss_number ~'^\\d{8}-\\d{2}$') OR  (contract_type IN ('sivp','apprenti') AND (cnss_number IS NULL OR cnss_number ~'^\\d{8}-\\d{2}$' ))",
        name= "ck_employee_valid_cnss_number"),
    )

    
    