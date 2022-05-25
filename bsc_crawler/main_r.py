'''Crawler v0.0.1'''
import requests, asyncio, re, pyquery
from pathlib import Path
from pyquery import PyQuery as pq


def get_urls(url_file: str) -> list[str]:
    urls: list[str] = Path(url_file).read_text().split('\n')
    return urls

async def fetch_html(orig_url: str) -> str:
    try:
        doc = requests.get('https://' + orig_url, timeout=10)
    except requests.ConnectTimeout:
        doc = requests.get('http://' + orig_url, timeout=10)

    print(doc.text)
    return doc.text

def main():
    '''Main function. Runs the above'''
    urls: list[str] = get_urls('domains_cat.txt')
    loop = asyncio.new_event_loop()
    loop.run_until_complete(fetch_html(urls))


main()
