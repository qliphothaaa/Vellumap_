from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from model.map_graphics_object import QMapGraphicsObject

DEBUG = True

#class that contain the graphics
class QMapGraphicsView(QGraphicsView):
    scenePosChanged = pyqtSignal(int, int)
    UpdateObjectPos = pyqtSignal(int, int)
    CreateObjectSignal = pyqtSignal(int, int)
    currentObjectSignal = pyqtSignal(int, str, str, str, str, int, int, int, str)
    BackSpaceSignal = pyqtSignal(int)
    #DrawCrossSignal = pyqtSignal(int, int)
    

    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.current_item = None
        self.z=0
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)

        self.mode = 'select'

        self.zoomInFactor = 1.25
        self.zoomOutFactor = 1 / self.zoomInFactor
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

    
    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing| QPainter.HighQualityAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def mouseMoveEvent(self, event):
        self.last_scene_mouse_position = self.mapToScene(event.pos())
        self.scenePosChanged.emit(int(self.last_scene_mouse_position.x()), int(self.last_scene_mouse_position.y()))
        super().mouseMoveEvent(event)

    def changeMode(self, mode_name):
        self.mode = mode_name
        if (mode_name == "create"):
            self.setDragMode(QGraphicsView.NoDrag)
        else:
            self.setDragMode(QGraphicsView.RubberBandDrag)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.zoomIn()
        elif event.key() == Qt.Key_Down:
            self.zoomOut()
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)

    def mouseReleaseEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)

    def leftMouseButtonPress(self, event):
        if (self.mode == 'select'):
            self.current_item = self.getItemAtClicked(event)
            if isinstance(self.current_item, QMapGraphicsObject):
                self.currentObjectSignal.emit(*self.current_item.map_object.getMapInfo())
                self.addToTop()
            else:
                self.currentObjectSignal.emit(-1,'','','','','','','','')
        elif (self.mode == 'create'):
            self.CreateObjectSignal.emit(int(self.mapToScene(event.pos()).x()), int(self.mapToScene(event.pos()).y()))

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        if (self.mode == 'select'):
            if isinstance(self.current_item, QMapGraphicsObject):
                self.currentObjectSignal.emit(*self.current_item.map_object.getMapInfo())
            else:
                self.currentObjectSignal.emit(-1,'','','','','','','','')
            for item in self.grScene.selectedItems():
                if isinstance(item, QMapGraphicsObject):
                    item.map_object.updatePosition(*item.map_object.getPosition())
                    


        super().mouseReleaseEvent(event)

    def getItemAtClicked(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def deleteSelectedItem(self):
        for item in self.grScene.selectedItems():
            if isinstance(item, QMapGraphicsObject):
                self.BackSpaceSignal.emit(item.map_object.getId())


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

    def focusOn(self, x, y):
        self.centerOn(x, y)
        #self.current_item = self.itemAt(x+20, y+20)
        #self.currentObjectSignal.emit(*self.current_item.map_object.getMapInfo())




