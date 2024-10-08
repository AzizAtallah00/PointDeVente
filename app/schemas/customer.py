from .employee import Base

class CustomerInput (Base):
    name : str
    email : str

class CustomerOutput (Base):
    id : int
    name : str
    email : str
  