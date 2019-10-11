from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
import os.path
import re

class LoadBackgroundDialog(QDialog):
    LoadBackgroundSignal = pyqtSignal(str, int)
    def __init__(self, parent=None):
        super(LoadBackgroundDialog, self).__init__(parent)
        
        self.namelabel = QLabel('name:')
        self.sizeLabel = QLabel('size:')
        self.backgroundNameEdit = QLineEdit()
        self.sizeEdit = QLineEdit()
        self.button1 = QPushButton("Open Existing Map")
        self.button1.clicked.connect(self.clickButton)
        

        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.layout.addRow(self.namelabel,self.backgroundNameEdit)
        self.layout.addRow(self.sizeLabel, self.sizeEdit)
        self.layout.addRow(self.button1)


    def clickButton(self):
        self.LoadBackgroundSignal.emit(self.backgroundNameEdit.text(), int(self.sizeEdit.text()))
        
