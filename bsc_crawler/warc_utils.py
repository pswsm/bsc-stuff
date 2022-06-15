'''Does everything related to network and warcs'''
from warcio.capture_http import capture_http
import requests
from url_is_live import url_is_live


def filter_w(req, resp, req_record):
    '''If request.statsucode is not 200, do not create a warc file'''
    try:
        if resp.http_headers.get_statuscode() != 200:
            return None, None
    except AttributeError:
        return None, None

    return req, resp


def fetch_html(orig_url: str, https_session: requests.Session, folder: str = '', warc_folder: str = 'warcs'):
    '''Requests html from given url.
       Uses protocol (http or https) from
       return value of is_live() function'''
    is_live, protocol = url_is_live(orig_url)
    savefile: str = folder.replace('/', '_')
    if len(folder) > 74:
        savefile = str([word[0] for word in set(folder.replace('/', '_').split('-'))])

    if is_live:
        try:
            with capture_http(f'{warc_folder}/{orig_url.replace("/", "_")}{savefile}.warc.gz', filter_w):
                https_session.get(f'{protocol}{orig_url}{folder}', timeout=5)
                print(f'"{protocol}{orig_url}{folder}" is online')
        except requests.ReadTimeout:
            print(f"{protocol}{orig_url}{folder} was online, but it's response timed out")
        except requests.exceptions.SSLError:
            with capture_http(f'{warc_folder}/{orig_url.replace("/", "_")}{savefile}.warc.gz', filter_w):
                https_session.get(f'http://{orig_url}{folder}', timeout=5)
                print(f'"http://{orig_url}{folder}" is online')


if __name__ == "__main__":
    from html_utils import get_html, remove_prefix, get_links
    sess: requests.Session = requests.Session()
    the_url: str = 'aceb.cat'
    done_links: list[str] = [ the_url ]
    html: str = get_html(the_url)
    fetch_html(the_url, sess, warc_folder='tests/warc_utils')
    links: set[str] = remove_prefix(the_url, get_links(html))

    for link in links:
        if not link.startswith('/'):
            link = f"/{link}"
        print(link)
        fetch_html(the_url, sess, folder=link, warc_folder='tests/warc_utils')
        done_links.append(link)
