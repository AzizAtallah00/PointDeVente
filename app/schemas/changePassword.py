from typing import List
from pydantic import BaseModel

class Base (BaseModel):
    class config:
        orm_mode = True

class PasswordReset(Base):
    new_password: str
    confirm_password: str