import json


def read():

    with open('tih-data.json') as infile:
        parsed_json = json.load(infile)

        return parsed_json
