from lxml import html
import requests
import re


url1 = "http://chroniclingamerica.loc.gov/search/pages/results/?date1="
url2 = "&searchType=advanced&language=&sequence=0&index=0&proxdistance=5&state=&rows=20&ortext=&proxtext=&phrasetext=iron+heel&andtext=&dateFilterType=yearRange&page=1"


def news(y1, y2):
    """
    Returns a list of the names of newspapers found for the query "iron heel".

    """

    html = requests.get(url1 + str(y1) + "&sort=date&date2=" + str(y2) + url2)
    return re.findall('\=1\">(\w.*?\.)', str(html.content))


def search(y1, y2):
    """
    Looks for the number of matches between year1, year2.
    Returns a string of the form 'XX results containing [...]'.
    This string is then used by collect() to know how many matches
    for a query there are in a given year.

    For "iron heel" query, time range is 1836 - 1922.

    """

    page = requests.get(url1 + str(y1) + "&sort=date&date2=" + str(y2) + url2)
    tree = html.fromstring(page.content)

    matches = tree.xpath('//p[@class="term"]/text()')

    return matches[0]


def collect():
    """
    Writes a dictionary to collect.txt. The dictionary is of the form {YEAR: [i0, i1, i2], [...]} where:
        i0 is number of matches found by search(YEAR, YEAR).
        i1 is number of different papers that appear in i1.
        i2 is number of papers in circulation in the USA in YEAR.

    """

    d_results = {}

    for i in range(1836, 1924):
        matches = search(i, i)
        if matches:
            numbermatches = [int(s) for s in matches[0].split() if s.isdigit()]
            d_results[i] = [numbermatches[0], len(set(news(i, i))), papers(i)]
            print(i)
        else:
            d_results[i] = 0

    with open('collect.txt', 'w') as outfile:
        outfile.write(str(d_results))
    print('Done!')
