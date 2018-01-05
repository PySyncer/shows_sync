import requests
import constants as CONSTANTS
import time
import logging
import processed

class TVTIME:

    def __init__(self, token):
        self.client_id = CONSTANTS.TVTIME_CLIENT_ID
        self.client_secret = CONSTANTS.TVTIME_CLIENT_SECRET
        if token:
            self.token = token
        else:
            self.token = self.get_token()
        self.already_proccess = processed.Processed.getInstance()

    def get_token(self):
        device = self.request(
            method='POST',
            url=CONSTANTS.TVTIME_DEVICE_CODE,
            data={'client_id': self.client_id}
        )

        r = {}
        r['result'] = 'KO'
        print(
            '[TVTIME] Linking with your TVTime account using the code {0}.'
            .format(device['device_code'])
        )
        print(
            '[TVTIME] Please open the URL {0} in your browser.'
            .format(device['verification_url'])
        )
        print('[TVTIME] Connect with your TVTime account and '
              'type in the following code :')
        print('[TVTIME] {0}'.format(device['user_code']))
        print('[TVTIME] Waiting for you to type in the code in TVShowTime.')
        while r['result'] != 'OK':
            r = self.request(
                    method='POST',
                    url=CONSTANTS.TVTIME_TOKEN,
                    data={'client_id': self.client_id,
                          'client_secret': self.client_secret,
                          'code': device['device_code']})
            time.sleep(device['interval'])
        print('TVTIME] Your account has been linked.')
        return r['access_token']

    def follow(self, show, show_key):
        r = self.request(
            method='POST',
            url=CONSTANTS.TVTIME_FOLLOW,
            data={'access_token': self.token,
                  'show_id': show['tvdb']['tvdb_id']})
        if r['result'] == 'OK':
            logging.info(
                'Follow {0}.'
                .format(show_key)
            )
        else:
            logging.warning(
                'Cannot Follow {0} with message : {1}.'
                .format(
                    show['tvdb']['show_title'],
                    r['message']
                )
            )

    def update(self, episodes):
        logging.debug('Starting updating on TVTime') 
        for show_key, show in episodes.items():
            if str(show['tvdb']['tvdb_id']) not in str(self.already_proccess):
                self.follow(show, show_key)
            for season_key, season in show['tvdb']['seasons'].items():
                for episode in season['episodes']:
                    episode_key = self.set_episode_key(show, season_key, episode['episode'])
                    if episode_key not in self.already_proccess:
                        r = self.request(
                            method='POST',
                            url=CONSTANTS.TVTIME_CHECKIN,
                            data={
                                'access_token': self.token,
                                'show_id': show['tvdb']['tvdb_id'],
                                'season_number': season_key,
                                'number': episode['episode']
                            }
                        )
                        if r['result'] == 'OK':
                            logging.info(
                                'Mark as watched {0} season {1} episode {2}'
                                .format(
                                    show['tvdb']['original_title'],
                                    season_key,
                                    episode['episode']
                                )
                            )
                            self.already_proccess.add(episode_key)
                        else:
                            logging.warning(
                                'Cannot mark as watched {0} season {1} episode {2} with message : {3}.'
                                .format(
                                    show_key,
                                    season_key,
                                    episode['episode'],
                                    r['message']
                                )
                            )

    def set_episode_key(self, show, season_key, episode):
        if show['tvdb']['tvdb_id'] is not None:
            return '0:{}:{}:{}'.format(
                str(show['tvdb']['tvdb_id']), 
                season_key,
                episode
            )
        return '1:{}:{}:{}'.format(
            str(show['tmdb']['tmdb_id']),
            season_key,
            episode
        )    

    def request(self, url, method='GET', data={}):
        r = requests.request(
            method=method,
            url=url,
            data=data,
        )
        if r.status_code is 200:
            return r.json()
        else:
            logging.info('Waiting 1 minute for new API slots.')
            time.sleep(65)
            return self.request(url, method=method, data=data)
