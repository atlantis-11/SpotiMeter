from argparse import ArgumentParser
import json
import authorization
import stats

parser = ArgumentParser()

parser.add_argument('--auth', action='store_true')
parser.add_argument('--top', choices=['tracks', 'artists', 'genres'])
parser.add_argument('--time-range', choices=['short_term', 'medium_term', 'long_term '])
parser.add_argument('--limit', choices=[str(i) for i in range(1, 51)])

args = parser.parse_args()

tokens = {} # access_token and refresh_token
scope = 'user-top-read'

with open('credentials.json', 'r') as f:
    credentials = json.load(f)

if not args.auth:
    try:
        with open('tokens.json', 'r') as f:
            tokens = json.load(f)

        if authorization.check_access_token_validity(tokens['access_token']):
            print('Authorized successfully')

        else:
            print('Access token not valid, attemting to refresh it...')
            tokens['access_token'] = authorization.get_refreshed_access_token(credentials['client_id'], credentials['client_secret'], tokens['refresh_token'])

            with open('tokens.json', 'w') as f:
                json.dump(tokens, f)

            print('Authorized successfully')

    except Exception as e:
        print(e)

else:
    try:
        tokens = authorization.get_tokens(credentials['client_id'], credentials['client_secret'], scope)

        with open('tokens.json', 'w') as f:
            json.dump(tokens, f)

        print('Authorized successfully')

    except Exception as e:
        print(e)

if args.top == 'tracks':
    print(stats.get_top_tracks(tokens['access_token'], args.time_range, args.limit))
elif args.top == 'artists':
    print(stats.get_top_artists(tokens['access_token'], args.time_range, args.limit))
elif args.top == 'genres':
    print(stats.get_top_genres(tokens['access_token'], args.time_range, args.limit))