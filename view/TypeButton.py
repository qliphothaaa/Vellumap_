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
    def __init__(self, object_type, parent):
        super(QTypePushButton, self).__init__( parent)
        self.title = object_type.type_name
        self.real_title =  re.sub('^type', '', self.title)
        self.setText(self.real_title)


    def mousePressEvent(self,e):
        if DEBUG: print('BUTTON: button pressed, create Object')
        if e.button() == Qt.LeftButton:
            self.TypeNameSignal.emit(self.title)
        super().mousePressEvent(e)
