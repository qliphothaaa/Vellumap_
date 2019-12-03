from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from view.add_type_dialog import AddTypeDialog
from view.update_type_dialog import UpdateTypeDialog

class TypeTableWidget(QWidget):
    RefreshSignal = pyqtSignal()
    DeleteSignal = pyqtSignal(str)
    AddSignal = pyqtSignal(str, str, str, float, float)
    UpdateSignal = pyqtSignal(str, str, str, float, float)
    ResetModeSignal = pyqtSignal()
    def __init__(self, mapName, parent=None):
        super(TypeTableWidget,self).__init__(parent,Qt.Window)
        self.setWindowTitle('type table')
        self.tableView = None
        self.mapName=mapName
        self.type_list = []
        
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
            if db.databaseName() != self.mapName:
                db.close()
                db.setDatabaseName('./db/%s.db' % self.mapName)
                db.open()
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/%s.db' % self.mapName)
            db.open()
        self.model = QSqlTableModel()
        self.tableView.setModel(self.model)
        self.model.setTable('Type')
        self.model.select()
        self.type_list.clear()
        for row in range(self.model.rowCount()):
            self.type_list.append(self.model.record(row).value('name'))
        self.RefreshSignal.emit()

    def updateTypeButtonClicked(self):
        updateTypeDialog = UpdateTypeDialog(self.type_list, self)
        updateTypeDialog.UpdateTypeSignal.connect(self.UpdateSignal)
        updateTypeDialog.show()
        updateTypeDialog.exec_()
        self.ResetModeSignal.emit()
        self.viewType()

    def addTypeButtonClicked(self):
        addTypeDialog = AddTypeDialog(self.type_list, self)
        addTypeDialog.AddTypeSignal.connect(self.AddSignal)
        addTypeDialog.show()
        addTypeDialog.exec_()
        self.ResetModeSignal.emit()
        self.viewType()

    def deleteTypeButtonClicked(self):
        if self.model:
            message_text = 'delete「%s」? this operation will delete all object belong to this type' %((self.model.record(self.tableView.currentIndex().row()).value('name')))
            message = QMessageBox.question(self, 'question message', message_text, QMessageBox.Yes, QMessageBox.No)
            if message == QMessageBox.Yes:
                self.DeleteSignal.emit(self.model.record(self.tableView.currentIndex().row()).value('name'))
                self.ResetModeSignal.emit()
                self.viewType()



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    wnd = TypeViewerWidget('a')
    wnd.show()
    sys.exit(app.exec_())
