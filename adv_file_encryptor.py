import requests, subprocess, sys, cryptography, hashlib
from cryptography.fernet import Fernet


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
    loop_2 = True
    done = False
    exit_ = False
    while loop == True:
        while loop_2 == True:
            if language == "English":
                choice = input("Do you want to use the encryption (1) or decryption (2) function? --> ")
            else:
                choice = input("Vuoi usare la funzione di criptazione (1) o decriptazione (2)? --> ")
            if choice.lower() == "exit":
                if language == "English":
                    print("Goodbye!\n")
                else:
                    print("Arrivederci!\n")
                loop = False
                loop_2 = False
                break
            elif choice == "1" or choice == "1.":
                while True:
                    if language == "English":
                        choice = input("Do you want to encrypt a string (1) or a file (2)? --> ")
                    else:
                        choice = input("Vuoi criptare una stringa (1) o un file (2)? --> ")
                    if choice.lower() == "exit":
                        if language == "English":
                            print("Goodbye!\n")
                        else:
                            print("Arrivederci!\n")
                        loop = False
                        loop_2 = False
                        break
                    if choice == "1" or choice == "1." or choice == "2" or choice == "2.":
                        exit_ = encryptor(choice, language)
                        done = True
                        loop_2 = False
                    else:
                        if language == "English":
                            print("You have not entered a valid choice!")
                        else:
                            print("Non hai inserito una scelta valida!")
                    if done == True:
                        if exit_ == True:
                            if language == "English":
                                print("Goodbye!\n")
                            else:
                                print("Arrivederci!\n")
                            loop = False
                            loop_2 = False
                            break
                        else:
                            break
            elif choice == "2" or choice == "2.":
                while True:
                    if language == "English":
                        choice = input("Do you want to decrypt a string (1) or a file (2)? --> ")
                    else:
                        choice = input("Vuoi decriptare una stringa (1) o un file (2)? --> ")
                    if choice.lower() == "exit":
                        if language == "English":
                            print("Goodbye!\n")
                        else:
                            print("Arrivederci!\n")
                        loop = False
                        loop_2 = False
                        break
                    if choice == "1" or choice == "1." or choice == "2" or choice == "2.":
                        exit_ = decryptor(choice, language)
                        done = True
                        loop_2 = False
                    else:
                        if language == "English":
                            print("You have not entered a valid choice!")
                        else:
                            print("Non hai inserito una scelta valida!")
                    if done == True:
                        if exit_ == True:
                            if language == "English":
                                print("Goodbye!\n")
                            else:
                                print("Arrivederci!\n")
                            loop = False
                            break
                        else:
                            break
            else:
                if language == "English":
                    print("You have not entered a valid choice!")
                else:
                    print("Non hai inserito una scelta valida!")
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
                    loop = True
                    loop_2 = True
                    if mode == "menu":
                        with open("lang.txt", "a") as lang_file:
                            lang_file.write("\nmenu")
                        subprocess.Popen("file_encryptor.bat", shell=True)
                        sys.exit()
                    else:
                        break
                else:
                    if language == "English":
                        print("You have not entered a valid choice!")
                    else:
                        print("Non hai inserito una scelta valida!")


