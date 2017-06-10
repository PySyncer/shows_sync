import configparser
from providers import plex, myanimelist, tmdb, tvtime
import logging
global connected_providers
connected_providers = []


def extract_config():
    config = configparser.ConfigParser()
    config.read('../settings.ini')

    Tmdb = tmdb.Tmdb(api_key=config['TMDB']['api_key'],
                     language=config['TMDB']['language'])

    Plex = plex.Plex(url=config['Plex']['url'], token=config['Plex']['token'],
                     tmdb=Tmdb)
    episodes = Plex.get_watched()
    # MyAnimeList
    if config['MyAnimeList']['enabled']:
        connected_providers.append(myanimelist.MyAnimeList(
            config['MyAnimeList']['username'],
            config['MyAnimeList']['password']))

    # TV TIME
    if config['TV Time']['enabled']:
        connected_providers.append(tvtime.TVTIME(
            config['TV Time']['token']))
        # if config['TV Time']['token'] != '':
        config.set('TV Time', 'token', connected_providers[-1].token)
        config['TV Time']['token'] = connected_providers[-1].token
        with open('../settings.ini', 'w') as configfile:
            config.write(configfile)

    for provider in connected_providers:
        provider.update(episodes)


if __name__ == '__main__':
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    extract_config()
