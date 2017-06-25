from tvdb_client import ApiV2Client
import logging
import constants as CONSTANTS


class TVDB(object):

    def __init__(self, username, account_identifier, api_key):
        self.username = username
        self.account_identifier = account_identifier
        self.api_key = api_key
        self.tvdb = None
        self.connect()

    def connect(self):
        api_client = ApiV2Client(self.username, self.api_key, self.account_identifier)
        api_client.login()
        if api_client.is_authenticated:
            self.tvdb = api_client
            logging.info(CONSTANTS.TVDB_SUCCESS_LOGIN)
            return
        logging.warning(CONSTANTS.TVDB_ERROR_LOGIN)
        raise Exception(CONSTANTS.TVDB_ERROR_LOGIN)

    def search(self, title):
        shows = self.tvdb.search_series(name=title)
        return shows

    def get_show(self, id):
        show = self.tvdb.get_series(series_id=id)
        return show['data']

    def get_series_episodes(self, show_id, aired_season=None, aired_episode=None):
        episode = self.tvdb.get_series_episodes(show_id, aired_season=aired_season, aired_episode=aired_episode)
        if episode['data']:
            return episode['data']
        else:
            return None

    def get_episode(self, episode_id):
        return self.tvdb.get_episode(episode_id)

    def get_absolute_number(self, season_number, episode_number, tvdb_id):
        tvdb_episode_id = self.tvdb.get_series_episodes(tvdb_id, aired_season=season_number, aired_episode=episode_number)
        return tvdb_episode_id['data'][0]['absoluteNumber']
