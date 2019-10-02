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
        self.button1.clicked.connect(self.openFileDialog)
        self.button2.clicked.connect(self.createNewMap)
        self.mapNameEdit = QLineEdit('newMap')
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.layout.addRow(self.label)
        self.layout.addRow(self.mapNameEdit,self.button2)
        self.layout.addRow(self.label2)
        self.layout.addRow(self.button1)


    def openFileDialog(self):
        filter = "database (*.db)"
        filename, _ = QFileDialog.getOpenFileName(None, "Open File", "./db/", filter)
        if filename:
            #print(filename)
            filename = re.split('/', filename)[-1]#get the last name on path
            filename = filename[:-3]#delete the ".db"
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

        self.fileNameSignal.emit(filename)
        self.setNameFinished = True
        self.close()

    def closeEvent(self,event):
        if self.setNameFinished == False:
            self.exitSignal.emit()

    def createDatabase(self,filename):
        filePath = './db/%s.db' % filename
        sqlfile = open('vellumap.sql', 'r').read()
        try:
            conn = sqlite3.connect(filePath)
        except Error as e:
            print(e)
        finally:
            c = conn.cursor()
            c.executescript(sqlfile)
            conn.commit()
            conn.close()

    '''
    def questionMessage(self):
            return
    '''

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    wnd = OpenMapDialog()
    wnd.show()
    sys.exit(app.exec_())
    
