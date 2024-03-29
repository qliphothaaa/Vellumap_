from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
import os.path
import re

class OpenMapDialog(QDialog):
    fileNameSignal = pyqtSignal(str)
    exitSignal = pyqtSignal()
    def __init__(self, parent=None):
        super(OpenMapDialog, self).__init__(parent)
        self.setNameFinished = False
        self.setGeometry(600,400,300,150)
        self.setWindowTitle('open file')
        
        self.label = QLabel("please input new map's name")
        self.label2 = QLabel('Or find an existing map')
        self.button1 = QPushButton("Open Existing Map")
        self.button2 = QPushButton("Create New Map")
        self.button3 = QPushButton("Open Map in View mode")
        self.button1.clicked.connect(self.openEditMode)
        self.button2.clicked.connect(self.createNewMap)
        self.button3.clicked.connect(self.openViewMode)
        self.mapNameEdit = QLineEdit('iseki')
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.layout.addRow(self.label)
        self.layout.addRow(self.mapNameEdit,self.button2)
        self.layout.addRow(self.label2)
        self.layout.addRow(self.button1)
        self.layout.addRow(self.button3)


    def openEditMode(self):
        filter = "database (*.db)"
        filename, _ = QFileDialog.getOpenFileName(None, "Open File", "./db/", filter)
        if filename:
            filename = re.split('/', filename)[-1]#get the last name on path
            #filename = filename[:-3]#delete the ".db"
            #filename = re.split('\.', filename)[-2]
            self.fileNameSignal.emit(filename)
            self.setNameFinished = True
            self.close()


    def openViewMode(self):
        filter = "JSON (*.json)"
        filename, _ = QFileDialog.getOpenFileName(None, "Open File", "./json/", filter)
        if filename:
            filename = re.split('/', filename)[-1]#get the last name on path
            #filename = filename[:-5]#delete the ".db"
            #filename = re.split('\.', filename)[-2]
            self.fileNameSignal.emit(filename)
            self.setNameFinished = True
            self.close()


    def createNewMap(self):
        filename = self.mapNameEdit.text()
        if filename == '':
            message = QMessageBox.warning(self, 'warning', 'The name could not be blank', QMessageBox.Yes, QMessageBox.Yes)
            return
        if '/' in filename:
            message = QMessageBox.warning(self, 'warning', 'contain illegal character', QMessageBox.Yes, QMessageBox.Yes)
            return
        filepath = './db/%s.db' % filename
        if os.path.isfile(filepath):
            message = QMessageBox.question(self, 'question message', 'file exists, load file?', QMessageBox.Yes, QMessageBox.No)
            if message == QMessageBox.No:
                return
        else:
            self.createDatabase(filename)

        self.fileNameSignal.emit(filename+'.db')
        self.setNameFinished = True
        self.close()

    def closeEvent(self,event):
        if self.setNameFinished == False:
            self.exitSignal.emit()

    def createDatabase(self,filename):
        filePath = './db/%s.db' % filename
        sqlfile = open('view/vellumap.sql', 'r').read()
        try:
            conn = sqlite3.connect(filePath)
            c = conn.cursor()
            c.executescript(sqlfile)
        except Error as e:
            print(e)
        finally:
            conn.commit()
            conn.close()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    wnd = OpenMapDialog()
    wnd.show()
    sys.exit(app.exec_())
    
