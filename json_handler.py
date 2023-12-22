import json

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