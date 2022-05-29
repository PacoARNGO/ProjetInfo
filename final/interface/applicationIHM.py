import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic

from PyQt5.QtWidgets import QDialog, QApplication, QWidget

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        uic.loadUi('welcomescreen.ui', self)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome = WelcomeScreen()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(welcome)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1200)
    widget.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Bye")

