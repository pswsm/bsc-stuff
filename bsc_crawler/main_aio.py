'''Crawler v0.0.1'''
import aiohttp, re, pyquery
from pathlib import Path
from pyquery import PyQuery as pq


def get_urls(url_file: str) -> list[str]:
    urls: list[str] = Path(url_file).read_text().split('\n')
    return urls

def fetch_html(orig_url: str) -> str:
    return ''

def main():
    '''Main function. Runs the above'''
    urls: list[str] = get_urls('domains_cat.txt')


if __name__ == '__main__':
    main()
