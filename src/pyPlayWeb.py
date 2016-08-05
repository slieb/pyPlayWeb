import requests
from bs4 import BeautifulSoup

response = requests.get('http://en.wikipedia.org/wiki/List_of_Nobel_laureates')

print "Status code is", response.status_code

soup = BeautifulSoup(response.content, "html.parser")
wikiTable = soup.find('table', {'class': 'wikitable sortable'})

def get_column_titles(table):
    # get the Nobel categories from the table header
    cols = []
    for th in table.find('tr').find_all('th')[1:]:  # ignore first column of Year and just get award categories
        link = th.find('a')
        # store the category name and any Wikipedia link it has
        if link:
            cols.append({'name': link.text, \
                         'href': link.attrs['href']})
        else:
            cols.append({'name': th.text, 'href': None})
    return cols


def get_nobel_winners_BS(table):
    cols = get_column_titles(table)
    winners = []
    for row in table.find_all('tr')[1:-1]:  # gets all rows starting from the second
        year = int(row.find('td').text)
        for i, td in enumerate(row.find_all('td')[1:]):
            for winner in td.find_all('a'):
                href = winner.attrs['href']
                if not href.startswith('#endnote'):
                    winners.append({
                        'year': year,
                        'category': cols[i]['name'],
                        'name': winner.text,
                        'link': winner.attrs['href']
                    })
    return winners


theWinners = get_nobel_winners_BS(wikiTable)
for winner in theWinners:
    if winner['category'] == "Literature":
        print winner['year'], ": ", winner['name']
