from argparse import ArgumentParser
import json
import authorization
import stats

parser = ArgumentParser()

parser.add_argument('--auth', action='store_true', help='add this option if you haven\'t authorized yet and tokens.json file is not present')
parser.add_argument('--top', choices=['tracks', 'artists', 'genres'])
parser.add_argument('--time-range', choices=['short_term', 'medium_term', 'long_term'])
parser.add_argument('--limit', help='how many items to return, 1 to 50')

parser.add_argument('--get-features', metavar='TRACK_ID')

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

def print_list(list):
    for item in list:
        print(item)

if args.top == 'tracks':
    print_list(stats.get_top_tracks(tokens['access_token'], args.time_range, args.limit))
elif args.top == 'artists':
    print_list(stats.get_top_artists(tokens['access_token'], args.time_range, args.limit))
elif args.top == 'genres':
    print_list(stats.get_top_genres(tokens['access_token'], args.time_range, args.limit))

elif args.get_features is not None:
    print_list(stats.get_audio_features(tokens['access_token'], args.get_features))