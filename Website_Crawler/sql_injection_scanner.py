import requests
import sys
import subprocess
import re
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint


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
        # Example URL: http://testphp.vulnweb.com/artists.php?artist=1
        if language == "English":
            url = input("Insert the URL to scan --> ")
        else:
            url = input("Inserisci l'URL da scannerizzare --> ")
        if url.lower() == "exit":
            if language == "English":
                print("Goodbye!\n")
            else:
                print("Arrivederci!\n")
            loop = False
            break
        else:
            s = requests.Session()
            # if "dvwa" in url.lower():
            # if("dvwa" in url.lower()):
            # Login on DVWA
            # login_payload = {
            #     "username": "admin",
            #     "password": "password",
            #     "Login": "Login",
            # }
            # # change URL to the login page of your DVWA login URL
            # login_url = "http://localhost/DVWA-master/login.php"
            # # login
            # r = s.get(login_url)
            # token = re.search("user_token'\s*value='(.*?)'", r.text).group(1)
            # login_payload['user_token'] = token
            # s.post(login_url, data=login_payload)
            scan_sql_injection(url, s)
        if loop:
            while True:
                if language == "English":
                    choice = input("Do you want to exit the program? [Y/n]: ")
                else:
                    choice = input("Vuoi uscire dal programma? [Y/n]: ")
                choice = choice.lower()
                if choice == "y" or choice == "yes":
                    if language == "English":
                        print("Goodbye!\n")
                    else:
                        print("Arrivederci!\n")
                    loop = False
                    break
                elif choice == "n" or choice == "no":
                    if language == "English":
                        print("Returning to the menu!\n")
                    else:
                        print("Ritorno al menù!\n")
                    if mode == "menu":
                        with open("lang.txt", "a") as lang_file:
                            lang_file.write("\nmenu")
                        subprocess.Popen("Website_Crawler\\sql_injection_scanner.bat", shell=True)
                        sys.exit()
                    else:
                        break
                else:
                    if language == "English":
                        print("You have not entered a valid choice!")
                    else:
                        print("Non hai inserito una scelta valida!")


def get_all_forms(url, s):
    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    details = {}
    try:
        action = form.attrs.get("action").lower()
    except Exception:
        action = None
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return


def is_vulnerable(response):
    errors = {
        # MySQL
        "you have an error in your sql syntax;",
        "warning: mysql",
        # SQL Server
        "unclosed quotation mark after the character string",
        # Oracle
        "quoted string not properly terminated",
    }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False


def scan_sql_injection(url, s):
    for c in "\"'":
        new_url = f"{url}{c}"
        print("[!] Trying ", new_url)
        res = s.get(new_url)
        if is_vulnerable(res):
            print("[+] SQL Injection vulnerability detected, link: ", new_url)
            return
    forms = get_all_forms(url, s)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    for form in forms:
        form_details = get_form_details(form)
        for c in "\"'":
            data = {}
            try:
                for input_tag in form_details["inputs"]:
                    if input_tag["type"] == "hidden" or input_tag["value"]:
                        try:
                            data[input_tag["name"]] = input_tag["value"] + c
                        except Exception:
                            pass
                    elif input_tag["type"] != "submit":
                        data[input_tag["name"]] = f"test{c}"
            except TypeError:
                pass
            try:
                url = urljoin(url, form_details["action"])
                if form_details["method"] == "post":
                    res = bs.post(url, data=data)
                elif form_details["method"] == "get":
                    res = bs.get(url, params=data)
            except TypeError:
                pass
            if is_vulnerable(res):
                print("[+] SQL Injection vulnerability detected, link: ", url)
                print("[+] Form: ")
                pprint(form_details)
                break


if __name__ == "__main__":
    main()
