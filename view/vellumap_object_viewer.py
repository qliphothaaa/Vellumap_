from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *

DEBUG = False

class MapObjectTableViewer(QWidget):
    DeleteSignal = pyqtSignal(int)
    FocusSignal = pyqtSignal(float, float)
    def __init__(self,mapName, parent=None):
        super(MapObjectTableViewer,self).__init__(parent, Qt.Window)
        self.setWindowTitle('Object table')
        self.mapName=mapName
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
        searchCondition = ['Type','Name']
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
        self.prevButton = QPushButton(' last page ')
        self.nextButton = QPushButton(' next page ')
        self.prevButton.setFixedWidth(100)
        self.nextButton.setFixedWidth(100)

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

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./db/%s.db'% self.mapName)
        self.db.open()
        self.tableView = QTableView()
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.queryModel = QSqlQueryModel()
        self.tableView.setModel(self.queryModel)

        self.queryModel.setHeaderData(0, Qt.Horizontal,  'Object Name')
        self.queryModel.setHeaderData(0, Qt.Horizontal, 'X')
        self.queryModel.setHeaderData(0, Qt.Horizontal, 'Y')
        self.queryModel.setHeaderData(0, Qt.Horizontal, 'Type')
        self.queryModel.setHeaderData(0, Qt.Horizontal, 'Size')

        self.deleteButton = QPushButton('delete')
        self.focusButton = QPushButton('focus')
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.focusButton .clicked.connect(self.focusButtonClicked)
        self.Hlayout3.addWidget(self.deleteButton)
        self.Hlayout3.addWidget(self.focusButton)


        self.layout.addLayout(self.Hlayout1)
        self.layout.addWidget(self.tableView)
        self.layout.addLayout(self.Hlayout3)
        self.layout.addLayout(self.Hlayout2)
        self.setLayout(self.layout)
        self.searchButton.clicked.connect(self.searchButtonClicked)
        self.prevButton.clicked.connect(self.prevButtonClicked)
        self.nextButton.clicked.connect(self.nextButtonClicked)
        self.jumpToButton.clicked.connect(self.jumpToButtonClicked)
        self.searchEdit.returnPressed.connect(self.searchButtonClicked)
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
        s = '%'
        for i in range(0, len(temp)):
            s = s + temp[i] + "%"
        queryCondition = ("select * from ObjectGraphic where %s like '%s' order by %s"%(conditionChoice, s, conditionChoice))
        self.queryModel.setQuery(queryCondition)
        self.totalRecord = self.queryModel.rowCount()


    def searchButtonClicked(self):
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
        self.DeleteSignal.emit(self.queryModel.record(r).value('id'))
        self.searchButtonClicked()

    def focusButtonClicked(self):
        r = self.tableView.currentIndex().row()
        self.FocusSignal.emit(self.queryModel.record(r).value('x'), self.queryModel.record(r).value('y'))
        #self.close()
        

if __name__ == "__main__":
    import sys
    app =QApplication(sys.argv)
    mainWindow =  MapObjectsTableViewer('newMap')
    mainWindow.show()
    sys.exit(app.exec_())