def encryptor(choice, language):
    exit_ = False
    write_key()
    key = load_key()
    f = Fernet(key)
    loop = True
    if choice == "1" or choice == "1.":
        while loop == True:
            if language == "English":
                choice = input("Do you want to use the AES (1), MD5 (2), SHA (3), SHA-3 (4) or BLAKE2 (5) algorythm? --> ")
            else:
                choice = input("Vuoi usare l'algoritmo AES (1), MD5 (2), SHA (3), SHA-3 (4) o BLAKE2 (5)? --> ")
            if choice == "1" or choice == "1.":
                if language == "English":
                    string = input("Insert the string to encrypt --> ").encode()
                else:
                    string = input("Inserisci la stringa da criptare --> ").encode()
                encrypted_string = f.encrypt(string)
                if language == "English":
                    print(f"Done!\nString encrypted: {encrypted_string}")
                else:
                    print(f"Fatto!\nStringa criptata: {encrypted_string}")
                break
            elif choice == "2" or choice == "2.":
                if language == "English":
                    string = input("Insert the string to encrypt --> ").encode()
                else:
                    string = input("Inserisci la stringa da criptare --> ").encode()
                print(f"MD5: {hashlib.md5(string).hexdigest()}")
                break
            elif choice == "3" or choice == "3.":
                while True:
                    if language == "English":
                        choice = input("Do you want to use the SHA-1 (1), SHA-224 (2), SHA-256 (3), SHA-384 (4) or SHA-512 (5) algorythm? --> ")
                    else:
                        choice = input("Vuoi usare l'algoritmo SHA-1 (1), SHA-224 (2), SHA-256 (3), SHA-384 (4) or SHA-512 (5)? --> ")
                    if choice == "1" or choice == "1.":
                        if language == "English":
                            string = input("Insert the string to encrypt --> ").encode()
                        else:
                            string = input("Inserisci la stringa da criptare --> ").encode()
                        print(f"SHA-1: {hashlib.sha1(string).hexdigest()}")
                        loop = False
                        break
                    elif choice == "2" or choice == "2.":
                        if language == "English":
                            string = input("Insert the string to encrypt --> ").encode()
                        else:
                            string = input("Inserisci la stringa da criptare --> ").encode()
                        print(f"SHA-224: {hashlib.sha224(string).hexdigest()}")
                        loop = False
                        break
                    elif choice == "3" or choice == "3.":
                        if language == "English":
                            string = input("Insert the string to encrypt --> ").encode()
                        else:
                            string = input("Inserisci la stringa da criptare --> ").encode()
                        print(f"SHA-256: {hashlib.sha256(string).hexdigest()}")
                        loop = False
                        break
                    elif choice == "4" or choice == "4.":
                        if language == "English":
                            string = input("Insert the string to encrypt --> ").encode()
                        else:
                            string = input("Inserisci la stringa da criptare --> ").encode()
                        print(f"SHA-256: {hashlib.sha384(string).hexdigest()}")
                        loop = False
                        break
                    elif choice == "5" or choice == "5.":
                        if language == "English":
                            string = input("Insert the string to encrypt --> ").encode()
                        else:
                            string = input("Inserisci la stringa da criptare --> ").encode()
                        print(f"SHA-512: {hashlib.sha512(string).hexdigest()}")
                        loop = False
                        break
                    elif choice.lower() == "exit":
                        loop = False
                        exit_ = True
                        break
                    else:
                        if language == "English":
                            print("You have not entered a valid choice!")
                        else:
                            print("Non hai inserito una scelta valida!")
            elif choice == "4" or choice == "4.":
                while True:
                    if language == "English":
                        choice = input("Do you want to use the SHA-3-224 (1), SHA-3-256 (2), SHA-3-384 (3) or SHA-3-512 (4) algorythm? --> ")
                    else:
                        choice = input("Vuoi usare l'algoritmo SHA-3-224 (1), SHA-3-256 (2), SHA-3-384 (3) o SHA-3-512 (4)? --> ")
                    if choice == "1" or choice == "1.":
                        if language == "English":
                            string = input("Insert the string to encrypt --> ").encode()
                        else:
                            string = input("Inserisci la stringa da criptare --> ").encode()
                        print(f"SHA-3-224: {hashlib.sha3_224(string).hexdigest()}")
                        loop = False
                        break
                    elif choice == "2" or choice == "2.":
                        if language == "English":
                            string = input("Insert the string to encrypt --> ").encode()
                        else:
                            string = input("Inserisci la stringa da criptare --> ").encode()
                        print(f"SHA-3-256: {hashlib.sha3_256(string).hexdigest()}")
                        loop = False
                        break
                    elif choice == "3" or choice == "3.":
                        if language == "English":
                            string = input("Insert the string to encrypt --> ").encode()
                        else:
                            string = input("Inserisci la stringa da criptare --> ").encode()
                        print(f"SHA-3-384: {hashlib.sha3_384(string).hexdigest()}")
                        loop = False
                        break
                    elif choice == "4" or choice == "4.":
                        if language == "English":
                            string = input("Insert the string to encrypt --> ").encode()
                        else:
                            string = input("Inserisci la stringa da criptare --> ").encode()
                        print(f"SHA-3-512: {hashlib.sha3_512(string).hexdigest()}")
                        loop = False
                        break
                    elif choice.lower() == "exit":
                        loop = False
                        exit_ = True
                        break
                    else:
                        if language == "English":
                            print("You have not entered a valid choice!")
                        else:
                            print("Non hai inserito una scelta valida!")
            elif choice == "5" or choice == "5.":
                while True:
                    if language == "English":
                        choice = input("Do you want to use the BLAKE2s (1) or BLAKE2b (2) algorythm? --> ")
                    else:
                        choice = input("Vuoi usare l'algoritmo BLAKE2s (1) o BLAKE2b (2)? --> ")
                    if choice == "1" or choice == "1.":
                        if language == "English":
                            string = input("Insert the string to encrypt --> ").encode()
                        else:
                            string = input("Inserisci la stringa da criptare --> ").encode()
                        print(f"BLAKE2s: {hashlib.blake2s(string).hexdigest()}")
                        loop = False
                        break
                    elif choice == "2" or choice == "2.":
                        if language == "English":
                            string = input("Insert the string to encrypt --> ").encode()
                        else:
                            string = input("Inserisci la stringa da criptare --> ").encode()
                        print(f"BLAKE2b: {hashlib.blake2b(string).hexdigest()}")
                        loop = False
                        break
                    elif choice.lower() == "exit":
                        loop = False
                        exit_ = True
                        break
                    else:
                        if language == "English":
                            print("You have not entered a valid choice!")
                        else:
                            print("Non hai inserito una scelta valida!")
            elif choice.lower() == "exit":
                loop = False
                exit_ = True
                break
            else:
                if language == "English":
                    print("You have not entered a valid choice!")
                else:
                    print("Non hai inserito una scelta valida!")
    else:
        while True:
            if language == "English":
                file_name = input("Insert the name of the file to encrypt --> ")
            else:
                file_name = input("Inserisci il nome del file da criptare --> ")
            if file_name.lower() == "exit":
                exit_ = True
                break
            else:
                try:
                    # file_data = open(file_name).read()
                    with open(file_name, "rb") as file:
                        file_data = file.read()
                    encrypted_data = f.encrypt(file_data)
                    with open(f"{file_name} - Encrypted.txt", "wb") as file:
                        file.write(encrypted_data)
                    if language == "English":
                        print("Done!")
                    else:
                        print("Fatto!")
                    break
                except FileNotFoundError:
                    if language == "English":
                        print("File not found!")
                    else:
                        print("File non trovato!")
    return exit_


