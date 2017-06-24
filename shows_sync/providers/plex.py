import helpers
import logging
import requests
import xml.etree.ElementTree as ET
import datetime
import sys


class Plex(object):
    def __init__(self, url, token, tmdb, tvdb):
        """
        """
        self.url = url
        self.token = token
        self.tmdb = tmdb
        self.tvdb = tvdb

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
            if show_title not in recently_watched:
                recently_watched[show_title] = {}
                show = self.tmdb.get_show(show_title)
                if show is not None:
                    recently_watched[show_title]['tmdb'] = {}
                    recently_watched[show_title]['tmdb'] = tmdb_data(show, show_title, season_number, episode_number, recently_watched)
                    try:
                        tvdb_id = self.get_external_ids(show)['tvdb_id']
                    except:
                        tvdb_id = None
                if tvdb_id is not None:
                    show = self.tvdb.get_show(tvdb_id)
                else:
                    show_id = self.tvdb.search(show_title)[0]['id']
                    show = self.tvdb.get_show(show_id)
                print(show)
                recently_watched[show_title]['tvdb'] = {}
                recently_watched[show_title]['tvdb'] = tvdb_data(show, show_title, season_number, episode_number, recently_watched)
        print(recently_watched)
        return recently_watched

    def tmdb_data(show, show_title, season_number, episode_number, recently_watched):
        tmdb = {}
        tmdb['show_title'] = show_title
        try:
            tmdb['original_title'] = show.info()['original_name']
        except:
            tmdb['original_title'] = show.info()['original_title']
        tmdb['tmdb_id'] = show.info()['id']
        tmdb['Seasons'] = []
        if season_number not in recently_watched[show_title]:
            season = {}
            season['season'] = season_number
            season['alias'] = self.getAlias(show, season_number)
            season['episodes'] = []
            tmdb['Seasons'].append(season)
        season['episodes'].append(episode)
        return tmdb

    def tvdb_data(show, show_title, season_number, episode_number, recently_watched):
        tvdb = {}
        tvdb['show_title'] = show_title
        try:
            tvdb['original_title'] = show['seriesName']
        except:
            tvdb['original_title'] = show['moviesName']
        tvdb['tmdb_id'] = show['id']
        tvdb['Seasons'] = []
        if season_number not in recently_watched[show_title]:
            season = {}
            season['season'] = season_number
            season['alias'] = show['aliases']
            season['episodes'] = []
            tvdb['Seasons'].append(season)
        season['episodes'].append(episode)
        return tvdb

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
