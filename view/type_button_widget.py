from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re

#button class for create object
#This is generate from type
DEBUG = False
class TypePushButton(QPushButton):
    ClickedSignal = pyqtSignal(str)
    def __init__(self, object_type, parent):
        super(TypePushButton, self).__init__( parent)
        self.button_size = QSize(100, 20)
        self.title = object_type
        self.real_title =  re.sub('^type', '', self.title)
        self.setText(self.real_title)
        self.color_changed = False
        self.setMinimumSize(self.button_size)


    def mousePressEvent(self,e):
        if DEBUG: print('BUTTON: button pressed, create Object')
        if e.button() == Qt.LeftButton:
            self.ClickedSignal.emit(self.title)
        super().mousePressEvent(e)


    def changeColor(self):
        if (self.color_changed):
            self.setStyleSheet(""); 
            self.color_changed = False
        else:
            self.setStyleSheet("color: black;");
            self.color_changed = True


    def checkPermission(self,permission, name):
        if (self.title == name):
            self.changeColor()


