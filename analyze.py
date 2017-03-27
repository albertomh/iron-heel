import json


def read():
    """
    Read, parse and return 'tih-data.json', which contains 46 records
    for mentions of Jack London's The Iron Heel in American newspapers.

    """

    with open('tih-data.json') as infile:
        parsed_json = json.load(infile)

        return parsed_json
