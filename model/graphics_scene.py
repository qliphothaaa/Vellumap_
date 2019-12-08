import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#background of map editor
class QMapGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.scene = scene
        self.gridSize = 20
        self._color_background = QColor('#393939')

        self.setBackgroundBrush(self._color_background)


    def setGrScene(self, width, height):
        self.setSceneRect(-width//2, -height//2, width, height)


    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

    def addBackgroundItem(self, item):
        self.addItem(item)
        self.background_graphic = item
        item.setZValue(-3)

    def clearBackground(self):
        for i in self.items():
            if i.object_id == -1:
                self.removeItem(i)

        

        
