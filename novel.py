import requests
import pyxiv
from artwork_info import NovelInfo


def get_artwork_info(novel_id: int):
    header = {
        'Referer': 'https://www.pixiv.net',
        'cookie': f'PHPSESSID={pyxiv.get_php_sessid()}',
        'user-agent': pyxiv.get_user_agent()
    }
    r = requests.get(f'https://www.pixiv.net/ajax/novel/{novel_id}', headers=header)
    return NovelInfo(r.json()['body'])
