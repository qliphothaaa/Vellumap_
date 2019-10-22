from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from model.new_map_object_graphics import QMapObjectGraphics

DEBUG = True

#class that contain the graphics
class QMapGraphicsView(QGraphicsView):
    ScenePosSignal = pyqtSignal(int, int)
    UpdateObjectPosSignal = pyqtSignal(int, int, int)
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

        self.mode = 'select'
        self.temp_type_name = ''

        self.zoomInFactor = 1.25
        self.zoomOutFactor = 1 / self.zoomInFactor
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

    def setTempTypeName(self, name):
        self.temp_type_name = name

    
    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing| QPainter.HighQualityAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setMouseTracking(True)
        #self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        #self.setDragMode(QGraphicsView.NoDrag)

    def mouseMoveEvent(self, event):
        self.last_scene_mouse_position = self.mapToScene(event.pos())
        self.ScenePosSignal.emit(int(self.last_scene_mouse_position.x()), int(self.last_scene_mouse_position.y()))
        super().mouseMoveEvent(event)

    def changeMode(self, mode_name):
        self.mode = mode_name

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.zoomIn()
        elif event.key() == Qt.Key_Down:
            self.zoomOut()
        elif event.key() == Qt.Key_S:
            self.showAll()
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
            if isinstance(self.current_item, QMapObjectGraphics):
                self.CurrentObjectSignal.emit(*self.current_item.getObjectInfo())
                
                self.addToTop()
            else:
                self.CurrentObjectSignal.emit(-1,'','','','','',0.0,0.0)
                pass
        elif (self.mode == 'create'):
            self.CreateObjectSignal.emit(self.temp_type_name, int(self.mapToScene(event.pos()).x()), int(self.mapToScene(event.pos()).y()))

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        if (self.mode == 'select'):
            for item in self.grScene.selectedItems():
                if isinstance(item, QMapObjectGraphics):
                    #item.map_object.renewPosition()
                    #item.map_object.updatePositionToDatabase(*item.map_object.getPosition())
                    self.UpdateObjectPosSignal.emit(item.object_id, item.scenePos().x(), item.scenePos().y())
            if isinstance(self.current_item, QMapObjectGraphics):
                self.CurrentObjectSignal.emit(*self.current_item.getObjectInfo())
                pass
            else:
                self.CurrentObjectSignal.emit(-1,'','','','','',0.0,0.0)
                pass
        super().mouseReleaseEvent(event)

    def getItemAtClicked(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def deleteSelectedItem(self):
        for item in self.grScene.selectedItems():
            if isinstance(item, QMapObjectGraphics):
                self.BackSpaceSignal.emit(item.object_id)


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

    def focusOn(self,object_id, x, y):
        width = -1
        height = -1
        for item in self.grScene.items():
            if item.object_id == object_id:
                width, height = item.getSize()
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
            item.hide()
            if item.object_id == -1:
                item.show()





