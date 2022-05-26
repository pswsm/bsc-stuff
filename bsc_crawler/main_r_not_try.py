'''Crawler v0.0.1'''
from pathlib import Path
from requests.models import Response
from warcio.capture_http import capture_http
import requests
# from ssl import ConnectionResetError
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def filter(req, resp, req_record):
    '''If request stattsucode is not 200, return none'''
    try:
        if resp.http_headers.get_statuscode() != "200":
            return None, None
        return req, resp
    except AttributeError:
        print('No headers')


def get_urls(url_file: str) -> list[str]:
    '''Reads domains from file and splits them'''
    urls: list[str] = Path(url_file).read_text().split('\n')
    return urls


def search_href(html: str) -> str:
    '''Searches an html text for a tags, and returns the link'''
    return ''


def fetch_html(orig_url: str):
    '''Requests html from given url.
       Tries https, if timeout falls back to http'''
    with capture_http(f'{orig_url}.warc.gz', filter):
        try:
            result: str = f'"{orig_url}" is online'
            requests.get('https://' + orig_url, timeout=3, verify=False)
        except requests.ConnectTimeout as timeout:
            result: str = f"{timeout}"
    print(result)


def main():
    '''Main function. Runs the above'''
    urls: list[str] = get_urls('domains_cat.txt')
    for url in urls:
        fetch_html(url)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Killed :P")
