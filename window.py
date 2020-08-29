from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setGeometry(500,200,300,300)
        self.setWindowTitle("Prova")
        self.initUI()
    
    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Ciao!")
        self.label.move(100,50)
        self.button = QtWidgets.QPushButton(self)
        self.button.setText("Premi")
        self.button.clicked.connect(self.clicked)
    
    def clicked(self):
        self.label.setText("You pressed the button!")
        self.update()
    
    def update(self):
        self.label.adjustSize()
