import os, sys, subprocess
from PyQt5.QtCore import QDateTime, Qt, QTimer, QProcess
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon


class MainWindow(QDialog):
    def __init__(self, parent=None):
        with open("lang.txt","r") as lang_file:
            self.language = lang_file.readline()
        # print(self.language)
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.originalPalette = QApplication.palette()
        self.styleComboBox = QComboBox()
        self.styleComboBox.addItems(QStyleFactory.keys())
        self.styleLabel = QLabel("&Style:")
        self.styleLabel.setBuddy(self.styleComboBox)
        index = self.styleComboBox.findText("Fusion", QtCore.Qt.MatchFixedString)
        self.styleComboBox.setCurrentIndex(index)
        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)
        self.disableWidgetsCheckBox = QCheckBox("&Disable widgets")
        self.createGroupBox()
        self.createProgressBar()
        self.styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        self.disableWidgetsCheckBox.toggled.connect(self.groupBox.setDisabled)
        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.styleLabel)
        self.topLayout.addWidget(self.styleComboBox)
        self.topLayout.addStretch(1)
        self.topLayout.addWidget(self.useStylePaletteCheckBox)
        self.topLayout.addWidget(self.disableWidgetsCheckBox)
        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout(self.topLayout, 0, 0, 1, 2)
        self.mainLayout.addWidget(self.groupBox, 1, 0, 2, 2)
        # self.mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        self.mainLayout.setRowStretch(1, 1)
        self.mainLayout.setRowStretch(2, 1)
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 1)
        self.setLayout(self.mainLayout)
        self.changeStyle('Fusion')
        self.setGeometry(450, 250, 800, 600)
        self.retranslating = False
        self.retranslateUi(MainWindow)
    

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        if self.retranslating == False:
            self.setWindowTitle(_translate("MainWindow", "MainWindow"))
            self.retranslating = True
        # self.language = self.languageBox.currentText()
        if self.language == "English":
            self.setWindowTitle("Choice menu")
            self.styleLabel.setText(_translate("MainWindow", "&Style:"))
            self.useStylePaletteCheckBox.setText(_translate("MainWindow", "&Use style's standard palette"))
            self.disableWidgetsCheckBox.setText(_translate("MainWindow", "&Disable widgets"))
            self.groupBox.setTitle("Group 1")
            self.network_scanner.setText("Network Scanner")
            self.subdomain_scanner.setText("Subdomain Scanner")
            self.syn_flooder.setText("SYN Flooding Tool")
            self.brute_forcer.setText("Brute-Forcer")
            self.steganotool.setText("Steganography Tool")
            self.website_crawler.setText("Website Crawler")
            self.file_encryptor.setText("File encryptor/decryptor")
            self.http_sniffer.setText("HTTP Sniffer")
            self.dns_spoofer.setText("DNS Spoofer")
            self.arp_spoofer.setText("ARP Spoofer")
            self.t_ssh_client.setText("SSH and Telnet client")
        else:
            self.setWindowTitle("Menù di scelta")
            self.styleLabel.setText(_translate("MainWindow", "&Stile:"))
            self.useStylePaletteCheckBox.setText(_translate("MainWindow", "&Usa i colori standard dello stile"))
            self.disableWidgetsCheckBox.setText(_translate("MainWindow", "&Disabilita i widgets"))
            self.groupBox.setTitle("Gruppo 1")
            self.network_scanner.setText("Scanner di rete")
            self.subdomain_scanner.setText("Scanner di sottodomini")
            self.syn_flooder.setText("Strumento di SYN Flooding")
            self.brute_forcer.setText("Brute-Forcer")
            self.steganotool.setText("Strumento di steganografia")
            self.website_crawler.setText("Website Crawler")
            self.file_encryptor.setText("Criptatore/Decriptatore di file")
            self.http_sniffer.setText("HTTP Sniffer")
            self.dns_spoofer.setText("DNS Spoofer")
            self.arp_spoofer.setText("ARP Spoofer")
            self.t_ssh_client.setText("Client SSH e Telnet")


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
  

    def createGroupBox(self):
        self.groupBox = QGroupBox("Group 1")
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
        self.file_encryptor = QPushButton("File Encryptor/Decryptor")
        self.file_encryptor.setDefault(True)
        self.http_sniffer = QPushButton("HTTP Sniffer")
        self.http_sniffer.setDefault(True)
        self.dns_spoofer = QPushButton("DNS Spoofer")
        self.dns_spoofer.setDefault(True)
        self.arp_spoofer = QPushButton("ARP Spoofer")
        self.arp_spoofer.setDefault(True)
        self.t_ssh_client = QPushButton("SSH and Telnet client")
        self.t_ssh_client.setDefault(True)
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
        self.layout.addWidget(self.file_encryptor)
        self.layout.addWidget(self.http_sniffer)
        self.layout.addWidget(self.dns_spoofer)
        self.layout.addWidget(self.arp_spoofer)
        self.layout.addWidget(self.t_ssh_client)
        # self.layout.addWidget(togglePushButton)
        # self.layout.addWidget(flatPushButton)
        self.layout.addStretch(1)
        self.groupBox.setLayout(self.layout)
        self.clicksOnButton = 0
        self.network_scanner.clicked.connect(self.open_network_scanner)
        self.subdomain_scanner.clicked.connect(self.open_subdomain_scanner)
        self.syn_flooder.clicked.connect(self.open_syn_flooder)
        self.brute_forcer.clicked.connect(self.open_brute_forcer)
        self.steganotool.clicked.connect(self.open_steganotool)
        self.website_crawler.clicked.connect(lambda: self.open_website_crawler_menu(self.styleName))


    """
    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)
        self.tab1 = QWidget()
        self.tableWidget = QTableWidget(10, 10)
        self.tab1hbox = QHBoxLayout()
        self.tab1hbox.setContentsMargins(5, 5, 5, 5)
        self.tab1hbox.addWidget(self.tableWidget)
        self.tab1.setLayout(self.tab1hbox)
        self.tab2 = QWidget()
        self.textEdit = QTextEdit()
        self.textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n" 
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n" 
                              "How I wonder what you are!\n")

        self.tab2hbox = QHBoxLayout()
        self.tab2hbox.setContentsMargins(5, 5, 5, 5)
        self.tab2hbox.addWidget(self.textEdit)
        self.tab2.setLayout(self.tab2hbox)
        self.bottomLeftTabWidget.addTab(self.tab1, "&Table")
        self.bottomLeftTabWidget.addTab(self.tab2, "Text &Edit")
    """


    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.advanceProgressBar)
        self.timer.start(1000)
    

    def open_network_scanner(self):
        """
        cmd = 'python network_scanner.py'
        proc = QProcess()
        clear = subprocess.call(['cls'], shell=True)
        proc.startDetached(cmd)
        proc = QProcess()
        proc.startDetached("open_network_scanner.bat")
        """
        with open("lang.txt", "a") as lang_file:
            lang_file.write("\nmenu")
        subprocess.Popen("network_scanner.bat", shell=True)


    def open_subdomain_scanner(self):
        with open("lang.txt", "a") as lang_file:
            lang_file.write("\nmenu")
        subprocess.Popen("subdomain_scanner.bat", shell=True)


    def open_syn_flooder(self):
        with open("lang.txt", "a") as lang_file:
            lang_file.write("\nmenu")
        subprocess.Popen("syn_flooder.bat", shell=True)


    def open_brute_forcer(self):
        with open("lang.txt", "a") as lang_file:
            lang_file.write("\nmenu")
        subprocess.Popen("brute-forcer.bat", shell=True)
    

    def open_steganotool(self):
        with open("lang.txt", "a") as lang_file:
            lang_file.write("\nmenu")
        subprocess.Popen("steganotool.bat", shell=True)
    

    def open_website_crawler_menu(self, style):
        with open("lang.txt", "a") as lang_file:
            lang_file.write(f"\n{style}")
        subprocess.Popen("website_crawler_menu.py", shell=True)


def main():
    app = QApplication(sys.argv)
    wind = MainWindow()
    wind.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
