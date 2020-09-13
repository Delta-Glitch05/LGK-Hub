import sys, subprocess, requests, random
from stem.control import Controller
from stem import Signal
from bs4 import BeautifulSoup as bs
from builtins import Exception


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
        stop = proxy_rotator(language)
        if stop == "True":
            break
        elif stop == "Exit":
            loop = False
            break
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
                        subprocess.Popen("Website_Crawler\\proxy_rotator.bat", shell=True)
                        sys.exit()
                    else:
                        break


def proxy_rotator(language):
    stop = "False"
    while True:
        if language == "English":
            choice = input("Do you want to use free proxies (1) or TOR (2)? --> ")
        else:
            choice = input("Vuoi usare proxy gratuiti (1) or TOR (2)? --> ")
        if choice == "1" or choice == "1.":
            proxies = get_free_proxies(language)
            for i in range(5):
                s = get_session(proxies)
                try:
                    if language == "English":
                        print("Request page with IP:", s.get("http://icanhazip.com", timeout=1.5).text.strip())
                    else:
                        print("Richiesta pagina con IP:", s.get("http://icanhazip.com", timeout=1.5).text.strip())
                except:
                    continue
            stop = "True"
            break
        elif choice == "2" or choice == "2.":
            try:
                s = get_tor_session(language)
                ip = s.get("http://icanhazip.com").text
                print("IP:", ip)
                renew_connection()
                s = get_tor_session(language)
                ip = s.get("http://icanhazip.com").text
                print("IP:", ip)
                stop = "True"
                break
            except requests.exceptions.InvalidSchema as Exception:
                if language == "English":
                    print("TOR is not running on port 9050.\n")
                else:
                    print("TOR non è in esecuzione sulla porta 9050.\n")
        # elif choice == "3" or choice == "3.":
        #     url = "http://icanhazip.com"
        #     proxy_host = "proxy.crawlera.com"
        #     proxy_port = 8010
        #     if language == "English":
        #         api_key = input("Insert you API key --> ")
        #     else:
        #         api_key = input("Inserisci la tua chiave API --> ")
        #     try:
        #         proxy_auth = f"{api_key}:"
        #         proxies = {
        #         "https": f"https://{proxy_auth}@{proxy_host}:{proxy_port}/",
        #         "http": f"http://{proxy_auth}@{proxy_host}:{proxy_port}/"
        #         }
        #         r = requests.get(url, proxies=proxies, verify=False)
        #         stop = "True"
        #         break
        elif choice.lower() == "exit":
            if language == "English":
                print("Goodbye!\n")
            else:
                print("Arrivederci!\n")
            stop = "Exit"
            break
        else:
            if language == "English":
                print("You have not entered a valid choice!")
            else:
                print("Non hai inserito una scelta valida!")
    return stop


def get_free_proxies(language):
    url = "https://free-proxy-list.net/"
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies


def get_session(proxies):
    session = requests.Session()
    proxy = random.choice(proxies)
    print(proxy)
    session.proxies = {"http": proxy, "https": proxy}
    return session


def get_tor_session(language):
    session = requests.Session()
    session.proxies = {"http": "socks5://localhost:9050", "https": "socks5://localhost:9050"}
    return session


def renew_connection():
    with Controller.from_port(port=9051) as c:
        c.authenticate()
        c.signal(Signal.NEWNYM)


if __name__ == "__main__":
    main()
