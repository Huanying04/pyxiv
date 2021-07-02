import requests
import json
import pathlib
import os.path
import pyxiv
from pixiv_keywords import PixivIllustrationSize


class ArtworkInfo:
    def __init__(self, info: json):
        self.info = info

    def get_title(self):
        return self.info['title']

    def get_id(self):
        return self.info['id']

    def get_description(self):
        return self.info['description']

    def get_tags(self):
        return self.info['tags']

    def get_page_count(self):
        return self.info['pageCount']

    def get_view_count(self):
        return self.info['viewCount']

    def get_bookmark_count(self):
        return self.info['bookmarkCount']

    def get_comment_count(self):
        return self.info['commentCount']

    def get_like_count(self):
        return self.info['likeCount']

    def get_image_response_count(self):
        return self.info['imageResponseCount']

    def get_author_id(self):
        return self.info['userId']

    def get_author_name(self):
        return self.info['userName']

    def get_create_date(self):
        return self.info['createDate']

    def get_upload_date(self):
        return self.info['uploadDate']

    def is_nfsw(self):
        return self.info['xRestrict'] > 0

    def is_r18(self):
        return self.info['xRestrict'] == 1

    def is_r18g(self):
        return self.info['xRestrict'] == 2

    def liked(self):
        return self.info['likeData']

    def bookmarked(self):
        return self.info['bookmarkData']

    def get_bookmark_id(self):
        if not self.bookmarked():
            return None
        else:
            return self.info['bookmarkData']['id']

    def is_bookmark_private(self):
        if not self.bookmarked():
            raise Exception("You haven't bookmarked the artwork")
        else:
            return self.info['bookmarkData']['private']


class IllustrationInfo(ArtworkInfo):
    def __init__(self, info: json):
        super().__init__(info)

    def __get_image_url(self, size: PixivIllustrationSize, page: int = 0):
        url = (self.info['urls'][size.value]).replace(f'{self.get_id()}_p0', f'{self.get_id()}_p{page}')
        return url

    def get_image(self, size: PixivIllustrationSize, page: int = 0):
        url = self.__get_image_url(size, page)
        header = {
            'Referer': 'https://www.pixiv.net',
            'user-agent': pyxiv.get_user_agent()
        }
        r = requests.get(url, headers=header)
        return r.content

    def get_image_format(self, size: PixivIllustrationSize, page: int = 0):
        return self.__get_image_url(size, page).split('.')[-1]

    def download(self, path, size: PixivIllustrationSize = PixivIllustrationSize.ORIGINAL, page: int = 0):
        pathlib.Path(path).parent.absolute().mkdir(parents=True, exist_ok=True)
        if os.path.isfile(path):
            f = open(path, 'wb')
            f.write(self.get_image(size, page))
        elif os.path.isdir(path):
            f = open(f'{self.get_id()}_p{page}.{self.get_image_format(size, page)}', 'xb')
            f.write(self.get_image(size, page))
        else:
            f = open(path, 'xb')
            f.write(self.get_image(size, page))

    def download_all(self, folder, size: PixivIllustrationSize = PixivIllustrationSize.ORIGINAL):
        page_count = self.get_page_count()
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

        while page_count > 0:
            self.download(f'{folder}/{self.get_id()}_p{page_count-1}.{self.get_image_format(size, page_count-1)}',
                          size, page_count-1)
            page_count -= 1


class NovelInfo(ArtworkInfo):
    def __init__(self, info: json):
        super().__init__(info)

    def get_content(self):
        return self.info['content']

    def get_marker_count(self):
        return self.info['markerCount']

    def get_text_count(self):
        return self.info['userNovels'][self.get_id()]['textCount']

    def __get_cover_url(self):
        return self.info['coverUrl']

    def get_cover_image(self):
        url = self.__get_cover_url()
        header = {
            'Referer': 'https://www.pixiv.net',
            'user-agent': pyxiv.get_user_agent()
        }
        r = requests.get(url, headers=header)
        return r.content

    def download_cover(self, path):
        pathlib.Path(path).parent.absolute().mkdir(parents=True, exist_ok=True)
        if os.path.isfile(path):
            f = open(path, 'wb')
            f.write(self.get_cover_image())
        elif os.path.isdir(path):
            f = open(self.__get_cover_url().rsplit("/", 1)[1], 'xb')
            f.write(self.get_cover_image())
        else:
            f = open(path, 'xb')
            f.write(self.get_cover_image())
