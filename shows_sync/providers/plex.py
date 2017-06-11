import helpers
import logging
import requests
import xml.etree.ElementTree as ET
import datetime
import sys


class Plex(object):
    def __init__(self, url, token, tmdb):
        """
        """
        self.url = url
        self.token = token
        self.tmdb = tmdb

    def get_watched(self):
        """
        """
        recently_watched = {}
        episodes = self.get_history()
        for episode in episodes:
            season_number = episode['season']
            show_title = episode['show_title']
            episode_number = episode['episode']
            logging.debug('Processing {} S{}E{}'.format(show_title, season_number, episode_number))
            show = self.tmdb.get_show(show_title)
            if show is not None:
                if show_title not in recently_watched:
                    recently_watched[show_title] = {}
                    recently_watched[show_title]['show_title'] = show_title
                    try:
                        recently_watched[show_title]['original_title'] = show.info()['original_name']
                    except:
                        recently_watched[show_title]['original_title'] = show.info()['original_title']
                    recently_watched[show_title]['tmdb_id'] = show.info()['id']
                    external_ids = self.get_external_ids(show)
                    try:
                        recently_watched[show_title]['tvdb_id'] = external_ids['tvdb_id']
                    except:
                        recently_watched[show_title]['tvdb_id'] = external_ids
                    recently_watched[show_title]['Seasons'] = []
                if season_number not in recently_watched[show_title]:
                    season = {}
                    season['season'] = season_number
                    season['alias'] = self.getAlias(show, season_number)
                    season['episodes'] = []
                    recently_watched[show_title]['Seasons'].append(season)
                season['episodes'].append(episode)
        return recently_watched

    def get_external_ids(self, show):
        try:
            return self.tmdb.get_external_ids(show)
        except:
            # TODO USE TVDB TO SEARCH SHOW_TITLE AND GET SHOW_ID
            return ''

    def getAlias(self, show, seasonNb):
        """

        """
        try:
            return self.tmdb.get_season_alias(show.info()['id'], seasonNb)
        except:
            return ''

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
                        element['viewed_at'] = parsed_time.strftime('%Y-%m-%d %H:%M:%S')
                        parsed_xml.append(element)
        return parsed_xml
