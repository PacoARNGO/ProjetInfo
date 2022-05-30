# -*- coding: utf-8 -*-
# scene.py
# integration avec les widgets

import sys
from game import Ui_MainWindow
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QBrush, QPen, QPainter,QTransform
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QGraphicsScene, QGraphicsView, QGraphicsItem, \
    QGraphicsEllipseItem, QColorDialog, QGraphicsItemGroup
from VariablesEtConstantes import *
from plateau import Plateau


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.scene = QGraphicsScene()
        self.remplirScene()
        self.dessinerMains()
        self.show()
        for vue in (self.vuePlateau, self.vueMain):
            vue.setScene(self.scene)
            vue.setRenderHints(QPainter.Antialiasing)
            if vue == self.vuePlateau:
                vue.fitInView(self.rectPlateau, Qt.KeepAspectRatio)

            vue.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            vue.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vueMain.centerOn(-L_PLATEAU/2 + 230 ,-H_PLATEAU)

    def remplirScene(self):
        global H_PLATEAU
        global L_PLATEAU
        scene = self.scene
        rectPlateau = scene.addRect(-H_PLATEAU / 2, -L_PLATEAU / 2, H_PLATEAU, L_PLATEAU, brush=QBrush(Qt.lightGray))
        self.rectPlateau = rectPlateau
        self.texte = scene.addText("Domino's game \n"\
                                   "by Antoine&Paco\n"\
                                      "\n"\
                                   "Jouer en mode 2 joueurs")
        self.texte.setPos(-L_PLATEAU/2 + 150 ,-H_PLATEAU)
        self.texte.setDefaultTextColor(Qt.cyan)
        scene.addItem(self.texte)

    def dessinerTuile(self, domino, pos=[0, 0]):

        x, y = pos[0], pos[1]

        group = QGraphicsItemGroup()
        group.addToGroup(self.scene.addRect(x, y, L_TUILE, H_TUILE, brush=QBrush(Qt.color0)))

        group.addToGroup(
            self.scene.addRect(x, y + H_TUILE / 2 - H_TUILE / 80, L_TUILE, H_TUILE / 40, brush=QBrush(Qt.black),
                               pen=QPen(Qt.black)))
        group.setFlag(QGraphicsItem.ItemIsMovable)

        x, y = x - D / 2, y - D / 3
        for num in domino:
            if domino.index(num) == 1:
                y += H_TUILE / 2
            if num == 0:
                pass
            elif num == 1:
                group.addToGroup(self.scene.addEllipse(x + L_TUILE / 2, y + L_TUILE / 2, D, D, brush=QBrush(Qt.black)))
            elif num == 2:
                group.addToGroup(self.scene.addEllipse(x + L_TUILE / 4, y + L_TUILE / 4, D, D, brush=QBrush(Qt.black)))
                group.addToGroup(
                    self.scene.addEllipse(x + L_TUILE * 3 / 4, y + L_TUILE * 3 / 4, D, D, brush=QBrush(Qt.black)))
            elif num == 3:
                group.addToGroup(self.scene.addEllipse(x + L_TUILE / 4, y + L_TUILE / 4, D, D, brush=QBrush(Qt.black)))
                group.addToGroup(
                    self.scene.addEllipse(x + L_TUILE * 2 / 4, y + L_TUILE * 2 / 4, D, D, brush=QBrush(Qt.black)))
                group.addToGroup(
                    self.scene.addEllipse(x + L_TUILE * 3 / 4, y + L_TUILE * 3 / 4, D, D, brush=QBrush(Qt.black)))
            elif num == 4:
                group.addToGroup(self.scene.addEllipse(x + L_TUILE / 4, y + L_TUILE / 4, D, D, brush=QBrush(Qt.black)))
                group.addToGroup(
                    self.scene.addEllipse(x + L_TUILE * 3 / 4, y + L_TUILE / 4, D, D, brush=QBrush(Qt.black)))
                group.addToGroup(
                    self.scene.addEllipse(x + L_TUILE * 1 / 4, y + L_TUILE * 3 / 4, D, D, brush=QBrush(Qt.black)))
                group.addToGroup(
                    self.scene.addEllipse(x + L_TUILE * 3 / 4, y + L_TUILE * 3 / 4, D, D, brush=QBrush(Qt.black)))
            elif num == 5:
                group.addToGroup(self.scene.addEllipse(x + L_TUILE / 4, y + L_TUILE / 4, D, D, brush=QBrush(Qt.black)))
                group.addToGroup(
                    self.scene.addEllipse(x + L_TUILE * 3 / 4, y + L_TUILE / 4, D, D, brush=QBrush(Qt.black)))
                group.addToGroup(
                    self.scene.addEllipse(x + L_TUILE * 1 / 4, y + L_TUILE * 3 / 4, D, D, brush=QBrush(Qt.black)))
                group.addToGroup(
                    self.scene.addEllipse(x + L_TUILE * 3 / 4, y + L_TUILE * 3 / 4, D, D, brush=QBrush(Qt.black)))
                group.addToGroup(
                    self.scene.addEllipse(x + L_TUILE * 2 / 4, y + L_TUILE * 2 / 4, D, D, brush=QBrush(Qt.black)))
            elif num == 6:
                group.addToGroup(self.scene.addEllipse(x + L_TUILE / 4, y + L_TUILE / 4, D, D, brush=QBrush(Qt.black)))
                group.addToGroup(
                    self.scene.addEllipse(x + L_TUILE * 3 / 4, y + L_TUILE / 4, D, D, brush=QBrush(Qt.black)))
                group.addToGroup(
                    self.scene.addEllipse(x + L_TUILE * 1 / 4, y + L_TUILE * 3 / 4, D, D, brush=QBrush(Qt.black)))
                group.addToGroup(
                    self.scene.addEllipse(x + L_TUILE * 3 / 4, y + L_TUILE * 3 / 4, D, D, brush=QBrush(Qt.black)))
                group.addToGroup(
                    self.scene.addEllipse(x + L_TUILE * 1 / 4, y + L_TUILE * 2 / 4, D, D, brush=QBrush(Qt.black)))
                group.addToGroup(
                    self.scene.addEllipse(x + L_TUILE * 3 / 4, y + L_TUILE * 2 / 4, D, D, brush=QBrush(Qt.black)))

        self.scene.addItem(group)
        group.setFlag(QGraphicsItem.ItemIsSelectable)

    def dessinerMains(self):
        plateau = Plateau()
        main_j1, main_j2, pioche = plateau.generation(7)
        dx = 0
        for tuile in main_j1:
            self.dessinerTuile(tuile, [-L_PLATEAU-50 + dx, H_PLATEAU/2+10])
            dx += 30 + L_TUILE
        dx = 0
        for tuile in main_j2:
            self.dessinerTuile(tuile, [L_PLATEAU-50 - dx, H_PLATEAU/2+10])
            dx += 30 + L_TUILE

    def changerVue(self, i):
        if i == 1:
            self.vueMain.centerOn(-L_PLATEAU/2 -300, H_PLATEAU/2+30)
        elif i == 2:
            self.vueMain.centerOn(L_PLATEAU/2 -300, H_PLATEAU/2 + 30)


    @pyqtSlot()
    def on_pushButtonJoueur1_clicked(self):
        self.changerVue(1)

    @pyqtSlot()
    def on_pushButtonJoueur2_clicked(self):
        self.changerVue(2)

    @pyqtSlot()
    def on_pushButtonTourner_clicked(self):
        itemsSelectionnes = self.scene.selectedItems()
        for item in itemsSelectionnes:
            item.setTransformOriginPoint(item.boundingRect().center())
            item.setRotation(item.rotation() +90)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
