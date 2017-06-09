from plexapi.server import PlexServer
import helpers
import tmdbsimple as tmdb

class Plex(object):

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def login(self):
        try:
            self.plex = PlexServer(self.url, self.token)
        except:
            raise Exception('Can\'t connect to your plex server!')

    def get_watched(self):
        tmdb.API_KEY = '4872fce46af01e10233fd95afef97662'
        episodes = []
        for section in self.plex.library.sections():
            if (section.__class__.__name__ == 'ShowSection'):
                for library in section.search():
                    for episode in library.watched():
                        if helpers.is_watch_recently(episode.lastViewedAt):
                            episode_temp = {}
                            search = tmdb.Search()
                            response = search.tv(query=library.title, language='fr-FR')
                            show = search.results[0]
                            if show is not None:
                                if episode.seasonNumber == '1':
                                    episode_temp['alias'] = show['name']
                                else:
                                    season_number = episode.seasonNumber
                                    alias = tmdb.TV_Seasons(search.results[0]['id'], season_number)['name']
                                    episode_temp['alias'] = alias
                                episode_temp['title'] = library.title
                                episode_temp['season'] = episode.seasonNumber
                                episode_temp['episode'] = episode.index
                                episodes.append(episode_temp)
                            else:
                                print('[TMDB] Cannot find {0}.'.format(library.title))
        episodes = sorted(episodes, key=lambda episode: episode['title'])
        return episodes

    def getSections(self, name=None):
        sections = self.plex.library.sections()
        if name:
            sections = filter(lambda sec: sec.__class__.__name__ == name, sections)
        return sections
