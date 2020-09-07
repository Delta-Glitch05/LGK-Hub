import pikepdf, subprocess, sys, fitz, re


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
            pdf_file = input("Insert the name of the PDF file --> ")
        else:
            pdf_file = input("Inserisci il nome del file PDF --> ")
        if pdf_file.lower() == "exit":
            if language == "English":
                print("Goodbye!\n")
            else:
                print("Arrivederci!\n")
            loop = False
            break
        pdf_link_extractor(pdf_file, language)
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
                        subprocess.Popen("Website_Crawler\\pdf_image_extractor.bat", shell=True)
                        sys.exit()
                    else:
                        break


def pdf_link_extractor(pdf_file, language):
    if language == "English":
        choice = input("Do you want to use the annotations (1) or the regex (2) method? --> ")
    else:
        choice = input("Vuoi usare il metodo con annotazioni (1) o con le espressioni regolari (2)? --> ")
    if choice == "1" or choice == "1.":
        pdf_file = pikepdf.Pdf.open(pdf_file)
        urls = []
        for page in pdf_file.pages:
            for annots in page.get("/Annots"):
                url = annots.get("/A").get("/URI")
                if url is not None:
                    if language == "English":
                        print(f"[+] URL Found: {url}")
                    else:
                        print(f"[+] URL Trovato: {url}")
                    urls.append(url)
        if language == "English":
            print(f"[*] Total URLs Extracted: {len(urls)}")
        else:
            print(f"[*] URL Totali Estratti: {len(urls)}")
    elif choice == "2" or choice == "2.":
        url_regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=\n]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
        with fitz.open(pdf_file) as pdf:
            text = ""
            for page in pdf:
                text += page.getText()
        urls = []
        for match in re.finditer(url_regex, text):
            url = match.group()
            if language == "English":
                print(f"[+] URL Found: {url}")
            else:
                print(f"[+] URL Trovato: {url}")
            urls.append(url)
        if language == "English":
            print(f"[*] Total URLs Extracted: {len(urls)}")
        else:
            print(f"[*] URL Totali Estratti: {len(urls)}")


if __name__ == "__main__":
    main()
