import authorization
import json
import requests

tokens = {}
scope = 'user-top-read'

while True:
    option = input('Use tokens file (1) or sign-in (2)? ')

    if option == '1':
        try:
            with open('tokens.json', 'r') as f:
                tokens = json.load(f)

            if authorization.check_access_token_validity(tokens['access_token']):
                print('Authorized successfully')
                break
            else:
                print('Access token not valid, attemting to refresh it...')
                tokens['access_token'] = authorization.get_refreshed_access_token(tokens['refresh_token'])
                print('Authorized successfully')
                break

        except Exception as e:
            print(e)

    elif option == '2':
        try:
            with open('credentials.json', 'r') as f:
                credentials = json.load(f)

            tokens = authorization.get_tokens(credentials['client_id'], credentials['client_secret'], scope)

            with open('tokens.json', 'w') as f:
                json.dump(tokens, f)

            print('Authorized successfully')

            break

        except Exception as e:
            print(e)

url = 'https://api.spotify.com/v1/me/top/artists'
headers = {
    'Authorization': 'Bearer ' + tokens['access_token']
}

response = requests.get(url, headers=headers)

print(response.json())