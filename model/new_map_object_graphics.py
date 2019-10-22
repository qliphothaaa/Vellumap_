from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math

class QMapObjectGraphics(QGraphicsItem):
    def __init__(self, map_object, color, shape, width, height, parent=None):
        super().__init__(parent)
        #self._color = Qt.white
        self._pen_defalut_color = QPen(Qt.black)
        self._pen_selected = QPen(Qt.white)
        self._pen_selected.setWidth(5)
        self._pen_defalut_color.setWidth(3)
        self.map_object = map_object
        self.object_id = map_object.object_id

        self._brush = QBrush(QColor(color))
        self.width = width
        self.height = height
        self.shape = shape
        self.initUI()

    def setShape(self, shape):
        self.shape = shape

    def setColor(self, color):
        self._brush = QBrush(QColor(color))

    def setWidth(self,width):
        self.width = width

    def setHeight(self, height):
        self.height = height

    def getSize(self):
        return (self.width, self.height)

    def getObjectInfo(self):
        return (*self.map_object.getObjectInfo(), self.width, self.height)

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        path_outline = QPainterPath()
        if self.shape == 'rect':
            path_outline.addRect(0,0,self.width,self.height)
        elif self.shape == 'ell':
            path_outline.addEllipse(0,0,self.width,self.height)
        elif self.shape == 'tri':
            myPolygon = QPolygonF([
            QPoint(0.5*self.width,0), 
            QPoint(0,0.5*math.sqrt(3)*self.width),
            QPoint(self.width,0.5*math.sqrt(3)*self.width)])
            path_outline.addPolygon(myPolygon)

        painter.setPen(self._pen_defalut_color if not self.isSelected() else self._pen_selected)
        painter.setBrush(self._brush)
        painter.drawPath(path_outline.simplified())
