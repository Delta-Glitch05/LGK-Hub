import os, sys, subprocess, json, base64, sqlite3, shutil
from win32 import win32crypt
from Crypto.Cipher import AES
from datetime import timezone, datetime, timedelta


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
        chrome_pass_extractor(language)
        while True:
            if language == "English":
                choice = input("Do you want to delete the passwords from the database? [Y/n] --> ")
            else:
                choice = input("Vuoi cancellare le password dal database? [Y/n] --> ")
            if choice.lower() == "y" or choice.lower() == "yes":
                delete_chrome_pass(language)
                break
            elif choice.lower() == "n" or choice.lower() == "no":
                break
            else:
                if language == "English":
                    print("You have not entered a valid choice!")
                else:
                    print("Non hai inserito una scelta valida!")
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
                    subprocess.Popen("chrome_pass_extractor.bat", shell=True)
                    sys.exit()
                else:
                    break
            else:
                if language == "English":
                    print("You have not entered a valid choice!")
                else:
                    print("Non hai inserito una scelta valida!")


def chrome_pass_extractor(language):
    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", 
                            "Google", "Chrome", "User Data", "default", "Login Data")
    file_name = "ChromeData.db"
    shutil.copyfile(db_path, file_name)
    db = sqlite3.connect(file_name)
    cursor = db.cursor()
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]
        if username or password:
            if language == "English":
                print(f"Origin URL: {origin_url}")
                print(f"Action URL: {action_url}")
                print(f"Username: {username}")
                print(f"Password: {password}")
            else:
                print(f"URL di origine: {origin_url}")
                print(f"URL di azione: {action_url}")
                print(f"Nome utente: {username}")
                print(f"Password: {password}")
        else:
            continue
        if date_created != 86400000000 and date_created:
            if language == "English":
                print(f"Creation date: {str(get_chrome_datetime(date_created))}")
            else:
                print(f"Data di creazione: {str(get_chrome_datetime(date_created))}")
        if date_last_used != 86400000000 and date_last_used:
            if language == "English":
                print(f"Last used date: {str(get_chrome_datetime(date_last_used))}")
            else:
                print(f"Data di ultimo uso: {str(get_chrome_datetime(date_last_used))}")
        print("="*50)
    cursor.close()
    db.close()
    try:
        os.remove(file_name)
    except:
        pass


def delete_chrome_pass(language):
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", 
                            "Google", "Chrome", "User Data", "default", "Login Data")
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    n_logins = len(cursor.fetchall())
    if language == "English":
        print(f"Deleting a total of {n_logins} logins...")
    else:
        print(f"Cancellando un totale di {n_logins} login...")
    cursor.execute("delete from logins")
    cursor.connection.commit()
    if language == "English":
        print("Done!")
    else:
        print("Fatto!")


def get_chrome_datetime(chrome_date):
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_date)


def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"], 
                                    "AppData", "Local", "Google", "Chrome", 
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""


if __name__ == "__main__":
    main()
