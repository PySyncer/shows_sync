from plexapi.server import PlexServer
import helpers
import logging


class Plex(object):

    def __init__(self, url, token, tmdb):
        self.url = url
        self.token = token
        self.tmdb = tmdb
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARNING)


    def login(self):
        self.logger.info("Connection to Plex")
        try:
            self.plex = PlexServer(self.url, self.token)
        except:
            raise Exception('Can\'t connect to your plex server!')

    def get_watched(self):
        shows_watched = []
        for section in self.getSections('ShowSection'):
            for library in section.search():
                watched_details = self.get_show_watched(library)
                if bool(watched_details) is not False:
                    shows_watched.append(watched_details)
        return shows_watched

    def getSections(self, name=None):
        sections = self.plex.library.sections()
        if name:
            sections = list(filter(lambda sec: sec.__class__.__name__ == name, sections))
        return sections

    def get_show_watched(self, library):
        recentlyWatched = {}
        show = self.tmdb.get_show(library.title)
        if show is not None:
            for season in library.seasons():
                for episode in season.watched():
                    if helpers.is_watch_recently(episode.lastViewedAt):
                        if library.title not in recentlyWatched:
                            recentlyWatched[library.title] = {}
                        if season.index not in recentlyWatched[library.title]:
                            recentlyWatched[library.title][season.index] = {}
                            recentlyWatched[library.title][season.index]['episodes'] = []
                            recentlyWatched[library.title][season.index]['alias'] = self.getAlias(show, season.index)
                        episode = self.parse_episode_details(episode)
                        recentlyWatched[library.title][season.index]['episodes'].append(episode)
        else:
            print("Unable to find {}".format(library.title))
        return recentlyWatched

    def parse_episode_details(self, episode):
        episode_temp = {}
        episode_temp['season'] = episode.seasonNumber
        episode_temp['episode'] = episode.index
        return episode_temp

    def getAlias(self, show, seasonNb):
        """

        """
        return self.tmdb.get_season_alias(show['id'], seasonNb)
