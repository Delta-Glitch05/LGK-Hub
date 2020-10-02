import whois
import sys
import subprocess
import os


def get_lang_and_mode(mode):
    with open("lang.txt", "r") as lang_file:
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
            with open("lang.txt", "w") as lang_file:
                lang_file.write(language)
    return language, mode


def main():
    mode = ""
    language, mode = get_lang_and_mode(mode)
    # print(f"{language}, {mode}")
    loop = True
    while loop:
        if language == "English":
            domain_name = input("Insert the domain to scan --> ")
        else:
            domain_name = input("Inserisci il dominio da scannerizzare --> ")
        if domain_name.lower() == "exit":
            if language == "English":
                print("Goodbye!\n")
            else:
                print("Arrivederci!\n")
            loop = False
            break
        dom_name_info_extractor(domain_name, language)
        if loop:
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
                        subprocess.Popen("Website_Crawler\\ytc_extractor.bat", shell=True)
                        sys.exit()
                    else:
                        break


def dom_name_info_extractor(domain_name, language):
    if language == "English":
        print(f"{domain_name} is registered" if is_registered(domain_name) else f"{domain_name} is not registered")
    else:
        print(f"{domain_name} è registrato" if is_registered(domain_name) else f"{domain_name} non è registrato")
    if is_registered(domain_name):
        whois_info = whois.whois(domain_name)
        print(f"Domain registrar: {whois_info.registrar}")
        print(f"WHOIS server: {whois_info.whois_server}")
        print(f"Domain creation date: {whois_info.creation_date}")
        print(f"Domain expiration date: {whois_info.expiration_date}")
        # print(whois_info)


def is_registered(domain_name):
    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(w.domain_name)


if __name__ == "__main__":
    main()
