from enum import Enum


class PixivIllustrationSize(Enum):
    THUMB = 'thumb'
    MINI = 'mini'
    SMALL = 'small'
    REGULAR = 'regular'
    ORIGINAL = 'original'


class PixivSearchOrder(Enum):
    NEW_TO_OLD = 'date_d'
    OLD_TO_NEW = 'date'
    POPULAR = 'popular_d'
    POPULAR_MALE = 'popular_male_d'
    POPULAR_FEMALE = 'popular_female_d'


class PixivSearchArtworkType(Enum):
    ARTWORKS = 'artworks'
    ILLUSTRATIONS = 'illustrations'
    MANGA = 'manga'
    NOVELS = 'novels'


class PixivSearchMode(Enum):
    ALL = 'all'
    SAFE = 'safe'
    R18 = 'r18'


class PixivSearchSMode(Enum):
    PERFECT_SIMILAR = 's_tag_full'
    SIMILAR = 's_tag'
    TITLE_OR_CONTENT = 's_tc'


class PixivSearchType(Enum):
    ALL = 'all'
    ILLUST_AND_UGOIRA = 'illust_and_ugoira'
    ILLUST = 'illust'
    UGOIRA = 'ugoira'
    MANGA = 'manga'
