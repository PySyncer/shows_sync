import helpers
import logging
import requests
import xml.etree.ElementTree as ET
import datetime
import json
import sys


class Plex(object):
    def __init__(self, url, token, tmdb, tvdb):
        """
            Create a Plex object
            :param url: url of your plex
            :param token: Token used for authentification
            :param tmdb: Tmdb client
            :param tvdb: Tvdb client
            :type url: str
            :type token: str
            :type tmdb: tmdb
            :type tvdb: str
            :return: The result of the addition
            :rtype: int
        """
        self.url = url
        self.token = token
        self.tmdb = tmdb
        self.tvdb = tvdb

    def get_watched(self):
        """
            Return a list with recently watched episodes from Plex.
            It'll get metadata from plex and enrich it with TMDB and TVDB.
            An episode is considered as recently watched if
            it has been seen in N-2 days.
            :return: Recently watched episodes
            :rtype: list
        """
        recently_watched = {}
        tmdb_show = {}
        # Get the history -2 days from plex
        episodes = self.get_history()
        # For each episode
        for episode in episodes:
            # Get season
            season_number = episode['season']
            # Get title
            show_title = episode['show_title']
            # Get episode number (aka 01 02 etc..)
            episode_number = episode['episode']
            logging.debug('Processing {} S{}E{}'.format(show_title, season_number, episode_number))
            # If the show has never been processed
            if show_title not in recently_watched:
                # We store one in recently_watched
                recently_watched[show_title] = {}
                recently_watched[show_title]['tmdb'] = {}
                recently_watched[show_title]['tvdb'] = {}
                # Getting info in TMDB
                tmdb_show[show_title] = self.tmdb.get_show(show_title)            
                 # We retrieve metadata for the show in TMDB
                recently_watched[show_title]['tmdb'] = self.tmdb_get_metadata_for_show(tmdb_show[show_title])
                # We retrieve the TVDB id from TMDB
                tvdb_show_id = self.get_tvdb_id_from_tmdb(tmdb_show[show_title], show_title)
                # We retrieve the show from TVDB
                tvdb_show = self.tvdb.get_show(tvdb_show_id)
                recently_watched[show_title]['tvdb'] = self.tvdb_get_metadata_for_show(tvdb_show)

            episode['absoluteNumber'] = self.tvdb.get_absolute_number(season_number, episode_number, recently_watched[show_title]['tvdb']['tvdb_id'] )
            if not self.check_season_exist(recently_watched[show_title]['tmdb']['seasons'], season_number):
                recently_watched[show_title]['tmdb']['seasons'][season_number] = self.tmdb_get_metadata_for_season(tmdb_show[show_title], season_number)
                recently_watched[show_title]['tvdb']['seasons'][season_number] = self.tvdb_get_metadata_for_season(self.tvdb.get_show(recently_watched[show_title]['tvdb']['tvdb_id']))
                recently_watched[show_title]['tmdb']['seasons'][season_number]['episodes'] = []
                recently_watched[show_title]['tvdb']['seasons'][season_number]['episodes'] = []
            recently_watched[show_title]['tmdb']['seasons'][season_number]['episodes'].append(episode)
            recently_watched[show_title]['tvdb']['seasons'][season_number]['episodes'].append(episode)
        return recently_watched

    def get_tvdb_id_from_tmdb(self, tmdb_show, show_title):
        try:
            return self.get_external_ids(tmdb_show)['tvdb_id']
        except:
            return self.tvdb.search(show_title)['data'][0]['id']


    def check_season_exist(self, seasons_list, season_number):
        if seasons_list is {}:
            return False
        if season_number in seasons_list.keys():
            return True
        else:
            return False

    def tmdb_get_metadata_for_season(self, tmdb_show, season_number):
            season = {}
            season['alias'] = self.getAlias(tmdb_show, season_number)
            season['episodes'] = []
            return season

    def tvdb_get_metadata_for_season(self, tmdb_show):
            season = {}
            season['alias'] = tmdb_show['aliases']
            season['episodes'] = []
            return season

    def tmdb_get_metadata_for_show(self, tmdb_show):
            show = {}
            if tmdb_show is not None:
                shows_infos = tmdb_show.info()
                try:
                    show['original_title'] = shows_infos['original_name']
                except:
                    show['original_title'] = shows_infos['original_title']
                show['tmdb_id'] = shows_infos['id']
                show['seasons'] = {}
            else:
                show['original_title'] = ''
                show['tmdb_id'] = ''
                show['seasons'] = {}
            return show

    def tvdb_get_metadata_for_show(self, tmdb_show):
            show = {}
            try:
                show['original_title'] = tmdb_show['seriesName']
            except:
                show['original_title'] = tmdb_show['moviesName']
            show['tvdb_id'] = tmdb_show['id']
            show['seasons'] = {}
            return show

    def get_external_ids(self, show):
        try:
            return self.tmdb.get_external_ids(show)
        except:
            return None

    def getAlias(self, show, seasonNb):
        """

        """
        try:
            return self.tmdb.get_season_alias(show.info()['id'], seasonNb)
        except:
            return None

    def get_history(self):
        """
        """
        history_url = '{}/status/sessions/history/all?X-Plex-Token={}'.format(self.url, self.token)
        response = requests.get(history_url).text
        return self.parse_history_xml(response)

    def parse_history_xml(self, xml):
        """
        """
        parsed_xml = []
        root = ET.fromstring(xml)
        for child in root:
            element = {}
            element['type'] = child.attrib['type']
            if child.attrib['viewedAt']:
                parsed_time = datetime.datetime.fromtimestamp(
                    int(child.attrib['viewedAt'])
                )
                if helpers.is_watch_recently(parsed_time):
                    if element['type'] == 'episode':
                        if child.attrib['parentIndex']:
                            element['season'] = child.attrib['parentIndex']
                        else:
                            element['season'] = None
                        element['episode'] = child.attrib['index']
                        element['show_title'] = child.attrib['grandparentTitle']
                        parsed_xml.append(element)
        return parsed_xml
