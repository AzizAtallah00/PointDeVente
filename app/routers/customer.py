from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import CustomerOutput, CustomerInput, TokenData
from ..oauth2 import getCurrentUser 
from ..database import get_db
from ..models import Customer

router = APIRouter(
    prefix="/customers",
    tags=["Customer"]
)

@router.post("/", response_model=CustomerOutput)
def addCustomer (cus : CustomerInput, currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
    if ('ADMIN' in currUser.roles or 'VENDOR' in currUser.roles or 'SUPERUSER' in currUser.roles):
        customer = Customer(**cus.model_dump())
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer
    else:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!!")


@router.get("/", response_model=List[CustomerOutput])
def getAll (currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db), limit : int = 10, offset : int = 0, search : Optional[str] = ""):
    if ('ADMIN' in currUser.roles or 'VENDOR' in currUser.roles or 'SUPERUSER' in currUser.roles):
        customers = db.query(Customer).filter(Customer.name.contains(search)).limit(limit).offset(offset).all()
        if customers == []:
            raise HTTPException (status_code=404, detail="Customer not found !!!!!")
        return customers
    else:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!!")
    

@router.put("/{id}", response_model=CustomerOutput)
def updateCustomer (id, cus:CustomerInput, currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
    if ('ADMIN' in currUser.roles or 'VENDOR' in currUser.roles or 'SUPERUSER' in currUser.roles):
        customer_query = db.query(Customer).filter(Customer.id == id)
        if customer_query.first() is None:
            raise HTTPException(status_code=404, detail="Customer not found !!!!!")
        customer_query.update(cus.model_dump(), synchronize_session=False)
        db.commit()
        db.refresh(customer_query.first())
        return customer_query.first()
    else:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!!")


@router.delete("/{id}")
def deleteCustomer (id, currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
    if ('ADMIN' in currUser.roles or 'VENDOR' in currUser.roles or 'SUPERUSER' in currUser.roles):
        customer = db.query(Customer).filter(Customer.id == id).first()
        if ( customer is None):
            raise HTTPException(status_code=404, detail="Customer not found !!!!!")
        db.delete(customer)
        db.commit()
        return {"message" : "Customer deleted successfully !!!!"}
    else:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!!")