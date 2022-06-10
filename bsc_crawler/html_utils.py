'''Does everything related to html.
   It is just text modification after all.'''
import re
import requests

# Disables warning for having SSL verification disabled
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def remove_prefix(base_url: str, urls: set[str]) -> set[str]:
    '''Removes "https://..." from a given url'''
    return set([url.removeprefix(base_url) for url in urls])

def get_html(url: str) -> str:
    '''Returns the html from a given URL'''
    try:
        html: str = requests.get(
            'https://' + url, timeout=3, verify=False).text
    except:
        print(f'\"{url}\" is not available')
    if 'html' in locals():
        return html
    return ''


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
