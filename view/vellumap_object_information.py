from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ObjectMapInfoWidget(QWidget):
    changeObjectNameSignal = pyqtSignal(int,str)
    def __init__(self, parent=None):
        super().__init__(parent)
        '''
        self.name = ''
        self.typeName = ''
        self.width = ''
        self.height = ''
        self.x = ''
        self.y = ''
        self.size = ''
        '''
        self.initUI()

    def initUI(self):
        self.setFixedSize(200,250)
        self.layout_sub = QHBoxLayout()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.idLabel = QLabel(' Id: ')
        self.nameLabel = QLabel(' Name: ')
        self.typeNameLabel = QLabel(' type: ')
        self.widthLabel = QLabel(' Width: ')
        self.heightLabel = QLabel(' Height: ')
        self.xLabel = QLabel(' X: ')
        self.yLabel = QLabel(' Y: ')
        self.sizeLabel = QLabel(' Size: ')

        self.nameLineEdit = QLineEdit()

        self.renameButton = QPushButton(' rename ')
        self.renameButton.clicked.connect(self.updateName)

        self.layout.addWidget(self.idLabel)
        self.layout.addWidget(self.nameLabel)
        self.layout.addWidget(self.typeNameLabel)
        self.layout.addWidget(self.widthLabel)
        self.layout.addWidget(self.heightLabel)
        self.layout.addWidget(self.xLabel)
        self.layout.addWidget(self.yLabel)
        self.layout.addWidget(self.sizeLabel)
        self.layout.addLayout(self.layout_sub)
        self.layout_sub.addWidget(self.nameLineEdit)
        self.layout_sub.addWidget(self.renameButton)

    def setInfo(self,id, name, typeName, width, height, x, y, size):
        self.idLabel.setText('Id:'+str(id))
        self.nameLabel.setText('Name:'+ name)
        self.typeNameLabel.setText('type:'+typeName)
        self.widthLabel.setText('width:'+width)
        self.heightLabel.setText('height:'+height)
        self.xLabel.setText('x:'+str(x))
        self.yLabel.setText('y:'+str(y))
        self.sizeLabel.setText('size:'+str(size))

    def updateName(self):
        id = int(self.idLabel.text().rsplit(':')[1])
        newName =  self.nameLineEdit.text()
        if id is not ' ' and newName is not '':
            self.changeObjectNameSignal.emit(id,newName)
            self.nameLineEdit.clear()
        


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindwo = ObjectMapInfoWidget()
    mainWindwo.show()
    sys.exit(app.exec_())
