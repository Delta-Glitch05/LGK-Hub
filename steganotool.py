import sys, subprocess, cv2
import numpy as np


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
        if language == "English":
            choice = input("Do you want to encode (1) or decode (2) an image? --> ")
        else:
            choice = input("Vuoi codificare (1) o decodificare (2) un'immagine? --> ")
        if choice == "1" or choice == "1.":
            if language == "English":
                image_name = input("Insert the name of the image you want to encode --> ")
                secret_data = input("Insert the message to hide in the image --> ")
            else:
                image_name = input("Inserisci il nome dell'immagine che vuoi codificare --> ")
                secret_data = input("Inserisci il messaggio da nascondere nell'immagine --> ")
            encoded_image = encode(image_name, secret_data, language)
            ext = image_name[-4:]
            output_image = image_name[:-4] + " - Encoded" + ext
            print(output_image)
            cv2.imwrite(output_image, encoded_image)
        elif choice == "2" or choice == "2.":
            if language == "English":
                image_name = input("Insert the name of the image you want to decode --> ")
            else:
                image_name = input("Inserisci il nome dell'immagine che vuoi decodificare --> ")
            secret_data = decoded_image = decode(image_name, language)
            print(secret_data)
        elif choice.lower() == "exit":
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
                        subprocess.Popen("steganotool.bat", shell=True)
                        sys.exit()
                    else:
                        break
                else:
                    if language == "English":
                        print("You have not entered a valid choice!")
                    else:
                        print("Non hai inserito una scelta valida!")
            


def to_bin(data, language):
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data,bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        if language == "English":
            raise TypeError("Type not supported.")
        else:
            raise TypeError("Tipo non supportato.")


def encode(image_name, secret_data, language):
    image = cv2.imread(image_name)
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    if language == "English":
        print("[*] Maximum bytes to encode:", n_bytes)
    else:
        print("[*] Bytes massimi da codificare:", n_bytes)
    if len(secret_data) > n_bytes:
        if language == "English":
            raise ValueError("[!] Insufficient bytes, need bigger immage or less data.")
        else:
            raise ValueError("[!] Bytes insufficienti, serve un'immagine più grande o meno dati.")
    if language == "English":
        print("[*] Encoding data...")
    else:
        print("[*] Codificando i dati...")
    secret_data += "====="
    data_index = 0
    binary_secret_data = to_bin(secret_data, language)
    data_len = len(binary_secret_data)
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel, language)
            if data_index < data_len:
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index >= data_len:
                break
    return image


def decode(image_name, language):
    if language == "English":
        print("[+] Decoding...")
    else:
        print("[+] Decodificando...")
    image = cv2.imread(image_name)
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel, language)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":
            break
    return decoded_data[:-5]


if __name__ == "__main__":
    main()
