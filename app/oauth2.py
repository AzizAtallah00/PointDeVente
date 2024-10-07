from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
import jwt
from .schemas import TokenData
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from .config import Settings
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
settings = Settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def createToken (data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm =ALGORITHM)
    return {"token" : encoded_jwt, "type" : "bearer"}

def verifyToken (token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("employee_id")
        roles : list = payload.get("roles")
        if id == None:
            raise credentials_exception
        token_data = TokenData(id=id, roles=roles)
    except InvalidTokenError:
        raise credentials_exception
    return token_data
    
def getCurrentUser (token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verifyToken(token, credentials_exception)