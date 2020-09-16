import sys, subprocess, platform
from scapy.all import ARP, Ether, srp
from socket import *
import time
from datetime import datetime
import threading
from threading import Thread
from queue import Queue
from colorama import init, Fore
from ipaddress import IPv4Network
from pprint import pprint


def main():
    mode = ""
    language, mode = get_lang_and_mode(mode)
    # print(f"{language}, {mode}")
    loop = True
    loop_2 = True
    while loop == True:
        if language == "English":
            print("""CHOOSE ONE OF THE FOLLOWING OPTIONS:
            1. SCAN THE NETWORK TO DISCOVER ITS DEVICES;
            2. SCAN THE NETWORK AND THEN THE SINGLE DEVICES;
            3. SCAN A SINGLE DEVICE;
            4. PING SWEEPING.""")
        else:
            print("""SCEGLI UNA DELLE SEGUENTI OPZIONI:
            1. SCANNERIZZARE LA RETE PER SCOPRIRNE I DISPOSITIVI;
            2. SCANNERIZZARE LA RETE E I SINGOLI DISPOSITIVI;
            3. SCANNERIZZARE UN SINGOLO DISPOSITIVO;
            4. PING SWEEPING.""")
        while loop_2 == True:
            if language == "English":
                choice = input("INSERT YOUR CHOICE: ")
            else:
                choice = input("INSERISCI LA TUA SCELTA: ")
            if choice == "1" or choice == "1.":
                if language == "English":
                    choice_2 = input("DO YOU WANT TO USE THE TCP (1) OR ARP (2) SCANNER? ")
                else:
                    choice_2 = input("VUOI USARE LO SCANNER TCP (1) O ARP (2)? ")
                if choice_2 == "1" or choice_2 == "1.":
                    tcp_network_scanner(language)
                    break
                elif choice_2 == "2" or choice_2 == "2.":
                    arp_scan(language)
                    break
                else:
                    if language == "English":
                        print("You have not entered a valid choice!")
                    else:
                        print("Non hai inserito una scelta valida!")
            elif choice == "2" or choice == "2.":
                adv_net_scanner(language)
                break
            elif choice == "3" or choice == "3.":
                while True:
                    if language == "English":
                        choice_2 = input("DO YOU WANT TO USE THE SOCKET (1) OR THREADED (2) SCANNER? ")
                    else:
                        choice_2 = input("VUOI USARE LO SCANNER SOCKET (1) O THREADED (2)? ")
                    if choice_2 == "1" or choice_2 == "1.":
                        socket_port_scanner(language)
                        loop_2 = False
                        break
                    elif choice_2 == "2" or choice_2 == "2.":
                        threaded_port_scanner(language)
                        loop_2 = False
                        break
                    else:
                        if language == "English":
                            print("You have not entered a valid choice!")
                        else:
                            print("Non hai inserito una scelta valida!")
            elif choice == "4" or choice == "4.":
                ping_sweeper(language)
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
                    print("You have not entered a valid choice!")
                else:
                    print("Non hai inserito una scelta valida!")
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
                elif exit_choice == "n" or exit_choice == "no":
                    if language == "English":
                        print("RETURNING TO THE MENU!\n")
                    else:
                        print("RITORNO AL MENÙ!\n")
                    if mode == "menu":
                        with open("lang.txt", "a") as lang_file:
                            lang_file.write("\nmenu")
                        subprocess.Popen("network_scanner.bat", shell=True)
                        sys.exit()
                    else:
                        break
                else:
                    if language == "English":
                        print("You have not entered a valid choice!")
                    else:
                        print("Non hai inserito una scelta valida!")


threads = []
clients = list()
class ARP_Network_Scanner(Thread):
    def __init__(self, ip):
        super().__init__()
        self.ip = ip
    def run(self):
        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=self.ip)
        result = srp(packet, timeout=3, verbose=0)[0]
        for _, received in result:
            clients.append(
                {
                    "ip": received.psrc,
                    "mac": received.hwsrc
                }
            )
        time.sleep(1)


def arp_scan(language):
    if language == "English":
        target_ip = input("Insert the IP address to scan --> ")
    else:
        target_ip = input("Inserisci l'indirizzo IP da scannerizzare --> ")
    start = time.time()
    for ip in IPv4Network(f"{target_ip}/24").hosts():
        t = ARP_Network_Scanner(str(ip))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    pprint(clients)
    if language == "English":
        print(f"Executed in {time.time() - start} seconds.")
    else:
        print(f"Eseguito in {time.time() - start} secondi.")
    return clients


