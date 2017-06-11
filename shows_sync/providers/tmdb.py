import tmdbsimple as tmdb
import logging


class Tmdb(object):

    def __init__(self, api_key, language='fr-FR'):
        self.api_key = api_key
        self.language = language
        tmdb.API_KEY = api_key
        self.cache = {}

    def search_tv(self, show_title):
        show = None
        search = tmdb.Search()
        search.tv(query=show_title, language=self.language)
        try:
            show = tmdb.TV(search.results[0]['id'])
            self.cache[show_title] = show
        except IndexError as e:
            logging.warning("Unable to find show {}".format(show_title))
        return show

    def search_movie(self, show_title):
        show = None
        search = tmdb.Search()
        search.movie(query=show_title, language=self.language)
        try:
            show = tmdb.Movies(search.results[0]['id'])
            self.cache[show_title] = show
        except IndexError as e:
            logging.warning("Unable to find movie {}".format(show_title))
        return show

    def get_show(self, show_title):
        if show_title in self.cache:
            return self.cache[show_title]
        show = self.search_tv(show_title)
        if show is None:
            show = self.search_movie(show_title)
        return show

    def get_external_ids(self, show):
        return show.external_ids()

    def get_season_details(self, show_id, season_number):
        return tmdb.TV_Seasons(show_id, season_number)

    def get_season_alias(self, show_id, season_number):
        details = self.get_season_details(show_id, season_number).info(language=self.language)
        return details['name']
