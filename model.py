import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date

with open('txt/DB_U.txt', encoding='utf-8') as f:
    db_uri = f.readline()
Base = declarative_base()
engine = create_engine(db_uri)

Session = sessionmaker(bind=engine)

session = Session()
con = engine.connect()


#CLIENT OF VK BOT
class User(Base):
    __tablename__ == 'user'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    name = sq.Column(sq.String)
    surname = sq.Column(sq.String)
    bdate = sq.Column(sq.Date)
    relation = sq.Column(sq.Integer)
    sex = sq.Column(sq.Integer)
    city = sq.Column(sq.String)
    country = sq.Column(sq.String)
    interests = sq.Column(sq.String)
    groups = sq.Column(sq.String)


class MatchedUser(Base):
    __tablename__ = 'matched_user'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String)
    surname = sq.Column(sq.String)
    city = sq.Column(sq.String)
    link = sq.Column(sq.String)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user_id', ondelete='CASCADE'))


class Photoes(Base):
    __tablename__ = 'photoes'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    link_photo = sq.Column(sq.String)
    likes_amount = sq.Column(sq.Integer)
    id_matched_user = sq.Column(sq.Integer, sq.ForeignKey('matched_user_id', ondelete='CASCADE'))
