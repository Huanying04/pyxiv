import requests
import pyxiv
from artwork_info import IllustrationInfo


def get_artwork_info(artwork_id: int):
    header = {
        'Referer': 'https://www.pixiv.net',
        'cookie': f'PHPSESSID={pyxiv.get_php_sessid()}',
        'user-agent': pyxiv.get_user_agent()
    }
    r = requests.get(f'https://www.pixiv.net/ajax/illust/{artwork_id}', headers=header)
    return IllustrationInfo(r.json()['body'])
