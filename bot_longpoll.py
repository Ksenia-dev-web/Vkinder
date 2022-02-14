import vk as vk
from get_user_info import *
from model import *
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

#API VK work
with open('txt/token.txt', encoding='utf-8') as f:
    token = f.readline()

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)

# DB work
session = Session()
con = engine.connect()


def write_msg(user_id, message, attachment=None):
    vk.method('messages.send',
              {'user_id': user_id,
               'message': message,
               'random_id': randrange(10 ** 7),
               'attachment': attachment})


def bot():
    for event1 in longpoll.listen():
        if event1.type == VkEventType.MESSAGE_NEW:
            if event1.to_me:
                text_of_message = event1.text
                return text_of_message, event1.user_id


def dialog(client_id):
    write_msg(client_id,
              f"Welcome to dating bot VKinder\n"
              f"\nIf it's your first time to use this bot - sign in.\n"
              f"\nIf you are already - let's start searching\n")


def sign_in_new(client_id):
    write_msg(client_id, 'Ok, ready to start')
    sign_in(client_id)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            text == event.text.lower()
            user = GetClientInfo(event.user_id)
            if text == 'hi' or text == 'привет' or text == 'здравствуйте':
                dialog(event.user_id, f"Здравствуйте, {event.user_id}")
            elif text == 'не нужно' or text == 'до свидания':
                dialog(event.user_id, "Возможно, в другой раз?")
            elif text == 'подбери мне пару':
                dialog(event.user_id, "Отлично, давайте начинать. Для начала я посмотрю Вашу информацию")
                user = GetClientInfo(event.user_id)


