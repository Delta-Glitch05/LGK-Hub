from PyQt5 import QtWidgets
import os, sys, subprocess
from PyQt5.QtCore import QDateTime, Qt, QTimer, QProcess
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon


class Payloads_Menu(QDialog):
    def __init__(self, parent=None):
        self.language, self.style, self.mode = self.get_lang_style_and_mode()
        super(Payloads_Menu, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Payloads Menu')
        self.setGeometry(550, 275, 500, 400)
        self.changeStyle()
        # print(self.style)
        # self.originalPalette = QApplication.palette()
        self.label = QtWidgets.QLabel("boh")
        self.createGroupBox()
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.groupBox, 1, 0, 2, 2)
        # self.mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        self.mainLayout.setRowStretch(1, 1)
        self.mainLayout.setRowStretch(2, 1)
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 1)
        self.setLayout(self.mainLayout)
    

    def createGroupBox(self):
        self.groupBox = QGroupBox("Group 1")
        self.remote_shell_cmd = QPushButton("Remote Shell Commands Executor")
        self.remote_shell_cmd.setDefault(True)
        self.reverse_shell = QPushButton("Reverse Shell")
        self.reverse_shell.setDefault(True)
        self.keylogger = QPushButton("Keylogger")
        self.keylogger.setDefault(True)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.remote_shell_cmd)
        self.layout.addWidget(self.reverse_shell)
        self.layout.addWidget(self.keylogger)
        self.layout.addStretch(1)
        self.groupBox.setLayout(self.layout)
        self.retranslating = False
        self.retranslateUi(Payloads_Menu)


    def retranslateUi(self, Payloads_Menu):
        _translate = QtCore.QCoreApplication.translate
        if self.retranslating == False:
            self.setWindowTitle(_translate("Payloads_Menu", "Payloads_Menu"))
            self.retranslating = True
        # self.language = self.languageBox.currentText()
        if self.language == "English":
            self.setWindowTitle("Payloads Menu")
            self.groupBox.setTitle("Group 1")
            self.remote_shell_cmd.setText("Remote Shell Commands Executor")
            self.reverse_shell.setText("Reverse Shell")
            self.keylogger.setText("Keylogger")
        else:
            self.setWindowTitle("Menù di Scelta")
            self.groupBox.setTitle("Gruppo 1")
            self.remote_shell_cmd.setText("Esecutore di Comandi in Shell Remota")
            self.reverse_shell.setText("Reverse Shell")
            self.keylogger.setText("Keylogger")

    
    def get_lang_style_and_mode(self):
        with open("lang.txt","r") as lang_file:
            list_ = lang_file.readlines()
            language = list_[0]
            lang_list = list(language)
            if lang_list[-1] == "\n":
                lang_list.pop()
            language = "".join(lang_list)
            if len(list_) >= 2:
                style = list_[1][:-1]
                if len(list_) == 3:
                    mode = list_[2]
                else:
                    mode = "terminal"
                with open("lang.txt","w") as lang_file:
                    lang_file.write(language)
        return language, style, mode


    def open_application(self, app):
        if self.mode == "menu":
            with open("lang.txt", "a") as lang_file:
                lang_file.write("\nmenu")
        subprocess.Popen(f"{app}.bat", shell=True)


    def changeStyle(self):
        QApplication.setStyle(QStyleFactory.create(self.style))
        # self.changePalette()
        QApplication.setPalette(QApplication.style().standardPalette())            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wind = Payloads_Menu()
    wind.show()
    sys.exit(app.exec_())
