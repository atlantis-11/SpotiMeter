import base64
import webbrowser
import urllib
from urllib.parse import parse_qs, urlparse
import requests
from requests.exceptions import HTTPError

def get_tokens(client_id: str, client_secret: str, scope: str, redirect_uri='http://localhost:8888/callback'):
    webbrowser.open('https://accounts.spotify.com/authorize?' + urllib.parse.urlencode({
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri
    }))

    parsed_url = urlparse(input('Paste url you were redirected to: '))

    query_params = parse_qs(parsed_url.query)

    if 'error' in query_params:
        raise PermissionError('Error when getting code')

    code = query_params['code'][0]

    token_url = 'https://accounts.spotify.com/api/token'
    data = {
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    headers = {
        'Authorization': 'Basic ' + base64.urlsafe_b64encode(f'{client_id}:{client_secret}'.encode()).decode(),
        'Content-Type':	'application/x-www-form-urlencoded'
    }

    token_response = requests.post(token_url, data=data, headers=headers, json=True)

    if token_response.status_code != 200:
        raise HTTPError('Error when retrieving access token')
    
    token_response = token_response.json()

    return {'access_token': token_response['access_token'], 'refresh_token': token_response['refresh_token']}



def get_refreshed_access_token(client_id: str, client_secret: str, refresh_token: str):
    token_url = 'https://accounts.spotify.com/api/token'
    data = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    headers = {
        'Authorization': 'Basic ' + base64.urlsafe_b64encode(f'{client_id}:{client_secret}'.encode()).decode(),
        'Content-Type':	'application/x-www-form-urlencoded'
    }

    token_response = requests.post(token_url, data=data, headers=headers, json=True)

    if token_response.status_code != 200:
        raise HTTPError('Error when retrieving access token')
    
    token_response = token_response.json()

    return token_response['access_token']



def check_access_token_validity(access_token: str):
    url = 'https://api.spotify.com/v1/me'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    return requests.get(url, headers=headers).status_code == 200