def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return open("key.key", "rb").read()


def decryptor(choice, language):
    exit_ = False
    key = load_key()
    f = Fernet(key)
    if choice == "1" or choice == "1.":
        while True:
            if language == "English":
                encrypted_string = input("Insert the encrypted string --> ")
            else:
                encrypted_string = input("Inserisci la stringa criptata --> ")
            if encrypted_string.lower() == "exit":
                exit_ = True
                break
            else:
                try:
                    encrypted_string = encrypted_string.encode()
                    decrypted_string = f.decrypt(encrypted_string)
                    if language == "English":
                        print(f"Done!\nString decrypted: {decrypted_string}")
                    else:
                        print(f"Fatto!\nStringa decriptata: {decrypted_string}")
                    break
                except Exception:
                    if language == "English":
                        print("You have not entered a valid crypted string!")
                    else:
                        print("Non hai inserito una stringa criptata valida!")
    else:
        while True:
            try:
                if language == "English":
                    file_name = input("Insert the name of the file to decrypt --> ")
                else:
                    file_name = input("Inserisci il nome del file da decriptare --> ")
                if file_name.lower() == "exit":
                    exit_ = True
                else:
                    # file_data = open(file_name.read()).encode()
                    with open(file_name, "rb") as file:
                        encrypted_data = file.read()
                    decrypted_data = f.decrypt(encrypted_data)
                    with open(f"{file_name} - Decrypted.txt", "wb") as file:
                        file.write(decrypted_data)
                    if language == "English":
                        print("Done!")
                    else:
                        print("Fatto!")
                break
            except FileNotFoundError:
                if language == "English":
                    print("File not found!")
                else:
                    print("File non trovato!")
            except cryptography.fernet.InvalidToken:
                if language == "English":
                    print("File not valid!")
                else:
                    print("File non valido!")
    return exit_


if __name__ == "__main__":
    main()
