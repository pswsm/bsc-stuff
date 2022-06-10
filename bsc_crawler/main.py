'''Runs the code'''
import html_utils
import warc_utils
import file_utils

def main():
    '''Main function'''
    all_urls: list[str] = file_utils.get_urls('domains_cat.txt')
    urls: list[str] = file_utils.trim_url_list(file_utils.last_url_index(all_urls), all_urls)
    for url in urls:
        done_links: list[str] = [ url ]
        warc_utils.fetch_html(url)
        html: str = html_utils.get_html(url)
        for link in html_utils.remove_prefix(url, html_utils.get_links(html)):
            if not link.startswith("/"):
                link = f"/{link}"
            if link not in done_links:
                warc_utils.fetch_html(url, folder=link)
                done_links.append(link)



if __name__ == "__main__":
    main()
