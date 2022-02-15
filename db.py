from bot_longpoll import write_msg
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from model import *
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from sqlalchemy.exc import IntegrityError, InvalidRequestError


with open('txt/DB_U.txt', encoding='utf-8') as f:
    db_uri = f.readline()

Base = declarative_base()
engine = create_engine(db_uri)

Session = sessionmaker(bind=engine)

with open('txt/token.txt', encoding='utf-8') as f:
    token = f.readline()

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)

session = Session()
con = engine.connect()


# REGISTER NEW CLIENT
def sign_in(vk_id):
    try:
        new_user = User(
            vk_id=vk_id
        )
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        return False


# TO ADD LIKED USER TO DB
def add_user(event_id, vk_id, first_name, surname, city, link, id_user):
    try:
        new_user = MatchedUser(
            vk_id=vk_id,
            f_name=first_name,
            s_name=surname,
            city=city,
            link=link,
            id_user=id_user
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id, 'ADDED USER TO MATCH')
        return True
    except(IntegrityError, InvalidRequestError):
        write_msg(event_id, 'Already in the list')
        return False


# TO ADD PHOTO OF THE MATCH TO DB
def add_match_photo(event_id, link_photo, likes_amount, id_match_user):
    try:
        new_user = Photoes(
            link_photo=link_photo,
            likes_amount=likes_amount,
            id_match_user=id_match_user
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id, 'PHOTOES OF MATCH ADDED TO DB')
        return True
    except(IntegrityError, InvalidRequestError):
        write_msg(event_id, 'COULD NOT SAVE PHOTOES')
        return False


# TO REMOVE FROM MATCHES
def remove_from_matches(id_):
    this_user = session.query(MatchedUser).filter_by(vk_id=id_).first()
    session.delete(this_user)
    session.commit()


# CHECK IF USER IS IN MATCHES ALREADY
def is_in_matched_users(ids):
    this_user_id = session.query(User).filter_by(vk_id=ids).first()
    all_list = session.query(User).filter_by(vk_id=this_user_id).first()
    return all_list


if __name__ == '__main__':
    Base.metadata.create_all(engine)






