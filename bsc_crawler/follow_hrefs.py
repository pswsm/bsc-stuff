import re, requests

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
    regexp: str = r"a.+href=\"([\w\.]*[/\w]+[\.(cat|com|es|net)]*)\""
    links: list[str] = re.findall(regexp, html)
    return set(links)

if __name__ == '__main__':
    text: str = get_html('acn.cat')
    for link in get_links(text):
        print(requests.get('https://acn.cat' + link).text, "\n" * 5)
