import tmdbsimple as tmdb
import logging


class Tmdb(object):

    def __init__(self, api_key, language='fr-FR'):
        self.api_key = api_key
        self.language = language
        tmdb.API_KEY = api_key
        self.cache = {}

    def get_show(self, show_title):
        show = None
        if show_title in self.cache:
            return self.cache[show_title]
        search = tmdb.Search()
        search.tv(query=show_title, language=self.language)
        try:
            show = search.results[0]
            self.cache[show_title] = show
        except IndexError as e:
            logging.warning("[TMDB] Unable to find {}".format(show_title))
        return show

    def get_season_details(self, show_id, season_number):
        return tmdb.TV_Seasons(show_id, season_number)

    def get_season_alias(self, show_id, season_number):
        details = self.get_season_details(show_id, season_number).info(language=self.language)
        return details['name']
