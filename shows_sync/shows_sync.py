import configparser
from providers import plex, myanimelist, tmdb, tvtime
from DaemonLite import DaemonLite
import logging
import time

global connected_providers
connected_providers = []


class Daemon(DaemonLite) :
    def __init__(self, pidFile):
        DaemonLite.__init__(self, pidFile=pidFile)
        self.Tmdb = None
        self.Plex = None
        self.delay = 3600
        self.extract_config()

    def run(self) :
        while True:
            self.update_providers()
            time.sleep(self.delay)

    def update_providers(self):
        episodes = self.Plex.get_watched()
        for provider in connected_providers:
            provider.update(episodes)

    def extract_config(self):
        config = configparser.ConfigParser()
        config.read('../settings.ini')

        self.Tmdb = tmdb.Tmdb(api_key=config['TMDB']['api_key'], language=config['TMDB']['language'])
        self.Plex = plex.Plex(url=config['Plex']['url'], token=config['Plex']['token'], tmdb=self.Tmdb)

        if config['DEFAULT']['delay']:
            try:
                self.delay = int(config['DEFAULT']['delay'])
            except Exception as e:
                logging.warning("Delay value is not valid")
        # MyAnimeList
        if config['MyAnimeList']['enabled']:
            connected_providers.append(myanimelist.MyAnimeList(
                config['MyAnimeList']['username'],
                config['MyAnimeList']['password']))

        # TV TIME
        if config['TV Time']['enabled']:
            connected_providers.append(tvtime.TVTIME(
                config['TV Time']['token']))
            config.set('TV Time', 'token', connected_providers[-1].token)
            config['TV Time']['token'] = connected_providers[-1].token
            with open('../settings.ini', 'w') as configfile:
                config.write(configfile)

if __name__ == '__main__':
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    staff = Daemon('/tmp/sync.pid')
    staff.run()