def tcp_network_scanner(language):
    loop = True
    while loop == True:
        if language == "English":
            net = input("Insert the IP address to scan --> ")
        else:
            net = input("Inserisci l'indirizzo IP da scannerizzare --> ")
        try:
            a = "."
            net_1 = net.split(a)
            net_2 = net_1[0] + a + net_1[1] + a + net_1[2] + a
            while True:
                if language == "English":
                    st_1 = int(input("Insert the starting number: "))
                else:
                    st_1 = int(input("Inserisci il numero d'inizio: "))
                if st_1 <= 0 or st_1 > 255:
                    if language == "English":
                        print("You have not entered a valid choice!")
                    else:
                        print("Non hai inserito una scelta valida!")
                else:
                    break
            while True:
                if language == "English":
                    en_1 = int(input("Insert the ending number: "))
                else:
                    en_1 = int(input("Inserisci l'ultimo numero: "))
                if en_1 <= 0 or en_1 > 255:
                    if language == "English":
                        print("You have not entered a valid choice!")
                    else:
                        print("Non hai inserito una scelta valida!")
                else:
                    break
            en_1 = en_1 + 1
            t1 = datetime.now()
            for ip in range(st_1, en_1):
                addr = net_2 + str(ip)
                if tcp_scan(addr):
                    if language == "English":
                        print(addr, " is available")
                    else:
                        print(addr, " è disponibile")
            t2 = datetime.now()
            total = t2 - t1
            if language == "English":
                print("Scan completed in: ", total)
            else:
                print("Scansione completata in: ", total)
            loop = False
            break
        except Exception as e:
            if language == "English":
                print("You have not entered a valid choice!")
            else:
                print("Non hai inserito una scelta valida!")
    

def tcp_scan(addr):
        s = socket(AF_INET, SOCK_STREAM)
        setdefaulttimeout(1)
        result = s.connect_ex((addr, 135))
        if result == 0:
            return 1
        else:
            return 0


def socket_port_scanner(language, target_ip=""):
    if target_ip == "":
        while True:
            if language == "English":
                choice = input("Do you want to insert an IP address (1) or a host name (2)? --> ")
            else:
                choice = input("Vuoi inserire un indirizzo IP (1) o il nome di un host (2)? --> ")
            if choice == "1" or choice == "1.":
                if language == "English":
                    target_ip = input("Insert the IP address to scan --> ")
                    print(f"Starting scan on the IP address: {target_ip}")
                else:
                    target_ip = input("Inserisci l'indirizzo IP da scannerizzare --> ")
                    print(f"Avvio della scansione sull'indirizzo IP: {target_ip}")
                break
            elif choice == "2" or choice == "2.":
                if language == "English":
                    host = input("Insert the host name --> ")
                    target_ip = gethostbyname(host)
                    print(f"Starting scan on the host: {host} ({target_ip})")
                else:
                    host = input("Inserisci il nome dell'host --> ")
                    target_ip = gethostbyname(host)
                    print(f"Avvio della scansione sull'host: {host} ({target_ip})")
                break
            else:
                if language == "English":
                    print("You have not entered a valid choice!")
                else:
                    print("Non hai inserito una scelta valida!")
            if language == "English":
                p_range = input("Insert the range of ports to scan (first-last) --> ")
            else:
                p_range = input("Inserisci il raggio di porte da scansionare (prima-ultima) --> ")
    elif target_ip != "":
        if language == "English":
            print(f"Starting scan on the IP address: {target_ip}")
        else:
            print(f"Avvio della scansione sull'indirizzo IP: {target_ip}")
    startTime = time.time()
    open_ports = []
    for port in range(0, 501):
        s = socket(AF_INET, SOCK_STREAM)
        conn = s.connect_ex((target_ip, port))
        if language == "English":
            print("Scanning port %d..." % (port))
        else:
            print("Scansione porta %d..." % (port))
        if conn == 0:
            if language == "English":
                print("Port %d: OPEN" % (port))
            else:
                print("Porta %d: APERTA" % (port))
            open_ports.append(port)
        s.close()
    if language == "English":
        print("Open ports:")
    else:
        print("Porte aperte:")
    for open_port in open_ports:
        print(open_port)
    if language == "English":
        print("Time taken: ", time.time() - startTime)
    else:
        print("Tempo impiegato: ", time.time() - startTime)


