import json
from urllib.request import urlopen
import urllib.request
import urllib.parse
import requests

import pyxiv
from pixiv_keywords import PixivSearchArtworkType, PixivSearchOrder, PixivSearchMode, PixivSearchSMode, PixivSearchType
from search_result import SearchResult


def get_token():
    req = urllib.request.Request('https://www.pixiv.net/')
    req.add_header('Referer', 'https://www.pixiv.net')
    req.add_header('cookie', 'PHPSESSID=' + pyxiv.get_php_sessid())
    req.add_header('user-agent', pyxiv.get_user_agent())
    webpage = str(urlopen(req).read().decode('utf-8'))

    index_start = webpage.find('<meta name="global-data" id="meta-global-data" content=\'')

    if index_start == -1:
        return None

    index_end = webpage.find('\'>', index_start)

    data = json.loads(webpage[index_start + 56:index_end])
    return data['token']


def search(keyword, page=1, artwork_type: PixivSearchArtworkType = PixivSearchArtworkType.ARTWORKS,
           order: PixivSearchOrder = PixivSearchOrder.NEW_TO_OLD, mode: PixivSearchMode = PixivSearchMode.SAFE,
           strict_mode: PixivSearchSMode = PixivSearchSMode.SIMILAR,
           search_type: PixivSearchType = PixivSearchType.ILLUST):
    url = f'https://www.pixiv.net/ajax/search/{artwork_type.value}/{urllib.parse.quote(keyword)}?word={urllib.parse.quote(keyword)}'
    data = {
        'order': order.value,
        'mode': mode.value,
        'p': page,
        's_mode': strict_mode.value,
        'type': search_type.value
    }
    url += '&' + urllib.parse.urlencode(data)
    header = {
        'Referer': 'https://www.pixiv.net',
        'cookie': f'PHPSESSID={pyxiv.get_php_sessid()}',
        'user-agent': pyxiv.get_user_agent()
    }

    r = requests.get(url, headers=header)

    result_type = ''
    if artwork_type == PixivSearchArtworkType.ARTWORKS:
        result_type = 'illustManga'
    elif artwork_type == PixivSearchArtworkType.ILLUSTRATIONS:
        result_type = 'illust'
    elif artwork_type == PixivSearchArtworkType.MANGA:
        result_type = 'manga'
    elif artwork_type == PixivSearchArtworkType.NOVELS:
        result_type = 'novel'
    else:
        result_type = 'illustManga'

    return SearchResult(r.json()['body'], result_type)
