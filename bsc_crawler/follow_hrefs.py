import re, requests

def get_url(url: str) -> str:
    '''Returns the html from a given URL'''
    html: str = requests.get('https://' + url).text
    return html

def get_links(html: str) -> set[str]:
    '''Searches an html text for urls in <a>'''
    links: list[str] = re.findall(r"href=\"([/\w]+)\"", html)
    return set(links)

if __name__ == '__main__':
    text: str = get_url('acn.cat')
    print(get_links(text))
