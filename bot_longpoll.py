import vk as vk
from get_user_info import GetClientInfo
from get_user_info import *
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

with open('txt/token.txt', encoding='utf-8') as f:
    token = f.readline()

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)


def dialog(user_id, message, attachment=''):
    vk.method('messages.send',
              {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), 'attachment': attachment})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            answer == event.text.lower()
            user = GetClientInfo(event.user_id)
            if answer == 'hi' or answer == 'привет' or answer == 'здравствуйте':
                dialog(event.user_id, f"Здравствуйте, {event.user_id}")
            elif answer == 'не нужно' or answer == 'до свидания':
                dialog(event.user_id, "Возможно, в другой раз?")
            elif answer == 'подбери мне пару':
                dialog(event.user_id, "Отлично, давайте начинать. Для начала я посмотрю Вашу информацию")
                user = GetClientInfo(event.user_id)


