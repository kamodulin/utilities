import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta

today = date.today()
first = today - timedelta(days=30)
today = today.strftime("%Y-%m-%d")
first = first.strftime("%Y-%m-%d")

def clean(string):
    return string.replace('\n', '').rstrip().lstrip().replace(u'\xa0', u' ')

class Journal:
    def request(self, search_url, payload):
        request = requests.post(search_url, data = payload)
        return BeautifulSoup(request.text, 'html.parser')
    
    def find_all(self, attrs):
        return self.result.find_all(attrs=attrs, limit=5)

    def find(self, pub, attrs):
        item = pub.find(attrs=attrs)
        if item:
            return clean(item.getText())

    def find_link(self, pub, attrs):
        link = pub.find(attrs=attrs, href=True)
        if link:
            return self.root + link['href']

    def search(self):
        self.pubs = []
        self.result = self.request(self.search_url, self.payload)
        for pub in self.find_all(self.pub):
            self.pubs.append([self.find(pub, self.title), self.find(pub, self.authors), self.find(pub, self.journal), self.find_link(pub, self.link)])
        return self.pubs

class bioRxiv(Journal):
    root = 'https://www.biorxiv.org'
    search_url = 'https://www.biorxiv.org/search'
    pub = {'class': 'search-result'}
    title = {'class': 'highwire-cite-title'}
    authors = {'class','highwire-citation-authors'}
    journal = {'class': 'highwire-cite-metadata-journal'}
    link = {'class': 'highwire-cite-linked-title'}

    def __init__(self, query):
        self.payload = {
            'txtsimple': query,
            'limit_from%5Bdate%5D_replacement': first,
            'limit_from%5Bdate%5D': today,
            'limit_to%5Bdate%5D_replacement': today,
            'limit_to%5Bdate%5D': today,
            'jcode%5B%5D': 'biorxiv',
            'numresults': '10',
            'sort': 'relevance-rank',
            'format_result': 'standard',
            'jcode_option': 'biorxiv',
            'form_id': 'highwire_search_form',
            'op': 'Search'
        }

class Nature(Journal):
    root = 'https://www.nature.com'
    search_url = 'https://www.nature.com/search/submit'
    pub = {'itemtype': 'http://schema.org/Article'}
    title = {'itemprop': 'url'}
    authors = {'class': 'js-list-authors-3'}
    journal = {'class': 'emphasis'}
    link = {'itemprop': 'url'}
    
    def __init__(self, query):
        self.payload = {
            'q': query,
            'author': '',
            'title': '',
            'start_year': '2019',
            'end_year': '2020',
            'journals': '',
            'volume': '',
            'spage': '',
            'order': 'relevance'
        }


print('Welcome to Magellan!')
print('What would you like to search for?')
query = input()
output_buffer = []
journals = Nature(query), bioRxiv(query)
for journal in journals:
    output_buffer.append(journal.search())
print(output_buffer)