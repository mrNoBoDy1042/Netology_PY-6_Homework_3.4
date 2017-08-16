import requests
from urllib.parse import urlencode
import json

AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
APP_ID = 6149348
VERSION = '5.67'

auth_data = {
    'client_id': APP_ID,
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'display': 'mobile',
    'scope': 'friends',
    'response_type': 'token',
    'v': VERSION
}

# Получаем ссылку для токена
print('Получение доступа к информации пользователя:')
print('?'.join(
    (AUTHORIZE_URL, urlencode(auth_data))
))

# Читаем токен из config.json
with open('config.json') as f:
    token = json.load(f)['token']

params = {
    'access_token': token,
    'v': VERSION
}
# Получаем список друзей и сохраняем его в friends_list
response = requests.get('https://api.vk.com/method/friends.get', params)
friends_list = response.json()['response']['items']

# Получаем список друзей для каждого друга из friends_list и сохраняем в словарь в виде множества
# ключ: id друга, значение: множество его друзей
friends_of_friends = {}
for friend in friends_list:
    params = {
        'access_token': token,
        'user_id': friend,
        'v': VERSION
    }
    response = requests.get('https://api.vk.com/method/friends.get', params)
    friends_of_friends[friend] = set(response.json()['response']['items'])

# Создаем множество общих друзей и
# находим пересечения множеств friends_list со множеством друзей из словаря friends_of_friends
friends_list = set(friends_list)
common_friends = set()
for friends in friends_of_friends.values():
    for friend_id in (friends_list & friends):
        common_friends.add(friend_id)

# Получаем имя и фамилию для каждого общего друга
for friend in common_friends:
    params = {
        'access_token': token,
        'user_ids': friend,
        'v': VERSION
    }
    response = requests.get('https://api.vk.com/method/users.get', params)
    print('Имя: {0}   Фамилия: {1}'.format(
        response.json()['response'][0]['first_name'], response.json()['response'][0]['last_name']))

