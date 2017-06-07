from lxml import etree
import time
import requests
import constants as CONSTANTS


class MyAnimeList(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def update(self, episodes):
        episodes = self.reduce(episodes)
        for episode in episodes:
            xml = etree.Element("entry")
            etree.SubElement(xml, "episode").text = episode['episode']
            etree.SubElement(xml, "status").text = '1'
            show_id = self.getId(episode['alias'])
            r = self.request(
                method='POST',
                url=CONSTANTS.MAL_ADD_URL.format(show_id),
                data=[('data', etree.tostring(xml))])
            if 'is already in the list' in r.text:
                r = self.request(
                    method='POST',
                    url=CONSTANTS.MAL_UPDATE_URL.format(show_id),
                    data=[('data', etree.tostring(xml))])
            print(r.text)

    def getId(self, title):
        r = self.request(url=CONSTANTS.MAL_SEARCH_URL.format(title))
        if r.text != '':
            result = etree.XML(r.content)
            show_id = result[0][0].text
        else:
            show_id = None
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

    def reduce(self, episodes):
        reduced_list = []
        print(episodes)
        titles = list(set(episode['alias'] for episode in episodes))
        for title in titles:
            different_episodes = list(filter(lambda episode: episode['alias'] == title, episodes))
            last_episode = different_episodes[0]
            if len(different_episodes) > 1:
                for episode in different_episodes[1:]:
                    # Dropping season, Mal doesn't support it,
                    # We'll have to preprocess data
                    if int(episode['episode']) > int(last_episode['episode']):
                        last_episode = episode
            reduced_list.append(last_episode)
        return reduced_list
