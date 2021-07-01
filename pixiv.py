import json
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import pyxiv


def get_token():
    req = urllib.request.Request('https://www.pixiv.net/')
    req.add_header('Referer', 'https://www.pixiv.net')
    req.add_header('cookie', 'PHPSESSID=' + pyxiv.get_php_sessid())
    req.add_header('user-agent', pyxiv.get_user_agent())
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "html.parser")
    data = soup.find("meta", id="meta-global-data")
    return json.loads(data['content'])['token']

