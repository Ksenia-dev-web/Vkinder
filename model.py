import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class User(Base):
    __tablename__ == 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    bdate = Column(Date)
    relation = Column(Integer)
    sex = Column(Integer)
    city = Column(String)
    country = Column(String)
    interests = Column(String)
    groups = Column(String)
    offset = Column(Integer)

