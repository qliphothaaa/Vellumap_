from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from view.type_checkbutton_widget import TypeCheckButton

class TypeCheckbuttonGroupWidget(QWidget):
    FilterSignal = pyqtSignal(str,bool)
    ShowAllSignal = pyqtSignal()
    HideAllSignal = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button_list = []
        self.all_type = []
        #self.show_type = []
        self.initUI()

    def initUI(self):
        self.layout_checkbox = QHBoxLayout()
        self.setLayout(self.layout_checkbox)
        

    def addButtonFromList(self, type_list):
        self.all_type = type_list.copy()
        #self.show_type = type_list.copy()

        self.checkAll = QCheckBox("show all")
        self.checkAll.setChecked(True)
        self.checkAll.stateChanged.connect(self.showAll)
        self.layout_checkbox.addWidget(self.checkAll)
        for objec_type_name in type_list:
            checkButton = TypeCheckButton(objec_type_name, self)
            checkButton.CheckedSignal.connect(self.fliter)
            checkButton.UncheckedSignal.connect(self.fliter)
            self.button_list.append(checkButton)
            self.layout_checkbox.addWidget(checkButton)

    def clearButtons(self):
        self.all_type = []
        #self.show_type = []
        for i in reversed(range(self.layout_checkbox.count())):
            self.layout_checkbox.itemAt(i).widget().deleteLater()
            self.button_list = []

    def fliter(self, type_name, state):
        self.FilterSignal.emit(type_name, state)

    def showAll(self, state):
        if state == 2:
            for button in self.button_list:
                button.setChecked(True)
            self.ShowAllSignal.emit()
        else:
            for button in self.button_list:
                button.setChecked(False)
            self.HideAllSignal.emit()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindwo = TypeCheckButtonGroupWidget()
    mainWindwo.addButtonFromList(['a', 'b'])
    mainWindwo.show()
    sys.exit(app.exec_())

