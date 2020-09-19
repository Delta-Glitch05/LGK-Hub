import requests, subprocess, sys
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.http import HTTPRequest
from colorama import init, Fore


init()
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET


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


show_raw = ""
language = ""
def main():
    mode = ""
    language, mode = get_lang_and_mode(mode)
    # print(f"{language}, {mode}")
    loop = True
    while loop == True:
        while True:
            if language == "English":
                iface = input("Insert the name of your network interface --> ")
            else:
                iface = input("Inserisci il nome della tua interfaccia di rete --> ")
            if iface.lower() == "exit":
                if language == "English":
                    print("Goodbye!\n")
                else:
                    print("Arrivederci!\n")
                loop = False
                break
            if language == "English":
                show_raw = input("Do you want to show RAW data? [Y/n] --> ")
            else:
                show_raw = input("Vuoi mostrare dati RAW? [Y/n] --> ")
            if show_raw.lower() == "yes" or show_raw == "y":
                show_raw = True
            elif show_raw.lower() == "no" or show_raw == "n":
                show_raw = False
            sniff_packets(iface)
        if loop == True:
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
                        subprocess.Popen("http_sniffer.bat", shell=True)
                        sys.exit()
                    else:
                        break
                else:
                    if language == "English":
                        print("You have not entered a valid choice!")
                    else:
                        print("Non hai inserito una scelta valida!")


def sniff_packets(iface):
    if iface:
        sniff(filter="port 80", prn=process_packet, iface=iface, store=False)
    else:
        sniff(filter="port 80", prn=process_packet, store=False)


def process_packet(packet):
    if packet.haslayer(HTTPRequest):
        url = packet[HTTPRequest].Host.decode() + packet[HTTPRequest].Path.decode()
        ip = packet[IP].src
        method = packet[HTTPRequest].Method.decode()
        if language == "English":
            print(f"\n{GREEN}[+] {ip} Requested {url} with {method}{RESET}")
        else:
            print(f"\n{GREEN}[+] {ip} Ha richiesto {url} con {method}{RESET}")
        if show_raw and packet.haslayer(Raw) and method == "POST":
            if language == "English":
                print(f"\n{RED}[*] Some useful RAW data: {packet[Raw].load}{RESET}")
            else:
                print(f"\n{RED}[*] Alcuni dati RAW utili: {packet[Raw].load}{RESET}")        


if __name__ == "__main__":
    main()
