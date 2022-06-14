'''Does everything related to html.
   It is just text modification after all.'''
import re
import requests
from url_is_live import url_is_live


def remove_prefix(base_url: str, urls: set[str]) -> set[str]:
    '''Removes "https://..." from a given url'''
    return {url.removeprefix(base_url) for url in urls}


def get_html(url: str) -> str:
    '''Returns the html from a given URL'''
    is_live, protocol = url_is_live(url)
    html: str = ''
    if is_live:
        html = requests.get(f"{protocol}{url}", timeout=3).text
    return html


def get_links(html: str) -> set[str]:
    '''Searches an html text for urls in <a>'''
    # regex: str = r"<a.+href=\"((?:[\w]+\.?)?[/\w]+(?:\.cat)?)\".*>"
    regex: str = r"<a.+href=\"(?:https://|[\w:]+\.(?!html)|http://)?([\/\w\-]+(?:\.cat)?[\/\w+\-]+)\".*>"
    link_list: list[str] = re.findall(regex, html, re.UNICODE)
    return set(link_list)


if __name__ == '__main__':
    text: str = get_html('pswsm.cat')
    links: set[str] = get_links(text)
    print(links)
    for link in remove_prefix('pswsm.cat', links):
        print(link)
#       print(requests.get(f'https://esperit.cat{link}').text, f"\n\n\n\n\n\n\n\n")
