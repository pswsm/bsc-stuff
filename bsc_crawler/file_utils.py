from pathlib import Path

def get_urls(url_file: str) -> list[str]:
    '''Reads domains from file and splits them'''
    urls: list[str] = Path(url_file).read_text().split('\n')
    return urls


def last_url_index(urls: list[str]) -> int:
    '''Compares the warc recors ds with the file to resume from where the process finished'''
    warcs: list[Path] = [warc for warc in Path('./warcs').glob('*.warc.gz')]
    if not warcs:
        return 0
    indexes: list[int] = [urls.index(Path(warc.stem).stem) for warc in warcs if Path(warc.stem).stem in urls]
    return max(indexes)


def trim_url_list(idx: int, urls: list[str]) -> list[str]:
    '''Returns a list starting from index'''
    return [url for url in urls[idx::]]

if __name__ == "__main__":
    urls: list[str] = get_urls("domains_cat.txt")
    urls_not_done: list[str] = trim_url_list(last_url_index(urls), urls)
    print(urls_not_done[0])
