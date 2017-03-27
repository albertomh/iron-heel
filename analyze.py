import json
from collections import Counter


def read():
    """
    Read, parse and return 'tih-data.json', which contains 46 records
    for mentions of Jack London's The Iron Heel in American newspapers.

    """

    with open('tih-data.json') as infile:
        parsed_json = json.load(infile)["data"]

        return parsed_json


def countcat():
    """
    Returns a list of the category tags found in the data.

    """

    l_cat = []

    for i in range(0, len(read()['data'])):
        l_cat.append(read()['data'][str(i)]['cat'])

    return l_cat


def placefinder():

    data = read()['data']
    l_city = []
    l_state = []

    for i in range(0, len(data)):
        l_city.append(data[str(i)]['loc'][0])
        l_state.append(data[str(i)]['loc'][1])

    print(Counter(l_city), '\n' * 2, set(l_state))
