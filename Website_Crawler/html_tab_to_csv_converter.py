import sys, subprocess, requests
import pandas as pd
from bs4 import BeautifulSoup as bs


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
            loop = False
            break
        tables_converter(url, language)
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
                        subprocess.Popen("Website_Crawler\\html_tab_to_csv_converter.bat", shell=True)
                        sys.exit()
                    else:
                        break


def tables_converter(url, language):
    soup = get_soup(url)
    tables = get_all_tables(soup)
    if language == "English":
        print(f"[+] Found a total of {len(tables)} tables.")
    else:
        print(f"[+] Trovate un totale di {len(tables)} tabelle.")
    for i, table in enumerate(tables, start=1):
        headers = get_table_headers(table)
        rows = get_table_rows(table)
        table_name = f"table-{i}"
        if language == "English":
            print(f"[+] Saving {table_name}")
        else:
            print(f"[+] Salvando {table_name}")
        save_as_csv(table_name, headers, rows)


def get_soup(url):
    session = requests.Session()
    html = session.get(url)
    return bs(html.content, "html.parser")


def get_all_tables(soup):
    return soup.find_all("table")


def get_table_headers(table):
    headers = []
    for th in table.find("tr").find_all("th"):
        headers.append(th.text.strip())
    return headers


def get_table_rows(table):
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = []
        tds = tr.find_all("td")
        if len(tds) == 0:
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
        else:
            for td in tds:
                cells.append(td.text.strip())
        rows.append(cells)
    return rows


def save_as_csv(table_name, headers, rows):
    pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")


if __name__ == "__main__":
    main()
