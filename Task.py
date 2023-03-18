import json
from datetime import datetime

import requests

import time

from tqdm import tqdm


class VkUser:

    def __init__(self, vk_token, user_id, count_photo):
        self.url = 'https://api.vk.com/method/'
        self.params = {
            'access_token': vk_token,
            'v': '5.131'
        }
        self.user_id = user_id
        self.count_photo = count_photo

    def get_photos(self, album_id=-6):
        url = self.url + '/photos.get'
        params = {
            'owner_id': self.user_id,
            'album_id': album_id,
            'count': self.count_photo,
            'rev': 1,
            'extended': 1,
            'photo_sizes': 1,
            'access_token': self.params['access_token'],
            'v': '5.131'
        }
        response = requests.get(url, params=params)
        data = json.loads(response.text)['response']['items']
        photos_info = []
        for photo in tqdm(data):
            time.sleep(0.15)
            if 'likes' in photo:
                file_name = f"{photo['likes']['count']}_{datetime.fromtimestamp(photo['date']).strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
            else:
                file_name = f"{datetime.fromtimestamp(photo['date']).strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
            size_dict = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
            size_max = max(photo['sizes'], key=lambda x: size_dict[x['type']])
            size = size_max['type'].upper()
            photos_info.append({'file_name': file_name, 'size': size})
        return photos_info

    def sort_photos(self):
        self.photos = sorted(self.photos, key=lambda x: (x['file_name'], x['size']))

    def save_photos_info(self, file_name='photos_info.json'):
        with open(file_name, 'w') as f:
            json.dump(self.photos, f, ensure_ascii=False, indent=4)



class YaDisc:
    files_url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self):
        with open('ya_token.ini', 'r', encoding='utf-8') as file:
            self.ya_token = file.read().strip()
        self.yandex_folder = input('Введите название новой папки куда сохранить фото: ')
        self.photo_urls = []

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.ya_token)
        }

    def create_folder(self):
        headers = self.get_headers()
        params = {"path": self.yandex_folder, "overwrite": "true"}
        response = requests.put(self.files_url, headers=headers, params=params)
        if response.status_code == 201:
            print(f'Папка: {self.yandex_folder} успешно создана на Yandex Disk')
        else:
            print(f'Что-то пошло не так! Посмотрите код ошибки: {response.status_code}')



    def upload_file(self, file_url, file_name):
        headers = self.get_headers()
        upload_url = f"{self.files_url}/upload"
        params = {"path": f"{self.yandex_folder}/{file_name}", "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        if response.status_code == 200:
            href = response.json().get("href")
            response = requests.post(href, data=requests.get(file_url).content)
            if response.status_code == 201:
                print(f"Файл {file_name} успешно загружен на Яндекс.Диск")
            else:
                print(f"Не удалось загрузить файл {file_name} на Яндекс.Диск. Код ошибки: {response.status_code}")
        else:
            print(f"Не удалось получить URL для загрузки файла {file_name} на Яндекс.Диск. Код ошибки: {response.status_code}")




if __name__ == '__main__':
    with open('vk_token.ini', 'r', encoding='utf-8') as file:
        vk_token = file.read().strip()

    user_id = int(input('Введите id вашего профиля в вк: '))
    count_photo = int(input('Введите кол-во фотографий: '))

    user = VkUser(vk_token, user_id, count_photo)
    photos = user.get_photos()
    user.photos = photos
    user.sort_photos()
    user.save_photos_info()
    user.sort_photos()
    ya = YaDisc()
    ya.create_folder()
    for photo in tqdm(photos):
        time.sleep(0.15)
        print(photo)
        url = photo.get('url')
        file_name = photo['file_name']
        if url and file_name:
            ya.upload_file(url, file_name)
        else:
            print('Не удалось загрузить фото:', photo)

