from typing import List
from pydantic import BaseModel
from datetime import date
from app.enum import ContractType, Gender, AccountStatus, Role

class Base (BaseModel):
    class config:
        orm_mode = True


class EmployeeInput (Base):
    first_name : str
    last_name : str
    number : int
    phone_number : str
    email : str
    password : str
    confirm_password : str
    birth_date : date
    cnss_number : str
    roles : List [Role]
    gender : Gender
    contract_type : ContractType
    account_status : AccountStatus = AccountStatus.INACTIVE
    
    
     
class EmployeeOutput (Base):
    id : int
    first_name : str
    last_name : str
    number : int
    phone_number : str
    email : str
    birth_date : date
    cnss_number : str

class EmployeeLogin (BaseModel):
    email : str
    password : str
