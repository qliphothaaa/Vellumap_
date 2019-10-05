from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re
#from model.map_object import MapObject

#button class for create object
#This is generate from type
DEBUG = False
class QTypePushButton(QPushButton):
    TypeNameSignal = pyqtSignal(str)
    ChangeModeSignal = pyqtSignal(str)
    def __init__(self, object_type, parent):
        super(QTypePushButton, self).__init__( parent)
        self.button_size = QSize(100, 20)
        self.title = object_type
        self.real_title =  re.sub('^type', '', self.title)
        self.setText(self.real_title)
        self.pressed = False
        self.setMinimumSize(self.button_size)


    def mousePressEvent(self,e):
        if DEBUG: print('BUTTON: button pressed, create Object')
        if e.button() == Qt.LeftButton:
            self.TypeNameSignal.emit(self.title)
            if(self.pressed):
                self.setStyleSheet("");
                self.ChangeModeSignal.emit('select')
            else:
                self.setStyleSheet("color: black;");
                self.ChangeModeSignal.emit('create')
            self.pressed = not(self.pressed)
            
        super().mousePressEvent(e)
