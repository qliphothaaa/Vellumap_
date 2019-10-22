from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class UpdateTypeDialog(QDialog):
    update_success_signal = pyqtSignal(str)
    UpdateTypeSignal = pyqtSignal(str, str, str, float, float)

    def __init__(self, mapName, type_list, parent=None):
        super(UpdateTypeDialog, self).__init__(parent)
        self.parent = parent
        self.mapName = mapName
        self.type_list = type_list
        self.initUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle('update Type')

    def initUI(self):
        Graphics = ['ell', 'rect', 'tri']
        self.resize(300,400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.titlelabel = QLabel(' update Type ')
        self.nameLabel = QLabel('Name:')
        self.shapeLabel = QLabel('Shape:')
        self.colorLabel = QLabel('Color:')
        self.widthLabel = QLabel('Width:')
        self.heightLabel = QLabel('Height:')

        self.colorButton = QPushButton(' select color ')
        self.confirmTypeButton = QPushButton(' confirm ')
        self.cancelTypeButton = QPushButton(' cancel ')

        self.nameEdit = QLineEdit()
        self.graphciComboBox = QComboBox()
        self.graphciComboBox.addItems(Graphics)
        self.colorEdit = QLineEdit()
        self.widthEdit = QLineEdit()
        self.heightEdit = QLineEdit()

        self.nameEdit.setMaxLength(10)
        self.colorEdit.setMaxLength(20)
        self.widthEdit.setMaxLength(7)
        self.heightEdit.setMaxLength(7)

        self.widthEdit.setValidator(QDoubleValidator(0, 10000, 1))
        self.heightEdit.setValidator(QDoubleValidator(0, 10000, 1))

        self.layout.addRow('',self.titlelabel)
        self.layout.addRow(self.nameLabel, self.nameEdit)
        self.layout.addRow(self.shapeLabel,self.graphciComboBox)
        self.layout.addRow(self.colorLabel, self.colorEdit)
        self.layout.addRow('', self.colorButton)
        self.layout.addRow(self.widthLabel, self.widthEdit)
        self.layout.addRow(self.heightLabel,self.heightEdit)
        self.layout.addRow('', self.confirmTypeButton)
        self.layout.addRow('', self.cancelTypeButton)

        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(14)
        self.nameEdit.setFont(font)
        self.colorEdit.setFont(font)
        self.widthEdit.setFont(font)
        self.heightEdit.setFont(font)
        self.nameLabel.setFont(font)
        self.colorLabel.setFont(font)
        self.shapeLabel.setFont(font)
        self.widthEdit.setFont(font)
        self.heightEdit.setFont(font)


        font.setPixelSize(16)
        self.colorButton.setFont(font)
        self.colorButton.setFixedHeight(32)
        self.colorButton.setFixedWidth(140)

        self.confirmTypeButton.setFont(font)
        self.confirmTypeButton.setFixedHeight(32)
        self.confirmTypeButton.setFixedWidth(140)

        self.cancelTypeButton.setFont(font)
        self.cancelTypeButton.setFixedHeight(32)
        self.cancelTypeButton.setFixedWidth(140)

        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)

        self.confirmTypeButton.clicked.connect(self.confirmTypeButtonClicked)
        self.cancelTypeButton.clicked.connect(self.close)
        self.nameEdit.textChanged.connect(self.typeNameChanged)
        self.colorButton.clicked.connect(self.showColorDialog)
        self.disableEdit()
    
    def typeNameChanged(self):
        name = self.nameEdit.text()
        full_name = 'type'+name
        if(name == ""):
            self.clearEdit()
            self.disableEdit()
        elif full_name in self.type_list:
            index = self.type_list.index(full_name)
            i = self.graphciComboBox.findText(self.parent.model.record(index).value('shape'), Qt.MatchFixedString)
            if i >= 0:
                self.graphciComboBox.setCurrentIndex(i)
            self.colorEdit.setText(self.parent.model.record(index).value('color'))
            self.widthEdit.setText(str(self.parent.model.record(index).value('width')))
            self.heightEdit.setText(str(self.parent.model.record(index).value('height')))
            self.enableEdit()

        else:
            self.clearEdit()
            self.disableEdit()


    def confirmTypeButtonClicked(self):
        name = 'type' + self.nameEdit.text()
        shape = self.graphciComboBox.currentText()
        color = self.colorEdit.text()
        width = float(self.widthEdit.text())
        height = float(self.heightEdit.text())


        self.UpdateTypeSignal.emit(name, shape, color, width, height)

        QMessageBox.information(self, 'info', 'success' , QMessageBox.Yes, QMessageBox.Yes)
        #self.update_success_signal.emit(name)
        #self.clearEdit()
        self.close()
        
    def showColorDialog(self):
        get_color = QColorDialog.getColor()
        if get_color.isValid():
            self.colorEdit.setText(get_color.name())

    def clearEdit(self):
        self.graphciComboBox.setCurrentIndex(-1)
        self.colorEdit.clear()
        self.widthEdit.clear()
        self.heightEdit.clear()

    def enableEdit(self):
        self.colorEdit.setDisabled(False)
        self.graphciComboBox.setDisabled(False)
        self.widthEdit.setDisabled(False)
        self.heightEdit.setDisabled(False)
        self.colorButton.setDisabled(False)
        self.confirmTypeButton.setDisabled(False)

    def disableEdit(self):
        self.colorEdit.setDisabled(True)
        self.graphciComboBox.setDisabled(True)
        self.widthEdit.setDisabled(True)
        self.heightEdit.setDisabled(True)
        self.colorButton.setDisabled(True)
        self.confirmTypeButton.setDisabled(True)


