import configparser
from providers import plex, myanimelist

global connected_providers
connected_providers = []


def extract_config():
    config = configparser.ConfigParser()
    config.read('../settings.ini')

    # Plex
    Plex = plex.Plex(url=config['Plex']['url'], token=config['Plex']['token'])
    Plex.login()
    episodes = Plex.get_watched()

    # MyAnimeList
    if config['MyAnimeList']['enabled']:
        connected_providers.append(myanimelist.MyAnimeList(
            config['MyAnimeList']['username'],
            config['MyAnimeList']['password']))

    for provider in connected_providers:
        provider.update(episodes)


if __name__ == '__main__':
    extract_config()
