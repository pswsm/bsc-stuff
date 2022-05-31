'''Crawler v0.0.1'''
from pathlib import Path
from warcio.capture_http import capture_http
import requests, file_utils
# from ssl import ConnectionResetError

# Disables warning for having SSL verification disabled
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def filter(req, resp, req_record):
    '''If request stattsucode is not 200, do not create a warc file'''
    try:
        if resp.http_headers.get_statuscode() != 200:
            return None, None
    except AttributeError:
       return None, None 
    return req, resp


def url_is_live(url: str) -> bool:
    '''Check if the url is live'''
    try:
        try:
            resp = requests.get(f'https://{url}', verify=False, timeout=3).status_code
            if resp == 200:
                return True
        except:
            pass
    except:
        try:
            resp = requests.get(f'http://{url}', verify=False, timeout=3).status_code
            if resp == 200:
                return True
        except:
            pass
    return False


def search_href(html: str) -> str:
    '''Searches an html text for a tags, and returns the link'''
    # unimplemented
    return ''


def fetch_html(orig_url: str):
    '''Requests html from given url.
       Tries https, if timeout falls back to http'''
    if url_is_live(orig_url):
        with capture_http(f'warcs/{orig_url}.warc.gz'):
            try:
                requests.get('https://' + orig_url, timeout=3, verify=False)
                print(f'"{orig_url}" is online')
            except (requests.ReadTimeout):
                print(f'"{orig_url}" timed out.')


def main():
    '''Main function. Runs the above'''
    all_urls: list[str] = file_utils.get_urls('domains_cat.txt')
    urls: list[str] = file_utils.trim_url_list(file_utils.last_url_index(all_urls), all_urls)
    for url in urls:
        fetch_html(url)


if __name__ == "__main__":
    main()
