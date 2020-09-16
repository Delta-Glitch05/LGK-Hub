import os, sys, subprocess, fbchat
from fbchat import Client
from fbchat.models import Message


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
        while True:
            if language == "English":
                print("WARNING: You must already have an existing account!")
                username = input("Enter the username --> ")
            else:
                print("ATTENZIONE: Devi già avere un account esistente!")
                username = input("Inserisci lo username --> ")
            if username.lower() == "exit":
                if language == "English":
                    print("Goodbye!\n")
                else:
                    print("Arrivederci!\n")
                loop = False
                break
            if language == "English":
                password = input("Enter the password --> ")
            else:
                password = input("Inserisci la password --> ")
            if password.lower() == "exit":
                if language == "English":
                    print("Goodbye!\n")
                else:
                    print("Arrivederci!\n")
                loop = False
                break
            client = Client(username, password)
            if "err.txt" in os.listdir():
                if language == "English":
                    print("You have not entered valid credentials!\n")
                else:
                    print("Non hai inserito delle credenziali valide!\n")
                os.remove("err.txt")
            else:
                fb_mess_bot(client, language)
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
                        subprocess.Popen("Website_Crawler\\fb_mess_bot.bat", shell=True)
                        sys.exit()
                    else:
                        break


def fb_mess_bot(client, language):
    users = client.fetchThreadList()
    if language == "English":
        print(f"Users you most recently talked to: {users}")
    else:
        print(f"Utenti con cui hai parlato di più recentemente: {users}")
    detailed_users = [list(client.fetchThreadInfo(user.uid).values())[0] for user in users]
    sorted_detailed_users = sorted(detailed_users, key=lambda u: u.message_count, reverse=True)
    best_friend = sorted_detailed_users[0]
    while True:
        if language == "English":
            choice = input("\nDo you want to know how many users you talked to in total? [Y/n] --> ")
        else:
            choice = input("\nVuoi sapere con quanti utenti hai parlato in totale? [Y/n] --> ")
        if choice.lower() == "y" or choice.lower() == "yes" or choice.lower() == "s" or choice.lower() == "si":
            all_users = client.fetchAllUsers()
            if language == "English":
                print(f"You talked with a total of {len(all_users)} users!")
            else:
                print(f"Hai parlato con un totale di {len(all_users)} utenti!")
            break
        elif choice.lower() == "n" or choice.lower() == "no":
            break
        else:
            if language == "English":
                print("You have not entered a valid choice!")
            else:
                print("Non hai inserito una scelta valida!")
    if language == "English":
        print(f"\nBest friend: {best_friend.name}, with a message count of {best_friend.message_count} messages!")
    else:
        print(f"\nMigliore amico: {best_friend.name}, con un conteggio messaggi di {best_friend.message_count} messaggi!")
    while True:
        if language == "English":
            choice = input("\nDo you want to send him a message? [Y/n] --> ")
        else:
            choice = input("\nVuoi inviargli un messaggio? [Y/n] --> ")
        if choice.lower() == "y" or choice.lower() == "yes" or choice.lower() == "s" or choice.lower() == "si":
            if language == "English":
                msg = input("Insert the message --> ")
            else:
                msg = input("Inserisci il messaggio --> ")
            client.send(Message(text=msg))
            break
        elif choice.lower() == "n" or choice.lower() == "no":
            break
        else:
            if language == "English":
                print("You have not entered a valid choice!")
            else:
                print("Non hai inserito una scelta valida!")
    if language == "English":
        print("Done!\n")
    else:
        print("Fatto!\n")
    client.logout()


if __name__ == "__main__":
    main()
