from datetime import datetime
import os
from typing import List

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from ..database import Base, get_db
from ..schemas import EmployeeInput, EmployeeOutput, EmployeeLogin, PasswordReset
from ..models import Employee, EmployeeRole, AccountActivation, ChangePassword
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..emailConfig import EmailSchema, send_with_template 
from ..config import Settings
from ..enum import AccountStatus, TokenStatus
from ..oauth2 import createToken
from passlib.context import CryptContext




router = APIRouter(
    prefix="/employees",
    tags=["employee"],
)

settings = Settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
serializer = URLSafeTimedSerializer(settings.SECRET_KEY)


@router.post("/login")
def login(emp : EmployeeLogin, db :Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.email == emp.email).first()
    if (employee is None):
        raise HTTPException(status_code=404, detail="Employee not found")
    if not pwd_context.verify (emp.password, employee.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    # get jwt token
    roles = db.query(EmployeeRole.role).filter(EmployeeRole.employeeId == employee.id).all()
    return createToken ({'employee_id': employee.id, 'roles':[role.role.name for role in roles] })


@router.post("/",response_model=EmployeeOutput)
async def createEmployee (emp : EmployeeInput, db : Session = Depends(get_db)):
    if (emp.password != emp.confirm_password): 
        raise HTTPException (status_code=400, detail ="passwords do not match")
    emp.password = pwd_context.hash(emp.password)
    emp_dict = emp.dict()
    emp_dict.pop("confirm_password")
    emp_dict.pop("roles")
    emp1 = Employee(**emp_dict)       
    db.add(emp1)
    db.commit()
    db.refresh(emp1)
    
    # add roles
    for role in emp.roles:
        role = EmployeeRole (employeeId=emp1.id, role=role)
        db.add(role)
        db.commit()
    
    # Generate confirmation token
    token = serializer.dumps(emp1.email, salt='email-confirm')
    activationAccount = AccountActivation(employeeId=emp1.id, email=emp1.email, status=TokenStatus.PENDING, token = token )
    db.add(activationAccount)
    db.commit()
    db.refresh(activationAccount)
    confirm_url = f"http://{settings.DATABASE_HOST}:8000/employees/confirm/{activationAccount.token}"
    
    # send confirmation email
    emails = EmailSchema(email = [emp1.email], body={"activation_link": confirm_url , "name" : emp1.first_name})
    await send_with_template(emails, "activation_account.html")
    
    return emp1

@router.get("/confirm/{token}")
async def confirm_email(token: str, db: Session = Depends(get_db)):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="The confirmation link has expired.")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid confirmation token.")
    
    employee = db.query(Employee).filter(Employee.email == email).first()
    accountActivation = db.query(AccountActivation).filter(AccountActivation.token == token).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    if not accountActivation:
        raise HTTPException(status_code=404, detail="accountActivation not found.")
    
    employee.account_status = AccountStatus.ACTIVE
    accountActivation.status = TokenStatus.USED
    db.commit()
    
    return {"message": "Email confirmed, account activated."}
    
    
@router.post("/forgot-password")
async def forgot_password(email: str, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.email == email).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Generate password reset token
    token = serializer.dumps(employee.email, salt='password-reset')
    reset_token = ChangePassword(employeeId=employee.id, token=token, email=email, status=TokenStatus.PENDING)
    db.add(reset_token)
    db.commit()
    
    # Send password reset email
    reset_url = f"http://{settings.DATABASE_HOST}:8000/employees/reset-password/{token}"
    emails = EmailSchema(email=[employee.email], body={"reset_link": reset_url, "name": employee.first_name})
    await send_with_template(emails, "reset_password.html")
    
    return {"message": "Password reset email sent"}

@router.post("/reset-password/{token}")
async def reset_password(token: str, request: PasswordReset, db: Session = Depends(get_db)):
    try:
        email = serializer.loads(token, salt='password-reset', max_age=3600)
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="The reset link has expired.")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid reset token.")
    
    employee = db.query(Employee).filter(Employee.email == email).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    
    # Verify token
    reset_token = db.query(ChangePassword).filter(ChangePassword.token == token).first()
    # if not reset_token or reset_token.expires_at < datetime.utcnow():
    #     raise HTTPException(status_code=400, detail="Invalid or expired reset token.")
    
    # Update password
    employee.password = pwd_context.hash(request.new_password)
    db.commit()
    
    # Update the used token
    reset_token.status = TokenStatus.USED
    db.commit()
    
    return {"message": "Password reset successful"}


@router.get("/", response_model=List[EmployeeOutput])
def getEmployees (db : Session = Depends(get_db)):
    return db.query(Employee).all()

@router.get("/{id}", response_model=EmployeeOutput)
def getEmployeeById (id : int, db : Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == id).first()
    if emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

