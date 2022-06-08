import re, requests

# Disables warning for having SSL verification disabled
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_html(url: str) -> str:
    '''Returns the html from a given URL'''
    try:
        html: str = requests.get('https://' + url, timeout=3, verify=False).text
    except:
        print(f'\"{url}\" is not available')
    if 'html' in locals():
        return html
    return ''

def get_links(html: str) -> set[str]:
    '''Searches an html text for urls in <a>'''
<<<<<<< Updated upstream
    regexp: str = r"a.+href=\"([\w\.]*[/\w]+[\.(cat|com|es|net)]*)\""
    links: list[str] = re.findall(regexp, html)
=======
    # regex: str = r"<a.+href=\"((?:[\w]+\.?)?[/\w]+(?:\.cat)?)\".*>"
    regex: str = r"<a.+href=\"((?:https://|[\w:]+\.|http://)?[\/\w\-]+(?:\.cat)?[\/\w+\-]+)\".*>"
    links: list[str] = re.findall(regex, html, re.UNICODE)
>>>>>>> Stashed changes
    return set(links)

if __name__ == '__main__':
    text: str = get_html('esperit.cat')
    for link in get_links(text):
<<<<<<< Updated upstream
        print(requests.get('https://acn.cat' + link).text, "\n" * 5)
=======
        print(link)
#       print(requests.get(f'https://esperit.cat{link}').text, f"\n\n\n\n\n\n\n\n")
>>>>>>> Stashed changes
