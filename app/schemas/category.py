from .employee import Base


class CategoryInput (Base):
    name : str
    description : str 
    icon : str

class CategoryOutput (CategoryInput):
    id : int