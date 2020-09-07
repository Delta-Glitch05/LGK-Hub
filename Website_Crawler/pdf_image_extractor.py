import sys, subprocess, pikepdf, fitz, io
from PIL import Image


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
            pdf_file = input("Insert the name of the PDF file --> ")
        else:
            pdf_file = input("Inserisci il nome del file PDF --> ")
        if pdf_file.lower() == "exit":
            if language == "English":
                print("Goodbye!\n")
            else:
                print("Arrivederci!\n")
            loop = False
            break
        pdf_image_extractor(pdf_file, language)
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
                        subprocess.Popen("Website_Crawler\\pdf_image_extractor.bat", shell=True)
                        sys.exit()
                    else:
                        break


def pdf_image_extractor(pdf_file, language):
    for page_index in range(len(pdf_file)):
        page = pdf_file[page_index]
        image_list = page.getImageList()
        if image_list:
            if language == "English":
                print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
            else:
                print(f"[+] Trovate un totale di {len(image_list)} immagini in pagina {page_index}")
        else:
            if language == "English":
                print(f"[!] No images found in page {page_index}")
            else:
                print(f"[!] Nessuna immagine trovata in pagina {page_index}")
        for image_index, img in enumerate(page.getImageList(), start=1):
            xref = img[0]
            base_image = pdf_file.extractImage(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))
            image.save(open(f"image{page_index+1}_{image_index}.{image_ext}", "wb"))


if __name__ == "__main__":
    main()
