import requests
from requests.exceptions import HTTPError
import urllib

def _get_response(url, headers):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPError()
    
    return response

def _get_top_items(access_token, type, time_range, limit): # type is either artists or tracks
    data = {}

    if time_range is not None:
        data['time_range'] = time_range

    if limit is not None:
        data['limit'] = limit

    url = f'https://api.spotify.com/v1/me/top/{type}?' + urllib.parse.urlencode(data)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = _get_response(url, headers)
    
    return response.json()['items']

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
            'popularity': track['popularity'],
            'id': track['id']
        })

    return res

def get_top_genres(access_token: str, time_range=None, limit=None):
    if (limit is None):
        limit = 5
    else:
        limit = int(limit)

    genres = {}

    for artist in get_top_artists(access_token, time_range, 50):
        for genre in artist['genres']:
            genres[genre] = genres.get(genre, 0) + 1

    genres = [i[0] for i in sorted(genres.items(), key=lambda x:x[1], reverse=True)[:limit]]

    return genres

def get_audio_features(access_token: str, track_id: str):
    url = f'https://api.spotify.com/v1/audio-features/{track_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = _get_response(url, headers)
    
    return {k: v for k, v in response.json().items() if type(v) == float}

def get_top_audio_features(access_token: str, time_range=None):
    ids = [track['id'] for track in get_top_tracks(access_token, time_range, 50)]

    url = f'https://api.spotify.com/v1/audio-features?ids={",".join(ids)}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = _get_response(url, headers)
    
    top_features = {}

    for track in response.json()['audio_features']:
        for k, v in track.items():
            if type(v) == float:
                top_features[k] = top_features.get(k, 0) + v

    track_count = len(response.json()['audio_features'])

    for k, v in top_features.items():
        top_features[k] = round(v / track_count, 2)

    return top_features