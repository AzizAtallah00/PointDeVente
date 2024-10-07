from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class JwtBlacklist(Base):
    __tablename__ = "jwt_blacklist"
    
    id = Column (Integer, primary_key = True)
    token = Column (String, nullable = False)