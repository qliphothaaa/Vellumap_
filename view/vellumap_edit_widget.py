from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from model.map_graphics_view import QMapGraphicsView
from model.map_scene import Scene
from model.map_object_type import ObjectType
from model.map_object import MapObject
from view.TypeButton import QTypePushButton
from view.vellumap_type_viewer_widget import MapTypeViewerWidget
from view.vellumap_object_information_widget import ObjectMapInfoWidget
from view.vellumap_object_viewer_widget import MapObjectViewerWidget

DEBUG = False
#main widget for map editor
class MapEditorWidget(QWidget):
    CreateObjectSignal = pyqtSignal(str)
    def __init__(self, mapName, parent=None):
        super().__init__(parent)
        self.mapName = mapName
        #self.stylesheet_filename = 'ass/mapstyle.qss'
        #self.loadStylesheet(self.stylesheet_filename)
        self.initUI()

    def __str__(self):
        return 'MapEditor'

    def initUI(self):
        self.layout_main = QVBoxLayout()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout_info = QVBoxLayout()

        self.layout_button = QVBoxLayout()
        self.layout_button_sub = QVBoxLayout()

        self.setLayout(self.layout_main)
        self.layout_main.addLayout(self.layout)

        self.showObjectTable_button = QPushButton('object table')
        self.showObjectTable_button.clicked.connect(self.showObjectTable)
        

        #create graphic scene
        self.scene = Scene(self.mapName)
        self.gr_scene = self.scene.gr_scene
        self.typeTable = MapTypeViewerWidget(self.mapName)
        self.objectTable = MapObjectViewerWidget(self.mapName)


        #load sub widgets
        self.loadInfo()
        self.loadView()
        self.loadTypeButtonSub()
        self.loadTypeButton()

    #clear all button from bottom group
    def clearLayout(self):
        for i in reversed(range(self.layout_button_sub.count())):
            self.layout_button_sub.itemAt(i).widget().deleteLater()

    #load button from type to sub layout
    def loadTypeButtonSub(self):
        if DEBUG: print('MAPWIDGET: start load button to sub layout')
        for objectType in self.scene.object_types:
            button = QTypePushButton(objectType, self)
            button.TypeNameSignal.connect(self.CreateObjectSignal)
            self.layout_button_sub.addWidget(button)

    #load all button
    def loadTypeButton(self):
        if DEBUG: print('MAPWIDGET: start load button to button layout')
        self.showTypeTable_button = QPushButton("+")
        self.showTypeTable_button.clicked.connect(self.showTypeTable)
        spacerItem = QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.Expanding)

        self.layout_button.addLayout(self.layout_button_sub)
        self.layout_button.addWidget(self.showTypeTable_button)
        self.layout_button.addItem(spacerItem)

        self.layout.addLayout(self.layout_button)

    
    #load View
    def loadView(self):
        if DEBUG: print('MAPWIDGET: start load graphic')
        self.view = QMapGraphicsView(self.scene.gr_scene, self)
        self.layout.addWidget(self.view)

    def loadInfo(self):
        if DEBUG: print('MAPWIDGET: start load object information widget')
        self.objectInfo = ObjectMapInfoWidget()
        spacerItem = QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.layout_info.addWidget(self.objectInfo)
        self.layout_info.addItem(spacerItem)
        self.layout.addLayout(self.layout_info)
        self.layout_info.addWidget(self.showObjectTable_button)


    #show the type table
    def showTypeTable(self):
        if DEBUG: print('MAPWIDGET: open type table')
        self.typeTable.show()

    def showObjectTable(self):
        if DEBUG: print('MAPWIDGET: open object table')
        self.objectTable.show()


    #load style sheet from qss
    def loadStylesheet(self, filename):
        if DEBUG: print('loading style', filename)
        file = QFile(filename)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))


