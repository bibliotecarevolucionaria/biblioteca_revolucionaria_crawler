import logging
import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup

import requests

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO
)


class Crawler:
    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls

    def write_html_to_file(self, text, name):
        if (name == ""):
            name = "index.html"
        with open(os.path.join('./output/', name), 'w', encoding='utf-8') as f:
            f.write(text)

    def download_url(self, url):
        page = requests.get(url).text
        self.write_html_to_file(page, url.rsplit('/', 1)[-1])
        return page

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')

            if path and (path.startswith('/') or path.endswith('.html')):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)


if __name__ == '__main__':
    crawler = Crawler(
        urls=['https://www.oocities.org/autonomiabvr/princpl.html'])
    crawler.run()
