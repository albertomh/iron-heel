import json
from collections import Counter
import indicoio

indicoio.config.api_key = '$YOUR_API_KEY'


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
    """
    Returns a Counter and a Set. The Counter is of the form C({CITY: X, [...]})
    for each city in the dataset, where X is the number of mentions of Iron Heel in papers
    published in the city.

    The Set lists the state codes for states in which these papers appeared.

    """

    data = read()['data']
    l_city = []
    l_state = []

    for i in range(0, len(data)):
        l_city.append(data[str(i)]['loc'][0])
        l_state.append(data[str(i)]['loc'][1])

    print(Counter(l_city), '\n' * 2, set(l_state))


def by_year():
    """
    Returns a Counter of the type C({YEAR: X}) for all years where X is
    the number of times The Iron Heel was mentioned in a year.

    """

    data = read()['data']
    l_years = []

    for i in range(0, len(data)):
        l_years.append(data[str(i)]['date'][0:4])

    return Counter(l_years)


def by_cat(y1, y2):
    """
    Returns a Counter of the form C({CAT: X, [...]}) where CAT is a category label and X
    is the number of times the category label appears between the years y1, y2.

    """

    data = read()['data']
    l_cat = []

    for i in range(0, len(data)):
        if int(data[str(i)]['date'][0:4]) in range(y1, y2):
            l_cat.append(data[str(i)]['cat'])

    return Counter(l_cat)


def sentiment():
    """
    Uses indico.io's Sentiment Analysis API to analyse each text in tih-data.json and
    assign it a sentiment value.

    Writes a csv file of the form:
        Item,Category,Year,Sentiment
        X: YYYY/MM/DD,$category,YYYY,sentiment_score

    Where: sentiment_score is an integer between -100 and 100.
           and category has been previously manually assigned in tih-data.json.

    """

    data = read()

    with open('sentiment.csv', 'a') as outfile:

        outfile.write('Item,Category,Year,Sentiment\n')

        for i in range(len(data)):
            # Item in the format X: YYYY/MM/DD
            s1 = "{}{}{}".format(i + 1, ": ", data[str(i)]["date"])
            # Category e.g. Opinion, Advert, etc.
            s2 = data[str(i)]["cat"]
            # Year
            s3 = data[str(i)]["date"][0:4]
            # Sentiment
            s4 = indicoio.sentiment_hq(data[str(i)]["article"]["text"])
            s4 = s4 * 100
            if s4 > 50:
                pass
            elif s4 < 50:
                s4 = s4 - 100
            s4 = int(round(s4, 0))

            s = "{},{},{},{}".format(s1, s2, s3, s4)

            outfile.write("{}{}".format(s, '\n'))
            print("{}    {}".format(s1, s4))
