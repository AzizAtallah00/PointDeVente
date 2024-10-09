from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import CategoryInput,CategoryOutput, TokenData
from ..database import get_db
from ..oauth2 import getCurrentUser
from ..models import Category


router = APIRouter(
    prefix="/categories",
    tags=["category"]
)

@router.post("/", response_model=CategoryOutput)
def addCategory (cat : CategoryInput, currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
        if ('INVENTORY_MANAGER' in currUser.roles or 'ADMIN' in currUser.roles or 'SUPERUSER' in currUser.roles):
            category = Category(**cat.model_dump())
            db.add(category)
            db.commit()
            db.refresh(category)
            return category
        else:
            raise HTTPException (status_code=403, detail="you have no privileges !!!!!")


@router.get("/", response_model=List[CategoryOutput])
def getAll (currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db), limit : int = 10, offset : int = 0, search : Optional[str] = ""):
    if ('INVENTORY_MANAGER' in currUser.roles or 'ADMIN' in currUser.roles or 'SUPERUSER' in currUser.roles):
        categories = db.query(Category).filter(Category.name.contains(search)).limit(limit).offset(offset).all()
        if categories == []:
            raise HTTPException (status_code=404, detail="Customer not found !!!!!")
        return categories
    else:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!!")
    

@router.put("/{id}", response_model=CategoryOutput)
def updateCustomer (id, cat:CategoryInput, currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
    if ('INVENTORY_MANAGER' in currUser.roles or 'ADMIN' in currUser.roles or 'SUPERUSER' in currUser.roles):
        category_querry = db.query(Category).filter(Category.id == id)
        if category_querry.first() is None:
            raise HTTPException(status_code=404, detail="Customer not found !!!!!")
        category_querry.update(cat.model_dump(), synchronize_session=False)
        db.commit()
        db.refresh(category_querry.first())
        return category_querry.first()
    else:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!!")


@router.delete("/{id}")
def deleteCustomer (id, currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
    if ('INVENTORY_MANAGER' in currUser.roles or 'ADMIN' in currUser.roles or 'SUPERUSER' in currUser.roles):
        category = db.query(Category).filter(Category.id == id).first()
        if ( category is None):
            raise HTTPException(status_code=404, detail="category not found !!!!!")
        db.delete(category)
        db.commit()
        return {"message" : "category deleted successfully !!!!"}
    else:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!!")


