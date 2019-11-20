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
        #self._color_light = QColor('#2f2f2f')
        #self._color_dark = QColor('#292929')
        #self._pen_light = QPen(self._color_light)
        #self._pen_light.setWidth(1)
        #self._pen_dark = QPen(self._color_dark)
        #self._pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)


    def setGrScene(self, width, height):
        self.setSceneRect(-width//2, -height//2, width, height)


    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

    def addBackgroundItem(self, item):
        self.addItem(item)
        item.setZValue(-3)
    def clearBackground(self):
        for i in self.items():
            if i.object_id == -1:
                self.removeItem(i)

        

        
