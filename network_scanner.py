from scapy.all import ARP, Ether, srp
from socket import *
import time
from datetime import datetime
import threading
from queue import Queue
import sys, subprocess, platform


def main():
    mode = ""
    language, mode = get_lang_and_mode(mode)
    # print(f"{language}, {mode}")
    loop = True
    while(loop == True):
        if(language == "English"):
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
        while True:
            if(language == "English"):
                choice = input("INSERT YOUR CHOICE: ")
            else:
                choice = input("INSERISCI LA TUA SCELTA: ")
            if(choice == "1" or choice == "1."):
                if(language == "English"):
                    choice_2 = input("DO YOU WANT TO USE THE TCP (1) OR UDP (2) SCANNER? ")
                else:
                    choice_2 = input("VUOI USARE LO SCANNER TCP (1) O UDP (2)? ")
                if(choice_2 == "1" or choice_2 == "1."):
                    tcp_network_scanner(language)
                    break
                elif(choice_2 == "2" or choice_2 == "2."):
                    udp_network_scanner(language)
                    break
                else:
                    if(language == "English"):
                        print("You have not entered a valid choice!")
                    else:
                        print("Non hai inserito una scelta valida!")
            elif(choice == "2" or choice == "2."):
                adv_net_scanner(language)
                break
            elif(choice == "3" or choice == "3."):
                if(language == "English"):
                    choice_2 = input("DO YOU WANT TO USE THE SOCKET (1) OR THREADED (2) SCANNER? ")
                else:
                    choice_2 = input("VUOI USARE LO SCANNER SOCKET (1) O THREADED (2)? ")
                if(choice_2 == "1" or choice_2 == "1."):
                    socket_port_scanner(language)
                    break
                elif(choice_2 == "2" or choice_2 == "2."):
                    threaded_port_scanner(language)
                    break
                else:
                    if(language == "English"):
                        print("You have not entered a valid choice!")
                    else:
                        print("Non hai inserito una scelta valida!")
            elif(choice == "4" or choice == "4."):
                ping_sweeper(language)
                break
            elif(choice.lower() == "exit"):
                if(language == "English"):
                    print("GOODBYE!\n")
                else:
                    print("ARRIVEDERCI!\n")
                loop = False
                break
            else:
                if(language == "English"):
                    print("You have not entered a valid choice!")
                else:
                    print("Non hai inserito una scelta valida!")
        if(loop == True):
            while True:
                if(language == "English"):
                    exit_choice = input("DO YOU WANT TO EXIT THE PROGRAM? [Y/n]: ")
                else:
                    exit_choice = input("VUOI USCIRE DAL PROGRAMMA? [Y/n]: ")
                exit_choice = exit_choice.lower()
                if(exit_choice == "y" or exit_choice == "yes"):
                    if(language == "English"):
                        print("GOODBYE!\n")
                    else:
                        print("ARRIVEDERCI!\n")
                    loop = False
                    break
                elif(exit_choice != "n" or exit_choice != "no"):
                    if(language == "English"):
                        print("RETURNING TO THE MENU!\n")
                    else:
                        print("RITORNO AL MENÙ!\n")
                    if(mode == "menu"):
                        with open("lang.txt", "a") as lang_file:
                            lang_file.write("\nmenu")
                        subprocess.Popen("open_network_scanner.bat", shell=True)
                        sys.exit()
                    else:
                        break


def udp_network_scanner(language):
    if(language == "English"):
        target_ip = input("Insert the IP address to scan --> ")
    else:
        target_ip = input("Inserisci l'indirizzo IP da scannerizzare --> ")
    target_ip = target_ip + "/24"
    # Create an ARP packet
    arp = ARP(pdst=target_ip)
    # Create the Ether broadcast packet
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Stack them
    packet = ether/arp
    result = srp(packet, timeout=3)[0]
    # List of clients
    clients = []

    for sent, received in result:
        # For each response, append the IP and the MAC address to the list
        clients.append({"ip":received.psrc,"mac":received.hwsrc})

    if(language == "English"):
        print("Available devices on the network: ")
    else:
        print("Dispositivi disponibili nella rete:")
    print("IP" + " "*18+"MAC")
    for client in clients:
        print("{:16}    {}".format(client["ip"], client["mac"]))
    return clients


