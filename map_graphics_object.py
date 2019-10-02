from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math
DEBUG =True
#Graphics object of map object
class QMapGraphicsObject(QGraphicsItem):
    def __init__(self, mapObject, colorDefault, shape, width, height, parent=None):
        super().__init__(parent)
        self._color = Qt.white
        self.mapObject = mapObject
        self._pen_defalut_color = Qt.black
        self._pen_selected = Qt.red

        self._brush = QBrush(QColor(colorDefault))
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

    def initTitle(self):
        pass

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
    

    

    
        
        
