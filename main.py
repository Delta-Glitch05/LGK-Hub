import os
import sys
import subprocess
import webbrowser
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QDateTime, Qt, QTimer, QProcess, QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QDesktopServices


class MainWindow(QDialog):
    def __init__(self, parent=None):
        with open("lang.txt", "r") as lang_file:
            self.language = lang_file.readline()
        # print(self.language)
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.originalPalette = QApplication.palette()
        self.styleComboBox = QComboBox()
        self.styleComboBox.addItems(QStyleFactory.keys())
        self.styleLabel = QLabel("&Style:")
        self.styleLabel.setBuddy(self.styleComboBox)
        self.index = self.styleComboBox.findText("Fusion", QtCore.Qt.MatchFixedString)
        self.styleComboBox.setCurrentIndex(self.index)
        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)
        self.disableWidgetsCheckBox = QCheckBox("&Disable widgets")
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()
        self.createProgressBar()
        self.createProgressBar()
        self.styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        self.disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        self.disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        self.disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        self.disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)
        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.styleLabel)
        self.topLayout.addWidget(self.styleComboBox)
        self.topLayout.addStretch(1)
        self.topLayout.addWidget(self.useStylePaletteCheckBox)
        self.topLayout.addWidget(self.disableWidgetsCheckBox)
        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout(self.topLayout, 0, 0, 1, 2)
        self.mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        self.mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        self.mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        self.mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        # self.mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        self.mainLayout.setRowStretch(1, 1)
        self.mainLayout.setRowStretch(2, 1)
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 1)
        self.setLayout(self.mainLayout)
        self.changeStyle('Fusion')
        self.setGeometry(400, 200, 800, 600)
        self.retranslating = False
        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        if not self.retranslating:
            self.setWindowTitle(_translate("MainWindow", "MainWindow"))
            self.retranslating = True
        # self.language = self.languageBox.currentText()
        if self.language == "English":
            self.setWindowTitle("Choice menu")
            self.styleLabel.setText(_translate("MainWindow", "&Style:"))
            self.useStylePaletteCheckBox.setText(_translate("MainWindow", "&Use style's standard palette"))
            self.disableWidgetsCheckBox.setText(_translate("MainWindow", "&Disable widgets"))
            self.topLeftGroupBox.setTitle("Applications")
            self.topRightGroupBox.setTitle("Settings")
            self.network_scanner.setText("Network Scanner")
            self.subdomain_scanner.setText("Subdomain Scanner")
            self.syn_flooder.setText("SYN Flooding Tool")
            self.brute_forcer.setText("Brute-Forcer")
            self.steganotool.setText("Steganography Tool")
            self.website_crawler.setText("Website Crawler")
            self.encryptor_decryptor.setText("String and File encryptor/decryptor")
            self.http_sniffer.setText("HTTP Sniffer")
            self.dns_spoofer.setText("DNS Spoofer")
            self.arp_spoofer.setText("ARP Spoofer")
            self.t_ssh_client.setText("SSH and Telnet client")
            self.app_settings_label.setText("Application Settings")
            self.return_to_start_label.setText("When returning to the start:")
        else:
            self.setWindowTitle("Menù di scelta")
            self.styleLabel.setText(_translate("MainWindow", "&Stile:"))
            self.useStylePaletteCheckBox.setText(_translate("MainWindow", "&Usa i colori standard dello stile"))
            self.disableWidgetsCheckBox.setText(_translate("MainWindow", "&Disabilita i widgets"))
            self.topLeftGroupBox.setTitle("Applicazioni")
            self.topRightGroupBox.setTitle("Impostazioni")
            self.network_scanner.setText("Scanner di rete")
            self.subdomain_scanner.setText("Scanner di sottodomini")
            self.syn_flooder.setText("Strumento di SYN Flooding")
            self.brute_forcer.setText("Brute-Forcer")
            self.steganotool.setText("Strumento di steganografia")
            self.website_crawler.setText("Website Crawler")
            self.encryptor_decryptor.setText("Criptatore/Decriptatore di Stringhe e File")
            self.http_sniffer.setText("HTTP Sniffer")
            self.dns_spoofer.setText("DNS Spoofer")
            self.arp_spoofer.setText("ARP Spoofer")
            self.t_ssh_client.setText("Client SSH e Telnet")
            self.app_settings_label.setText("Impostazioni delle Applicazioni")
            self.return_to_start_label.setText("Quando si ritorna all'inizio:")
            self.radioButton1.setText("Riavvia l'applicazione e pulisci la finestra del terminale")
            self.radioButton2.setText("Mantiene l'output e non pulisce la finestra del terminale")

    def changeStyle(self, styleName):
        self.styleName = styleName
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if self.useStylePaletteCheckBox.isChecked():
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def advanceProgressBar(self):
        self.curVal = self.progressBar.value()
        self.maxVal = self.progressBar.maximum()
        self.progressBar.setValue(self.curVal + (self.maxVal - self.curVal) // 100)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Applications")
        self.network_scanner = QPushButton("Network Scanner")
        self.network_scanner.setDefault(True)
        self.subdomain_scanner = QPushButton("Subdomain Scanner")
        self.subdomain_scanner.setDefault(True)
        self.syn_flooder = QPushButton("SYN Flooding tool")
        self.syn_flooder.setDefault(True)
        self.brute_forcer = QPushButton("Brute-Forcer")
        self.brute_forcer.setDefault(True)
        self.steganotool = QPushButton("Steganography tool")
        self.steganotool.setDefault(True)
        self.website_crawler = QPushButton("Website Crawler")
        self.website_crawler.setDefault(True)
        self.encryptor_decryptor = QPushButton("String and File Encryptor/Decryptor")
        self.encryptor_decryptor.setDefault(True)
        self.http_sniffer = QPushButton("HTTP Sniffer")
        self.http_sniffer.setDefault(True)
        self.dns_spoofer = QPushButton("DNS Spoofer")
        self.dns_spoofer.setDefault(True)
        self.arp_spoofer = QPushButton("ARP Spoofer")
        self.arp_spoofer.setDefault(True)
        self.arp_spoof_detecter = QPushButton("ARP Spoof Attack Detecter")
        self.arp_spoof_detecter.setDefault(True)
        self.t_ssh_client = QPushButton("SSH and Telnet client")
        self.t_ssh_client.setDefault(True)
        self.chrome_pass_extractor = QPushButton("Chrome Password Extractor")
        self.chrome_pass_extractor.setDefault(True)
        self.payloads = QPushButton("Payloads")
        self.payloads.setDefault(True)
        self.wifi_dev_disconnecter = QPushButton("Wi-Fi Device Disconnecter")
        self.wifi_dev_disconnecter.setDefault(True)
        self.fake_access_point = QPushButton("Fake Access Points Generator")
        self.fake_access_point.setDefault(True)
        # self.togglePushButton = QPushButton("Toggle Push Button")
        # self.togglePushButton.setCheckable(True)
        # self.togglePushButton.setChecked(True)
        # self.flatPushButton = QPushButton("Flat Push Button")
        # self.flatPushButton.setFlat(True)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.network_scanner)
        self.layout.addWidget(self.subdomain_scanner)
        self.layout.addWidget(self.syn_flooder)
        self.layout.addWidget(self.brute_forcer)
        self.layout.addWidget(self.steganotool)
        self.layout.addWidget(self.website_crawler)
        self.layout.addWidget(self.encryptor_decryptor)
        self.layout.addWidget(self.http_sniffer)
        self.layout.addWidget(self.dns_spoofer)
        self.layout.addWidget(self.arp_spoofer)
        self.layout.addWidget(self.arp_spoof_detecter)
        self.layout.addWidget(self.t_ssh_client)
        self.layout.addWidget(self.chrome_pass_extractor)
        self.layout.addWidget(self.payloads)
        self.layout.addWidget(self.wifi_dev_disconnecter)
        self.layout.addWidget(self.fake_access_point)
        # self.layout.addWidget(togglePushButton)
        # self.layout.addWidget(flatPushButton)
        self.layout.addStretch(1)
        self.topLeftGroupBox.setLayout(self.layout)
        self.clicksOnButton = 0
        self.network_scanner.clicked.connect(lambda: self.open_application("network_scanner"))
        self.subdomain_scanner.clicked.connect(lambda: self.open_application("subdomain_scanner"))
        self.syn_flooder.clicked.connect(lambda: self.open_application("syn_flooder"))
        self.brute_forcer.clicked.connect(lambda: self.open_application("brute-forcer"))
        self.steganotool.clicked.connect(lambda: self.open_application("steganotool"))
        self.website_crawler.clicked.connect(lambda: self.open_website_crawler_menu(self.styleName))
        self.encryptor_decryptor.clicked.connect(lambda: self.open_application("encryptor-decryptor"))
        self.http_sniffer.clicked.connect(lambda: self.open_application("http_sniffer"))
        self.chrome_pass_extractor.clicked.connect(lambda: self.open_application("chrome_pass_extractor"))
        self.payloads.clicked.connect(lambda: self.open_payloads_menu(self.styleName))
        self.arp_spoofer.clicked.connect(lambda: self.open_application("arp_spoofer"))
        self.arp_spoof_detecter.clicked.connect(lambda: self.open_application("arp_spoof_detecter"))

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Settings")
        self.gen_font = QtGui.QFont()
        self.gen_font.setFamily("Arial Black")
        self.gen_font.setPointSize(10)
        # self.gen_font.setWeight(100)
        self.gen_font.setBold(True)
        self.topRightGroupBox.setFont(self.gen_font)
        self.app_settings_label = QLabel("Application Settings")
        self.font_1 = QtGui.QFont()
        self.font_1.setFamily("Arial Nova")
        self.font_1.setWeight(40)
        self.font_1.setBold(True)
        self.return_to_start_label = QLabel("When returning to the start:")
        self.return_to_start_label.setFont(self.font_1)
        self.font_2 = QtGui.QFont()
        self.font_2.setFamily("Arial")
        self.font_2.setPointSize(9)
        self.font_2.setWeight(60)
        # self.font_2.setBold(True)
        self.app_settings_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.return_to_start_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.radioButton1 = QRadioButton("Restart the application and clear the terminal window")
        self.radioButton2 = QRadioButton("Keep the output and don't clean the terminal window")
        self.radioButton1.setChecked(True)
        self.radioButton1.setFont(self.font_2)
        self.radioButton2.setFont(self.font_2)
        self.button_font = QtGui.QFont()
        self.button_font.setFamily("Arial Nova")
        self.button_font.setWeight(50)
        self.conf_button = QPushButton("Confirm")
        self.conf_button.setDefault(True)
        self.conf_button.setFont(self.button_font)
        self.checkBox = QCheckBox("Tri-state check box")
        self.checkBox.setTristate(True)
        self.checkBox.setCheckState(Qt.PartiallyChecked)
        layout = QVBoxLayout()
        layout.addWidget(self.app_settings_label)
        layout.addWidget(self.return_to_start_label)
        layout.addWidget(self.radioButton1)
        layout.addWidget(self.radioButton2)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)
        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)
        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n"
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n"
                              "How I wonder what you are!\n")
        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)
        self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Group 3")
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(True)
        self.lineEdit = QLineEdit('s3cRe7')
        self.lineEdit.setEchoMode(QLineEdit.Password)
        self.spinBox = QSpinBox(self.bottomRightGroupBox)
        self.spinBox.setValue(50)
        self.dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.slider = QSlider(Qt.Horizontal, self.bottomRightGroupBox)
        self.slider.setValue(40)
        self.scrollBar = QScrollBar(Qt.Horizontal, self.bottomRightGroupBox)
        self.scrollBar.setValue(60)
        self.dial = QDial(self.bottomRightGroupBox)
        self.dial.setValue(30)
        self.dial.setNotchesVisible(True)
        self.link = "https://github.com/Delta-Glitch05/LGK-Hub"
        self.github_link = QLabel(f"<a href='{self.link}'>{self.link}</a>")
        self.github_link.setFont(self.font_2)
        self.github_link.setOpenExternalLinks(True)
        # self.github_link.linkActivated.connect(lambda: QDesktopServices.openUrl(QUrl(self.link)))
        layout = QGridLayout()
        layout.addWidget(self.lineEdit, 0, 0, 1, 2)
        layout.addWidget(self.spinBox, 1, 0, 1, 2)
        layout.addWidget(self.dateTimeEdit, 2, 0, 1, 2)
        layout.addWidget(self.slider, 3, 0)
        layout.addWidget(self.scrollBar, 4, 0)
        layout.addWidget(self.dial, 3, 1, 2, 1)
        layout.addWidget(self.github_link, 6, 0)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.advanceProgressBar)
        self.timer.start(1000)

    def open_application(self, app):
        if self.radioButton1.isChecked():
            with open("lang.txt", "a") as lang_file:
                lang_file.write("\nmenu")
        subprocess.Popen(f"{app}.bat", shell=True)

    def open_website_crawler_menu(self, style):
        with open("lang.txt", "a") as lang_file:
            lang_file.write(f"\n{style}")
            if self.radioButton1.isChecked():
                lang_file.write("\nmenu")
        subprocess.Popen("website_crawler_menu.py", shell=True)

    def open_payloads_menu(self, style):
        with open("lang.txt", "a") as lang_file:
            lang_file.write(f"\n{style}")
            if self.radioButton1.isChecked():
                lang_file.write("\nmenu")
        subprocess.Popen("payloads_menu.py", shell=True)


def main():
    app = QApplication(sys.argv)
    wind = MainWindow()
    wind.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