def tcp_network_scanner(language):
    if(language == "English"):
        net = input("Insert the IP address to scan --> ")
    else:
        net = input("Inserisci l'indirizzo IP da scannerizzare --> ")
    net_1 = net.split(".")
    a = "."
    net_2 = net_1[0] + a + net_1[1] + a + net_1[2] + a
    if(language == "English"):
        st_1 = int(input("Insert the starting number: "))
        en_1 = int(input("Insert the ending number: "))
    else:
        st_1 = int(input("Inserisci il numero d'inizio: "))
        en_1 = int(input("Inserisci l'ultimo numero: "))
    en_1 = en_1 + 1
    t1 = datetime.now()
    for ip in range(st_1, en_1):
        addr = net_2 + str(ip)
        if(tcp_scan(addr)):
            if(language == "English"):
                print(addr, " is available")
            else:
                print(addr, " è disponibile")
    t2 = datetime.now()
    total = t2 - t1
    if(language == "English"):
        print("Scan completed in: ", total)
    else:
        print("Scansione completata in: ", total)
    

def tcp_scan(addr):
        s = socket(AF_INET, SOCK_STREAM)
        setdefaulttimeout(1)
        result = s.connect_ex((addr, 135))
        if result == 0:
            return 1
        else:
            return 0


def socket_port_scanner(language, target_ip=""):
    startTime = time.time()
    if(target_ip == ""):
        if(language == "English"):
            choice = input("Do you want to insert an IP address (1) or a host name (2)? --> ")
        else:
            choice = input("Vuoi inserire un indirizzo IP (1) o il nome di un host (2)? --> ")
        if(choice == "1" or choice == "1."):
            if(language == "English"):
                target_ip = input("Insert the IP address to scan --> ")
                print(f"Starting scan on the IP address: {target_ip}")
            else:
                target_ip = input("Inserisci l'indirizzo IP da scannerizzare --> ")
                print(f"Avvio della scansione sull'indirizzo IP: {target_ip}")
        elif(choice == "2" or choice == "2."):
            if(language == "English"):
                host = input("Insert the host name --> ")
                target_ip = gethostbyname(host)
                print(f"Starting scan on the host: {host} ({target_ip})")
            else:
                host = input("Inserisci il nome dell'host --> ")
                target_ip = gethostbyname(host)
                print(f"Avvio della scansione sull'host: {host} ({target_ip})")
        else:
            if(language == "English"):
                print("You have not entered a valid choice!")
            else:
                print("Non hai inserito una scelta valida!")
    elif(target_ip != ""):
        if(language == "English"):
            print(f"Starting scan on the IP address: {target_ip}")
        else:
            print(f"Avvio della scansione sull'indirizzo IP: {target_ip}")
    open_ports = []
    for port in range(50, 501):
        s = socket(AF_INET, SOCK_STREAM)
        conn = s.connect_ex((target_ip, port))
        if(language == "English"):
            print("Scanning port %d..." % (port))
        else:
            print("Scansione porta %d..." % (port))
        if(conn == 0):
            if(language == "English"):
                print("Port %d: OPEN" % (port))
            else:
                print("Porta %d: APERTA" % (port))
            open_ports.append(port)
        s.close()
    if(language == "English"):
        print("Open ports:")
    else:
        print("Porte aperte:")
    for open_port in open_ports:
        print(open_port)
    if(language == "English"):
        print("Time taken: ", time.time() - startTime)
    else:
        print("Tempo impiegato: ", time.time() - startTime)


