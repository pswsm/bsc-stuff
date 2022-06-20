"""Does everything related to html.
   It is just text modification after all."""
import re
import requests
from url_is_live import url_is_live


def correct(bad_link: str) -> str:
    '''Corrects the link to what this program needs'''
    regex: str = r"(www\.[\w]+\.[a-z]{3})|([\w\.]+\.cat)"
    subst = ""
    result = re.sub(regex, subst, bad_link, 0, flags = re.MULTILINE | re.UNICODE)
    if result.endswith('/'):
        result = ''.join(result.rsplit('/', 1))
    if not result.startswith('/'):
        result = f"/{result}"
    return result


def filter_urls(base_url: str, urls: set[str]) -> set[str]:
    """Removes "http[s]://..." from a given url
       and runs the "correct" function on each"""
    return {correct(url.removeprefix(base_url)) for url in urls if url != '/'}


def get_html(url: str) -> str:
    """Returns the html from a given URL"""
    is_live, protocol, _resp = url_is_live(url)
    html: str = ''
    if is_live:
        try:
            requests.get(f"{protocol}{url}", timeout=3)
            html = requests.get(f"{protocol}{url}", timeout=3).text
        except requests.exceptions.SSLError:
            pass
        except requests.exceptions.RequestException:
            pass
    return html


def get_links(html: str) -> set[str]:
    """Searches an html text for urls in <a>"""
    # regex: str = r"<a.+href=\"((?:[\w]+\.?)?[/\w]+(?:\.cat)?)\".*>"
    regex: str = r"<a.+href=\"(?:https://|[\w:]+\.(?!html)|http://)?(?:\.?www\.?)?([\/\w\-]+(?:\.cat)?[\/\w\-]+)\".*>"
    link_list: list[str] = re.findall(regex, html, re.UNICODE)
    return set(link_list)


if __name__ == "__main__":
    the_url: str = '1973.cat'
    text: str = get_html(the_url)
    links: set[str] = get_links(text)
    for link in filter_urls(the_url, links):
        print(link)
