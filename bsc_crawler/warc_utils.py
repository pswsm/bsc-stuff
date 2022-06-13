'''Does everything related to network and warcs'''
from pathlib import Path
from warcio.capture_http import capture_http
import requests
from url_is_live import url_is_live


def filter(req, resp, req_record):
    '''If request.statsucode is not 200, do not create a warc file'''
    try:
        if resp.http_headers.get_statuscode() != 200:
            return None, None
    except AttributeError:
       return None, None 
    return req, resp


def fetch_html(orig_url: str, folder: str = '', warc_folder: str = 'warcs'):
    '''Requests html from given url.
       Uses protocol (http or https) from
       return value of is_live() function'''
    is_live, protocol = url_is_live(orig_url)
    if is_live:
        with capture_http(f'{warc_folder}/{orig_url.replace("/", "_")}{folder.replace("/", "_")}.warc.gz', filter):
            requests.get(f'{protocol}{orig_url}{folder}', timeout=3)
            print(f'"{orig_url}{folder}" is online')


if __name__ == "__main__":
    from html_utils import get_html, remove_prefix, get_links
    the_url: str = 'plataforma-llengua.cat'
    done_links: list[str] = [ the_url ]
    html: str = get_html(the_url)
    fetch_html(the_url, warc_folder='tests/warc_utils')
    links: set[str] = remove_prefix(the_url, get_links(html))
    print(links)
    for link in links:
        if not link.startswith('/'):
            link = f"/{link}"
        fetch_html(the_url, folder=link, warc_folder='tests/warc_utils')
        done_links.append(link)
