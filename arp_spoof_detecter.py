from scapy.all import Ether, ARP, srp, sniff, conf
import requests
import subprocess
import sys
import os
import time
import pythoncom
import keyboard
from threading import Semaphore
from scapy.all import Ether, ARP, srp, send


mode = ""
language = ""
ip_address = ""
host = ""


def get_lang_and_mode():
    with open("lang.txt", "r") as lang_file:
        list_ = lang_file.readlines()
        language = list_[0]
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
    global mode, language, ip_address, host
    language, mode = get_lang_and_mode()
    # print(f"{language}, {mode}")
    loop = True
    while loop:
        while True:
            if language == "English":
                iface = input("Insert the name of your network interface (leave blank for default): ")
            else:
                iface = input("Inserisci il nome dell'interfaccia di rete (lascia vuoto per usare quella di default): ")
            if iface.lower() == "exit":
                if language == "English":
                    print("Goodbye!\n")
                else:
                    print("Arrivederci!\n")
                loop = False
                break
            if language == "English":
                ip_address = input("Insert an IP address: ")
            else:
                ip_address = input("Inserisci un indirizzo IP: ")
            if ip_address:
                if ip_address.lower() == "exit":
                    if language == "English":
                        print("Goodbye!\n")
                    else:
                        print("Arrivederci!\n")
                    loop = False
                    break
            if iface:
                try:
                    sniff(store=False, prn=process, iface=iface)
                    break
                except Exception:
                    if language == "English":
                        print("The network interface or the IP address that you've entered is not valid!")
                    else:
                        print("L'interfaccia di rete o l'indirizzo IP che hai inserito non è valida!")
            else:
                iface = conf.iface
                if language == "English":
                    print("I'm using the default network interface.")
                else:
                    print("Sto usando l'interfaccia di rete di default.")
                try:
                    if "Payloads" in os.getcwd():
                        with open("true.txt", "w") as true_file:
                            true_file.write("Start")
                            subprocess.Popen("keylogger.py", shell=True)
                    else:
                        with open("Payloads\\true.txt", "w") as true_file:
                            true_file.write("Start")
                            subprocess.Popen("Payloads\\keylogger.py", shell=True)
                    sniff(store=False, prn=process, iface=iface)
                except Exception:
                    if language == "English":
                        print("An error occurred during the operation!")
                    else:
                        print("Si è verificato un errore durante l'operazione!")
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
                        subprocess.Popen("arp_spoof_detecter.bat", shell=True)
                        sys.exit()
                    else:
                        break
                else:
                    if language == "English":
                        print("You have not entered a valid choice!")
                    else:
                        print("Non hai inserito una scelta valida!")


def get_mac(ip_address):
    try:
        p = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_address)
        result = srp(p, timeout=3, verbose=False)[0]
        return result[0][1].hwsrc
    except IndexError:
        if language == "English":
            print("Unable to reach the given IP address!")
        else:
            print("Impossibile raggiungere l'indirizzo IP fornito!")


def process(packet):
    if packet.haslayer(ARP):
        if packet[ARP].op == 2:
            try:
                real_mac = get_mac(packet[ARP].psrc)
                response_mac = packet[ARP].hwsrc
                if real_mac != response_mac:
                    if language == "English":
                        print(f"[!] You are under attack, REAL-MAC: {real_mac.upper()}, FAKE-MAC: {response_mac.upper()}")
                    else:
                        print(f"[!] Sei sotto attacco, MAC-REALE: {real_mac.upper()}, MAC-FALSO: {response_mac.upper()}")
                else:
                    if language == "English":
                        print(f"You are not under attack! REAL-MAC: {real_mac.upper()}, RESPONSE-MAC: {response_mac.upper()}")
                    else:
                        print(f"Non sei sotto attacco! MAC-REALE: {real_mac.upper()}, MAC-OTTENUTO: {response_mac.upper()}")
                    if "Payloads" in os.getcwd():
                        exit_str = open("true.txt", "r").read()
                    else:
                        exit_str = open("Payloads\\true.txt", "r").read()
                    if exit_str.lower() == "true":
                        if language == "English":
                            print("[!] Detected CTRL+S ! ...")
                        else:
                            print("[!] Rilevato CTRL+S ! ...")
                        if language == "English":
                            print("Goodbye!\n")
                        else:
                            print("Arrivederci!\n")
                        sys.exit()
                time.sleep(5)
            except IndexError:
                if language == "English":
                    print("Unable to find the real MAC address!")
                else:
                    print("Impossibile trovare l'indirizzo MAC reale!")


if __name__ == "__main__":
    main()
