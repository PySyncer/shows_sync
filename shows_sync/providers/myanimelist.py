from lxml import etree
import time
import requests
import constants as CONSTANTS
import urllib
import logging
from pymal import Mal
import sys

class MyAnimeList(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.mal = Mal.Mal(username, password)

    def update(self, episodes):
        for show_key, show in episodes.items():
            for season_key, season in show['tvdb']['seasons'].items():
                try:
                    # Try to get ID of show on MAL
                    anime = self.mal.anime.search(show['tvdb']['original_title'])[0]
                    id = anime['id']
                except:
                    logging.warning('Cannot find show {0}.'.format(show['tvdb']['original_title']))
                    break

                # IF the total number of epiosde is smaller than the absolute number of the episode,
                # MAL probably add another show coresponding to the season of the episode, so we will search this show
                if int(anime['episodes']) < season['episodes'][-1]['absoluteNumber']:
                    try:
                        # Search show coresponding to the season
                        anime = self.mal.anime.search(show['tvdb']['original_title'] + ' ' + season_key)[0]
                        id = anime['id']
                    except:
                        logging.warning('Cannot find show {0}.'.format(show['tvdb']['original_title'] + ' ' + season_key))
                        break
                    # Mark as watched with not absolute number
                    r = self.mark_as_watched(id, season['episodes'][-1]['episode'])
                    self.watch_log(r, anime['title'], season['episodes'][-1]['episode'])
                else:
                    # Mark as watched with absolute number
                    r = self.mark_as_watched(id, season['episodes'][-1]['absoluteNumber'])
                    self.watch_log(r, anime['title'], season['episodes'][-1]['absoluteNumber'])

    def watch_log(self, r, title, episode):
        if r == 'Updated' or r == 'Created':
            logging.info('{0} {1}, episode {2}.'.format(r, title, episode))
        else:
            logging.warning('Cannot update {0}, episode {1} with message : {2}.'.format(title, episode, r))

    def mark_as_watched(self, id, episode):
        r = self.mal.anime.add(id, str(episode))
        if 'is already in the list' in r:
            logging.debug(r)
            r = self.mal.anime.update(id, str(episode))
        return r

    def reduce(self, history):
        # TODO
        pass
