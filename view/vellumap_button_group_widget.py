from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from view.TypeButton import QTypePushButton

class TypeButtonGroupWidget(QWidget):
    ChangeModeSignal = pyqtSignal(str)
    SetCurrentTypeNameSignal = pyqtSignal(str)
    ChangeColorSignal = pyqtSignal(bool, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.recent_button_name = ''
        self.initUI()

    def initUI(self):
        self.layout_button = QVBoxLayout()
        self.setLayout(self.layout_button)
        

    def addButtonFromList(self, type_name_list):
        for objec_type_name in type_name_list:
            button = QTypePushButton(objec_type_name, self)
            self.ChangeColorSignal.connect(button.checkPermission)
            button.ClickedSignal.connect(self.changeButtonColor)
            
            self.layout_button.addWidget(button)


    def clearButtons(self):
        for i in reversed(range(self.layout_button.count())):
            self.layout_button.itemAt(i).widget().deleteLater()


    def changeButtonColor(self, button_title):
        if (button_title == self.recent_button_name):
            self.ChangeColorSignal.emit(True,button_title)
            self.ChangeModeSignal.emit('select')
            print("The titel is same, reset the button")
            self.recent_button_name = ''
        else:
            if (self.recent_button_name == ''):
                self.ChangeColorSignal.emit(True,button_title)
                self.ChangeModeSignal.emit('create')
                self.SetCurrentTypeNameSignal.emit(button_title)
                self.recent_button_name = button_title

            elif (self.recent_button_name is not button_title):
                self.ChangeColorSignal.emit(True,button_title)
                self.ChangeColorSignal.emit(True,self.recent_button_name)
                self.SetCurrentTypeNameSignal.emit(button_title)
                self.recent_button_name = button_title


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindwo = TypeButtonGroupWidget()
    mainWindwo.addButtonFromList(['a', 'b'])
    mainWindwo.show()
    sys.exit(app.exec_())

