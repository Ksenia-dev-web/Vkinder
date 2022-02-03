import requests
import vk as vk
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime
import time
from model import *
from db import *


class MakeMatches:
    def __init__(self, _id):
        self.id = id
        self.version = '5.131'
        with open('txt/token.txt', encoding='UTF-8') as file:
            self.token = file.readline()
        self.params = {
            'access_token': self.token,
            'v': self.version,
        }

        self.url = 'https://api.vk.com/method/'

    def make_matches(self):
#         ?????????????????????????
