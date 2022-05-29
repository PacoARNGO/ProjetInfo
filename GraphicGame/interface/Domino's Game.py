# -*- coding: utf-8 -*-
# scene.py
# integration avec les widgets

import sys
from game import Ui_MainWindow
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QBrush, QPen, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QGraphicsScene, QGraphicsView, QGraphicsItem, \
    QGraphicsEllipseItem, QColorDialog


class MainWindow(QMainWindow, Ui_MainWindow):

        def __init__(self, parent=None):
            super(MainWindow, self).__init__(parent)
            self.setupUi(self)
            self.scene = QGraphicsScene()
            self.remplirScene()
            self.show()
            for vue in (self.vuePlateau, self.vueMain):
                vue.setScene(self.scene)
                vue.setRenderHints(QPainter.Antialiasing)
                vue.fitInView(self.rectPlateau, Qt.KeepAspectRatio)
                vue.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                vue.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        def remplirScene(self):
            scene = self.scene
            rectPlateau = scene.addRect(0, 0, 200, 150, brush=QBrush(Qt.lightGray))
            self.rectPlateau = rectPlateau
            self.texte = scene.addText("Domino's game")
            dy = rectPlateau.rect().height()
            self.texte.setPos(rectPlateau.x(), rectPlateau.y() + dy)
            self.texte.setDefaultTextColor(Qt.cyan)
            scene.addItem(self.texte)


        #def faireTuile(self):

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())