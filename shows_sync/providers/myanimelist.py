from lxml import etree
import time
import requests
import constants as CONSTANTS
import urllib
import logging
import sys

class MyAnimeList(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def generate_watch_xml(self, episode_number):
        xml = etree.Element("entry")
        etree.SubElement(xml, "episode").text = episode_number
        etree.SubElement(xml, "status").text = '1'
        return xml

    def mark_as_watched(self, xml, show_id):
        r = self.request(
                method='POST',
                url=CONSTANTS.MAL_ADD_URL.format(show_id),
                data=[('data', etree.tostring(xml))])
        if 'is already in the list' in r.text:
            r = self.request(
                method='POST',
                url=CONSTANTS.MAL_UPDATE_URL.format(show_id),
                data=[('data', etree.tostring(xml))])
        return True

    def update(self, episodes):
        logging.warn('MAL Provider not available, rework in progress')
        pass
        # for episode in self.reduce(episodes):
        #     xml = self.generate_watch_xml(episode['episode'])
        #     show_id = self.getId(episode['alias'])
        #     self.mark_as_watched(xml, show_id)
        #     logging.info('[MAL] Updated {0}, episode {1}.'.format(episode['alias'],
        #                                                    episode['episode']))

    def getId(self, title):
        title = urllib.parse.quote_plus(title)
        r = self.request(url=CONSTANTS.MAL_SEARCH_URL.format(title)).json()
        show_id = r['categories'][0]['items'][0]['id']
        return show_id

    def request(self, url, data='', method='GET'):
        r = requests.request(
            method=method,
            url=url,
            data=data,
            auth=(self.username, self.password)
            )

        if 'Too Many Requests' in r.text:
            time.sleep(2)
            self.request(url, data=data)
        return r

    def reduce(self, history):
        # TODO
        pass
