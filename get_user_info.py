import requests
import vk as vk
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime
import time
from model import *
from db import *


class GetClientInfo:
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
        session = Session()
        db_of_users = session.query(User).filter(User.id == self.id).first()
        if not db_of_users:
            data_to_collect = ['name', 'surname', 'bdate', 'relation', 'sex', 'city', 'country', 'interests', 'groups']
            self.data = requests.get(self.url + 'users.get',
                                     params={**self.params, **{'user_ids': self.id, 'fields': ', '.join(data_to_collect)
                                                               }
                                             }).json()['response'][0]
            add_client(self.id, self.data)
        else:
            self.data = db_of_users

        def ask_client_about_prefs(user_id, message):
            vk.method('messages.send',
                      {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)}



        def client_prefs(self):
            vk_session1 = vk_api.VkApi(token=self.token)
            longpoll1 = VkLongPoll(vk_session1)
            for event2 in longpoll1.listen():
                for item in data_to_collect:
                    if item[3] not in self.data or item[3].split == 2:
                        ask_client_about_prefs(id, 'Уточните дату рождения в формате ДД.ММ.ГГГГ')
                        if event2.type == VkEventType.MESSAGE_NEW and event2.to_me and event2.text.split == 4:
                            self.data[3].append
                            ask_client_about_prefs(id, 'Отлично, информация заполнена')

                        session.query(User).filter(User.user_vk_id == self.id).update({"bdate": self.data[3]})
                        session.commit()

                    elif item[4] not in self.data:
                        ask_client_about_prefs(id, 'А что с семейным положением?')
                        if event2.type == VkEventType.MESSAGE_NEW and event2.to_me and event2.text == 'не женат' or event2.text == 'не замужем':
                            self.data['relation'] = 1
                            ask_client_about_prefs(id, 'Отлично, информация заполнена')
                        elif event2.type == VkEventType.MESSAGE_NEW and event2.to_me and event2.text == 'есть друг' or event2.text == 'есть подруга':
                            self.data['relation'] = 2
                            ask_client_about_prefs(id, 'Отлично, информация заполнена')
                        elif event2.type == VkEventType.MESSAGE_NEW and event2.to_me and event2.text == 'помолвлен' or event2.text == 'помолвлена':
                            self.data['relation'] = 3
                            ask_client_about_prefs(id, 'Отлично, информация заполнена')
                        elif event2.type == VkEventType.MESSAGE_NEW and event2.to_me and event2.text == 'женат' or event2.text == 'замужем':
                            self.data['relation'] = 4
                            ask_client_about_prefs(id, 'Отлично, информация заполнена')
                        elif event2.type == VkEventType.MESSAGE_NEW and event2.to_me and event2.text == 'всё сложно':
                            self.data['relation'] = 5
                            ask_client_about_prefs(id, 'Отлично, информация заполнена')
                        elif event2.type == VkEventType.MESSAGE_NEW and event2.to_me and event2.text == 'в активном поиске':
                            self.data['relation'] = 6
                            ask_client_about_prefs(id, 'Отлично, информация заполнена')
                        elif event2.type == VkEventType.MESSAGE_NEW and event2.to_me and event2.text == 'влюблён' or event2.text == 'влюблена':
                            self.data['relation'] = 7
                            ask_client_about_prefs(id, 'Отлично, информация заполнена')
                        elif event2.type == VkEventType.MESSAGE_NEW and event2.to_me and event2.text == 'в гражданском браке':
                            self.data['relation'] = 8
                            ask_client_about_prefs(id, 'Отлично, информация заполнена')

                        else:
                            return 'Простите, нужно уточнение информации'

                        session.query(User).filter(User.user_vk_id == self.id).update({"relation": self.data[4]})
                        session.commit()

                    elif item[5] not in self.data:
                        ask_client_about_prefs(id, 'Укажите Ваш пол')
                        if event2.type == VkEventType.MESSAGE_NEW and event2.to_me and event2.text == 'мужской':
                            self.data['sex'] = 2
                            ask_client_about_prefs(id, 'Отлично, информация заполнена')
                        elif event2.type == VkEventType.MESSAGE_NEW and event2.to_me and event2.text == 'женский':
                            self.data['sex'] = 1
                            ask_client_about_prefs(id, 'Отлично, информация заполнена')

                        session.query(User).filter(User.user_vk_id == self.id).update({"sex": self.data[5]})
                        session.commit()

                    elif item[6] not in self.data:
                        ask_client_about_prefs(id, 'Укажите Ваш город')
                        if event2.type == VkEventType.MESSAGE_NEW and event2.to_me and event2.text:
                            self.data['city'] = event2.text
                            ask_client_about_prefs(id, 'Отлично, информация заполнена')

                        session.query(User).filter(User.user_vk_id == self.id).update({"city": self.data[6]})
                        session.commit()

                    elif item[7] not in self.data:
                        ask_client_about_prefs(id, 'Укажите Вашу страну')
                        if event2.type == VkEventType.MESSAGE_NEW and event2.to_me and event2.text:
                            self.data['country'] = event2.text
                            ask_client_about_prefs(id, 'Отлично, информация заполнена')

                        session.query(User).filter(User.user_vk_id == self.id).update({"country": self.data[7]})
                        session.commit()
                    session.query(User).filter(User.user_vk_id == self.id).update({"groups": self.data[8]})
                    session.commit()
                    session.query(User).filter(User.user_vk_id == self.id).update({"interests": self.data[9]})
                    session.commit()










