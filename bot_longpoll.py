import vk as vk
from get_user_info import *
from model import *
from random import randrange
import vk_api
from get_user_info import search_for_matches, make_json, get_photo, sort_by_likes
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


def use_matched_users_list(ids):
    all_list = is_in_matched_users(ids)
    write_msg(ids, f'Your matches:')
    for index, users in enumerate(all_list):
        write_msg(ids, f'{users.first_name}, {users.surname}, {users.link}')
        write_msg(ids, '1 - delete from list, 0 - Forward, \nq- Exit')
        msg_texts, user_ids = bot()
        if msg_texts == '0':
            if index >= len(all_list) - 1:
                write_msg(user_ids, f'That was the last match\n'
                          f'Vkinder - go back to menu\n')
        elif msg_texts == '1':
            remove_from_matches(users.vk_id)
            write_msg(user_ids, f'Match deleted from the list')
            if index >= len(all_list) - 1:
                write_msg(user_ids, f'The last match\n'
                          f'Vkinder - go back to menu\n')
        elif msg_texts.lower() == 'q':
            write_msg(ids, 'Vkinder - start')
            break


if __name__ == '__main__':
    while True:
        msg_text, user_id = bot()
        if msg_text == 'hi' or msg_text == 'vkinder':
            dialog(user_id)
            msg_text, user_id = bot()
            # client sign in
            if msg_text.lower() == 'yes' or msg_text.lower() == 'да':
                sign_in(user_id)
            # look for matches
            elif len(msg_text) > 1:
                sex = 0
                if msg_text[0:7].lower() == 'женский':
                    sex = 1
                elif msg_text[0:7].lower() == 'мужской':
                    sex = 2
                start_age = msg_text[8:10]
                max_age = msg_text[11:14]
                city = msg_text[14:len(msg_text)].lower()
                # search matches
                result = search_for_matches(sex, int(start_age), int(max_age), city)
                make_json(result)
                this_user_id = is_in_matched_users(user_id)
                # form list of matches
                for i in range(len(result)):
                    matched_user = is_in_matched_users(result[i][3])
                    # get photoes
                    user_photo = get_photo(result[i][3])
                    if user_photo == 'нет доступа к фото' or matched_user is not None:
                        continue
                    sorted_user_photo = sort_by_likes(user_photo)
                    # print sorted data
                    write_msg(user_id, f'\n{result[i][0]} {result[i][1]} {result[i][2]}')
                    try:
                        write_msg(user_id, f'фото',
                                  attachment=','.join([sorted_user_photo[-1][1], sorted_user_photo[-2][1], sorted_user_photo[-3][1]]))
                    except IndexError:
                        for photo in range(len(sorted_user_photo)):
                            write_msg(user_id, f'фото:', attachment=sorted_user_photo[photo][1])
                    write_msg(user_id, '1 - add, 2 - remove, 0 - next\nq - quit')
                    msg_text, user_id = bot()
                    if msg_text == '0':
                        if i >= len(result) - 1:
                            dialog()
#                     add to matches
                    elif msg_text == '1':
                        if i >= len(result) - 1:
                            dialog()
                            break
                        try:
                            add_user(user_id, result[i][3], result[i][1], result[i][0], city, result[i][2], this_user_id.id)
                            add_match_photo(user_id, sorted_user_photo[0][1], sorted_user_photo[0][0], this_user_id.id)
                        except AttributeError:
                            write_msg(user_id, 'You are not signed in, write "hi" or "привет" to sign in vkinder')
                            break
                    elif msg_text.lower() == 'q':
                        write_msg(user_id, 'Goodbye!')
                        break

