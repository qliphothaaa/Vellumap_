from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from model.map_graphics_view import QMapGraphicsView
from model.new_map_scene import Scene


class MainWidget(QWidget):
    def __init__(self, mapName, parent=None):
        super().__init__(parent)
        self.mapName = mapName
        #self.stylesheet_filename = 'ass/mapstyle.qss'
        #self.loadStylesheet(self.stylesheet_filename)
        self.initUI()


    def initUI(self):
        self.layout_main = QVBoxLayout()

        self.layout = QHBoxLayout()#main layout 
        self.layout_view = QVBoxLayout() #layout for view
        self.layout.setContentsMargins(0,0,0,0) 

        self.setLayout(self.layout_main)
        self.layout_main.addLayout(self.layout)

        self.scene = Scene(self.mapName)
        self.view = QMapGraphicsView(self.scene.gr_scene, self)

        self.layout_view.addWidget(self.view)
        self.layout.addLayout(self.layout_view)
