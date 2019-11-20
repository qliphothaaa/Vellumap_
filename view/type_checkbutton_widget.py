from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re

class TypeCheckButton(QPushButton):
    CheckedSignal = pyqtSignal(str, bool)
    UncheckedSignal = pyqtSignal(str, bool)
    def __init__(self, object_type_name, parent):
        super(TypeCheckButton, self).__init__(parent)
        self.button_size = QSize(100, 20)
        self.title = object_type_name
        self.real_title =  re.sub('^type', '', self.title)
        self.setText(self.real_title)
        self.setMinimumSize(self.button_size)
        self.setCheckable(True)
        self.setChecked(True)


    def mousePressEvent(self,e):
        if(self.isChecked()):
            self.UncheckedSignal.emit(self.title,False)
        else:
            self.CheckedSignal.emit(self.title, True)

        super().mousePressEvent(e)



