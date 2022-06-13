'''Searches the las warc done, and compares it to the domain list'''
from pathlib import Path

def get_urls(url_file: str) -> list[str]:
    '''Reads domains from file and splits them'''
    url_list: list[str] = Path(url_file).read_text(encoding='utf-8').split('\n')
    return url_list


def last_url_index(url_list: list[str]) -> int:
    '''Compares the warc recors ds with the file to resume from where the process finished'''
    warcs: list[Path] = list(Path('./warcs').glob('*.warc.gz'))
    if not warcs:
        return 0
    indexes: list[int] = [url_list.index(Path(warc.stem).stem) for warc in warcs
                          if Path(warc.stem).stem in url_list]
    if not indexes:
        return 0
    return max(indexes)


def trim_url_list(idx: int, url_list: list[str]) -> list[str]:
    '''Returns a list starting from index'''
    return list(url_list[idx:])

if __name__ == "__main__":
    urls: list[str] = get_urls("domains_cat.txt")
    urls_not_done: list[str] = trim_url_list(last_url_index(urls), urls)
    print(urls_not_done[0])
