from PyQt5.QtWidgets import *
from vellumap_edit_widget import MapEditorWidget
from open_map_dialog import OpenMapDialog
import sys
import re

#The main window of application
class VellumapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_open = False
        self.filename = 'None'
        self.onFileOpen()
        self.initUI()

    def __str__(self):
        return 'main Window'

    def initUI(self):
        menubar = self.menuBar()

#create menubar
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(self.createAct('Open file', 'Ctrl+O', 'Open file', self.onFileOpen))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('Export to 2D', 'Ctrl+S', 'Save map in pic', self.onFileSave2D))
        fileMenu.addAction(self.createAct('Export to 3D', 'Ctrl+Shift+S', 'Save map in obj', self.onFileSave3D))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('Exit', 'Ctrl+Q', 'Exit application', self.close))


        editMenu = menubar.addMenu('Edit')
        editMenu.addAction(self.createAct('Delete', 'Backspace', 'delete object', self.onEditDelete))



#check the database

#generate GUI
        mapEditor = MapEditorWidget(self.filename)
        self.setCentralWidget(mapEditor)
        
        self.status_mouse_pos = QLabel('')
        self.statusBar().addPermanentWidget(self.status_mouse_pos)

        mapEditor.view.scenePosChanged.connect(self.onScenePosChanged)
        mapEditor.view.currentObjectSignal.connect(mapEditor.objectInfo.setInfo)

        mapEditor.typeTable.RefreshSignal.connect(mapEditor.clearLayout)
        mapEditor.typeTable.RefreshSignal.connect(mapEditor.loadTypeButtonSub)
        
        mapEditor.view.BackSpaceSignal.connect(mapEditor.scene.removeObjectById)
        mapEditor.typeTable.DeleteSignal.connect(mapEditor.scene.removeTypeByName)
        mapEditor.typeTable.AddSignal.connect(mapEditor.scene.loadNewType)
        mapEditor.typeTable.UpdateSignal.connect(mapEditor.scene.updateType)
        mapEditor.CreateObjectSignal.connect(mapEditor.scene.createNewObject)
        mapEditor.objectInfo.changeObjectNameSignal.connect(mapEditor.scene.renameObject)
        mapEditor.objectTable.DeleteSignal.connect(mapEditor.scene.removeObjectById)

#finish generate GUI

        self.setGeometry(0,0,1200,800)
        self.setWindowTitle('Vellumap - %s'% self.filename)

        self.show()
        self.is_open = True




    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText('Scene Pos: [%d, %d]' % (x, y))

    def createAct(self, name, shortCut, tooltip, callback):
        act = QAction(name, self)
        act.setShortcut(shortCut)
        act.setToolTip(tooltip)
        act.triggered.connect(callback)
        return act

    def onFileOpen(self):
        openfileDialog = OpenMapDialog(self)
        openfileDialog.fileNameSignal.connect(self.setFilename)
        if (self.is_open):
            pass
        else:
            openfileDialog.exitSignal.connect(sys.exit)
        openfileDialog.show()
        openfileDialog.exec_()
        

    def setFilename(self, name):
        self.filename = name


    def onFileSave2D(self):
        print(self.filename)
        print('Save to picture')
        #not implement yet

    def onFileSave3D(self):
        print('save to 3D ojbect')
        #not implement yet

    def onEditDelete(self):
        self.centralWidget().view.deleteSelectedItem()
