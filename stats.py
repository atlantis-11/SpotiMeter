import requests
from requests.exceptions import HTTPError
import urllib

def get_top_artists(access_token: str, time_range=None, limit=None):
    items = _get_top_items(access_token, 'artists', time_range, limit)

    res = []

    for artist in items:
        res.append({
            'name': artist['name'],
            'genres': artist['genres'],
            'popularity': artist['popularity']
        })

    return res

def get_top_tracks(access_token: str, time_range=None, limit=None):
    items = _get_top_items(access_token, 'tracks', time_range, limit)

    res = []

    for track in items:
        res.append({
            'name': track['name'],
            'artists': [d['name'] for d in track['artists']],
            'album': track['album']['name'],
            'popularity': track['popularity']
        })

    return res

def _get_top_items(access_token, type, time_range, limit):
    data = {}

    if time_range is not None:
        data['time_range'] = time_range

    if limit is not None:
        data['limit'] = limit

    url = f'https://api.spotify.com/v1/me/top/{type}?' + urllib.parse.urlencode(data)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPError()
    
    return response.json()['items']