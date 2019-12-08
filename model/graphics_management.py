from model.object_graphics import QMapObjectGraphics
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QBrush, QImageReader, QColor, QPainterPath, QPolygonF
from PyQt5.QtCore import Qt, QPoint, QRectF
import math

class GraphicsManagement():
    def __init__(self):
        self.graphics = {}
        self.background = None


    def generateGraphics(self, map_object, color, shape, width, height, mode=True):
        grMapObject = QMapObjectGraphics(map_object, color, shape, width, height, mode)
        x =  map_object.getPosition()[0]
        y =  map_object.getPosition()[1]
        x = x - width/2
        y = y - height/2
        grMapObject.setPos(x, y)
        self.graphics[map_object.object_id] = grMapObject

    def getGraphics(self, object_id):
        try:
            return self.graphics[object_id]
        except(KeyError):
            return None

    def printGra(self):
        num = 1
        for i in self.graphics.values():
            print(num, end=' ')
            print(i)
            num += 1
        print(num, end=' ')
        print(self.background)

    def removeGraphics(self, object_id):
        if not object_id in self.graphics:
            raise KeyError('cannot find the graphic')
        del self.graphics[object_id]


    def updateGraphics(self, object_id, color, shape, width, height):
        if not object_id in self.graphics:
            raise KeyError('cannot find the graphic')
        target_graphic = self.getGraphics(object_id)
        target_graphic.setColor(color)
        target_graphic.setShape(shape)
        target_graphic.setWidth(width)
        target_graphic.setHeight(height)
        target_graphic.renewPosition()
        target_graphic.redarwTitle()

    def hideGraphics(self, object_id_set):
        if not isinstance(object_id_set, set):
            raise ValueError('input should be set')
        for object_id in object_id_set:
            if not object_id in self.graphics:
                raise KeyError('cannot find the graphic')
            self.graphics[object_id].hide()
            self.graphics[object_id].show_bool = False

    def showGraphics(self, object_id_set):
        if not isinstance(object_id_set, set):
            raise ValueError('input should be set')
        for object_id in object_id_set:
            if not object_id in self.graphics:
                raise KeyError('cannot find the graphic')
            self.graphics[object_id].show()
            self.graphics[object_id].show_bool = True

    def clear(self):
        self.graphics.clear()

    def saveToPic(self, map_name):
        #get background picture
        self.back_img = self.background.generatePixmap().toImage()

        #get the size of picture
        width = self.background.size.width()
        height = self.background.size.height()

        #draw objects
        painter = QPainter(self.back_img)
        painter.setPen(QPen(Qt.black))

        for i in self.graphics.values():
            if i.show_bool:
                center = (width/2 + i.map_object.x - i.width/2, height/2 + i.map_object.y - i.height/2)
                path_outline = QPainterPath()

                if i.shape == 'rect':
                    path_outline.addRect(*center, i.width, i.height)
                elif i.shape == 'ell':
                    path_outline.addEllipse(*center, i.width, i.height)
                elif i.shape == 'tri':
                    myPolygon = QPolygonF([
                    QPoint(center[0]+i.width/2, center[1]), 
                    QPoint(center[0], center[1]+i.height),
                    QPoint(center[0]+i.width, center[1]+i.height)])

                    path_outline.addPolygon(myPolygon)

                painter.setBrush(i.brush)
                painter.drawPath(path_outline.simplified())

        #draw text
        for i in self.graphics.values():
            if i.show_bool:
                #center = (width/2 + i.map_object.x, height/2 + i.map_object.y)
                center = (width/2 + i.map_object.x - i.width/2, height/2 + i.map_object.y - i.height/2)
                rect = QRectF(*center, i.width, i.height)
                painter.setFont(i.title_font)
                painter.drawText(rect,Qt.AlignCenter, str(i.object_id))

        
        #save to jpg
        self.back_img.save('./export/map-%s.jpg'% map_name,quality=100)

    
    
