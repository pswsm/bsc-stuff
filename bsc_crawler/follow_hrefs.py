import re
import requests

# Disables warning for having SSL verification disabled
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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


def correct_link(inner_link: str) -> str:
    '''Checks if html link is correct and corrects it:
        some/link.html -> /some/link.html'''
    if not link.startswith("/"):
        return f"/{inner_link}"
    return inner_link


def get_links(html: str) -> set[str]:
    '''Searches an html text for urls in <a>'''
    # regex: str = r"<a.+href=\"((?:[\w]+\.?)?[/\w]+(?:\.cat)?)\".*>"
    regex: str = r"<a.+href=\"((?:https://|[\w:]+\.|http://)?[\/\w\-]+(?:\.cat)?[\/\w+\-]+)\".*>"
    links: list[str] = re.findall(regex, html, re.UNICODE)
    return set(links)


if __name__ == '__main__':
    text: str = get_html('esperit.cat')
    for link in get_links(text):
        corrected_link: str = correct_link(link)
        print(corrected_link)
#       print(requests.get(f'https://esperit.cat{link}').text, "\n" * 5)
