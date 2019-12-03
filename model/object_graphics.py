from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math

class QMapObjectGraphics(QGraphicsItem):
    def __init__(self, map_object, color, shape, width, height, editmode=False, parent=None):
        super().__init__(parent)
        #self._color = Qt.white
        self._pen_defalut_color = QPen(Qt.NoPen)
        self._pen_selected = QPen(Qt.black)
        self._pen_selected.setWidth(3)
        self._pen_defalut_color.setWidth(3)
        self.map_object = map_object
        self.object_id = map_object.object_id
        self.editmode = editmode

        self._brush = QBrush(QColor(color))
        self.width = width
        self.height = height
        self.shape = shape
        self.initTitle()
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

    def renewPosition(self):
        x  = self.map_object.getPosition()[0]
        y  = self.map_object.getPosition()[1]
        x = x - self.width/2
        y = y - self.height/2
        self.setPos(x, y)

    def getCentrelPos(self):
        x = self.scenePos().x() + self.width/2
        y = self.scenePos().y() + self.height/2
        return (x, y)



    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.object_id = -2
        self.title_item.setDefaultTextColor(Qt.black)
        self.title_item.setPlainText(str(self.object_id))
        title_font = QFont("", self.width/4)
        self.title_item.setFont(title_font)
        self.title_item.setTextWidth(self.width)
        self.title_item.setPos(self.width/4, self.height/3.5)
        self.title_item.adjustSize()

    def redarwTitle(self):
        title_font = QFont("", self.width/4)
        self.title_item.setFont(title_font)
        self.title_item.setTextWidth(self.width)
        self.title_item.setPos(self.width/4, self.height/3.5)
        self.title_item.adjustSize()

        
    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        if self.editmode:
            self.setFlag(QGraphicsItem.ItemIsMovable)


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        #autline
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
