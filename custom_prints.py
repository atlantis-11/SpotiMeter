from tabulate import tabulate

def print_list_of_dicts(lst):
    print(tabulate([list(item.values()) for item in lst], [key.capitalize() for key in lst[0].keys()]))

def print_list(lst):
    for item in lst:
        print(item)

def print_dict(d, headers=['Key', 'Value']):
    rows = [[k, v] for k, v in d.items()]
    print(tabulate(rows, headers))