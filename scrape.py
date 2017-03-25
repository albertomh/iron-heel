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
