import json
import authorization
import stats

tokens = {}
scope = 'user-top-read'
with open('credentials.json', 'r') as f:
    credentials = json.load(f)

while True:
    option = input('Use saved tokens (1) or sign-in (2)? ')

    if option == '1':
        try:
            with open('tokens.json', 'r') as f:
                tokens = json.load(f)

            if authorization.check_access_token_validity(tokens['access_token']):
                print('Authorized successfully')
                break

            else:
                print('Access token not valid, attemting to refresh it...')
                tokens['access_token'] = authorization.get_refreshed_access_token(credentials['client_id'], credentials['client_secret'], tokens['refresh_token'])

                with open('tokens.json', 'w') as f:
                    json.dump(tokens, f)

                print('Authorized successfully')
                break

        except Exception as e:
            print(e)

    elif option == '2':
        try:
            tokens = authorization.get_tokens(credentials['client_id'], credentials['client_secret'], scope)

            with open('tokens.json', 'w') as f:
                json.dump(tokens, f)

            print('Authorized successfully')
            break

        except Exception as e:
            print(e)