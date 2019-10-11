from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from view.add_type_dialog import AddTypeDialog
from view.update_type_dialog import UpdateTypeDialog

class TypeTableWidget(QWidget):
    RefreshSignal = pyqtSignal()
    DeleteSignal = pyqtSignal(str)
    AddSignal = pyqtSignal(str)
    UpdateSignal = pyqtSignal(str)
    ResetModeSignal = pyqtSignal()
    def __init__(self, mapName, parent=None):
        super(TypeTableWidget,self).__init__(parent,Qt.Window)
        self.setWindowTitle('type table')
        self.tableView = None
        self.mapName=mapName
        
        self.initUI()

    def initUI(self):
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.setGeometry(900,200,800,600)

        #button group
        self.groupBox = QGroupBox('management')
        self.groupBox_layout = QVBoxLayout()
        self.groupBox.setLayout(self.groupBox_layout)

        self.tableView = QTableView()
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.grid_layout.addWidget(self.groupBox,0,0)
        self.grid_layout.addWidget(self.tableView,0,1)

        self.addButton = QPushButton('add type')
        self.addButton.clicked.connect(self.addTypeButtonClicked)
        self.updateButton = QPushButton('update type')
        self.updateButton.clicked.connect(self.updateTypeButtonClicked)
        self.deleteButton = QPushButton('delete type')
        self.deleteButton.clicked.connect(self.deleteTypeButtonClicked)

        self.groupBox_layout.addWidget(self.addButton)
        self.groupBox_layout.addWidget(self.updateButton)
        self.groupBox_layout.addWidget(self.deleteButton)
        self.viewType()

    def viewType(self):
        if QSqlDatabase.contains('qt_sql_default_connection'):
            db = QSqlDatabase.database('qt_sql_default_connection')
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/%s.db' % self.mapName)
            db.open()

        self.model = QSqlTableModel()
        self.tableView.setModel(self.model)
        self.model.setTable('Type')
        self.model.select()
        self.RefreshSignal.emit()

    def updateTypeButtonClicked(self):
        updateTypeDialog = UpdateTypeDialog(self.mapName, self)
        updateTypeDialog.update_success_signal.connect(self.UpdateSignal)
        updateTypeDialog.show()
        updateTypeDialog.exec_()
        self.ResetModeSignal.emit()
        self.viewType()

    def addTypeButtonClicked(self):
        addTypeDialog = AddTypeDialog(self.mapName,self)
        addTypeDialog.add_success_signal.connect(self.AddSignal)
        addTypeDialog.show()
        addTypeDialog.exec_()
        self.ResetModeSignal.emit()
        self.viewType()

    def deleteTypeButtonClicked(self):
        if self.model:
            self.DeleteSignal.emit(self.model.record(self.tableView.currentIndex().row()).value('name'))
            self.model.removeRow(self.tableView.currentIndex().row())
        self.ResetModeSignal.emit()
        self.viewType()
        

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    wnd = TypeViewerWidget('a')
    wnd.show()
    sys.exit(app.exec_())