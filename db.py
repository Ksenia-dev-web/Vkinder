from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base


with open('txt/DB_U.txt', encoding='utf-8') as f:
    db_uri = f.readline()

engine = create_engine(db_uri)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
s = Session()


def add_client(user_id, data, offset=0):
    session = Session()
    user = session.query(User).filter(User.user_vk_id == user_id).first()
    if not user:
        user_vk_id = User(user_vk_id=user_id, data=data, offset=offset)
        session.add(user_vk_id)
        session.commit()
    return