def adv_net_scanner(language):
    clients = udp_network_scanner(language)
    for couple in clients:
        socket_port_scanner(language, couple["ip"])


def ping_sweeper(language):
    if(language == "English"):
        net = input("Insert the IP address to scan --> ")
    else:
        net = input("Inserisci l'indirizzo IP da scannerizzare --> ")
    net_1 = net.split(".")
    a = "."
    net_2 = net_1[0] + a + net_1[1] + a + net_1[2] + a
    if(language == "English"):
        st_1 = int(input("Insert the starting number: "))
        en_1 = int(input("Insert the ending number: "))
    else:
        st_1 = int(input("Inserisci il numero d'inizio: "))
        en_1 = int(input("Inserisci l'ultimo numero: "))
    en_1 = en_1 + 1
    oper = platform.system()
    if(oper == "Windows"):
        ping_1 = "ping -n 1 "
    elif(oper == "Linux"):
        ping_1 = "ping -c 1 "
    else:
        ping_1 = "ping -c 1 "
    t1 = datetime.now()
    if(language == "English"):
        print("Scanning in progress:")
    else:
        print("Scansione in corso:")
    for ip in range(st_1, en_1):
        addr = net_2 + str(ip)
        comm = ping_1 + addr
        response = os.popen(comm)
        for line in response.readlines():
            if(line.count("TTL")):
                if(language == "English"):
                    print(addr, " --> Available")
                else:
                    print(addr, " --> Disponibile")
                break
    t2 = datetime.now()
    total = t2 - t1
    if(language == "English"):
        print("Scanning completed in: ", total)
    else:
        print("Scansione completata in: ", total)


def threaded_port_scanner(language, target_ip=""):
    setdefaulttimeout(0.25)
    print_lock = threading.Lock()
    if(target_ip == ""):
        if(language == "English"):
            choice = input("Do you want to insert an IP address (1) or a host name (2)? --> ")
        else:
            choice = input("Vuoi inserire un indirizzo IP (1) o il nome di un host (2)? --> ")
        if(choice == "1" or choice == "1."):
            if(language == "English"):
                target_ip = input("Insert the IP address to scan --> ")
                print(f"Starting the scan on the IP address: {target_ip}")
            else:
                target_ip = input("Inserisci l'indirizzo IP da scannerizzare --> ")
                print(f"Avvio della scansione sull'indirizzo IP: {target_ip}")
        elif(choice == "2" or choice == "2."):
            if(language == "English"):
                host = input("Insert a host name --> ")
                target_ip = gethostbyname(host)
                print(f"Starting the scan on the host: {host} ({target_ip})")
            else:
                host = input("Inserisci il nome dell'host --> ")
                target_ip = gethostbyname(host)
                print(f"Avvio della scansione sull'host: {host} ({target_ip})")
        else:
            if(language == "English"):
                print("You have not entered a valid choice!")
            else:
                print("Non hai inserito una scelta valida!")
    elif(target_ip != ""):
        if(language == "English"):
            print(f"Starting the scan on the IP address: {target_ip}")
        else:
            print(f"Avvio della scansione sull'indirizzo IP: {target_ip}")
    def portscan(port):
        s = socket(AF_INET, SOCK_STREAM)
        try:
            conn = s.connect((target_ip, port))
            with print_lock:
                if(language == "English"):
                    print(f"Port {port} is open")
                else:
                    print(f"La porta {port} è aperta")
            conn.close()
        except:
            pass
    def threader():
        while True:
            worker = q.get()
            portscan(worker)
            q.task_done()
    q = Queue()
    startTime = time.time()
    for x in range(100):
        t = threading.Thread(target = threader)
        t.daemon = True
        t.start()
    for worker in range(1, 501):
        q.put(worker)
    q.join()
    if(language == "English"):
        print("Time taken: ", time.time() - startTime)
    else:
        print("Tempo impiegato: ", time.time() - startTime)
    

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
