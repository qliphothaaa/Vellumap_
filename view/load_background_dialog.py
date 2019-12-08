from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import os.path
import re


class LoadBackgroundDialog(QDialog):
    LoadBackgroundSignal = pyqtSignal(str, float, float, float)
    ErrorInputSignal = pyqtSignal(str)
    RemoveBackgroundSignal = pyqtSignal()

    def __init__(self, mapName, parent=None):
        super(LoadBackgroundDialog, self).__init__(parent)
        self.mapName = mapName
        
        self.namelabel = QLabel('name:')
        self.xLabel = QLabel('x')
        self.yLabel = QLabel('y')
        self.emptyLabel = QLabel('')
        self.sizeLabel = QLabel('size:')

        self.backgroundNameEdit = QLineEdit('')
        self.xEdit = QLineEdit('')
        self.xEdit.setValidator(QDoubleValidator(-4, 4, 1))
        self.yEdit = QLineEdit('')
        self.yEdit.setValidator(QDoubleValidator(-4, 4, 1))
        self.sizeEdit = QLineEdit('')
        self.sizeEdit.setValidator(QDoubleValidator(0, 1000, 1))

        self.setBackgroundButton = QPushButton("set background")
        self.setBackgroundButton.clicked.connect(self.importBackground)
        self.openLocalPicButton = QPushButton("find pic from storage")
        self.openLocalPicButton.clicked.connect(self.openFile)
        self.deleteButton = QPushButton("remove background")
        self.deleteButton.clicked.connect(self.removeBackground)
        

        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.layout.addRow(self.namelabel,self.backgroundNameEdit)
        self.layout.addRow(self.emptyLabel,self.openLocalPicButton)
        self.layout.addRow(self.xLabel, self.xEdit)
        self.layout.addRow(self.yLabel, self.yEdit)
        self.layout.addRow(self.sizeLabel, self.sizeEdit)
        self.layout.addRow(self.setBackgroundButton, self.deleteButton)
        self.setEdit()


    def importBackground(self):
        self.LoadBackgroundSignal.emit(self.backgroundNameEdit.text(),float(self.xEdit.text()),float(self.yEdit.text()) ,float(self.sizeEdit.text()))

    def removeBackground(self):
        self.RemoveBackgroundSignal.emit()

    def openFile(self):
        filter = "picture (*.jpg)"
        filename, _ = QFileDialog.getOpenFileName(None, "Open File", "./pic/", filter)
        if filename:
            filename = re.split('/', filename)[-1]#get the last name on path
            self.backgroundNameEdit.setText(filename)
        self.xEdit.setText('0.0')
        self.yEdit.setText('0.0')
        self.sizeEdit.setText('1.0')


    def setEdit(self):
        if QSqlDatabase.contains('qt_sql_default_connection'):
            db = QSqlDatabase.database('qt_sql_default_connection')
            if db.databaseName() != self.mapName:
                db.close()
                db.setDatabaseName('./db/%s' % self.mapName)
                db.open()
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/%s' % self.mapName)
            db.open()

        self.model = QSqlTableModel()
        self.model.setTable('background')
        self.model.select()
        pic_name = self.model.record(0).value('name')
        x = self.model.record(0).value('x')
        y = self.model.record(0).value('y')
        size_rate = self.model.record(0).value('size_rate')
        

        self.backgroundNameEdit.setText(pic_name)
        self.xEdit.setText(str(x))
        self.yEdit.setText(str(y))
        self.sizeEdit.setText(str(size_rate))


        
