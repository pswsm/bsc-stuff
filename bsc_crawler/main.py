'''Crawler v0.0.1'''
import requests, asyncio, re, pyquery
from pathlib import Path
from pyquery import PyQuery as pq


def get_urls(url_file: str) -> list[str]:
    urls: list[str] = Path(url_file).read_text().split('\n')
    return urls

async def fetch_html(orig_url: str):
    try:
        doc = pq(url = 'https://' + orig_url)
    except requests.ConnectTimeout:
        doc = pq(url = 'http://' + orig_url)
    print(doc)
    return doc

def main():
    '''Main function. Runs the above'''
    urls = get_urls('domains_cat.txt')
    loop = asyncio.new_event_loop()
    loop.run_until_complete(fetch_html(urls[0]))


main()
