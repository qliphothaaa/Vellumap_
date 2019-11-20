import sys
from PyQt5.QtWidgets import *

from view.vellumap_window import VellumapWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = VellumapWindow()
    sys.exit(app.exec_())
