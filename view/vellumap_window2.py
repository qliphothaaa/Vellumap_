from PyQt5.QtWidgets import *
from view.main_widget2 import MainWidget
import sys
import re

class VellumapWindow2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        mainEditor = MainWidget('newMap')
        self.setCentralWidget(mainEditor)
        self.setGeometry(0,0,1200,800)
        self.setWindowTitle('first')
        self.show()
