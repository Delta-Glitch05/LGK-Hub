import os, sys, subprocess, wikipedia
from requests_html import HTMLSession
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
            research = input("enter what you want to search for on Wikipedia (ex: Python programming language) --> ")
        else:
            research = input("inserisci ciò che vuoi cercare su Wikipedia (es: Python) --> ")
        if research.lower() == "exit":
            if language == "English":
                print("Goodbye!\n")
            else:
                print("Arrivederci!\n")
            loop = False
            break
        wiki_data_extractor(research, language)
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
                        subprocess.Popen("Website_Crawler\\wiki_data_extractor.bat", shell=True)
                        sys.exit()
                    else:
                        break


def wiki_data_extractor(research, language):
    page = wikipedia.page(research)
    if language == "English":
        sent_n = input("How many sentences of summary do you want? (Default: 2) --> ")
    else:
        sent_n = input("Quante frasi di riassunto vuoi? (Default: full summary) --> ")
    if not sent_n:
        summary = page.summary
    else:
        sent_n = int(sent_n)
        summary = wikipedia.summary(research, sentences=sent_n)
    result = wikipedia.search(research)
    #if language == "English":
    #    print(f"Summary: {summary}")
    #else:
    #    print(f"Riassunto: {summary}")
    title = page.title
    categories = page.categories
    content = page.content
    links = page.links
    references = page.references
    print(f"\nPage title: {title}")
    print(f"\nSummary: {summary}")
    if language == "English":
        choice = input("\nDo you want to visualize the categories? [Y/n] --> ")
    else:
        choice = input("\nVuoi visualizzare le categorie? [Y/n] --> ")
    if choice.lower() == "y" or choice.lower() == "yes" or choice.lower() == "s" or choice.lower() == "si":
        print(f"\nCategories: {categories}")
    if language == "English":
        choice = input("\nDo you want to visualize the links? [Y/n] --> ")
    else:
        choice = input("\nVuoi visualizzare i link? [Y/n] --> ")
    if choice.lower() == "y" or choice.lower() == "yes" or choice.lower() == "s" or choice.lower() == "si":
        print(f"\nLinks: {links}")
    if language == "English":
        choice = input("\nDo you want to visualize the references? [Y/n] --> ")
    else:
        choice = input("\nVuoi visualizzare i riferimenti? [Y/n] --> ")
    if choice.lower() == "y" or choice.lower() == "yes" or choice.lower() == "s" or choice.lower() == "si":
        print(f"\nReferences: {references}")
    if language == "English":
        choice = input("\nDo you want to visualize the full content? [Y/n] --> ")
    else:
        choice = input("\nVuoi visualizzare l'intero contenuto? [Y/n] --> ")
    if choice.lower() == "y" or choice.lower() == "yes" or choice.lower() == "s" or choice.lower() == "si":
        print(f"\nContent: {content}")

    if language == "English":
        choice = input("\nDo you want to visualize the related pages? [Y/n] --> ")
        if choice.lower() == "y" or choice.lower() == "yes":
            print(f"Related pages: {result}")
        choice = input("\nDo you want to visit a related page? [Y/n] --> ")
        if choice.lower() == "y" or choice.lower() == "yes":
            page_n = int(input("Insert the number of the related page to visit --> "))
            wiki_data_extractor(result[page_n], language)
    else:
        choice = input("\Vuoi visualizzare le pagine correlate? [Y/n] --> ")
        if choice.lower() == "y" or choice.lower() == "yes":
            print(f"Pagine correlate: {result}")
        choice = input("\nVuoi visitare una pagina correlata? [Y/n] --> ")
        if choice.lower() == "y" or choice.lower() == "yes" or choice.lower() == "s" or choice.lower() == "si":
            page_n = int(input("Inserisci il numero della pagina correlata da visitare --> "))
            wiki_data_extractor(result[page_n], language)


if __name__ == "__main__":
    main()
