import configparser
from providers import plex, myanimelist, tmdb, tvtime, tvdb
from DaemonLite import DaemonLite
import logging
import time
import argparse
import sys
import json

global connected_providers
connected_providers = []


class Daemon(DaemonLite):
    def __init__(self, pidFile, configFile):
        DaemonLite.__init__(self, pidFile=pidFile)
        self.Tmdb = None
        self.Tvdb = None
        self.Plex = None
        self.delay = 3600
        self.config_file = configFile
        self.extract_config()

    def run(self):
        while True:
            self.update_providers()
            time.sleep(self.delay)

    def update_providers(self):
        episodes = self.Plex.get_watched()
        sys.exit()
        for provider in connected_providers:
            provider.update(episodes)

    def extract_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)

        self.Tmdb = tmdb.Tmdb(api_key=config['TMDB']['api_key'], language=config['TMDB']['language'])
        self.tvdb = tvdb.TVDB(config['TVDB']['username'], config['TVDB']['account_identifier'], config['TVDB']['api_key'])
        self.Plex = plex.Plex(url=config['Plex']['url'], token=config['Plex']['token'], tmdb=self.Tmdb, tvdb=self.tvdb)

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
            with open(self.config_file, 'w') as configfile:
                config.write(configfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Syncronize Plex with multiple providers')
    parser.add_argument('--config', help="Path to config file", type=str, default='/etc/sync_shows.ini')
    parser.add_argument('--pid', help="Path to pid file", type=str, default='/var/run/sync_shows.pid')
    parser.add_argument('--log', help="Path to log file", type=str, default='/var/log/sync_shows.log')
    parser.add_argument('--fg', help="Run the program in the foreground", action='store_true')
    parser.add_argument('--debug', help="Debug mode", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    # parser.add_argument('--verbose', help="Be verbose", action="store_const", dest="loglevel", const=logging.INFO)
    args = parser.parse_args()

    logging.basicConfig(
        filename=args.log,
        level=args.loglevel,
        format='%(asctime)s - %(module)s - %(levelname)s - %(message)s'
    )

    staff = Daemon(args.pid, args.config)
    if args.fg:
        staff.run()
    else:
        staff.start()
