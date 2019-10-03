from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re


class ObjectMapInfoWidget(QWidget):
    changeObjectNameSignal = pyqtSignal(int,str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_id = 0
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
        #self.layout = QVBoxLayout()
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.idLabel = QLabel('Id:')
        self.nameLabel = QLabel('Name:')
        self.typeNameLabel = QLabel('type:')
        self.widthLabel = QLabel('Width:')
        self.heightLabel = QLabel('Height:')
        self.xLabel = QLabel('X:')
        self.yLabel = QLabel('Y:')
        self.renameLabel = QLabel('new name:')
        #self.sizeLabel = QLabel('Size:')

        self.object_id = QLabel('')
        self.object_name = QLabel('')
        self.object_type = QLabel('')
        self.object_width = QLabel('')
        self.object_height = QLabel('')
        self.object_x = QLabel('')
        self.object_y = QLabel('')
        self.object_size = QLabel('')

        self.nameLineEdit = QLineEdit()

        self.renameButton = QPushButton(' rename ')
        self.renameButton.clicked.connect(self.updateName)

        self.layout.addRow(self.idLabel, self.object_id)
        self.layout.addRow(self.nameLabel, self.object_name)
        self.layout.addRow(self.typeNameLabel, self.object_type)
        self.layout.addRow(self.widthLabel, self.object_width)
        self.layout.addRow(self.heightLabel, self.object_height)
        self.layout.addRow(self.xLabel, self.object_x)
        self.layout.addRow(self.yLabel, self.object_y)
        #self.layout.addRow(self.sizeLabel, self.object_size)
        #self.layout.addLayout(self.layout_sub)
        self.layout.addRow(self.renameLabel, self.nameLineEdit)
        self.layout.addRow(self.renameButton)

    def setInfo(self,id, name, typeName, width, height, x, y, size):

        typeName = re.sub('^type', '', typeName)
        self.object_id.setText(str(id))
        self.object_name.setText(name)
        self.object_type.setText(typeName)
        self.object_width.setText(width)
        self.object_height.setText(height)
        self.object_x.setText(str(x))
        self.object_y.setText(str(y))
        self.current_id = id
        #self.object_size.setText(str(size))

    def updateName(self):
        #id = int(self.idLabel.text().rsplit(':')[1])
        target_id = int(self.object_id.text())
        newName =  self.nameLineEdit.text()
        if target_id is not ' ' and newName is not '':
            self.changeObjectNameSignal.emit(target_id,newName)
            self.nameLineEdit.clear()
            

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindwo = ObjectMapInfoWidget()
    mainWindwo.show()
    sys.exit(app.exec_())
