from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from model.graphics_view import QMapGraphicsView
from model.scene import Scene
from view.type_table_widget import TypeTableWidget
from view.object_information_widget import ObjectInfoWidget
from view.object_table_widget import ObjectTableWidget
from view.type_button_group_widget import TypeButtonGroupWidget
from view.load_background_dialog import LoadBackgroundDialog
from view.type_checkbutton_group_widget import TypeCheckbuttonGroupWidget

DEBUG = False
#main widget for map editor
class MainWidget(QWidget):
    setTempTypeNameSignal = pyqtSignal(str)
    ChangeModeSignal = pyqtSignal(str)
    ErrorInputSignal = pyqtSignal(str)
    RemoveBackgroundSignal = pyqtSignal()
    def __init__(self, mapName, parent=None):
        super().__init__(parent)
        self.mapName = mapName
        #self.stylesheet_filename = 'ass/mapstyle.qss'
        #self.loadStylesheet(self.stylesheet_filename)
        self.initUI()

    '''
    def __del__(self):
        print("finish main table work")
    '''


    def initUI(self):
        self.layout_main = QVBoxLayout()

        self.layout = QHBoxLayout()#main layout 
        self.layout_view = QVBoxLayout() #layout for view
        self.layout.setContentsMargins(0,0,0,0) 

        self.layout_info = QVBoxLayout() #layout for infomation

        self.layout_button = QVBoxLayout() #layout for button

        self.buttonGroup = TypeButtonGroupWidget()
        self.checkButtonGroup = TypeCheckbuttonGroupWidget()

        self.setLayout(self.layout_main)
        self.layout_main.addLayout(self.layout)

        self.showObjectTable_button = QPushButton('object table')
        self.showObjectTable_button.clicked.connect(self.showObjectTable)
        

        #create graphic scene
        self.scene = Scene(self.mapName)
        self.typeTable = TypeTableWidget(self.mapName)
        self.objectTable = ObjectTableWidget(self.mapName)


        #load sub widgets
        self.loadInfo()
        self.loadView()
        self.loadTypeButtonSub()
        self.loadTypeButton()
        

    def loadInfo(self):
        if DEBUG: print('MAPWIDGET: start load object information widget')
        self.objectInfo = ObjectInfoWidget()
        spacerItem = QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.layout_info.addWidget(self.objectInfo)
        self.layout_info.addItem(spacerItem)
        self.layout.addLayout(self.layout_info)
        self.layout_info.addWidget(self.showObjectTable_button)


    #load View
    def loadView(self):
        if DEBUG: print('MAPWIDGET: start load graphic')
        self.view = QMapGraphicsView(self.scene.gr_scene, self)
        self.checkButtonGroup.addButtonFromList(self.scene.getTypeNameList())
        self.pushButton = QPushButton('Import picture')
        self.pushButton.setFixedWidth(300)
        self.pushButton.clicked.connect(self.showLoadBackground)
        self.layout_view.addWidget(self.checkButtonGroup)
        self.layout_view.addWidget(self.view)
        self.layout_view.addWidget(self.pushButton)
        self.layout.addLayout(self.layout_view)


    #load button from type to button group widget
    def loadTypeButtonSub(self):
        if DEBUG: print('MAPWIDGET: start load button to sub layout')
        self.buttonGroup.addButtonFromList(self.scene.getTypeNameList())
        self.buttonGroup.ChangeModeSignal.connect(self.ChangeModeSignal)
        self.buttonGroup.SetCurrentTypeNameSignal.connect(self.setTempTypeNameSignal)

    def reloadTypeButtonSub(self):
        self.buttonGroup.addButtonFromList(self.scene.getTypeNameList())
        self.checkButtonGroup.addButtonFromList(self.scene.getTypeNameList())
        self.buttonGroup.ChangeModeSignal.connect(self.ChangeModeSignal)


    def deleteButtonGroup(self):
        for i in reversed(range(self.layout_button.count())):
            self.layout_button.itemAt(i).widget().deleteLater()
        

    #load all button
    def loadTypeButton(self):
        if DEBUG: print('MAPWIDGET: start load button to button layout')
        self.showTypeTable_button = QPushButton("+")
        self.showTypeTable_button.clicked.connect(self.showTypeTable)
        self.spacerItem = QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.layout_button.addWidget(self.buttonGroup)
        self.layout_button.addWidget(self.showTypeTable_button)
        self.layout_button.addItem(self.spacerItem)
        self.layout.addLayout(self.layout_button)


    #show the type table
    def showTypeTable(self):
        if DEBUG: print('MAPWIDGET: open type table')
        self.typeTable.show()

    def showObjectTable(self):
        if DEBUG: print('MAPWIDGET: open object table')
        self.objectTable.show()

    def showLoadBackground(self):
        loadBackgroundDialog = LoadBackgroundDialog(self.mapName, self)
        loadBackgroundDialog.LoadBackgroundSignal.connect(self.scene.importBackground)
        loadBackgroundDialog.ErrorInputSignal.connect(self.ErrorInputSignal)
        loadBackgroundDialog.RemoveBackgroundSignal.connect(self.RemoveBackgroundSignal)
        loadBackgroundDialog.show()
        loadBackgroundDialog.exec_()
        #loadBackgroundDialog.LoadBackgroundSignal.emit('img.jpg', 10)
 

    #load style sheet from qss
    def loadStylesheet(self, filename):
        if DEBUG: print('loading style', filename)
        file = QFile(filename)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))



