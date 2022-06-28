'''Runs the code'''
import re
import warc_utils
import html_utils
import file_utils


def main_loop(url_list: list[str] = [], done_links: list[str] = []):
    '''The main loop'''
    for url in url_list:
        html: str = html_utils.get_html(url)
        warc_utils.fetch_html(url)
        done_links.append(url)
        all_links: set[str] = html_utils.get_links(html)
        filtered_urls: set[str] = html_utils.filter_urls(url, all_links)
        for link in filtered_urls:
            if link not in done_links:
                if re.search(r"[\w]\.cat", link, flags=re.UNICODE):
                    warc_utils.fetch_html(link)
                    done_links.append(link)
                else:
                    warc_utils.fetch_html(url, folder=link)
                    done_links.append(f"{url}/{link}")
                main_loop(url_list[1::], done_links)



def main():
    '''Main function'''
    try:
        done: list[str] = []
        all_urls: list[str] = file_utils.get_urls('domains_cat.txt')
        urls: list[str] = file_utils.trim_url_list(file_utils.last_url_index(all_urls), all_urls)
        print(f'Starting point: "{urls[0]}"')
    #   main_loop(urls, done)
        for url in urls:
            html: str = html_utils.get_html(url)
            warc_utils.fetch_html(url)
            all_links: set[str] = html_utils.get_links(html)
            filtered_urls: set[str] = html_utils.filter_urls(url, all_links)
            for link in filtered_urls:
                if re.search(r"[\w]\.cat", link, flags=re.UNICODE):
                    warc_utils.fetch_html(link)
                else:
                    warc_utils.fetch_html(url, folder=link)
    except:
        print('That web sucks and the server is just wrong')


if __name__ == "__main__":
    main()
