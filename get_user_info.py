import requests
import vk as vk
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime
import time
from model import *
from db import *
from vk_api.exceptions import ApiError


#API VK work
with open('txt/token.txt', encoding='utf-8') as f:
    token = f.readline()

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)

# DB work
session = Session()
con = engine.connect()

# search for suitable users
def search_for_matches(sex, start_age, max_age, city):
    list_of_all = []
    profile_link = 'https://vk.com/id'
    vk1 = vk_api.VkApi(token = token)
    response = vk1.method('users.search',
                          {'sort': 1,
                           'sex': sex,
                           'status': 1,
                           'age_from': start_age,
                           'age_to': max_age,
                           'has_photo': 1,
                           'count': 25,
                           'online': 1,
                           'hometown': city
                           })
    for ind in response['items']:
        profile = [
           ind['first_name'],
           ind['surname'],
            profile_link + str(ind['id']),
            ind['id']
        ]
        list_of_all.append(profile)
    return list_of_all


def get_photo(user_owner_id):
    vk1 = vk_api.VkApi(token=token)
    try:
        response = vk1.method('photos.get',
                              {
                                  'access_token': token,
                                  'v': 5.131,
                                  'owner_id': user_owner_id,
                                  'album_id': 'profile',
                                  'count': 10,
                                  'extended': 1,
                                  'photo_sizes': 1,
                              })
    except ApiError:
        return 'no access to photo'
    users_photoes = []
    for i in range(11):
        try:
            users_photoes.append(
                [response['items'][i]['likes']['count'],
                 'photo' + str(response['items'][i]['owner_id']) + '_' + str(response['items'][i]['id'])]
            )
        except IndexError:
            users_photoes.append(['no photoes'])
    return users_photoes


def sort_by_likes(photoes):
    count_likes = []
    for ind in photoes:
        if ind != ['no photoes'] and photoes != 'no access to photo':
            count_likes.append(ind)
    return sorted(count_likes)


