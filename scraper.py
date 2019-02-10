from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
found_links = {
        'https://medium.com/': True
}

def get_links(url):
    response = session.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')

    links = []
    for link in soup.find_all('a'):
        link_url = link.get('href')

        if link_url is not None and link_url.startswith('http'):
            if link_url.startswith('https://medium.com') and link_url not in found_links:
                    if link_url.startswith('https://medium.com/about') or link_url.startswith('https://medium.com/member'):
                        continue
                    found_links[link_url] = True
                    links.append(link_url + '\n')

    write_to_file(links)
    return links


def write_to_file(links):
    with open('data.txt', 'a') as f:
        f.writelines(links)


def get_all_links(url):
    for link in get_links(url):
        get_all_links(link)


website = 'https://medium.com/'
write_to_file([website])
write_to_file('\n')
get_all_links(website)
print('total number of links are {}'.format(len(found_links)))
