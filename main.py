import authorization
import stats
from argparse import ArgumentParser
from custom_prints import *
from json_handler import *

def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('--auth', action='store_true', help='add this option if you haven\'t authorized yet and tokens.json file is not present')
    parser.add_argument('--top', choices=['tracks', 'artists', 'genres', 'features'])
    parser.add_argument('--time-range', choices=['short_term', 'medium_term', 'long_term'])
    parser.add_argument('--limit', help='how many items to return, 1 to 50')

    parser.add_argument('--get-features', metavar='TRACK_ID')

    return parser.parse_args()

def main():
    args = parse_arguments()

    credentials = load_from_json('credentials.json')

    tokens = {} # access_token and refresh_token
    scope = 'user-top-read'

    if args.auth:
        try:
            tokens = authorization.get_tokens(credentials['client_id'], credentials['client_secret'], scope)

            save_to_json('tokens.json', tokens)

            print('Authorized successfully')

        except Exception as e:
            print(e)

    else:
        try:
            tokens = load_from_json('tokens.json')

            if authorization.check_access_token_validity(tokens['access_token']):
                print('Authorized successfully')

            else:
                print('Access token not valid, attemting to refresh it...')
                tokens['access_token'] = authorization.get_refreshed_access_token(credentials['client_id'], credentials['client_secret'], tokens['refresh_token'])

                save_to_json('tokens.json', tokens)

                print('Authorized successfully')

        except Exception as e:
            print(e)

    if args.top == 'artists':
        res = stats.get_top_artists(tokens['access_token'], args.time_range, args.limit)
        print_list_of_dicts(res)

    elif args.top == 'tracks':
        res = stats.get_top_tracks(tokens['access_token'], args.time_range, args.limit)
        print_list_of_dicts(res)

    elif args.top == 'genres':
        res = stats.get_top_genres(tokens['access_token'], args.time_range, args.limit)
        print_list(res)

    elif args.top == 'features':
        res = stats.get_top_audio_features(tokens['access_token'], args.time_range)
        print_dict(res, headers=['Feature', 'Value'])

    elif args.get_features:
        res = stats.get_audio_features(tokens['access_token'], args.get_features)
        print_dict(res, headers=['Feature', 'Value'])

if __name__ == '__main__':
    main()