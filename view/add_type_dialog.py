from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *


class AddTypeDialog(QDialog):
    add_success_signal = pyqtSignal(str)

    def __init__(self,mapName, parent=None):
        super(AddTypeDialog, self).__init__(parent)
        self.mapName = mapName
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

        self.nameEdit = QLineEdit('test')
        self.graphciComboBox = QComboBox()
        self.graphciComboBox.addItems(Graphics)
        self.colorEdit = QLineEdit('green')
        self.widthEdit = QLineEdit('100')
        self.heightEdit = QLineEdit('100')

        self.nameEdit.setMaxLength(10)
        self.colorEdit.setMaxLength(20)
        self.widthEdit.setMaxLength(7)
        self.widthEdit.setMaxLength(7)

        self.layout.addRow('',self.titleLabel)
        self.layout.addRow(self.nameLabel, self.nameEdit)
        self.layout.addRow(self.shapeLabel,self.graphciComboBox)
        self.layout.addRow(self.colorLabel, self.colorEdit)
        self.layout.addRow('', self.colorButton)
        self.layout.addRow(self.widthLabel, self.widthEdit)
        self.layout.addRow(self.heightLabel,self.heightEdit)
        self.layout.addRow('', self.confirmTypeButton)
        self.layout.addRow('', self.cancelTypeButton)
        #self.layout.addRow('', self.colorButton)

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
        name = self.nameEdit.text()
        shape = self.graphciComboBox.currentText()
        color = self.colorEdit.text()
        width = self.widthEdit.text()
        height = self.heightEdit.text()

        if ( name == '' or shape == '' or color =='' or width == '' or height == ''):
            print(QMessageBox.warning(self, 'warning', 'empty input' , QMessageBox.Yes, QMessageBox.Yes))
            return
        else:
            if QSqlDatabase.contains('qt_sql_default_connection'):
                db = QSqlDatabase.database('qt_sql_default_connection')
            else:
                db = QSqlDatabase.addDatabase("QSQLITE")
                db.setDatabaseName('./db/%s.db' % self.mapName)
                db.open()
            query = QSqlQuery()
            sql = "select * from type where Name = '%s'" % ('type'+name)
            query.exec_(sql)
            if (query.next()):
                print(QMessageBox.warning(self, 'warning', 'exised!' , QMessageBox.Yes, QMessageBox.Yes))
                return

            else:
                sql = "insert into type values('type%s','%s','%s','%s','%s')" % (name, shape, color, width, height)
                query.exec_(sql)
                try: 
                    db.commit()
                except:
                    print("SQL error:", sys.exc_info()[0])
                print(QMessageBox.information(self, 'info', 'success' , QMessageBox.Yes, QMessageBox.Yes))
                self.add_success_signal.emit('type'+name)
                self.close()
                self.clearEdit()
            return

    def showColorDialog(self):
        get_color = QColorDialog.getColor()
        if get_color.isValid():
            self.colorEdit.setText(get_color.name())

    def clearEdit(self):
        self.nameEdit.clear()
        self.colorEdit.clear()
        self.widthEdit.clear()
        self.heightEdit.clear()

        


        

        
