from urllib.parse import urljoin


MAL_BASEURL = 'https://myanimelist.net'
MAL_ADD_URL = urljoin(MAL_BASEURL, '/api/animelist/add/{0}.xml')
MAL_UPDATE_URL = urljoin(MAL_BASEURL, '/api/animelist/update/{0}.xml')
MAL_SEARCH_URL = urljoin(MAL_BASEURL, '/search/prefix.json?type=anime&keyword={0}&v=1')

TMDB_BASEURL = 'https://api.themoviedb.org'
TMDB_SEARCH_TV = urljoin(TMDB_BASEURL, '/3/search/tv')
TMDB_SEASON_DETAIL = urljoin(TMDB_BASEURL, '/3/tv/{0}/season/{1}')

TVTIME_CLIENT_ID = 'UOWED7wBGRQv17skSZJO'
TVTIME_CLIENT_SECRET = 'ZHYcO8n8h6WbYuMDWVgXr7T571ZF_s1r1Rzu1-3B'
TVTIME_BASEURL = 'https://api.tvshowtime.com'
TVTIME_DEVICE_CODE = urljoin(TVTIME_BASEURL, '/v1/oauth/device/code')
TVTIME_TOKEN = urljoin(TVTIME_BASEURL, '/v1/oauth/access_token')
TVTIME_CHECKIN = urljoin(TVTIME_BASEURL, '/v1/checkin')
