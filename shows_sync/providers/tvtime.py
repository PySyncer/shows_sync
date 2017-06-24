import requests
import constants as CONSTANTS
import time
import logging


class TVTIME:

    def __init__(self, token):
        self.client_id = CONSTANTS.TVTIME_CLIENT_ID
        self.client_secret = CONSTANTS.TVTIME_CLIENT_SECRET
        if token:
            self.token = token
        else:
            self.token = self.get_token()

    def get_token(self):
        device = self.request(
            method='POST',
            url=CONSTANTS.TVTIME_DEVICE_CODE,
            data={'client_id': self.client_id})

        r = {}
        r['result'] = 'KO'
        print('[TVTIME] Linking with your TVTime account using the code {0}.'
              .format(device['device_code']))
        print('[TVTIME] Please open the URL {0} in your browser.'
              .format(device['verification_url']))
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

    def follow(self, show):
        r = self.request(
            method='POST',
            url=CONSTANTS.TVTIME_FOLLOW,
            data={'access_token': self.token,
                  'show_id': show['tvdb_id']})
        if r['result'] == 'OK':
            logging.info('Follow {0}.'.format(show['show_title']))
        else:
            logging.warning('Cannot Follow {0} with message : {1}.'.format(show['show_title'], r['message']))

    def update(self, episodes):
        for show_key, show in episodes['tvdb'].items():
            self.follow(show)
            for season in show['Seasons']:
                for episode in season['episodes']:
                    r = self.request(
                            method='POST',
                            url=CONSTANTS.TVTIME_CHECKIN,
                            data={'access_token': self.token,
                                  'show_id': show['tvdb_id'],
                                  'season_number': season['season'],
                                  'number': episode['episode']})
                    if r['result'] == 'OK':
                        logging.info('Mark as watched {0} season {1} episode {2}'.format(show['show_title'], season['season'], episode['episode']))
                    else:
                        logging.warning('Cannot mark as watched {0} season {1} episode {2} with message : {3}.'.format(show['show_title'], season['season'], episode['episode'], r['message']))

    def request(self, url, method='GET', data={}):
        r = requests.request(
            method=method,
            url=url,
            data=data,
            ).json()
        try:
            if r['message'] == 'API rate limit exceeded.':
                logging.info('Waiting 1 minute for new API slots.')
                time.sleep(65)
                self.request(url, method=method, data=data)
        except:
            pass
        return r
