from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re

class ObjectInfoViewWidget(QWidget):
    ChangeObjectNameSignal = pyqtSignal(int,str)
    ChangeObjectDescriptionSignal = pyqtSignal(int, str)
    def __init__(self, parent=None):
        super().__init__(parent)
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
        self.descriptionEdit = QTextEdit()
        self.descriptionEdit.setDisabled(True)
        self.descriptionEdit.setFixedHeight(200)

        #create button 
        spacerItem = QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.Expanding)

        #set layout
        self.layout.addRow(self.idLabel, self.object_id)
        self.layout.addRow(self.nameLabel, self.object_name)
        self.layout.addRow(self.typeNameLabel, self.object_type)
        self.layout.addRow(self.widthLabel, self.object_width)
        self.layout.addRow(self.heightLabel, self.object_height)
        self.layout.addRow(self.xLabel, self.object_x)
        self.layout.addRow(self.yLabel, self.object_y)
        self.layout.addRow(self.descriptionEdit)
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


            

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindwo = ObjectInfoWidget()
    mainWindwo.show()
    sys.exit(app.exec_())
