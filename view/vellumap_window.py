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
        #Menubar = self.menuBar()

        #add action to menuBar
        self.initMenu()

        #generate GUI
        self.mainEditor = MainWidget(self.filename)
        self.setCentralWidget(self.mainEditor)
        self.status_mouse_pos = QLabel('')
        self.statusBar().addPermanentWidget(self.status_mouse_pos)

        #connect signal with function

        #signal in view widget
        self.mainEditor.view.ScenePosSignal.connect(self.onScenePosChanged)
        self.mainEditor.view.CurrentObjectSignal.connect(self.mainEditor.objectInfo.setInfo)
        self.mainEditor.view.BackSpaceSignal.connect(self.mainEditor.scene.removeObject)
        self.mainEditor.view.BackSpaceSignal.connect(self.mainEditor.objectTable.searchButtonClicked)
        self.mainEditor.view.CreateObjectSignal.connect(self.mainEditor.scene.createNewObject)
        self.mainEditor.view.UpdateObjectPosSignal.connect(self.mainEditor.scene.updatePosition)

        #signal in type table widget
        self.mainEditor.typeTable.RefreshSignal.connect(self.mainEditor.buttonGroup.clearButtons)
        self.mainEditor.typeTable.RefreshSignal.connect(self.mainEditor.checkButtonGroup.clearButtons)
        self.mainEditor.typeTable.RefreshSignal.connect(self.mainEditor.reloadTypeButtonSub)

        #c
        self.mainEditor.typeTable.DeleteSignal.connect(self.mainEditor.scene.removeType)
        self.mainEditor.typeTable.AddSignal.connect(self.mainEditor.scene.createNewType)
        self.mainEditor.typeTable.UpdateSignal.connect(self.mainEditor.scene.updateType)
        #c
        self.mainEditor.typeTable.ResetModeSignal.connect(self.mainEditor.buttonGroup.resetRecent)

        #signal in checkbutton group
        self.mainEditor.checkButtonGroup.FilterSignal.connect(self.mainEditor.scene.filterGraphicsByType)
        self.mainEditor.checkButtonGroup.ShowAllSignal.connect(self.mainEditor.view.showAll)
        self.mainEditor.checkButtonGroup.HideAllSignal.connect(self.mainEditor.view.hideAll)

        #signal in object table widget
        self.mainEditor.objectTable.DeleteSignal.connect(self.mainEditor.scene.removeObject)
        self.mainEditor.objectTable.FocusSignal.connect(self.mainEditor.view.focusOn)

        #signal in object information widget
        self.mainEditor.objectInfo.ChangeObjectNameSignal.connect(self.mainEditor.scene.renameObject)
        self.mainEditor.objectInfo.ChangeObjectDescriptionSignal.connect(self.mainEditor.scene.changeDescription)

        #signal in main widget
        self.mainEditor.setTempTypeNameSignal.connect(self.mainEditor.view.setTempTypeName)
        self.mainEditor.ChangeModeSignal.connect(self.mainEditor.view.changeMode)
        self.mainEditor.ErrorInputSignal.connect(self.openErrorDialog)
        self.mainEditor.RemoveBackgroundSignal.connect(self.mainEditor.scene.removeBackground)
        

        #finish generate GUI
        self.setGeometry(0,0,1200,800)
        self.setWindowTitle('Vellumap - %s'% self.filename)
        self.show()
        self.is_open = True

    def setFilename(self, name):
        self.filename = name

    def initMenu(self):
        fileMenu = self.menuBar().addMenu('File')
        fileMenu.addAction(self.createAct('Open file', 'Ctrl+O', 'Open file', self.onFileOpen))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('Export to 2D', 'Ctrl+S', 'Save map in pic', self.onFileSave2D))
        fileMenu.addAction(self.createAct('About', 'Ctrl+A', 'about', self.about))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('Exit', 'Ctrl+Q', 'Exit application', self.close))
        editMenu = self.menuBar().addMenu('Edit')
        editMenu.addAction(self.createAct('Delete', 'Backspace', 'delete object', self.onEditDelete))


    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText('Scene Pos: [%d, %d]' % (x, y))


    def createAct(self, name, shortCut, tooltip, callback):
        act = QAction(name, self)
        act.setShortcut(shortCut)
        act.setToolTip(tooltip)
        act.triggered.connect(callback)
        return act

    '''
    def disconntect(self):
        self.mainEditor.typeTable.DeleteSignal.disconnect(self.mainEditor.scene.removeType)
    '''

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



    def onFileSave2D(self):
        print(self.filename)
        print('Save to picture')
        #not implement yet

    def onEditDelete(self):
        pass
        #self.centralWidget().view.deleteSelectedItem()

    def about(self):
        QMessageBox.about(self, "About Vellumap", "The vellumap is a desktop application for making map using Qt")

    def openErrorDialog(self, message):
            message = QMessageBox.warning(self, 'warning message', message, QMessageBox.Yes)


