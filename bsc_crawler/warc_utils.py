"""Does everything related to network and warcs"""
from warcio.capture_http import capture_http
import requests

from url_is_live import url_is_live


def fetch_html(orig_url: str, folder: str = "", warc_folder: str = "warcs"):
    """Requests html from given url.
    Uses protocol (http or https) from return value of url_is_live() function"""
    is_live, protocol, _resp = url_is_live(orig_url)
    savefile: str = folder.replace("/", "_")
    if len(folder) > 74:
        savefile = str([word[0]
                       for word in set(folder.replace("/", "_").split("-"))])

    if is_live:
        try:
            requests.get(f"{protocol}{orig_url}{folder}", timeout=5)
        except requests.exceptions.SSLError:
            print(f'"{protocol}{orig_url}{folder}" has an invalid certificate. Skipping')
        except requests.exceptions.RequestException:
            print(f'"{protocol}{orig_url}{folder}" was alive, but hasn not set a response')
        else:
            with capture_http(
                f'{warc_folder}/{orig_url.replace("/", "_")}{savefile}.warc.gz'
            ):
                requests.get(f"{protocol}{orig_url}{folder}", timeout=5)
                print(f'"{protocol}{orig_url}{folder}" is online')


if __name__ == "__main__":
    from html_utils import get_html, get_links, filter_urls

    the_urls: list[str] = ['12dos.cat']
    for the_url in the_urls:
        html: str = get_html(the_url)
        fetch_html(the_url, warc_folder="tests/warc_utils")
        links: set[str] = filter_urls(the_url, get_links(html))
        for link in links:
            fetch_html(the_url, folder=link, warc_folder="tests/warc_utils")
            print(link)
