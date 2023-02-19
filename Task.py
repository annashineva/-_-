from pprint import pprint

import requests

url = 'http://api.vk.com/method/photos.get'
token = ''
params = {
    'owner_id': input('Введите id пользователя vk '),
    'album_id': 'wall',
    'extended': '1',
    'access_token': token,
    'v': '5.131'
}
res = requests.get(url, params=params).json()
pprint(res)


def max_sizes(self, album):
    vk_sizes = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
    p = []
    for photo in album:
        size = max(photo['sizes'], key=lambda x: vk_sizes[x['type']])
        p.append(size)
        return size


def upload_file_to_disk(self, path_to_file, file_name):
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {'Content-Type': 'application/json', 'Authorization': 'OAuth {}'.format(self.token)}
    params = {"path": path_to_file, "overwrite": "true"}
    href = requests.get(upload_url, headers=headers, params=params, path_to_file=path_to_file)
    with open(file_name, 'rb') as file:
        response = requests.put(href, file)
        response.raise_for_status


if __name__ == '__main__':
    path_to_file = max_sizes()
    token = input("Введите токен с Полигона Яндекс.Диска")
    file_name = res['items']['likes']
    result = upload_file_to_disk(path_to_file, file_name)
