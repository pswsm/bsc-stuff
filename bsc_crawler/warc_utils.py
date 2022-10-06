"""Does everything related to network and warcs"""
import re
from warcio.capture_http import capture_http
import requests

from url_is_live import url_is_live


def fetch_html(orig_url: str, folder: str = "", warc_folder: str = "warcs"):
    """Requests html from given url.
    Uses protocol (http or https) from return value of url_is_live() function"""
    is_live, protocol, _resp = url_is_live(orig_url)
    savefile: str = folder.replace("/", "_")
    if len(folder) > 74:
        savefile = '-'.join([word[0]
                       for word in set(savefile.split("-")) if word])

    if is_live:
        print(f'"{protocol}{orig_url}{folder}" is online')
        try:
            test: requests.Response = requests.get(f"{protocol}{orig_url}{folder}", timeout=3)
        except requests.exceptions.SSLError:
            print(f'"{protocol}{orig_url}{folder}" has an invalid certificate. Skipping')
        except requests.exceptions.RequestException:
            print(f'"{protocol}{orig_url}{folder}" was alive, but hasn not set a response')
        else:
            with capture_http(
                f'{warc_folder}/{orig_url.replace("/", "_")}{savefile}.warc.gz'
            ):
                try:
                    requests.get(f"{protocol}{orig_url}{folder}")
                except:
                    print("{orig_url} sucks")
                else:
                    requests.get(f"{protocol}{orig_url}{folder}")
    else:
        print(f"Skipping {protocol}{orig_url}{folder}")



if __name__ == "__main__":
    from html_utils import get_html, get_links, filter_urls

    the_urls: list[str] = ['3cat24.cat']
    for the_url in the_urls:
        html: str = get_html(the_url)
        fetch_html(the_url, warc_folder="tests/warc_utils")
        links: set[str] = filter_urls(the_url, get_links(html))
        for link in links:
            print(link)
            if re.search(r"[\w]\.cat", link, flags=re.UNICODE):
                fetch_html(link, warc_folder="tests/warc_utils")
            else:
                fetch_html(the_url, folder=link, warc_folder="tests/warc_utils")
