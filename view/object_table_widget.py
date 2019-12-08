from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *

DEBUG = False

class ObjectTableWidget(QWidget):
    DeleteSignal = pyqtSignal(int)
    FocusSignal = pyqtSignal(int)
    def __init__(self,mapName, parent=None):
        super(ObjectTableWidget,self).__init__(parent, Qt.Window)
        self.setWindowTitle('Object table')
        #self.mapName=mapName
        self.mapName="iseki"
        self.squeryModel = None
        self.tableView = None
        self.currentPage = 0
        self.totalPage = 0
        self.totalRecord = 0
        self.pageRecord = 10
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()
        self.Hlayout3 = QHBoxLayout()
        self.Hlayout_table = QHBoxLayout()
        self.setGeometry(900,200,800,600)

        #init Hlayout 1
        self.searchEdit = QLineEdit()
        self.searchEdit.setFixedHeight(32)
        font = QFont()
        font.setPixelSize(15)
        self.searchEdit.setFont(font)

        self.searchButton = QPushButton(' search ')
        self.searchButton.setFixedHeight(32)

        self.conditionComboBox = QComboBox()
        searchCondition = ['Type','Name', 'description']
        self.conditionComboBox.setFixedHeight(32)
        self.conditionComboBox.setFont(font)
        self.conditionComboBox.addItems(searchCondition)

        self.Hlayout1.addWidget(self.searchEdit)
        self.Hlayout1.addWidget(self.searchButton)
        self.Hlayout1.addWidget(self.conditionComboBox)

        #init Hlayout 2
        self.jumpToLabel = QLabel('jump')
        self.pageEdit = QLineEdit()
        self.pageEdit.setFixedWidth(30)
        s = "/" + str(self.totalPage) + 'page'
        self.pageLabel = QLabel(s)

        self.jumpToButton = QPushButton('jump to')
        self.jumpToButton.setFixedWidth(100)
        self.jumpToButton.clicked.connect(self.jumpToButtonClicked)

        self.prevButton = QPushButton(' last page ')
        self.prevButton.setFixedWidth(100)
        self.prevButton.clicked.connect(self.prevButtonClicked)

        self.nextButton = QPushButton(' next page ')
        self.nextButton.setFixedWidth(100)
        self.nextButton.clicked.connect(self.nextButtonClicked)

        Hlayout = QHBoxLayout()
        Hlayout.addWidget(self.jumpToLabel)
        Hlayout.addWidget(self.pageEdit)
        Hlayout.addWidget(self.pageLabel)
        Hlayout.addWidget(self.jumpToButton)
        Hlayout.addWidget(self.prevButton)
        Hlayout.addWidget(self.nextButton)
        widget = QWidget()
        widget.setLayout(Hlayout)
        widget.setFixedWidth(500)
        self.Hlayout2.addWidget(widget)

        #init table
        if QSqlDatabase.contains('qt_sql_default_connection'):
            db = QSqlDatabase.database('qt_sql_default_connection')
            if db.databaseName() != self.mapName:
                db.close()
                #db = QSqlDatabase.addDatabase("QSQLITE")
                db.setDatabaseName('./db/%s.db' % self.mapName)
                db.open()
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/%s.db' % self.mapName)
            db.open()
        self.tableView = QTableView()
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.tableView.setSelectionMode(QTableView.ExtendedSelection)
        self.queryModel = QSqlQueryModel()
        self.tableView.setModel(self.queryModel)
        self.tableView.clicked.connect(self.setDescription)
        self.tableView.clicked.connect(self.changeFocusButton)


        self.descriptionText = QTextEdit()
        self.descriptionText.setFixedWidth(150)
        self.descriptionText.setDisabled(True)
        self.descriptionText.setStyleSheet("color: white;");

        self.Hlayout_table.addWidget(self.tableView)
        self.Hlayout_table.addWidget(self.descriptionText)


        #init layout 3
        self.deleteButton = QPushButton('delete')
        self.deleteButton.clicked.connect(self.deleteButtonClicked)

        self.focusButton = QPushButton('focus')
        self.focusButton.clicked.connect(self.focusButtonClicked)
        self.Hlayout3.addWidget(self.deleteButton)
        self.Hlayout3.addWidget(self.focusButton)


        #combine all layout
        self.layout.addLayout(self.Hlayout1)
        self.layout.addLayout(self.Hlayout_table)
        self.layout.addLayout(self.Hlayout3)
        self.layout.addLayout(self.Hlayout2)
        self.setLayout(self.layout)
        self.searchButton.clicked.connect(self.searchButtonClicked)
        self.searchEdit.returnPressed.connect(self.searchButtonClicked)

        #init data
        self.searchButtonClicked()


    def setButtonStatus(self):
        if(self.currentPage == self.totalPage):
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(False)
        elif(self.currentPage==1):
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(True)
        else:
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(True)

    def getTotalRecordCount(self):
        self.queryModel.setQuery("select * from obejctGraphic")
        self.totalRecord = self.queryModel.rowCount()
        return

    def getPageCount(self):
        self.getTotalRecordCount()
        self.totalPage == int((self.totalRecord+self.pageRecord-1)/ self.pageRecord)
        return

    def recordQuery(self, index):
        queryCondition = ""
        conditionChoice = self.conditionComboBox.currentText()

        if(self.searchEdit.text() == ""):
            queryCondition = "select * from ObjectGraphic"
            self.queryModel.setQuery(queryCondition)
            self.totalRecord = self.queryModel.rowCount()
            self.totalPage = int((self.totalRecord + self.pageRecord-1)/self.pageRecord)
            label = '/' + str(int(self.totalPage)) + 'page'
            self.pageLabel.setText(label)
            queryCondition = ("select * from ObjectGraphic ORDER BY %s limit %d, %d" % (conditionChoice, index, self.pageRecord))
            self.queryModel.setQuery(queryCondition)
            self.setButtonStatus()
            return


        temp = self.searchEdit.text()
        s = '%' + temp + '%'
        if (conditionChoice == 'Type'):
            queryCondition = ("select * from ObjectGraphic where %s like '____%s' order by %s"%(conditionChoice, s, conditionChoice))
        if (conditionChoice == 'Name'):
            queryCondition = ("select * from ObjectGraphic where %s like '%s' order by %s"%(conditionChoice, s, conditionChoice))
        if (conditionChoice == 'description'):
            queryCondition = "select id from ObjectDescription where Description like '%s' order by %s"%( s,  conditionChoice)

        self.queryModel.setQuery(queryCondition)
        self.totalRecord = self.queryModel.rowCount()



    def searchButtonClicked(self, num=-1):
        self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        self.getPageCount()
        s = "/" + str(int(self.totalPage)) + 'page'
        self.pageLabel.setText(s)
        index = (self.currentPage-1) * self.pageRecord
        self.recordQuery(index)
        return

    def prevButtonClicked(self):
        self.currentPage -= 1
        if(self.currentPage<=1):
            self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    def nextButtonClicked(self):
        self.currentPage += 1
        if(self.currentPage>=int(self.totalPage)):
            self.currentPage = int(self.totalPage)
        self.pageEdit.setText(str(self.currentPage))
        index = (self.currentPage-1) * self.pageRecord
        self.recordQuery(index)
        return

    def jumpToButtonClicked(self):
        if (self.pageEdit.text().isdigit()):
            self.currentPage = int(self.pageEdit.text())
            if(self.currentPage > self.totalPage):
                self.currentPage = self.totalPage
            if(self.currentPage <= 1):
                self.currentPage = 1
        else:
            self.currentPage = 1
        index = (self.currentPage - 1) * self.pageRecord
        self.pageEdit.setText(str(self.currentPage))
        self.recordQuery(index)
        return

    def deleteButtonClicked(self):
        r = self.tableView.currentIndex().row()
        if(r is not -1):
            message_text = 'delete object %s (id:%s)?' %(self.queryModel.record(r).value('name'), self.queryModel.record(r).value('id'))
            message = QMessageBox.question(self, 'question message', message_text, QMessageBox.Yes, QMessageBox.No)
            if message == QMessageBox.Yes:
                self.DeleteSignal.emit(self.queryModel.record(r).value('id'))
                self.searchButtonClicked()

    def focusButtonClicked(self):
        r = self.tableView.currentIndex().row()
        if (self.queryModel.record(r).value('id') is not None):
            self.FocusSignal.emit(self.queryModel.record(r).value('id'))

    def changeFocusButton(self):
        r = self.tableView.currentIndex().row()
        self.focusButton.setText('Focus on: ' + str(self.queryModel.record(r).value('id')))


    def setDescription(self):
        r = self.tableView.currentIndex().row()
        object_id = self.queryModel.record(r).value('id')
        queryModelDescription = QSqlQueryModel()
        queryModelDescription.setQuery("select * from ObjectDescription where id is %d "% object_id)
        self.descriptionText.setText(queryModelDescription.record(0).value('description'))

if __name__ == "__main__":
    import sys
    app =QApplication(sys.argv)
    mainWindow =  MapObjectsTableViewer('newMap')
    mainWindow.show()
    sys.exit(app.exec_())
