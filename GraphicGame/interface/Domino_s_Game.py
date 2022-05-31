# -*- coding: utf-8 -*-
# scene.py
# integration avec les widgets

import sys

from GraphicGame.interface.joueurs import Joueur
from game import Ui_MainWindow
from PyQt5.QtCore import Qt, pyqtSlot, QPointF, QRectF
from PyQt5.QtGui import QBrush, QPen, QPainter, QTransform, QPainterPath
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QGraphicsScene, QGraphicsView, QGraphicsItem, \
    QGraphicsEllipseItem, QColorDialog, QGraphicsItemGroup, QGraphicsRectItem
from VariablesEtConstantes import *
from plateau import Plateau
from tour import Tour


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.scene = QGraphicsScene()
        plateau = Plateau()
        tour = Tour(plateau)
        #self.scene.setSceneRect(-H_PLATEAU/2,-L_PLATEAU/2,H_PLATEAU,L_PLATEAU)
        self.remplirScene()
        main_j1, main_j2 = self.dessinerMains(plateau)
        joueurs = []
        joueurs.append(Joueur("Joueur 1", main_j1))
        joueurs.append(Joueur("Joueur 2", main_j2))



        self.dessiner_Tuile([6,6], self.rectPlateau.rect().center())
        self.dessiner_Tuile([6,1], [100,100])
        print("Plateau")
        for item in self.selectionner_plateau():
            print(self.reco_tuile(item))
            print("Main")
        for item in self.selectionner_main(1):
            print(self.reco_tuile(item))
        self.show()

        for vue in (self.vuePlateau, self.vueMain):
            vue.setScene(self.scene)
            vue.setRenderHints(QPainter.Antialiasing)
            if vue == self.vuePlateau:
                vue.fitInView(self.rectPlateau, Qt.KeepAspectRatio)

            vue.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            vue.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vueMain.centerOn(self.rectPlateau.rect().center())
        self.vueMain.scale(1,1.25)



    def remplirScene(self):
        global H_PLATEAU
        global L_PLATEAU
        scene = self.scene
        rectPlateau = scene.addRect(0, 0, H_PLATEAU, L_PLATEAU, brush=QBrush(Qt.lightGray))
        self.rectPlateau = rectPlateau

        #TEXTE

        # self.texte = scene.addText("Domino's game \n"\
        #                            "by Antoine&Paco\n"\
        #                               "\n"\
        #                            "Jouer en mode 2 joueurs")
        #self.texte.setPos(-L_PLATEAU/2 + 150 ,-H_PLATEAU)
        #self.texte.setDefaultTextColor(Qt.cyan)
        #scene.addItem(self.texte)


    def dessiner_Tuile(self, domino, pos, rot = 0):

        try:
            x, y = pos[0], pos[1]
        except:
            x, y = pos.x(), pos.y()

        tuile = QGraphicsRectItem(0, 0, L_TUILE, H_TUILE,parent=self.rectPlateau)
        tuile.setPos(x, y)
        tuile.setBrush(QBrush(Qt.color0))
        tuile.setFlag(QGraphicsItem.ItemIsMovable)
        tuile.setFlag(QGraphicsItem.ItemIsSelectable)
        mediatrice = QGraphicsRectItem(0,0,L_TUILE, H_TUILE / 40, parent=tuile)
        mediatrice.setPos(mediatrice.mapToParent(0,0).x(), mediatrice.mapToParent(0,0).y() + H_TUILE / 2 - H_TUILE / 80)
        brush = QBrush(Qt.black)
        mediatrice.setBrush(brush)
        tuileA = QGraphicsRectItem(0,0, H_TUILE / 2,H_TUILE / 2, parent=tuile)
        tuileA.setPos(tuileA.mapToParent(0,0).x(),tuileA.mapToParent(0,0).y())
        tuileA.setBrush(QBrush(Qt.color0))
        tuileB = QGraphicsRectItem(0,0, H_TUILE / 2,H_TUILE / 2, parent=tuile)
        tuileB.setPos(tuileB.mapToParent(0,0).x(), tuileB.mapToParent(0,0).y()+H_TUILE / 2)
        tuileB.setBrush(QBrush(Qt.color0))
        #x, y = x - D / 2, y - D / 3
        dx = -D / 2
        dy = -D / 3
        num = domino[0]
        if num == 0:
            pass
        elif num == 1:
            A1 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A1.setPos(A1.mapToParent(0,0).x() +dx+ L_TUILE / 2, A1.mapToParent(0,0).y()+dy + L_TUILE / 2)
            A1.setBrush(brush)
        elif num == 2:
            A1 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A1.setPos(A1.mapToParent(0,0).x()+dx + L_TUILE / 4, A1.mapToParent(0,0).y()+dy + L_TUILE / 4)
            A1.setBrush(brush)
            A2 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A2.setPos(A2.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A2.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4)
            A2.setBrush(brush)

        elif num == 3:
            A1 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A1.setPos(A1.mapToParent(0,0).x()+dx + L_TUILE / 4, A1.mapToParent(0,0).y()+dy + L_TUILE / 4)
            A1.setBrush(brush)
            A2 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A2.setPos(A2.mapToParent(0,0).x()+dx + L_TUILE * 2 / 4, A2.mapToParent(0,0).y()+dy + L_TUILE * 2 / 4)
            A2.setBrush(brush)
            A3 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A3.setPos(A3.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A3.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4)
            A3.setBrush(brush)

        elif num == 4:
            A1 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A1.setPos(A1.mapToParent(0,0).x()+dx + L_TUILE / 4, A1.mapToParent(0,0).y()+dy + L_TUILE / 4)
            A1.setBrush(brush)
            A2 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A2.setPos(A2.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A2.mapToParent(0,0).y()+dy + L_TUILE / 4)
            A2.setBrush(brush)
            A3 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A3.setPos(A3.mapToParent(0,0).x()+dx + L_TUILE * 1 / 4, A3.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4 )
            A3.setBrush(brush)
            A4 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A4.setPos(A4.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A4.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4)
            A4.setBrush(brush)

        elif num == 5:
            A1 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A1.setPos(A1.mapToParent(0,0).x()+dx + L_TUILE / 4, A1.mapToParent(0,0).y() +dy+ L_TUILE / 4)
            A1.setBrush(brush)
            A2 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A2.setPos(A2.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A2.mapToParent(0,0).y()+dy + L_TUILE / 4)
            A2.setBrush(brush)
            A3 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A3.setPos(A3.mapToParent(0,0).x()+dx + L_TUILE * 1 / 4, A3.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4)
            A3.setBrush(brush)
            A4 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A4.setPos(A4.mapToParent(0,0).x() +dx+ L_TUILE * 3 / 4, A4.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4)
            A4.setBrush(brush)
            A5 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A5.setPos(A5.mapToParent(0,0).x()+dx + L_TUILE * 2 / 4, A5.mapToParent(0,0).y()+dy + L_TUILE * 2 / 4)
            A5.setBrush(brush)

        elif num == 6:
            A1 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A1.setPos(A1.mapToParent(0,0).x()+dx + L_TUILE / 4, A1.mapToParent(0,0).y()+dy + L_TUILE / 4)
            A1.setBrush(brush)
            A2 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A2.setPos(A2.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A2.mapToParent(0,0).y()+dy + L_TUILE / 4)
            A2.setBrush(brush)
            A3 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A3.setPos(A3.mapToParent(0,0).x()+dx + L_TUILE * 1 / 4, A3.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4)
            A3.setBrush(brush)
            A4 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A4.setPos(A4.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A4.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4)
            A4.setBrush(brush)
            A5 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A5.setPos(A5.mapToParent(0,0).x()+dx + L_TUILE * 1 / 4, A5.mapToParent(0,0).y()+dy + L_TUILE * 2 / 4)
            A5.setBrush(brush)
            A6 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)
            A6.setPos(A6.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A6.mapToParent(0,0).y()+dy + L_TUILE * 2 / 4)
            A6.setBrush(brush)

        #y += H_TUILE / 2
        num = domino[1]

        if num == 0:
            pass
        elif num == 1:
            B1 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B1.setPos(B1.mapToParent(0, 0).x()+dx + L_TUILE / 2, B1.mapToParent(0, 0).y()+dy + L_TUILE / 2)
            B1.setBrush(brush)
        elif num == 2:
            B1 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B1.setPos(B1.mapToParent(0, 0).x()+dx + L_TUILE / 4, B1.mapToParent(0, 0).y()+dy + L_TUILE / 4)
            B1.setBrush(brush)
            B2 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B2.setPos(B2.mapToParent(0, 0).x()+dx + L_TUILE * 3 / 4, B2.mapToParent(0, 0).y()+dy + L_TUILE * 3 / 4)
            B2.setBrush(brush)

        elif num == 3:
            B1 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B1.setPos(B1.mapToParent(0, 0).x()+dx + L_TUILE / 4, B1.mapToParent(0, 0).y()+dy + L_TUILE / 4)
            B1.setBrush(brush)
            B2 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B2.setPos(B2.mapToParent(0, 0).x()+dx + L_TUILE * 2 / 4, B2.mapToParent(0, 0).y()+dy + L_TUILE * 2 / 4)
            B2.setBrush(brush)
            B3 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B3.setPos(B3.mapToParent(0, 0).x()+dx + L_TUILE * 3 / 4, B3.mapToParent(0, 0).y()+dy + L_TUILE * 3 / 4)
            B3.setBrush(brush)

        elif num == 4:
            B1 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B1.setPos(B1.mapToParent(0, 0).x()+dx + L_TUILE / 4, B1.mapToParent(0, 0).y()+dy + L_TUILE / 4)
            B1.setBrush(brush)
            B2 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B2.setPos(B2.mapToParent(0, 0).x()+dx + L_TUILE * 3 / 4, B2.mapToParent(0, 0).y()+dy + L_TUILE / 4)
            B2.setBrush(brush)
            B3 = QGraphicsEllipseItem(0,0, D, D, parent=tuileB)
            B3.setPos(B3.mapToParent(0, 0).x()+dx + L_TUILE * 1 / 4, B3.mapToParent(0, 0).y()+dy + L_TUILE * 3 / 4)
            B3.setBrush(brush)
            B4 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B4.setPos(B4.mapToParent(0, 0).x()+dx + L_TUILE * 3 / 4, B4.mapToParent(0, 0).y()+dy + L_TUILE * 3 / 4)
            B4.setBrush(brush)

        elif num == 5:
            B1 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B1.setPos(B1.mapToParent(0, 0).x()+dx + L_TUILE / 4, B1.mapToParent(0, 0).y() +dy+ L_TUILE / 4)
            B1.setBrush(brush)
            B2 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B2.setPos(B2.mapToParent(0, 0).x()+dx + L_TUILE * 3 / 4, B2.mapToParent(0, 0).y()+dy + L_TUILE / 4)
            B2.setBrush(brush)
            B3 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B3.setPos(B3.mapToParent(0, 0).x()+dx + L_TUILE * 1 / 4, B3.mapToParent(0, 0).y()+dy + L_TUILE * 3 / 4)
            B3.setBrush(brush)
            B4 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B4.setPos(B4.mapToParent(0, 0).x()+dx + L_TUILE * 3 / 4, B4.mapToParent(0, 0).y()+dy + L_TUILE * 3 / 4)
            B4.setBrush(brush)
            B5 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B5.setPos(B5.mapToParent(0, 0).x()+dx + L_TUILE * 2 / 4, B5.mapToParent(0, 0).y() +dy+ L_TUILE * 2 / 4)
            B5.setBrush(brush)

        elif num == 6:
            B1 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B1.setPos(B1.mapToParent(0, 0).x()+dx + L_TUILE / 4, B1.mapToParent(0, 0).y()+dy + L_TUILE / 4)
            B1.setBrush(brush)
            B2 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B2.setPos(B2.mapToParent(0, 0).x()+dx + L_TUILE * 3 / 4, B2.mapToParent(0, 0).y()+dy + L_TUILE / 4)
            B2.setBrush(brush)
            B3 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B3.setPos(B3.mapToParent(0, 0).x() +dx+ L_TUILE * 1 / 4, B3.mapToParent(0, 0).y() +dy+ L_TUILE * 3 / 4)
            B3.setBrush(brush)
            B4 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B4.setPos(B4.mapToParent(0, 0).x()+dx + L_TUILE * 3 / 4, B4.mapToParent(0, 0).y()+dy + L_TUILE * 3 / 4)
            B4.setBrush(brush)
            B5 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B5.setPos(B5.mapToParent(0, 0).x()+dx + L_TUILE * 1 / 4, B5.mapToParent(0, 0).y()+dy + L_TUILE * 2 / 4)
            B5.setBrush(brush)
            B6 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B6.setPos(B6.mapToParent(0, 0).x()+dx + L_TUILE * 3 / 4, B6.mapToParent(0, 0).y()+dy + L_TUILE * 2 / 4)
            B6.setBrush(brush)

        self.scene.addItem(tuile)
        tuile.setRotation(rot)


    def dessinerMains(self,plateau):
        main_j1, main_j2, pioche = plateau.generation(7)
        dx = 0
        for domino in main_j1:
            pos = [self.rectPlateau.rect().bottomLeft().x()+ dx, self.rectPlateau.rect().bottomLeft().y()+10]
            self.dessiner_Tuile(domino,pos)
            dx += 20 + L_TUILE
        dx = L_TUILE
        for domino in main_j2:
            pos = [self.rectPlateau.rect().bottomRight().x()- dx, self.rectPlateau.rect().bottomRight().y()+10]
            self.dessiner_Tuile(domino,pos)
            dx += 20 + L_TUILE

        joueurs = []
        joueurs.append(Joueur("Joueur 1", main_j1))
        joueurs.append(Joueur("Joueur 2", main_j2))
        return main_j1, main_j2

    #def dessinerPlateau(self):
    def reco_tuile(self,item):
        a,b = [0,0]
        tuileA = item.childItems()[1]
        tuileB = item.childItems()[2]
        a = len(tuileA.childItems())
        b = len(tuileB.childItems())
        return [a,b]

    def selectionner_main(self,joueur):
        path = QPainterPath()
        if joueur == 1:
            rect = QRectF(self.rectPlateau.rect().bottomLeft().x(), self.rectPlateau.rect().bottomLeft().y()+8, \
                          H_PLATEAU/2-10,L_TUILE+5)
        elif joueur == 2:
            rect = QRectF(self.rectPlateau.rect().bottomRight().x(), self.rectPlateau.rect().bottomRight().y()+8, \
                          -H_PLATEAU/2+10,L_TUILE+5)

        path.addRect(rect)
        self.scene.setSelectionArea(path)
        mains_items = self.scene.selectedItems()
        return mains_items

    def selectionner_plateau(self):
        path = QPainterPath()
        rect = QRectF(self.rectPlateau.rect())
        path.addRect(rect)
        self.scene.setSelectionArea(path)
        plateau_items = self.scene.selectedItems()
        return plateau_items

    def changerVue(self, i):
        if i == 1:
            self.vueMain.centerOn(self.rectPlateau.rect().bottomLeft().x(), self.rectPlateau.rect().bottomLeft().y()+10)
        elif i == 2:
            self.vueMain.centerOn(self.rectPlateau.rect().bottomRight().x(), self.rectPlateau.rect().bottomRight().y()+10)
        # if i == 1:
        #     self.vueMain.centerOn(-L_PLATEAU/2 -300, H_PLATEAU/2+30)
        # elif i == 2:
        #     self.vueMain.centerOn(L_PLATEAU/2 +300, H_PLATEAU/2 + 30)


    def jouer(self,item1,item2):
        rectPlateau = self.rectPlateau
        [a,b] = self.reco_tuile(item1)
        c,d = self.reco_tuile(item2)
        print(a,b)
        print(c,d)
        print(item1)
        tuileA1 = item1.childItems()[1]
        tuileB1 = item1.childItems()[2]
        tuileA2 = item2.childItems()[1]
        tuileB2 = item2.childItems()[2]
        print("start")
        if a==c:
            pos1 = item1.scenePos()
            print(pos1)
            pos2 = item2.scenePos()
            print(pos2)
            vect = pos2-pos1
            print(vect)
            item1.setPos(item1.scenePos()+vect)




    def get_coord(self,item):
        pos = item.mapToScene(self.rectPlateau.rect().center())
        return pos

    def item2global_pos(self,item):
        sceneP = item.mapToScene(item.boundingRect().center())
        viewP = self.vuePlateau.mapFromScene(sceneP)
        sendPos = self.vuePlateau.viewport().mapToGlobal(viewP)
        return sendPos

    def global2item_pos(self,pos):
        viewP = self.vuePlateau.viewport().mapFromGlobal(pos)
        sceneP = self.rectPlateau.mapToScene(viewP)
        item_pos = self.rectPlateau.mapFromScene(self.rectPlateau.boundingRect().center())

    @pyqtSlot()
    def on_pushButtonJoueur1_clicked(self):
        self.changerVue(1)
        print("joueur 1")

    @pyqtSlot()
    def on_pushButtonJoueur2_clicked(self):
        self.changerVue(2)
        print("joueur 2")

    @pyqtSlot()
    def on_pushButtonTourner_clicked(self):
        itemsSelectionnes = self.scene.selectedItems()
        item = itemsSelectionnes[0]
        item.setTransformOriginPoint(item.boundingRect().center())
        item.setRotation(item.rotation()+90)
        print("je tourne")

    @pyqtSlot()
    def on_pushButtonJouer_clicked(self):
        itemsSelectionnes = self.scene.selectedItems()
        print(itemsSelectionnes)
        if len(itemsSelectionnes)>0:
            print("button")

            item1 = itemsSelectionnes[0]
            item2 = itemsSelectionnes[1]
            print(self.item2global_pos(item1))
            print("coord",self.get_coord(item1))
            for item in itemsSelectionnes:
                print(self.reco_tuile(item))
            self.jouer(item1,item2)


    @pyqtSlot()
    def on_pushButtonNouvellePartie_clicked(self):
        self.close()
        self.__init__()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
