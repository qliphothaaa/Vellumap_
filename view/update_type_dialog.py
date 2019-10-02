from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *


class UpdateTypeDialog(QDialog):
    update_success_signal = pyqtSignal(str)

    def __init__(self,mapName, parent=None):
        super(UpdateTypeDialog, self).__init__(parent)
        self.mapName = mapName
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
        self.widthEdit.setMaxLength(7)

        self.layout.addRow('',self.titlelabel)
        self.layout.addRow(self.nameLabel, self.nameEdit)
        self.layout.addRow(self.shapeLabel,self.graphciComboBox)
        self.layout.addRow(self.colorLabel, self.colorEdit)
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
    
    def typeNameChanged(self):
        name = self.nameEdit.text()
        if(name == ""):
            self.graphciComboBox.clear()
            self.colorEdit.clear()
            self.widthEdit.clear()
            self.heightEdit.clear()
        if QSqlDatabase.contains('qt_sql_default_connection'):
            db = QSqlDatabase.database('qt_sql_default_connection')
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/%s.db' % self.mapName)
            db.open()
        query = QSqlQuery()
        sql = "select * from type where Name = 'type%s'" % (name)
        query.exec_(sql)
        if(query.next()):
            index = self.graphciComboBox.findText(query.value(1), Qt.MatchFixedString)
            if index >= 0:
                self.graphciComboBox.setCurrentIndex(index)
            self.colorEdit.setText(query.value(2))
            self.widthEdit.setText(str(query.value(3)))
            self.heightEdit.setText(str(query.value(4)))
        return

    def confirmTypeButtonClicked(self):
        name = self.nameEdit.text()
        shape = self.graphciComboBox.currentText()
        color = self.colorEdit.text()
        width = self.widthEdit.text()
        height = self.heightEdit.text()
        if QSqlDatabase.contains('qt_sql_default_connection'):
            db = QSqlDatabase.database('qt_sql_default_connection')
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/%s.db' % self.mapName)
            db.open()
        query = QSqlQuery()
        sql = "update type set Shape = '%s', Color = '%s', width = '%s', height = '%s' where Name = 'type%s'" % (shape, color, width, height, name)
        query.exec_(sql)
        try: 
            db.commit()
        except:
            print("SQL error:", sys.exc_info()[0])
        print(QMessageBox.information(self, 'info', 'success' , QMessageBox.Yes, QMessageBox.Yes))
        self.update_success_signal.emit('type'+name)
        self.clearEdit()
        self.close()
        
    def clearEdit(self):
        self.nameEdit.clear()
        self.colorEdit.clear()
        self.widthEdit.clear()
        self.heightEdit.clear()
