from datetime import date
from pydantic import BaseModel
from . import EmployeeOutput

class Base (BaseModel):
    class config:
        orm_mode = True

class SessionOutput(Base):
    id : int
    opened_at : date
    closed_at : date | None = None
    session_status : str
    employee : EmployeeOutput