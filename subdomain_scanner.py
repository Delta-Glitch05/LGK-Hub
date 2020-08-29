import requests, subprocess, sys

def main():
    mode = ""
    language, mode = get_lang_and_mode(mode)
    # print(f"{language}, {mode}")
    subdomain_scanner(language, mode)


def subdomain_scanner(language, mode):
    loop = True
    while(loop == True):
        if(language == "English"):
            domain = input("Insert the domain to scan --> ")
            if(domain.lower() == "exit"):
                print("Goodbye!\n")
                break
            sub_file = input("Enter the name of the list of subdomains to try --> ")
        else:
            domain = input("Inserisci il dominio da scannerizzare --> ")
            if(domain.lower() == "exit"):
                print("Arrivederci!\n")
                break
            sub_file = input("Inserisci il nome della lista di sottodomini da provare --> ")
        with open(sub_file, "r") as sub_file:
            subdomains = sub_file.read()
        subdomains = subdomains.splitlines()
        subdomains_list = []
        for subdomain in subdomains:
            url = f"http://{subdomain}.{domain}"
            try:
                requests.get(url)
                if(language == "English"):
                    print(f"[+] Discovered subdomain: {url}")
                else:
                    print(f"[+] Sottodominio scoperto: {url}")
                subdomains_list.append(url)
            except requests.ConnectionError:
                pass
        while True:
            if(language == "English"):
                choice = input("Do you want to save the URLs in a file? [Y/n]: ")
            else:
                choice = input("Vuoi salvare gli URL in un file? [Y/n]: ")
            choice = choice.lower()
            if(choice == "y" or choice == "yes"):
                if(language == "English"):
                    file_to_save = input("Insert the name of the file --> ")
                else:
                    file_to_save = input("Inserisci il nome del file --> ")
                with open(file_to_save, "w") as file_to_save:
                    for subdomain in subdomains_list:
                        file_to_save.write(f"{subdomain}\n")
                break
            elif(choice == "n" or choice == "no"):
                break
            else:
                if(language == "English"):
                    print("You have not entered a valid choice!")
                else:
                    print("Non hai inserito una scelta valida!")
        while True:
            if(language == "English"):
                choice = input("Do you want to exit the program? [Y/n]: ")
            else:
                choice = input("Vuoi uscire dal programma? [Y/n]: ")
            choice = choice.lower()
            if(choice == "y" or choice == "yes"):
                if(language == "English"):
                    print("Goodbye!\n")
                else:
                    print("Arrivederci!\n")
                loop = False
                break
            elif(choice == "n" or choice == "no"):
                if(language == "English"):
                    print("Returning to the menu!\n")
                else:
                    print("Ritorno al menù!\n")
                if(mode == "menu"):
                    with open("lang.txt", "a") as lang_file:
                        lang_file.write("\nmenu")
                    subprocess.Popen("open_subdomain_scanner.bat", shell=True)
                    sys.exit()
                else:
                    break
            else:
                if(language == "English"):
                    print("You have not entered a valid choice!")
                else:
                    print("Non hai inserito una scelta valida!")


def get_lang_and_mode(mode):
    with open("lang.txt","r") as lang_file:
        list_ = lang_file.readlines()
        language = list_[0]
        if(mode == ""):
            if(len(list_) == 2):
                mode = list_[1]
            else:
                mode = "terminal"
        lang_list = list(language)
        if(lang_list[-1] == "\n"):
            lang_list.pop()
        language = "".join(lang_list)
        if(len(list_) >= 2):
            mode = list_[1]
            with open("lang.txt","w") as lang_file:
                lang_file.write(language)
    return language, mode


if __name__ == "__main__":
    main()
