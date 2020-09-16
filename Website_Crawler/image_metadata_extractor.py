import sys, subprocess, hachoir
from PIL import Image
from PIL.ExifTags import TAGS


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
            image_name = input("Insert the name of the image --> ")
        else:
            image_name = input("Inserisci il nome dell'immagine --> ")
        if image_name.lower() == "exit":
            if language == "English":
                print("Goodbye!\n")
            else:
                print("Arrivederci!\n")
            loop = False
            break
        while True:
            if language == "English":
                choice = input("Do you want to use ExifTool (1) or Hachoir (2)? --> ")
            else:
                choice = input("Vuoi usare ExifTool (1) o Hachoir (2)? --> ")
            if choice == "1." or choice == "1":
                tool = "ExifTool"
                break
            elif choice == "2." or choice == "2":
                tool = "Hachoir"
                break
            elif choice.lower == "exit":
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
        image_metadata_extractor(image_name, tool, mode, language)
        if loop == True:
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
                        subprocess.Popen("Website_Crawler\\ytc_extractor.bat", shell=True)
                        sys.exit()
                    else:
                        break


def image_metadata_extractor(image_name, tool, mode, language):
    if tool == "ExifTool":
        infoDict = {}
        import os
        print(os.getcwd())
        exifToolPath = "ExifTool\\exiftool.exe"
        process = subprocess.Popen([exifToolPath, image_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for tag in process.stdout:
            line = tag.strip().split(":")
            infoDict[line[0].strip()] = line[-1].strip()
        for k, v in infoDict.items():
            print(k, ":", v)
    elif tool == "Hachoir":
        exeProcess = "hachoir-metadata"
        process = subprocess.Popen([exeProcess, image_name], stdout=subprocess.PIPE, 
                                        stderr=subprocess.STDOUT, universal_newlines=True)
        infoDict = {}
        for tag in process.stdout:
                line = tag.strip().split(':')
                infoDict[line[0].strip()] = line[-1].strip()
        for k,v in infoDict.items():
            print(k,':', v)


if __name__ == "__main__":
    main()
