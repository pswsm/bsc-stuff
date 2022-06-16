'''Runs the code'''
import warc_utils
import html_utils
import file_utils


def main():
    '''Main function'''
    all_urls: list[str] = file_utils.get_urls('domains_cat.txt')
    urls: list[str] = file_utils.trim_url_list(file_utils.last_url_index(all_urls), all_urls)
    for url in urls:
        html: str = html_utils.get_html(url)
        warc_utils.fetch_html(url)
        all_links: set[str] = html_utils.get_links(html)
        filtered_urls: set[str] = html_utils.filter_urls(url, all_links)
        for link in filtered_urls:
            warc_utils.fetch_html(url, folder=link)


if __name__ == "__main__":
    main()
