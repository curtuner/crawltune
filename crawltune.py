import requests
import queue
from bs4 import BeautifulSoup
from urllib.parse import urljoin


roots = ['https://www.douban.com',
         'https://www.bing.com']

# a set of visited url
visited = set()

# a set of url that need to be read
urls_to_read = queue.Queue


def handle_page(page, page_url):
    """
    这里的page是文本格式的
    """
    soup = BeautifulSoup(page, 'lxml')
    for link in soup.find_all('a'):
        url = link.get('href')
        if url:
            url = urljoin(page_url, url)
            url = url.split('#')[0]
            if url[0:4] == 'http':
                urls_to_read.put(url)


def main():
    # init
    for root in roots:
        urls_to_read.put(root)

    while not urls_to_read.empty():
        url = urls_to_read.get()
        if url not in visited:
            response = requests.get(url)
            response.encoding = 'utf-8'
            handle_page(requests.text, url)


if __name__ == '__main__':
    main()