def adv_net_scanner(language):
    clients = arp_scan(language)
    for couple in clients:
        threaded_port_scanner(language, couple["ip"])


def ping_sweeper(language):
    if language == "English":
        net = input("Insert the IP address to scan --> ")
    else:
        net = input("Inserisci l'indirizzo IP da scannerizzare --> ")
    a = "."
    net_1 = net.split(a)
    net_2 = net_1[0] + a + net_1[1] + a + net_1[2] + a
    if language == "English":
        st_1 = int(input("Insert the starting number: "))
        en_1 = int(input("Insert the ending number: "))
    else:
        st_1 = int(input("Inserisci il numero d'inizio: "))
        en_1 = int(input("Inserisci l'ultimo numero: "))
    en_1 = en_1 + 1
    oper = platform.system()
    if oper == "Windows":
        ping_1 = "ping -n 1 "
    elif oper == "Linux":
        ping_1 = "ping -c 1 "
    else:
        ping_1 = "ping -c 1 "
    t1 = datetime.now()
    if language == "English":
        print("Scanning in progress:")
    else:
        print("Scansione in corso:")
    for ip in range(st_1, en_1):
        addr = net_2 + str(ip)
        comm = ping_1 + addr
        response = os.popen(comm)
        for line in response.readlines():
            if line.count("TTL"):
                if language == "English":
                    print(addr, " --> Available")
                else:
                    print(addr, " --> Disponibile")
                break
    t2 = datetime.now()
    total = t2 - t1
    if language == "English":
        print("Scanning completed in: ", total)
    else:
        print("Scansione completata in: ", total)


GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX
N_THREADS = 200
q = Queue()
print_lock = threading.Lock()
def threaded_port_scanner(language, target_ip=""):
    # setdefaulttimeout(0.25)
    global q
    global print_lock
    if target_ip == "":
        while True:
            if language == "English":
                choice = input("Do you want to insert an IP address (1) or a host name (2)? --> ")
            else:
                choice = input("Vuoi inserire un indirizzo IP (1) o il nome di un host (2)? --> ")
            if choice == "1" or choice == "1.":
                if language == "English":
                    target_ip = input("Insert the IP address to scan --> ")
                    print(f"Starting scan on the IP address: {target_ip}")
                else:
                    target_ip = input("Inserisci l'indirizzo IP da scannerizzare --> ")
                    print(f"Avvio della scansione sull'indirizzo IP: {target_ip}")
                break
            elif choice == "2" or choice == "2.":
                if language == "English":
                    host = input("Insert the host name --> ")
                    target_ip = gethostbyname(host)
                    print(f"Starting scan on the host: {host} ({target_ip})")
                else:
                    host = input("Inserisci il nome dell'host --> ")
                    target_ip = gethostbyname(host)
                    print(f"Avvio della scansione sull'host: {host} ({target_ip})")
                break
            else:
                if language == "English":
                    print("You have not entered a valid choice!")
                else:
                    print("Non hai inserito una scelta valida!")
    elif target_ip != "":
        if language == "English":
            print(f"Starting the scan on the IP address: {target_ip}")
        else:
            print(f"Avvio della scansione sull'indirizzo IP: {target_ip}")
    startTime = time.time()
    for t in range(N_THREADS):
        t = threading.Thread(target=lambda: threader(target_ip, language))
        t.daemon = True
        t.start()
    for worker in range(1, 501):
        q.put(worker)
    q.join()
    if language == "English":
        print("Scanning completed in:", time.time() - startTime)
    else:
        print("Scansione completata in:", time.time() - startTime)


def threaded_portscan(target_ip, port, language):
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((target_ip, port))
    except:
        with print_lock:
            if language == "English":
                print(f"{GRAY}{target_ip:15}:{port:5} is closed  {RESET}", end='\r')
            else:
                print(f"{GRAY}{target_ip:15}:{port:5} è chiusa  {RESET}", end='\r')
    else:
        with print_lock:
            if language == "English":
                print(f"{GREEN}{target_ip:15}:{port:5} is open    {RESET}")
            else:
                print(f"{GREEN}{target_ip:15}:{port:5} è aperta    {RESET}")
    finally:
        s.close()


def threader(target_ip, language):
    global q
    while True:
        worker = q.get()
        threaded_portscan(target_ip, worker, language)
        q.task_done()


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


if __name__ == "__main__":
    main()
