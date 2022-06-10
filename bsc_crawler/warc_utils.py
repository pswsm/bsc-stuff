'''Does everything related to network and warcs'''
from pathlib import Path
from warcio.capture_http import capture_http
import requests, file_utils
import html_utils
# from ssl import ConnectionResetError

# Disables warning for having SSL verification disabled
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def filter(req, resp, req_record):
    '''If request.statsucode is not 200, do not create a warc file'''
    try:
        if resp.http_headers.get_statuscode() != 200:
            return None, None
    except AttributeError:
       return None, None 
    return req, resp




def fetch_html(orig_url: str, folder: str = '', autoprotocol: bool = True):
    '''Requests html from given url.
       Uses protocol (http or https) from
       return value of is_live() function'''
    is_live, protocol = url_is_live(orig_url)
    if is_live:
        with capture_http(f'warcs/{orig_url.replace(":", "_").replace("/", "_")}{folder.replace("/", "_")}.warc.gz'):
            try:
                requests.get(f'{protocol}{orig_url}{folder}', timeout=3, verify=False)
                print(f'"{orig_url}{folder}" is online')
            except (requests.ReadTimeout, requests.ConnectionError):
                print(f'"{orig_url}{folder}" timed out.')


if __name__ == "__main__":
    print("Do something")
