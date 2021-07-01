import requests

import pixiv
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


def like(novel_id: int):
    url = "https://www.pixiv.net/ajax/novels/like"
    post = {
        'novel_id': str(novel_id)
    }
    header = {
        'content-type': 'application/json; charset=utf-8',
        'referer': 'https://www.pixiv.net/',
        'cookie': f'PHPSESSID={pyxiv.get_php_sessid()}',
        'user-agent': pyxiv.get_user_agent(),
        'x-csrf-token': pixiv.get_token()
    }

    r = requests.post(url, json=post, headers=header)
    if r.json()['error']:
        raise Exception(r.json()['message'])
    return r.json()['body']['is_liked']


def bookmark(novel_id: int):
    url = "https://www.pixiv.net/ajax/illusts/bookmarks/add"
    post = {
        'novel_id': str(novel_id),
        'restrict': 0,
        'comment': '',
        'tags': []
    }
    header = {
        'content-type': 'application/json; charset=utf-8',
        'referer': 'https://www.pixiv.net/',
        'cookie': f'PHPSESSID={pyxiv.get_php_sessid()}',
        'user-agent': pyxiv.get_user_agent(),
        'x-csrf-token': pixiv.get_token()
    }

    r = requests.post(url, json=post, headers=header)
    if r.json()['error']:
        raise Exception(r.json()['message'])
    return r.json()['body']['last_bookmark_id']


def remove_bookmark(novel_id: int):
    url = "https://www.pixiv.net/novel/bookmark_setting.php"
    if get_artwork_info(novel_id).is_bookmark_private():
        rest = 'hide'
    else:
        rest = 'show'
    post = {
        'tt': pixiv.get_token(),
        'p': '1',
        'untagged': 0,
        'rest': rest,
        'book_id[]': get_artwork_info(novel_id).get_bookmark_id(),
        'del': '1'
    }
    header = {
        'content-type': 'application/x-www-form-urlencoded',
        'referer': 'https://www.pixiv.net/',
        'cookie': f'PHPSESSID={pyxiv.get_php_sessid()}',
        'user-agent': pyxiv.get_user_agent(),
        'x-csrf-token': pixiv.get_token()
    }

    session = requests.Session()
    r = session.post(url, data=post, headers=header)
    return r.status_code
