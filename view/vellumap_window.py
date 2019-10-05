from PyQt5.QtWidgets import *
from view.vellumap_edit_widget import MapEditorWidget
from view.open_map_dialog import OpenMapDialog
import sys
import re

#The main window of application
class VellumapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_open = False
        self.filename = 'None'
        self.onFileOpen()
        #self.initUI()

    def __str__(self):
        return 'main Window'

    def initUI(self):
        #create menubar
        menubar = self.menuBar()

        #add action to menuBar
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

        #connect signal with function

        #signal in view widget
        mapEditor.view.scenePosChanged.connect(self.onScenePosChanged)
        mapEditor.view.currentObjectSignal.connect(mapEditor.objectInfo.setInfo)
        mapEditor.view.BackSpaceSignal.connect(mapEditor.scene.removeObjectById)
        mapEditor.view.BackSpaceSignal.connect(mapEditor.objectTable.searchButtonClicked)
        mapEditor.view.CreateObjectSignal.connect(mapEditor.scene.createNewObject)

        #signal in type table widget
        mapEditor.typeTable.RefreshSignal.connect(mapEditor.clearLayout)
        mapEditor.typeTable.RefreshSignal.connect(mapEditor.loadTypeButtonSub)
        mapEditor.typeTable.DeleteSignal.connect(mapEditor.scene.removeTypeByName)
        mapEditor.typeTable.AddSignal.connect(mapEditor.scene.loadNewType)
        mapEditor.typeTable.UpdateSignal.connect(mapEditor.scene.updateType)

        #signal in object table widget
        mapEditor.objectTable.DeleteSignal.connect(mapEditor.scene.removeObjectById)
        mapEditor.objectTable.FocusSignal.connect(mapEditor.view.focusOn)

        #signal in object information widget
        mapEditor.objectInfo.ChangeObjectNameSignal.connect(mapEditor.scene.renameObject)
        mapEditor.objectInfo.ChangeObjectDescriptionSignal.connect(mapEditor.scene.changeDescriptionObject)

        #signal in  main widget
        mapEditor.setTempTypeNameSignal.connect(mapEditor.scene.setTempTypeName)
        mapEditor.ChangeModeSignal.connect(mapEditor.view.changeMode)
        #mapEditor.view.DrawCrossSignal.connect(mapEditor.scene.drawCross)
        

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
        old_name = self.filename
        if (self.is_open):
            pass
        else:
            openfileDialog.exitSignal.connect(sys.exit)
        openfileDialog.show()
        openfileDialog.exec_()
        if(old_name != self.filename):
            self.initUI()
        
        

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
