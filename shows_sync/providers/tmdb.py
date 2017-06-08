import requests
import constants as CONSTANTS


class Tmdb(object):

    def __init__(self, api_key, language='fr-FR'):
        self.api_key = api_key
        self.language = language

    def get_show(self, show_title):
        data = {}
        data['query'] = show_title
        r = self.request(url=CONSTANTS.TMDB_SEARCH_TV, data=data)
        if r['total_results'] != 0:
            show = {}
            show['id'] = r['results'][0]['id']
            show['title'] = r['results'][0]['name']
            return show
        return None

    def get_season_details(self, show_id, season_number):
        r = self.request(url=CONSTANTS.TMDB_SEASON_DETAIL.format(show_id,
                                                                 season_number))
        return r

    def request(self, url, data={}, method='GET'):
        data['api_key'] = self.api_key
        data['language'] = self.language
        r = requests.request(
            method=method,
            url=url,
            data=data,
            )
        return r.json()
