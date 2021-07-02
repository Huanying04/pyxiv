import math


class SearchResult:
    def __init__(self, json, data_type):
        self.__json = json
        self.__data_type = data_type

    def get_ids(self):
        array = []
        for i in range(0, 60):
            if 'isAdContainer' in self.__json[self.__data_type]['data'][i]:
                continue
            array.append(self.__json[self.__data_type]['data'][i]['id'])
        return array

    def get_last_page_index(self):
        return math.ceil(self.__json[self.__data_type]['total'] / 60)
