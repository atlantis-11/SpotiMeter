import requests
from requests.exceptions import HTTPError
import urllib

def get_top_artists(access_token: str, time_range='medium_term', limit=5):
    url = 'https://api.spotify.com/v1/me/top/artists?' + urllib.parse.urlencode({
        'time_range': time_range,
        'limit': limit
    })
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPError()

    res = []

    for artist in response.json()['items']:
        res.append({
            'name': artist['name'],
            'genres': artist['genres'],
            'popularity': artist['popularity']
        })

    return res

def get_top_tracks(access_token: str, time_range='medium_term', limit=5):
    url = 'https://api.spotify.com/v1/me/top/tracks?' + urllib.parse.urlencode({
        'time_range': time_range,
        'limit': limit
    })
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPError()

    res = []

    for track in response.json()['items']:
        res.append({
            'name': track['name'],
            'artists': [d['name'] for d in track['artists']],
            'album': track['album']['name'],
            'popularity': track['popularity']
        })

    return res