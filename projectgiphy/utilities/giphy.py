import requests
from projectgiphy import app
from projectgiphy.utilities.db import Aux

class SearchObj(object):
    """
    Search structure and data assignment of a single returned object
    """
    def __init__(self,
                 id=None,
                 name=None,
                 url=None,
                 preview=None,
                 data_payload=None):
        self.url = url
        self.preview = preview
        self.id = id
        self.name = name

    def parse(self, data_payload):
        """ Parses and assigns specified nested elements

        Arg:
            data_payload (object): Request payload json response
        Response:
            object: Search Object for each returned image
        """
        self.id = data_payload.get('id')
        self.name = data_payload.get('title')
        images = data_payload.get('images')
        preview_gif = images.get('preview_gif')
        original = images.get('original')
        self.url = original.get('url')
        self.preview = preview_gif.get('url')
        return self


class Giphy(object):
    """ Base searching class for the Giphy API """

    LIMIT = 25
    LANG = 'en'

    def __init__(self):
        aux = Aux()
        self.base_url = "https://api.giphy.com/v1/gifs"
        self.search_url = f"{self.base_url}/search"
        self.api_key = app.config.get('GIPHY_KEY')
        # self.ratings = aux.get_ratings()
        self.ratings = 'G'


    def search(self, search_string, offset=0):
        """ Search method to query the API

        Args:
            search_string (str): String to be searched against the API
            offset (int:optional): Offset to extend searches
        Returns:
            dict: Dictonary response containing search objects
        """
        urlparts = [f"{self.search_url}?api_key={self.api_key}",
                    f"q={search_string}",
                    f"limit={self.LIMIT}",
                    f"offset={offset}",
                    f"rating={self.ratings}",
                    f"lang={self.LANG}"]
        url = ('&').join(urlparts)
        r = requests.get(url)
        data = r.json()
        pagination = data.get('pagination')
        total_count = pagination.get('total_count')
        offset = pagination.get('offset')
        offset_next = offset + 1 if total_count / self.LIMIT >= offset else 0
        offset_previous = offset -1 if offset > 0 else 0
        response = {'total': total_count,
                    'offset': offset,
                    'gifs': {},
                    'next': offset_next,
                    'previous': offset_previous}
        for gif in data.get('data'):
            so = SearchObj()
            gifobj = so.parse(gif)
            response[gifobj.id] = gifobj.__dict__
        return response

        
if __name__ == '__main__':
    g = Giphy()
    res = g.search('bear')
    print(res)
