from PyQt5 import QtWidgets
import os, sys, subprocess
from PyQt5.QtCore import QDateTime, Qt, QTimer, QProcess
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon


class Website_Crawler_Menu(QDialog):
    def __init__(self, parent=None):
        self.language, self.style, self.mode = self.get_lang_style_and_mode()
        super(Website_Crawler_Menu, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Website Crawler Menu')
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
        self.pdf_image_extractor = QPushButton("Image Extractor from PDF")
        self.pdf_image_extractor.setDefault(True)
        self.pdf_link_extractor = QPushButton("Link Extractor from PDF")
        self.pdf_link_extractor.setDefault(True)
        self.ytc_extractor = QPushButton("YouTube Comments Extractor")
        self.ytc_extractor.setDefault(True)
        self.dom_name_info_extractor = QPushButton("Domain Name Info Extractor")
        self.dom_name_info_extractor.setDefault(True)
        self.sql_inj_scanner = QPushButton("SQL Injection Scanner (EXPERIMENTAL)")
        self.sql_inj_scanner.setDefault(True)
        self.web_forms_extractor = QPushButton("Web Forms Extractor/Submitter")
        self.web_forms_extractor.setDefault(True)
        self.img_meta_extractor = QPushButton("Image Metadata Extractor")
        self.img_meta_extractor.setDefault(True)
        self.script_css_extractor = QPushButton("Script and CSS Files Extractor")
        self.script_css_extractor.setDefault(True)
        self.proxy_rotator = QPushButton("Proxy Rotator")
        self.proxy_rotator.setDefault(True)
        self.html_tab_to_csv_converter = QPushButton("HTML Tables to CSV Converter")
        self.html_tab_to_csv_converter.setDefault(True)
        self.email_extractor = QPushButton("E-Mail Extractor")
        self.email_extractor.setDefault(True)
        self.xss_scanner = QPushButton("Cross-Site Scripting (XSS) Scanner (EXPERIMENTAL)")
        self.xss_scanner.setDefault(True)
        self.link_extractor = QPushButton("Websites Link Extractor")
        self.link_extractor.setDefault(True)
        self.image_downloader = QPushButton("Image Downloader")
        self.image_downloader.setDefault(True)
        self.weather_data_extractor = QPushButton("Weather Data Extractor")
        self.weather_data_extractor.setDefault(True)
        self.yt_data_extractor = QPushButton("YouTube Data Extractor")
        self.yt_data_extractor.setDefault(True)
        self.wiki_data_extractor = QPushButton("Wikipedia Data Extractor")
        self.wiki_data_extractor.setDefault(True)
        self.fb_mess_bot = QPushButton("Facebook Messenger Bot")
        self.fb_mess_bot.setDefault(True)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.pdf_image_extractor)
        self.layout.addWidget(self.pdf_link_extractor)
        self.layout.addWidget(self.ytc_extractor)
        self.layout.addWidget(self.dom_name_info_extractor)
        self.layout.addWidget(self.sql_inj_scanner)
        self.layout.addWidget(self.web_forms_extractor)
        self.layout.addWidget(self.img_meta_extractor)
        self.layout.addWidget(self.script_css_extractor)
        self.layout.addWidget(self.proxy_rotator)
        self.layout.addWidget(self.html_tab_to_csv_converter)
        self.layout.addWidget(self.email_extractor)
        self.layout.addWidget(self.xss_scanner)
        self.layout.addWidget(self.link_extractor)
        self.layout.addWidget(self.image_downloader)
        self.layout.addWidget(self.weather_data_extractor)
        self.layout.addWidget(self.yt_data_extractor)
        self.layout.addWidget(self.wiki_data_extractor)
        self.layout.addWidget(self.fb_mess_bot)
        self.layout.addStretch(1)
        self.groupBox.setLayout(self.layout)
        self.pdf_image_extractor.clicked.connect(lambda: self.open_application("pdf_image_extractor"))
        self.pdf_link_extractor.clicked.connect(lambda: self.open_application("pdf_link_extractor"))
        self.ytc_extractor.clicked.connect(lambda: self.open_application("ytc_extractor"))
        self.dom_name_info_extractor.clicked.connect(lambda: self.open_application("dom_name_info_extractor"))
        self.sql_inj_scanner.clicked.connect(lambda: self.open_application("sql_injection_scanner"))
        self.web_forms_extractor.clicked.connect(lambda: self.open_application("web_forms_extractor"))
        self.img_meta_extractor.clicked.connect(lambda: self.open_application("image_metadata_extractor"))
        self.script_css_extractor.clicked.connect(lambda: self.open_application("script_css_extractor"))
        self.proxy_rotator.clicked.connect(lambda: self.open_application("proxy_rotator"))
        self.html_tab_to_csv_converter.clicked.connect(lambda: self.open_application("html_tab_to_csv_converter"))
        self.email_extractor.clicked.connect(lambda: self.open_application("email_extractor"))
        self.xss_scanner.clicked.connect(lambda: self.open_application("xss_scanner"))
        self.link_extractor.clicked.connect(lambda: self.open_application("link_extractor"))
        self.image_downloader.clicked.connect(lambda: self.open_application("image_downloader"))
        self.weather_data_extractor.clicked.connect(lambda: self.open_application("weather_data_extractor"))
        self.yt_data_extractor.clicked.connect(lambda: self.open_application("yt_data_extractor"))
        self.wiki_data_extractor.clicked.connect(lambda: self.open_application("wiki_data_extractor"))
        self.fb_mess_bot.clicked.connect(lambda: self.open_application("fb_mess_bot"))
        self.retranslating = False
        self.retranslateUi(Website_Crawler_Menu)


    def retranslateUi(self, Website_Crawler_Menu):
        _translate = QtCore.QCoreApplication.translate
        if self.retranslating == False:
            self.setWindowTitle(_translate("Website_Crawler_Menu", "Website_Crawler_Menu"))
            self.retranslating = True
        # self.language = self.languageBox.currentText()
        if self.language == "English":
            self.setWindowTitle("Website Crawler Menu")
            self.groupBox.setTitle("Group 1")
            self.pdf_image_extractor.setText("Image Extractor from PDF")
            self.pdf_link_extractor.setText("Link Extractor from PDF")
            self.ytc_extractor.setText("YouTube Comments Extractor")
            self.dom_name_info_extractor.setText("Domain Name Info Extractor")
            self.sql_inj_scanner.setText("SQL Injection Scanner (EXPERIMENTAL)")
            self.web_forms_extractor.setText("Web Forms Extractor/Submitter")
            self.img_meta_extractor.setText("Image Metadata Extractor")
            self.script_css_extractor.setText("Script and CSS Files Extractor")
            self.proxy_rotator.setText("Proxy Rotator")
            self.html_tab_to_csv_converter.setText("HTML Tables to CSV Converter")
            self.email_extractor.setText("E-Mail Extractor")
            self.xss_scanner.setText("Cross-Site Scripting (XSS) Scanner (EXPERIMENTAL)")
            self.link_extractor.setText("Websites Link Extractor")
            self.image_downloader.setText("Image Downloader")
            self.weather_data_extractor.setText("Weather Data Extractor")
            self.yt_data_extractor.setText("YouTube Data Extractor")
            self.wiki_data_extractor.setText("Wikipedia Data Extractor")
            self.fb_mess_bot.setText("Facebook Messenger Bot")
        else:
            self.setWindowTitle("Menù di Scelta")
            self.groupBox.setTitle("Gruppo 1")
            self.pdf_image_extractor.setText("Estrattore di Immagini da PDF")
            self.pdf_link_extractor.setText("Estrattore di Link da PDF")
            self.ytc_extractor.setText("Estrattore di Commenti di YouTube")
            self.dom_name_info_extractor.setText("Estrattore di Informazioni su Nomi di Dominio")
            self.sql_inj_scanner.setText("Scansionatore di Vulnerabilità SQL Injection (SPERIMENTALE)")
            self.web_forms_extractor.setText("Estrattore/Mittente di Moduli Web")
            self.img_meta_extractor.setText("Estrattore di Metadata da Immagini")
            self.script_css_extractor.setText("Estrattore di File Script e CSS")
            self.proxy_rotator.setText("Rotatore di Proxy")
            self.html_tab_to_csv_converter.setText("Convertitore di tabelle da HTML a CSV")
            self.email_extractor.setText("Estrattore di E-Mail")
            self.xss_scanner.setText("Scansionatore di Vulnerabilità Cross-Site Scripting (XSS) (SPERIMENTALE)")
            self.link_extractor.setText("Estrattore di Link da Siti Web")
            self.image_downloader.setText("Scaricatore di Immagini")
            self.weather_data_extractor.setText("Estrattore di Dati sul Meteo")
            self.yt_data_extractor.setText("Estrattore di Dati di YouTube")
            self.wiki_data_extractor.setText("Estrattore di Dati di Wikipedia")
            self.fb_mess_bot.setText("Bot di Facebook Messenger")

    
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
        subprocess.Popen(f"Website_Crawler\\{app}.bat", shell=True)
    

    def changeStyle(self):
        QApplication.setStyle(QStyleFactory.create(self.style))
        # self.changePalette()
        QApplication.setPalette(QApplication.style().standardPalette())            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wind = Website_Crawler_Menu()
    wind.show()
    sys.exit(app.exec_())
