from .employee import Base
from ..schemas import CategoryOutput


class Product(Base):
    name : str
    description : str | None = None
    price : float
    quantity : int
    image_link : str

class ProductInput (Product):
    category_name : str

class ProductOutput (Product):
    id : int
    category : CategoryOutput