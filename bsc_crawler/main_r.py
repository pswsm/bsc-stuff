'''Crawler v0.0.1'''
from pathlib import Path
from warcio.capture_http import capture_http
import requests
# from ssl import ConnectionResetError
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def filter(req, resp, req_record):
    '''If request stattsucode is not 200, return none'''
    if resp.http_headers.get_statuscode() != "200":
        return None, None
    return req, resp


def get_urls(url_file: str) -> list[str]:
    '''Reads domains from file and splits them'''
    urls: list[str] = Path(url_file).read_text().split('\n')
    return urls


def url_is_live(url: str) -> bool:
    '''Check if the url is live'''
    try:
        resp = requests.head(f'https://{url}', timeout=3)
        if resp:
            return True
        return False
    except:
        pass
    try:
        resp = requests.head(f'http://{url}', timeout=3)
        if resp:
            return True
        return False
    except:
        pass
    return False


def search_href(html: str) -> str:
    '''Searches an html text for a tags, and returns the link'''
    return ''


def fetch_html(orig_url: str):
    '''Requests html from given url.
       Tries https, if timeout falls back to http'''
    if url_is_live(orig_url):
        try:
            with capture_http(f'{orig_url}.warc.gz', filter):
                requests.get('https://' + orig_url, timeout=3, verify=False)
            result: str = f'"{orig_url}" is online (https)'
        except requests.ConnectTimeout:
            result: str = f'"{orig_url}" timed out'
        except requests.ConnectionError:
            result: str = f'"{orig_url}": Could not connect'
        try:
            with capture_http(f'{orig_url}.warc.gz', filter):
                requests.get('http://' + orig_url, timeout=3, verify=False)
            result: str = f'"{orig_url}" is online (http)'
        except requests.ConnectTimeout:
            result: str = f'"{orig_url}" timed out'
        except requests.ConnectionError:
            result: str = f'"{orig_url}": Could not connect'
        print(result)
    print(f"\"{orig_url}\" not alive")


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
