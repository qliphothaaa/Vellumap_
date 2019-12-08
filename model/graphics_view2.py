from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from model.object_graphics import QMapObjectGraphics


#class that contain the graphics
class QMapGraphicsView2(QGraphicsView):
    ScenePosSignal = pyqtSignal(int, int)
    UpdateObjectPosSignal = pyqtSignal(int, float, float)
    CreateObjectSignal = pyqtSignal(str, int, int)
    CurrentObjectSignal = pyqtSignal(int, str, str, int, int, str, float, float)#id, name, type, x, y, des, width, height
    BackSpaceSignal = pyqtSignal(int)
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.current_item = None
        self.z=0
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)


        #drawing part
        self.drawing = False
        self.drawing2 = False
        self.brushSize = 2
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

        

        self.zoomInFactor = 1.25
        self.zoomOutFactor = 1 / self.zoomInFactor
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

    def setTempTypeName(self, name):
        self.temp_type_name = name

    def setPan(self, condition):
        self.drawing2 = condition

    
    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing| QPainter.HighQualityAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setMouseTracking(True)
        #self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def mouseMoveEvent(self, event):
        self.last_scene_mouse_position = self.mapToScene(event.pos())
        self.ScenePosSignal.emit(int(self.last_scene_mouse_position.x()), int(self.last_scene_mouse_position.y()))
        if(event.buttons() & Qt.LeftButton) & (self.drawing & self.drawing2):
            painter = QPainter(self.grScene.background_graphic.scaled_pixmap)
            painter.setPen(QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.changePoint(self.lastPoint), self.changePoint(self.mapToScene(event.pos())))
            #painter.drawLine(QPoint(-250,-250), QPoint(250,250))
            self.lastPoint = self.mapToScene(event.pos())
            self.grScene.background_graphic.updateBack()
        super().mouseMoveEvent(event)


    def changeMode(self, mode_name):
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.zoomIn()
        elif event.key() == Qt.Key_Down:
            self.zoomOut()
        elif event.key() == Qt.Key_C:
            self.clear()
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = self.mapToScene(event.pos())
            
            self.leftMouseButtonPress(event)

    def mouseReleaseEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            #self.grScene.background_graphic.save('asdzxc.png' ,quality=100)
            self.leftMouseButtonRelease(event)

    def leftMouseButtonPress(self, event):
        self.current_item = self.getItemAtClicked(event)
        if isinstance(self.current_item, QMapObjectGraphics):
            self.CurrentObjectSignal.emit(*self.current_item.getObjectInfo())
            self.addToTop()
        else:
            self.CurrentObjectSignal.emit(-1,'','','','','',0.0,0.0)

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        if isinstance(self.current_item, QMapObjectGraphics):
            self.CurrentObjectSignal.emit(*self.current_item.getObjectInfo())
        else:
            self.CurrentObjectSignal.emit(-1,'','','','','',0.0,0.0)
        super().mouseReleaseEvent(event)

    def getItemAtClicked(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        if obj and isinstance(obj.parentItem(), QMapObjectGraphics):
            obj = obj.parentItem()
        return obj

    def clear(self):
        self.grScene.background_graphic.resetBack()

    def changePoint(self,point):
        size = self.grScene.background_graphic.size
        width = size.width()
        height = size.width()
        x = point.x()
        y = point.y()

        if x >(width/2):
            x = width
        elif x <(-width/2):
            x = 0
        else:
            x = x +width/2
        
        if y >(height/2):
            y = height
        elif y <(-height/2):
            y = 0
        else:
            y = y + height/2
        return QPoint(x,y)



    def addToTop(self):
        if isinstance(self.current_item,QGraphicsItem):
            self.current_item.setZValue(self.z+0.01)
            self.z += 0.01

    def zoomIn(self):
        self.zoomFactor = self.zoomInFactor
        self.zoom += self.zoomStep
        self.zoomInOut()

    def zoomOut(self):
        self.zoomFactor = self.zoomOutFactor
        self.zoom -= self.zoomStep
        self.zoomInOut()


    def zoomInOut(self):
        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom = self.zoomRange[0]
            clamped = True
        if self.zoom > self.zoomRange[1]:
            self.zoom = self.zoomRange[1]
            clamped = True

        if (self.zoomFactor == 1):
            pass
        else:
            if not (clamped or self.zoomClamp is False):
                self.scale(self.zoomFactor, self.zoomFactor)

    def focusOn(self,object_id):
        width = -1
        height = -1
        for item in self.grScene.items():
            if isinstance(item, QMapObjectGraphics) and item.object_id == object_id:
                width, height = item.getSize()
                x, y = item.pos().x(), item.pos().y()
                item.setSelected(True)
                self.CurrentObjectSignal.emit(*item.getObjectInfo())
            else:
                item.setSelected(False)
        if (width>0 and height > 0):
            self.centerOn(x+width/2, y+height/2)

    def fliter(self, type_name):
        for item in self.grScene.items():
            if isinstance(item, QMapObjectGraphics) and item.map_object.object_type_name == type_name:
                item.show()

    def showAll(self):
        for item in self.grScene.items():
            item.show()

    def hideAll(self):
        for item in self.grScene.items():
            if isinstance(item, QMapObjectGraphics):
                item.hide()





