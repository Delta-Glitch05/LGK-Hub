import sys, subprocess
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pprint import pprint
from urllib.parse import urljoin
import webbrowser


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


def main():
    mode = ""
    language, mode = get_lang_and_mode(mode)
    # print(f"{language}, {mode}")
    loop = True
    while(loop == True):
        if(language == "English"):
            url = input("Insert the URL of the website --> ")
        else:
            url = input("Inserisci l'URL del sito web --> ")
        if(url.lower() == "exit"):
            if(language == "English"):
                print("Goodbye!\n")
            else:
                print("Arrivederci!\n")
            loop = False
            break
        web_forms_extractor(url, language)
        if(loop == True):
            while True:
                if(language == "English"):
                    exit_choice = input("Do you want to exit the program? [Y/n]: ")
                else:
                    exit_choice = input("Vuoi uscire dal programma? [Y/n]: ")
                exit_choice = exit_choice.lower()
                if(exit_choice == "y" or exit_choice == "yes"):
                    if(language == "English"):
                        print("Goodbye!\n")
                    else:
                        print("Arrivederci!\n")
                    loop = False
                    break
                elif(exit_choice != "n" or exit_choice != "no"):
                    if(language == "English"):
                        print("Returning to the menu!\n")
                    else:
                        print("Ritorno al menù!\n")
                    if(mode == "menu"):
                        with open("lang.txt", "a") as lang_file:
                            lang_file.write("\nmenu")
                        subprocess.Popen("Website_Crawler\\web_forms_extractor.bat", shell=True)
                        sys.exit()
                    else:
                        break


def get_all_forms(session, url):
    res = session.get(url)
    # for javascript driven website
    # res.html.render()
    soup = BeautifulSoup(res.html.html, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    details = {}
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value =input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def web_forms_extractor(url, language):
    session = HTMLSession()
    forms = get_all_forms(session, url)
    for i, form in enumerate(forms, start=1):
        form_details = get_form_details(form)
        print("="*50, f"form #{i}", "="*50)
        pprint(form_details)
    while True:
        if language == "English":
            choice = input("Do you want to submit a web form? [Y/n]: ")
        else:
            choice = input("Vuoi inviare un modulo web? [Y/n]: ")
        if(choice.lower() == "yes" or choice.lower() == "y"):
            web_forms_submitter(url, session, language)
            break
        elif(choice.lower() == "n" or choice.lower() == "no"):
            break
        else:
            if language == "English":
                print("You have not entered a valid choice!")
            else:
                print("Non hai inserito una scelta valida!")


def web_forms_submitter(url, session, language):
    if language == "English":
        num = int(input("Which web form do you want to submit? (Insert the number) --> "))
    else:
        num = int(input("Quale modulo web vuoi inviare? (Inserisci il numero) --> "))
    form = get_all_forms(session, url)[num - 1]
    form_details = get_form_details(form)
    data = {}
    for input_tag in form_details["inputs"]:
        if input_tag["type"] == "hidden":
            data[input_tag["name"]] = input_tag["value"]
        elif input_tag["type"] != "submit":
            if language == "English":
                value = input(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): ")
            else:
                value = input(f"Inserisci il valore nel campo '{input_tag['name']}' (tipo: {input_tag['type']}): ")
            data[input_tag["name"]] = value
    url = urljoin(url, form_details["action"])
    if form_details["method"] == "post":
        res = session.post(url, data=data)
    elif form_details["method"] == "get":
        res = session.get(url, params=data)

    # the below code is only for replacing relative URLs to absolute ones
    soup = BeautifulSoup(res.content, "html.parser")
    for link in soup.find_all("link"):
        try:
            link.attrs["href"] = urljoin(url, link.attrs["href"])
        except:
            pass
    for script in soup.find_all("script"):
        try:
            script.attrs["src"] = urljoin(url, link.attrs["src"])
        except:
            pass
    for img in soup.find_all("img"):
        try:
            img.attrs["src"] = urljoin(url, img.attrs["src"])
        except:
            pass
    for a in soup.find_all("a"):
        try:
            a.attrs["href"] = urljoin(url, a.attrs["href"])
        except:
            pass
    
    open("page.html", "w", encoding="utf-8").write(str(soup.prettify()))
    webbrowser.open("page.html")


if __name__ == "__main__":
    main()
