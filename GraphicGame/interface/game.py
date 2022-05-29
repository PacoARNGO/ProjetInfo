# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\arang\PycharmProjects\ProjetInfo\GraphicGame\interface\game.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.vuePlateau = QtWidgets.QGraphicsView(self.centralwidget)
        self.vuePlateau.setObjectName("vuePlateau")
        self.horizontalLayout.addWidget(self.vuePlateau)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.NomJoueur = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.NomJoueur.setObjectName("NomJoueur")
        self.verticalLayout.addWidget(self.NomJoueur)
        self.pushButtonJoueur = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonJoueur.setObjectName("pushButtonJoueur")
        self.verticalLayout.addWidget(self.pushButtonJoueur)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.vueMain = QtWidgets.QGraphicsView(self.dockWidgetContents)
        self.vueMain.setObjectName("vueMain")
        self.verticalLayout.addWidget(self.vueMain)
        self.pushButtonTourner = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonTourner.setObjectName("pushButtonTourner")
        self.verticalLayout.addWidget(self.pushButtonTourner)
        self.pushButtonJouer = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonJouer.setObjectName("pushButtonJouer")
        self.verticalLayout.addWidget(self.pushButtonJouer)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.pushButtonNouvellePartie = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonNouvellePartie.setObjectName("pushButtonNouvellePartie")
        self.verticalLayout.addWidget(self.pushButtonNouvellePartie)
        self.pushButtonQuitter = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonQuitter.setObjectName("pushButtonQuitter")
        self.verticalLayout.addWidget(self.pushButtonQuitter)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)

        self.retranslateUi(MainWindow)
        self.pushButtonQuitter.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fenêtre avec vues"))
        self.dockWidget.setWindowTitle(_translate("MainWindow", "Boîte à outils"))
        self.pushButtonJoueur.setText(_translate("MainWindow", "Entrée le nom d\'un joueur"))
        self.pushButtonTourner.setText(_translate("MainWindow", "Tourner"))
        self.pushButtonJouer.setText(_translate("MainWindow", "Jouer"))
        self.pushButtonNouvellePartie.setText(_translate("MainWindow", "Nouvelle partie"))
        self.pushButtonQuitter.setText(_translate("MainWindow", "Quitter"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
