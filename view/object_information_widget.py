from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re


class ObjectInfoWidget(QWidget):
    ChangeObjectNameSignal = pyqtSignal(int,str)
    ChangeObjectDescriptionSignal = pyqtSignal(int, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.current_id = 0
        self.initUI()

    def initUI(self):
        #set layout
        self.setFixedSize(200,500)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        #crate labels
        self.idLabel = QLabel('Id:')
        self.nameLabel = QLabel('Name:')
        self.typeNameLabel = QLabel('type:')
        self.widthLabel = QLabel('Width:')
        self.heightLabel = QLabel('Height:')
        self.xLabel = QLabel('X:')
        self.yLabel = QLabel('Y:')
        self.renameLabel = QLabel('new name:')

        self.object_id = QLabel('')
        self.object_name = QLabel('')
        self.object_type = QLabel('')
        self.object_width = QLabel('')
        self.object_height = QLabel('')
        self.object_x = QLabel('')
        self.object_y = QLabel('')
        #self.object_size = QLabel('')

        #crate editor
        self.nameLineEdit = QLineEdit()
        self.descriptionEdit = QTextEdit()
        self.descriptionEdit.setFixedHeight(200)

        #create button 
        self.renameButton = QPushButton(' rename ')
        self.renameButton.clicked.connect(self.changeName)
        self.changeDescriptionButton = QPushButton(' change Description ')
        self.changeDescriptionButton.clicked.connect(self.changeDescription)
        spacerItem = QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.Expanding)

        #set layout
        self.layout.addRow(self.idLabel, self.object_id)
        self.layout.addRow(self.nameLabel, self.object_name)
        self.layout.addRow(self.typeNameLabel, self.object_type)
        self.layout.addRow(self.widthLabel, self.object_width)
        self.layout.addRow(self.heightLabel, self.object_height)
        self.layout.addRow(self.xLabel, self.object_x)
        self.layout.addRow(self.yLabel, self.object_y)
        self.layout.addRow(self.renameLabel, self.nameLineEdit)
        self.layout.addRow(self.renameButton)
        self.layout.addRow(self.descriptionEdit)
        self.layout.addRow(self.changeDescriptionButton)
        self.layout.addItem(spacerItem)
        

    def setInfo(self,id, name, type_name, x, y, description, width, height):
        if (id+1):
            type_name = re.sub('^type', '', type_name)
            self.object_id.setText(str(id))
            self.object_name.setText(name)
            self.object_type.setText(type_name)
            self.object_width.setText(str(width))
            self.object_height.setText(str(height))
            self.object_x.setText(str(x))
            self.object_y.setText(str(y))
            self.descriptionEdit.setText(description)
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
        self.descriptionEdit.setText('')


    def changeName(self):
        new_name =  self.nameLineEdit.text()
        if (self.object_id.text() is not '' and new_name is not ''):
            target_id = int(self.object_id.text())
            self.ChangeObjectNameSignal.emit(target_id,new_name)
            self.nameLineEdit.clear()
            self.object_name.setText(new_name)


    def changeDescription(self):
        description_text = self.descriptionEdit.toPlainText()
        if (self.object_id.text() is not '' and description_text is not ''):
            target_id = int(self.object_id.text())
            self.ChangeObjectDescriptionSignal.emit(target_id, description_text)
            

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindwo = ObjectInfoWidget()
    mainWindwo.show()
    sys.exit(app.exec_())
