import requests, sys, os, subprocess 
from tqdm import tqdm
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse


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
            path = input("Insert the path --> ")
        else:
            path = input("Inserisci il percorso --> ")
        if path.lower() == "exit":
            if language == "English":
                print("Goodbye!\n")
            else:
                print("Arrivederci!\n")
            loop = False
            break
        image_extractor(url, path, language)
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
                        subprocess.Popen("Website_Crawler\\image_extractor.bat", shell=True)
                        sys.exit()
                    else:
                        break


def image_extractor(url, path, language):
    images = get_all_images(url, language)
    for image in images:
        download(image, path, language)


def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images(url, language):
    session = HTMLSession()
    response = session.get(url)
    response.html.render()
    soup = bs(response.html.html, "html.parser")
    urls = []
    if language == "English":
        ext = "Extracting images"
    else:
        ext = "Estraendo le immagini"
    for img in tqdm(soup.find_all("img"), ext):
        img_url = img.attrs.get("src") or img.attrs.get("data-src")
        if not img_url:
            continue
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        if is_valid(img_url):
            urls.append(img_url)
    return urls


def download(url, path, language):
    if not os.path.isdir(path):
        os.makedirs(path)
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    file_name = os.path.join(path, url.split("/")[-1])
    if language == "English":
        downloading = "Downloading"
    else:
        downloading = "Scaricando"
    progress = tqdm(response.iter_content(1024), f"{downloading} {file_name}", total=file_size, unit="B", 
                    unit_scale=True, unit_divisor=1024)
    with open(file_name, "wb") as f:
        for data in progress:
            f.write(data)
            progress.update(len(data))


if __name__ == "__main__":
    main()
