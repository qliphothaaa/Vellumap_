from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from model.change_pic import strToImage
import math
DEBUG =True
#Graphics object of map object
class QMapGraphicsBackground(QGraphicsPixmapItem):
    def __init__(self, background, parent=None):
        super().__init__(parent)
        self.background = background
        self.object_id = -1
        self.setPixmap(self.generatePixmap()) 
        self.setPosition()

    def generatePixmap(self):
        self.path = strToImage(self.background.pic_str, self.background.pic_name)
        reader = QImageReader(self.path)
        self.size = reader.size() * self.background.rate
        background_pic = QPixmap(self.path)
        scaled_pixmap = background_pic.scaled(self.size, Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        return scaled_pixmap


    def setSize(self, size):
        self.size = size

    def setPosition(self):
        self.setPos(self.background.x - self.size.width()/2, self.background.y - self.size.height()/2)
