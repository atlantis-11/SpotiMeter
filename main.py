from argparse import ArgumentParser
import json
import authorization
import stats
from custom_prints import print_list, print_dict

def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('--auth', action='store_true', help='add this option if you haven\'t authorized yet and tokens.json file is not present')
    parser.add_argument('--top', choices=['tracks', 'artists', 'genres'])
    parser.add_argument('--time-range', choices=['short_term', 'medium_term', 'long_term'])
    parser.add_argument('--limit', help='how many items to return, 1 to 50')

    parser.add_argument('--get-features', metavar='TRACK_ID')

    return parser.parse_args()

def load_from_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
        
    except FileNotFoundError:
        raise FileNotFoundError(f'No {filename} file')
    
def save_to_json(filename, dict):
    try:
        with open(filename, 'w') as f:
            json.dump(dict, f)

    except FileNotFoundError:
        raise FileNotFoundError(f'No {filename} file')

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

    if args.get_features:
        print_dict(stats.get_audio_features(tokens['access_token'], args.get_features))

    elif args.top:
        top_functions = {'tracks': stats.get_top_tracks, 'artists': stats.get_top_artists, 'genres': stats.get_top_genres}
        get_top = top_functions[args.top]

        print_list(get_top(tokens['access_token'], args.time_range, args.limit))

if __name__ == '__main__':
    main()