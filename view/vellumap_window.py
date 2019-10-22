from PyQt5.QtWidgets import *
from view.main_widget import MainWidget
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


    def initUI(self):
        #create menubar
        Menubar = self.menuBar()

        #add action to menuBar
        fileMenu = Menubar.addMenu('File')
        fileMenu.addAction(self.createAct('Open file', 'Ctrl+O', 'Open file', self.onFileOpen))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('Export to 2D', 'Ctrl+S', 'Save map in pic', self.onFileSave2D))
        fileMenu.addAction(self.createAct('Export to 3D', 'Ctrl+Shift+S', 'Save map in obj', self.onFileSave3D))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('Exit', 'Ctrl+Q', 'Exit application', self.close))
        editMenu = Menubar.addMenu('Edit')
        editMenu.addAction(self.createAct('Delete', 'Backspace', 'delete object', self.onEditDelete))



#check the database

#generate GUI
        mainEditor = MainWidget(self.filename)
        self.setCentralWidget(mainEditor)
        
        self.status_mouse_pos = QLabel('')
        self.statusBar().addPermanentWidget(self.status_mouse_pos)

        #connect signal with function

        #signal in view widget
        mainEditor.view.ScenePosSignal.connect(self.onScenePosChanged)
        mainEditor.view.CurrentObjectSignal.connect(mainEditor.objectInfo.setInfo)
        mainEditor.view.BackSpaceSignal.connect(mainEditor.scene.removeObject)
        mainEditor.view.BackSpaceSignal.connect(mainEditor.objectTable.searchButtonClicked)
        mainEditor.view.CreateObjectSignal.connect(mainEditor.scene.createNewObject)
        mainEditor.view.UpdateObjectPosSignal.connect(mainEditor.scene.updatePosition)

        #signal in type table widget
        mainEditor.typeTable.RefreshSignal.connect(mainEditor.buttonGroup.clearButtons)
        mainEditor.typeTable.RefreshSignal.connect(mainEditor.checkButtonGroup.clearButtons)
        mainEditor.typeTable.RefreshSignal.connect(mainEditor.reloadTypeButtonSub)

        #c
        mainEditor.typeTable.DeleteSignal.connect(mainEditor.scene.removeType)
        mainEditor.typeTable.AddSignal.connect(mainEditor.scene.createNewType)
        mainEditor.typeTable.UpdateSignal.connect(mainEditor.scene.updateType)
        #c
        mainEditor.typeTable.ResetModeSignal.connect(mainEditor.buttonGroup.resetRecent)

        #signal in checkbutton group
        mainEditor.checkButtonGroup.FilterSignal.connect(mainEditor.scene.filterGraphicsByType)
        mainEditor.checkButtonGroup.ShowAllSignal.connect(mainEditor.view.showAll)
        mainEditor.checkButtonGroup.HideAllSignal.connect(mainEditor.view.hideAll)

        #signal in object table widget
        mainEditor.objectTable.DeleteSignal.connect(mainEditor.scene.removeObject)
        mainEditor.objectTable.FocusSignal.connect(mainEditor.view.focusOn)

        #signal in object information widget
        mainEditor.objectInfo.ChangeObjectNameSignal.connect(mainEditor.scene.renameObject)
        mainEditor.objectInfo.ChangeObjectDescriptionSignal.connect(mainEditor.scene.changeDescription)

        #signal in main widget
        mainEditor.setTempTypeNameSignal.connect(mainEditor.view.setTempTypeName)
        mainEditor.ChangeModeSignal.connect(mainEditor.view.changeMode)
        

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
