from plexapi.server import PlexServer
import helpers
import sys
import requests
import constants as CONSTANTS


class Plex(object):

    def __init__(self, url, token, tmdb_api_key, tmdb_language='fr-FR'):
        self.url = url
        self.token = token
        self.tmdb = {}
        self.tmdb['api_key'] = tmdb_api_key
        self.tmdb['language'] = tmdb_language

    def login(self):
        try:
            self.plex = PlexServer(self.url, self.token)
        except:
            raise Exception('Can\'t connect to your plex server!')

    def get_watched(self):
        episodes = []
        for section in self.plex.library.sections():
            if (section.__class__.__name__ == 'ShowSection'):
                for library in section.search():
                    for episode in library.watched():
                        if helpers.is_watch_recently(episode.lastViewedAt):
                            episode_temp = {}
                            result = self.request(
                                        url=CONSTANTS.TMDB_SEARCH_TV,
                                        data={'query': library.title}
                                        )
                            if episode.seasonNumber == '1':
                                episode_temp['alias'] = result['results'][0]['name']
                            else:
                                show_id = result['results'][0]['id']
                                result = self.request(url=CONSTANTS.TMDB_SEASON_DETAIL.format(show_id,episode.seasonNumber))
                                episode_temp['alias'] = result['name']
                            episode_temp['title'] = library.title
                            episode_temp['season'] = episode.seasonNumber
                            episode_temp['episode'] = episode.index
                            episodes.append(episode_temp)
        episodes = sorted(episodes, key=lambda episode: episode['title'])
        return episodes

    def request(self, url, data={}, method='GET'):
        data['api_key'] = self.tmdb['api_key']
        data['language'] = self.tmdb['language']
        r = requests.request(
            method=method,
            url=url,
            data=data,
            )
        return r.json()
