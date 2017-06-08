from urllib.parse import urljoin


MAL_BASEURL = 'https://myanimelist.net'
MAL_ADD_URL = urljoin(MAL_BASEURL, '/api/animelist/add/{0}.xml')
MAL_UPDATE_URL = urljoin(MAL_BASEURL, '/api/animelist/update/{0}.xml')
MAL_SEARCH_URL = urljoin(MAL_BASEURL, '/search/prefix.json?type=anime&keyword={0}&v=1')

TMDB_BASEURL = 'https://api.themoviedb.org'
TMDB_SEARCH_TV = urljoin(TMDB_BASEURL, '/3/search/tv')
TMDB_SEASON_DETAIL = urljoin(TMDB_BASEURL, '/3/tv/{0}/season/{1}')
