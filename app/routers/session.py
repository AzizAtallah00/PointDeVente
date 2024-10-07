from fastapi import Depends, APIRouter, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import getCurrentUser
from ..schemas import TokenData, SessionOutput
from ..models import Session
from ..enum import SessionStatus, Role



router = APIRouter(
    prefix = "/sessions",
    tags = ["Sessions"]
)

@router.post("/open", response_model=SessionOutput)
def openSession (currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
    if 'INVENTORY_MANAGER' in currUser.roles:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!")
    session_opened = Session (employee_id = currUser.id, opened_at = datetime.now().date(), session_status = SessionStatus.OPEN)
    db.add(session_opened)
    db.commit()
    db.refresh(session_opened)
    return session_opened

@router.post("/pause/{id}", response_model=SessionOutput)
def openSession (id, currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
    if 'INVENTORY_MANAGER' in currUser.roles:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!")
    session_opened = db.query(Session).filter(Session.id == id).first()
    if session_opened is None:
        raise HTTPException (status_code=404, detail="session not found !!!!!")
    if session_opened.employee_id != currUser.id:
        raise HTTPException (status_code=403, detail= "you have no privileges to this session !!!!")
    if session_opened.session_status == SessionStatus.CLOSED:
        raise HTTPException (status_code=403, detail= "session is closed !!!!!")
    session_opened.session_status = SessionStatus.PAUSED
    db.commit()
    db.refresh(session_opened)
    return session_opened

@router.post ("/reopen/{id}", response_model=SessionOutput)
def reopenSession (id, currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
    if 'INVENTORY_MANAGER' in currUser.roles:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!")
    session_opened = db.query(Session).filter(Session.id == id).first()
    if session_opened is None:
        raise HTTPException (status_code=404, detail="session not found !!!!!")
    if session_opened.employee_id != currUser.id:
        raise HTTPException (status_code=403, detail= "you have no privileges to this session !!!!")
    match session_opened.session_status:
        case SessionStatus.CLOSED :
            raise HTTPException (status_code=403, detail="session is closed !!!!!")
        case SessionStatus.OPEN:
            raise HTTPException (status_code=403, detail="session is opened !!!!!!")
        case SessionStatus.PAUSED:
            session_opened.session_status = SessionStatus.OPEN
            db.commit()
            db.refresh(session_opened)
            return session_opened
        

@router.post ("/close/{id}", response_model=SessionOutput)
def closeSession (id, currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
    if 'INVENTORY_MANAGER' in currUser.roles:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!")
    session_opened = db.query(Session).filter(Session.id == id).first()
    if session_opened is None:
        raise HTTPException (status_code=404, detail="session not found !!!!!")
    if session_opened.employee_id != currUser.id:
        raise HTTPException (status_code=403, detail= "you have no privileges to this session !!!!")
    match session_opened.session_status:
        case SessionStatus.CLOSED :
            raise HTTPException (status_code=403, detail="session is closed !!!!!")
        case _:
            session_opened.session_status = SessionStatus.CLOSED
            db.commit()
            db.refresh(session_opened)
            return session_opened


@router.get("/", response_model=list[SessionOutput])
def getAll (currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
    if "ADMIN" in currUser.roles or "SUPERUSER" in currUser.roles : 
        sessions = db.query(Session).all()
        return sessions
    else:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!!")
    
@router.delete("/{id}")
def deleteSession(id, currUser : TokenData = Depends(getCurrentUser), db : Session = Depends(get_db)):
    if "ADMIN" in currUser.roles or "SUPERUSER" in currUser.roles : 
        session = db.query(Session).filter(Session.id == id).first()
        db.delete(session)
        db.commit()
        return {"message" : "Session deleted Successfully !!!!"}
    else:
        raise HTTPException (status_code=403, detail="you have no privileges !!!!!")