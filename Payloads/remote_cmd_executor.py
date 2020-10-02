import sys
import os
import subprocess
import paramiko


def get_lang_and_mode(mode):
    if "lang.txt" in os.getcwd():
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
    return language, mode


def main():
    mode = ""
    language, mode = get_lang_and_mode(mode)
    # print(f"{language}, {mode}")
    loop = True
    while loop:
        if language == "English":
            print("STILL IN WORK!")
        else:
            print("ANCORA IN LAVORO!")
        loop = False
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
                            subprocess.Popen("remote_cmd_executor.bat", shell=True)
                        else:
                            subprocess.Popen("Payloads\\remote_cmd_executor.bat", shell=True)
                        sys.exit()
                    else:
                        break


if __name__ == "__main__":
    main()
