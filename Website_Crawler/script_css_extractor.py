import requests, sys, subprocess
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin


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
        script_css_extractor(url, language)
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
                        subprocess.Popen("Website_Crawler\\script_css_extractor.bat", shell=True)
                        sys.exit()
                    else:
                        break


def script_css_extractor(url, language):
    session = requests.Session()
    html = session.get(url).content
    soup = bs(html, "html.parser")
    script_files = []
    for script in soup.find_all("script"):
        if script.attrs.get("src"):
            script_url = urljoin(url, script.attrs.get("src"))
            script_files.append(script_url)
    css_files = []
    for css in soup.find_all("link"):
        if css.attrs.get("href"):
            css_url = urljoin(url, css.attrs.get("href"))
            css_files.append(css_url)
    if language == "English":
        print(f"Total JavaScript files found: {len(script_files)}")
        print(f"Total CSS files found: {len(css_files)}")
    else:
        print(f"File JavaScript totali trovati: {len(script_files)}")
        print(f"File CSS totali trovati: {len(css_files)}")
    with open("javascript_files.txt", "w") as f:
        for js_file in script_files:
            print(js_file, file=f)
    with open("css_files.txt", "w") as f:
        for css_file in css_files:
            print(css_file, file=f)


if __name__ == "__main__":
    main()
