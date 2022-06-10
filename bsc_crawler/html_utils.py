'''Does everything related to html.
   It is just text modification after all.'''
import re
import requests


def remove_prefix(base_url: str, urls: set[str]) -> set[str]:
    '''Removes "https://..." from a given url'''
    return set([url.removeprefix(base_url) for url in urls])


def get_html(url: str) -> str:
    '''Returns the html from a given URL'''
    from url_is_live import url_is_live
    is_live, protocol = url_is_live(url)
    if is_live:
        html: str = requests.get(f"{protocol}{url}", timeout=3).text
    return html


def get_links(html: str) -> set[str]:
    '''Searches an html text for urls in <a>'''
    # regex: str = r"<a.+href=\"((?:[\w]+\.?)?[/\w]+(?:\.cat)?)\".*>"
    regex: str = r"<a.+href=\"(?:https://|[\w:]+\.|http://)?([\/\w\-]+(?:\.cat)?[\/\w+\-]+)\".*>"
    links: list[str] = re.findall(regex, html, re.UNICODE)
    return set(links)


if __name__ == '__main__':
    text: str = get_html('esperit.cat')
    for link in remove_prefix('esperit.cat', get_links(text)):
        print(link)
#       print(requests.get(f'https://esperit.cat{link}').text, f"\n\n\n\n\n\n\n\n")