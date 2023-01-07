from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from server.database import Base

class DepotUser(Base):
    __tablename__ = 'depot_users'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    username = Column(String(64), unique=True, nullable=False)
    passwd = Column(String(256), unique=True, nullable=False)
    files = relationship('DepotFile')

class DepotFile(Base):
    filename = Column(String(64), unique=True, nullable=False)
