from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re


class ObjectMapInfoWidget(QWidget):
    changeObjectNameSignal = pyqtSignal(int,str)
    changeObjectDescriptionSignal = pyqtSignal(int, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.current_id = 0
        self.initUI()

    def initUI(self):
        self.setFixedSize(200,500)
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
        self.renameButton.clicked.connect(self.changeName)
        self.descriptionEdit = QTextEdit()
        self.descriptionEdit.setFixedHeight(200)
        self.changeDescriptionButton = QPushButton(' change Description ')
        self.changeDescriptionButton.clicked.connect(self.changeDescription)
        spacerItem = QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.Expanding)
        

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
        self.layout.addRow(self.descriptionEdit)
        self.layout.addRow(self.changeDescriptionButton)
        self.layout.addItem(spacerItem)
        

    def setInfo(self,id, name, type_name, width, height, x, y, size):
        if (id+1):
            type_name = re.sub('^type', '', type_name)
            self.object_id.setText(str(id))
            self.object_name.setText(name)
            self.object_type.setText(type_name)
            self.object_width.setText(width)
            self.object_height.setText(height)
            self.object_x.setText(str(x))
            self.object_y.setText(str(y))
            #self.current_id = id
            #self.object_size.setText(str(size))
        else:
            self.clearInfo()

    def clearInfo(self):
        self.object_id.setText('')
        self.object_name.setText('')
        self.object_type.setText('')
        self.object_width.setText('')
        self.object_height.setText('')
        self.object_x.setText('')
        self.object_y.setText('')
        #self.current_id = -1


    def changeName(self):
        newName =  self.nameLineEdit.text()
        if (self.object_id.text() is not '' and newName is not ''):
            target_id = int(self.object_id.text())
            self.changeObjectNameSignal.emit(target_id,newName)
            self.nameLineEdit.clear()
            self.object_name.setText(newName)

    def changeDescription(self):
        description_text = self.descriptionEdit.toPlainText()
        if (self.object_id.text() is not '' and description_text is not ''):
            target_id = int(self.object_id.text())
            self.changeObjectDescriptionSignal.emit(target_id, description_text)
            

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindwo = ObjectMapInfoWidget()
    mainWindwo.show()
    sys.exit(app.exec_())
