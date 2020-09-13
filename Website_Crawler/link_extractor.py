import sys, subprocess, requests, colorama
from requests_html import HTMLSession
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as bs


colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
internal_urls = set()
external_urls = set()
total_urls_visited = 0


def get_lang_and_mode(mode):
    with open("lang.txt","r") as lang_file:
        list_ = lang_file.readlines()
        language = list_[0]
        if mode == "":
            if len(list_) == 2:
                mode = list_[1]
            else:
                mode = "terminal"
        lang_list = list(language)
        if lang_list[-1] == "\n":
            lang_list.pop()
        language = "".join(lang_list)
        if len(list_) >= 2:
            mode = list_[1]
            with open("lang.txt","w") as lang_file:
                lang_file.write(language)
    return language, mode


def main():
    mode = ""
    language, mode = get_lang_and_mode(mode)
    # print(f"{language}, {mode}")
    loop = True
    while loop == True:
        if language == "English":
            url = input("Insert the URL --> ")
        else:
            url = input("Inserisci l'URL --> ")
        if url.lower() == "exit":
            if language == "English":
                print("Goodbye!\n")
            else:
                print("Arrivederci!\n")
            loop = False
            break
        if language == "English":
            max_urls = input("Insert the maximum number of URLs --> ")
        else:
            max_urls = input("Inserisci il numero massimo di URL --> ")
        if max_urls.lower() == "exit":
            if language == "English":
                print("Goodbye!\n")
            else:
                print("Arrivederci!\n")
            loop = False
            break
        link_extractor(url, int(max_urls), language)
        if loop == True:
            while True:
                if language == "English":
                    exit_choice = input("Do you want to exit the program? [Y/n]: ")
                else:
                    exit_choice = input("Vuoi uscire dal programma? [Y/n]: ")
                exit_choice = exit_choice.lower()
                if exit_choice == "y" or exit_choice == "yes":
                    if language == "English":
                        print("Goodbye!\n")
                    else:
                        print("Arrivederci!\n")
                    loop = False
                    break
                elif exit_choice != "n" or exit_choice != "no":
                    if language == "English":
                        print("Returning to the menu!\n")
                    else:
                        print("Ritorno al menù!\n")
                    if mode == "menu":
                        with open("lang.txt", "a") as lang_file:
                            lang_file.write("\nmenu")
                        subprocess.Popen("Website_Crawler\\link_extractor.bat", shell=True)
                        sys.exit()
                    else:
                        break


def link_extractor(url, max_urls, language):
    crawl(url, max_urls, language)
    if language == "English":
        print(f"[+] Total Internal URLs: {len(internal_urls)}")
        print(f"[+] Total External URLs: {len(external_urls)}")
        print(f"[+] Total URLs: {len(internal_urls) + len(external_urls)}")
    else:
        print(f"[+] URL Interni Totali: {len(internal_urls)}")
        print(f"[+] URL Esterni Totali: {len(external_urls)}")
        print(f"[+] URL Totali: {len(internal_urls) + len(external_urls)}")
    domain_name = urlparse(url).netloc
    with open(f"{domain_name}_internal_links.txt", "w") as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)
    with open(f"{domain_name}_external_links.txt", "w") as f:
        for external_link in external_urls:
            print(external_link.strip(), file=f)


def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url, language):
    urls = set()
    domain_name = urlparse(url).netloc
    session = HTMLSession()
    response = session.get(url)
    try:
        response.html.render()
    except:
        pass
    # soup = bs(requests.get(url).content, "html.parser")
    soup = bs(response.html.html, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            continue
        if href in internal_urls:
            continue
        if domain_name not in href:
            if href not in external_urls:
                if language == "English":
                    print(f"{GRAY}[!] External link: {href}{RESET}")
                else:
                    print(f"{GRAY}[!] Link esterno: {href}{RESET}")
                external_urls.add(href)
            continue
        if language == "English":
            print(f"{GREEN}[*] Internal link: {href}{RESET}")
        else:
            print(f"{GREEN}[*] Link interno: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls


def crawl(url, max_urls, language):
    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url, language)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls, language)


if __name__ == "__main__":
    main()
