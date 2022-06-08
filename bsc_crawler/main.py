'''Crawler v0.0.1'''
from pathlib import Path
from warcio.capture_http import capture_http
import requests, file_utils
import follow_hrefs
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


def url_is_live(url: str) -> tuple[bool, str]:
    '''Check if the url is live'''
    try:
        try:
            resp: int = requests.get(f'https://{url}', verify=False, timeout=3).status_code
            if resp == 200:
                return True, 'https://'
        except:
            pass
    except:
        try:
            resp: int = requests.get(f'http://{url}', verify=False, timeout=3).status_code
            if resp == 200:
                return True, 'http://'
        except:
            pass
    return False, ''


def fetch_html(orig_url: str, folder: str = '', autoprotocol: bool = True):
    '''Requests html from given url.
       Tries https, if timeout falls back to http'''
    is_live, protocol = url_is_live(orig_url)
    if autoprotocol:
        if is_live:
            with capture_http(f'warcs/{orig_url.replace(":", "_").replace("/", "_")}{folder.replace("/", "_")}.warc.gz'):
                try:
                    requests.get(f'{protocol}{orig_url}{folder}', timeout=3, verify=False)
                    print(f'"{orig_url}{folder}" is online')
                except (requests.ReadTimeout, requests.ConnectionError):
                    print(f'"{orig_url}{folder}" timed out.')
    else:
        with capture_http(f'warcs/{orig_url.replace(":", "_").replace("/", "_")}{folder.replace("/", "_")}.warc.gz'):
            try:
                requests.get(f'{orig_url}{folder}', timeout=3, verify=False)
                print(f'"{orig_url}{folder}" is online')
            except (requests.ReadTimeout, requests.ConnectionError):
                print(f'"{orig_url}{folder}" timed out.')



def main():
    '''Main function. Runs the above'''
    all_urls: list[str] = file_utils.get_urls('domains_cat.txt')
    urls: list[str] = file_utils.trim_url_list(file_utils.last_url_index(all_urls), all_urls)
    for url in urls:
        done_links: list[str] = [ url ]
        fetch_html(url)
        html: str = follow_hrefs.get_html(url)
        for link in follow_hrefs.get_links(html):
            if link not in done_links:
                if link.startswith('http'):
                    fetch_html(link, autoprotocol=False)
                    done_links.append(link)
                else:
                    fetch_html(url, folder=link)
                    done_links.append(link)



if __name__ == "__main__":
    main()
