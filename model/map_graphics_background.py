from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
import math
DEBUG =True
#Graphics object of map object
class QMapGraphicsBackground(QGraphicsPixmapItem):
    def __init__(self, path, size, parent=None):
        super().__init__(parent)

        self.size = size
        self.path = path
        background_pic = QPixmap(self.path)
        scaled = background_pic.scaled(self.size, Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        #scaled.fill(Qt.transparent)
        self.setPixmap(scaled) 
        self.setPos(-self.size.width()/2,-self.size.height()/2)

    def setSize(self, size):
        self.size = size





    
