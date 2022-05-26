'''Crawler v0.0.1'''
from pathlib import Path
from warcio.capture_http import capture_http
import requests
# from ssl import ConnectionResetError


def get_urls(url_file: str) -> list[str]:
    '''Reads domains from file and splits them'''
    urls: list[str] = Path(url_file).read_text().split('\n')
    return urls


def fetch_html(orig_url: str) -> str:
    '''Requests html from given url.
       Tries https, if timeout falls back to http'''
    with capture_http(f'{orig_url}.warc.gz'):
        try:
            doc = requests.get('https://' + orig_url, timeout=3)
            result: str = f'{orig_url} is online'
        except requests.ConnectTimeout:
            try:
                doc = requests.get('http://' + orig_url, timeout=3)
                result: str = f'"{orig_url}" is online'
            except requests.ConnectTimeout:
                result: str = f'"{orig_url}" timed out'
        except requests.ConnectionError:
            result: str = f'"{orig_url}" not available'
    return result


def main():
    '''Main function. Runs the above'''
    urls: list[str] = get_urls('domains_cat.txt')
    for url in urls:
        fetch_html(url)


main()
