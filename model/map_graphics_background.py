from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
import math
DEBUG =True
#Graphics object of map object
class QMapGraphicsBackground(QGraphicsPixmapItem):
    def __init__(self, background, parent=None):
        super().__init__(parent)
        self.object_id = -1
        self.size = background.size
        self.path = background.path_name
        self.background = background
        background_pic = QPixmap(self.path)
        scaled = background_pic.scaled(self.size, Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.setPixmap(scaled) 
        self.setPosition()

    def setSize(self, size):
        self.size = size

    def setPosition(self):
        self.setPos(self.background.x - self.size.width()/2, self.background.y - self.size.height()/2)





    
