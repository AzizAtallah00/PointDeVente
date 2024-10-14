from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import ProductOutput, ProductInput, TokenData
from ..database import get_db
from ..oauth2 import getCurrentUser
from ..models import Product, Category
from .category import getByName

router = APIRouter(
    prefix = "/products",
    tags= ["product"]
)

@router.post ("/", response_model=ProductOutput)
def addProduct ( prod : ProductInput, currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
    if ('INVENTORY_MANAGER' in currUser.roles or 'ADMIN' in currUser.roles or 'SUPERUSER' in currUser.roles):
        category = getByName (prod.category_name, currUser, db)
        product_dict = prod.model_dump()
        del product_dict ["category_name"]
        product =  Product(**product_dict, category_id = category.id)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    else:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!!")


@router.get ("/", response_model=List[ProductOutput])
def getAllProducts (currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
    if ('INVENTORY_MANAGER' in currUser.roles or 'ADMIN' in currUser.roles or 'SUPERUSER' in currUser.roles):
        products = db.query(Product).all()
        if (products == []):
            raise HTTPException (status_code=404, detail="No products found")
        return products
    else:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!!")


@router.get("/{id}", response_model=ProductOutput)
def getByid (id, currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
        if ('INVENTORY_MANAGER' in currUser.roles or 'ADMIN' in currUser.roles or 'SUPERUSER' in currUser.roles):
            product = db.query(Product).filter(Product.id == id).first()
            if (product is None):
                raise HTTPException (status_code=404, detail="Product not found")
            return product
        else:
            raise HTTPException (status_code=403, detail="you have no privileges !!!!!")


@router.put ("/{id}", response_model=ProductOutput)
def updateProduct (id, prod : ProductInput, currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
        if ('INVENTORY_MANAGER' in currUser.roles or 'ADMIN' in currUser.roles or 'SUPERUSER' in currUser.roles):
            product_query = db.query(Product).filter(Product.id == id)
            product = product_query.first()
            if (product is None):
                raise HTTPException (status_code=404, detail="Product not found")
            else:
                prodInput = prod.model_dump()
                category = db.query(Category).filter(Category.name == prod.category_name).first()
                prodInput.pop("category_name")
                prodInput["category_id"] = category.id
                product_query.update(prodInput, synchronize_session=False)
                db.commit()
                # db.refresh(product_query.first())
                return product_query.first()
            

@router.delete ("/{id}")
def deleteProduct (id, currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
    if ('INVENTORY_MANAGER' in currUser.roles or 'ADMIN' in currUser.roles or 'SUPERUSER' in currUser.roles):
        product = db.query(Product).filter(Product.id == id).first()
        if (product is None):
            raise HTTPException (status_code=404, detail="Product not found !!!!!")
        db.delete(product)
        db.commit()
        return {"message" : "Product deleted successfully !!!!!"} 
    else:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!!")
            


