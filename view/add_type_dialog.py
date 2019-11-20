from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class AddTypeDialog(QDialog):
    AddTypeSignal = pyqtSignal(str, str, str, float, float)

    def __init__(self, type_list, parent=None):
        super(AddTypeDialog, self).__init__(parent)
        self.parent = parent
        self.type_list = type_list
        self.initUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle('add Type')

    def initUI(self):
        Graphics = ['ell', 'rect', 'tri']
        self.resize(300,400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.titleLabel = QLabel(' add Type ')
        self.nameLabel = QLabel('Name:')
        self.shapeLabel = QLabel('Shape:')
        self.colorLabel = QLabel('Color:')
        self.widthLabel = QLabel('Width:')
        self.heightLabel = QLabel('Height:')

        self.colorButton = QPushButton(' select color ')
        self.confirmTypeButton = QPushButton(' confirm ')
        self.cancelTypeButton = QPushButton(' cancel ')

        self.nameEdit = QLineEdit('')
        self.graphciComboBox = QComboBox()
        self.graphciComboBox.addItems(Graphics)
        self.colorEdit = QLineEdit('')
        self.widthEdit = QLineEdit('')
        self.heightEdit = QLineEdit('')

        self.nameEdit.setMaxLength(10)
        self.colorEdit.setMaxLength(20)
        self.widthEdit.setMaxLength(7)
        self.widthEdit.setMaxLength(7)

        self.widthEdit.setValidator(QDoubleValidator(0, 10000, 1))
        self.heightEdit.setValidator(QDoubleValidator(0, 10000, 1))

        self.layout.addRow('',self.titleLabel)
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
        self.titleLabel.setFont(font)
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

        self.titleLabel.setMargin(8)
        self.layout.setVerticalSpacing(10)

        self.confirmTypeButton.clicked.connect(self.confirmTypeButtonClicked)
        self.cancelTypeButton.clicked.connect(self.close)
        self.colorButton.clicked.connect(self.showColorDialog)
    
    def confirmTypeButtonClicked(self):
        if ( self.nameEdit.text() == '' or self.graphciComboBox.currentText() == '' or self.colorEdit.text() =='' or self.widthEdit.text() == '' or self.heightEdit.text() == ''):
            QMessageBox.warning(self, 'warning', 'empty input' , QMessageBox.Yes, QMessageBox.Yes)
            return
        name = self.nameEdit.text()
        shape = self.graphciComboBox.currentText()
        color = self.colorEdit.text()
        width = float(self.widthEdit.text())
        height = float(self.heightEdit.text())
        full_name = 'type' + name

        if full_name in self.type_list:
            QMessageBox.warning(self, 'warning', 'exised!' , QMessageBox.Yes, QMessageBox.Yes)
        else:
            self.AddTypeSignal.emit(full_name, shape, color, width, height)
            QMessageBox.information(self, 'info', 'success' , QMessageBox.Yes, QMessageBox.Yes)
            self.close()

    def showColorDialog(self):
        get_color = QColorDialog.getColor()
        if get_color.isValid():
            self.colorEdit.setText(get_color.name())

    def clearEdit(self):
        self.nameEdit.clear()
        self.colorEdit.clear()
        self.widthEdit.clear()
        self.heightEdit.clear()
