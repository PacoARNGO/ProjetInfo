# -*- coding: utf-8 -*-
# scene.py
# integration avec les widgets

import sys

from GraphicGame.interface.joueurs import Joueur
from game import Ui_MainWindow
from PyQt5.QtCore import Qt, pyqtSlot, QPointF, QRectF, QSize
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
        self.zoomPctVue = 1
        self.k = 0
        self.setupUi(self)
        self.scene = QGraphicsScene()
        self.plateau = Plateau()
        self.tour = Tour(self.plateau)
        self._joueurs = [Joueur("Joueur 1"), Joueur("Joueur 2")]  # Liste des joueurs
        self.choix = None
        #self.scene.setSceneRect(0,0,H_PLATEAU,L_PLATEAU)
        self.remplirScene()

        self.show()

        for vue in (self.vuePlateau, self.vueMain):
            vue.setScene(self.scene)
            vue.setRenderHints(QPainter.Antialiasing)
            if vue == self.vuePlateau:
                vue.fitInView(self.rectPlateau, Qt.KeepAspectRatio)
        self.vueMain.centerOn(self.rectPlateau.rect().center())
        self.vueMain.scale(1,1.25)

    @property
    def joueurs(self):
        return self._joueurs

    def remplirScene(self):
        global H_PLATEAU
        global L_PLATEAU
        scene = self.scene
        rectPlateau = scene.addRect(0, 0, H_PLATEAU, L_PLATEAU, brush=QBrush(Qt.lightGray))
        self.rectPlateau = rectPlateau
        self.plateau.bienvenue()
        self.dessinerMains(self.plateau)




        self.texte = scene.addText("Domino's game \n"\
                                   "by Antoine&Paco\n"\
                                      "\n"\
                                   "Jouer en mode 2 joueurs\n"
                                   "Pour Jouer: sélectionner un domino dans la main du joueur,\n"\
                                   "puis sélectionner (Ctr+clic) un domino \n"
                                   " sur le plateau et appuyer sur Jouer\n"
                                   "Tourner le domino avant de le bouger \n"
                                   "pour l'ajuster à la place imaginée sur le plateau")
        self.texte.setPos(QPointF(L_PLATEAU/4, H_PLATEAU/4))
        self.texte.setDefaultTextColor(Qt.black)
        scene.addItem(self.texte)


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
        tuiles = plateau.generation(7)
        main_j1, main_j2, pioche = tuiles
        self.plateau.pioche = pioche
        self.joueurs[0].pieces = main_j1
        self.joueurs[1].pieces = main_j2
        self.k = self.plateau.premier_joueur(main_j1, main_j2)
        k = self.k
        print(f"{self.joueurs[k].nom} - Choisissez, si possible, un double le plus élevé possible : ")
        print('------------------------------------------------------- \n')

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

    def afficher_selection(self,dominos):
        for item in dominos:
            print(self.reco_tuile(item))

    def changerVue(self, i):
        if i == 1:
            self.vueMain.centerOn(self.rectPlateau.rect().bottomLeft().x(), self.rectPlateau.rect().bottomLeft().y()+10)
        elif i == 2:
            self.vueMain.centerOn(self.rectPlateau.rect().bottomRight().x(), self.rectPlateau.rect().bottomRight().y()+10)
        elif i == 3:
            self.vueMain.centerOn(self.rectPlateau.rect().center())

    def premier_tour(self,item):
        a,b = self.reco_tuile(item)
        item.setPos(self.rectPlateau.rect().center())
        self.choix = [a,b]
        joueur1 = self.joueurs[0]
        joueur2 = self.joueurs[1]
        self.k = self.plateau.premier_joueur(joueur1.pieces,joueur2.pieces)  # k est l'indice du joueur commencant la partie (plus grand double)
        self.plateau.plateau = self.tour.mise_en_jeu(self.plateau.plateau, self.joueurs, self.k,
                                                self.choix)  # On met les pièces sur le plateau
        self.changerVue(3)
        self.scene.removeItem(self.texte)


    def jouer(self,item1,item2):
        [a,b] = self.reco_tuile(item1)
        c,d = self.reco_tuile(item2)
        rot = item1.rotation()
        item1.setRotation(0)
        pos1 = item1.scenePos()
        pos2 = item2.scenePos()
        vect = pos2 - pos1
        pos1 = item1.scenePos()
        pos2 = item2.scenePos()
        vect = pos2 - pos1
        if a == b:
            equal = True
        if a==c:
            point = QPointF(0,-5)
            if rot == 0:
                point = QPointF(0, 10+H_TUILE)
            elif rot == 90:
                point += QPointF(L_TUILE,-L_TUILE)
            elif rot == 180:
                point += QPointF(L_TUILE,0)
            elif rot == 270:
                point += QPointF(0,0)
        elif a == d:
            #pareil qu'au dessus
            point = QPointF(0,5)
            if rot == 0:
                point = QPointF(0,H_TUILE)
            elif rot == 90:
                point += QPointF(L_TUILE, -L_TUILE)
            elif rot == 180:
                point += QPointF(L_TUILE, 0)
            elif rot == 270:
                point += QPointF(0, H_TUILE+L_TUILE)
        elif b == c:
            point = QPointF(0, -5)
            if rot == 0:
                point += QPointF(0, -H_TUILE)
            elif rot == 90:
                point += QPointF(L_TUILE, -L_TUILE)
            elif rot == 180:
                point += QPointF(0, 2*H_TUILE)
            elif rot == 270:
                point += QPointF(0, L_TUILE)

        elif b == d:
            #pareil qu'au dessus
            point = QPointF(0,5)
            if rot == 90:
                point += QPointF(H_TUILE, H_TUILE)
            if rot == 180:
                point += QPointF(L_TUILE,H_TUILE+ L_TUILE)
            if rot == 270:
                point += QPointF(0, H_TUILE+L_TUILE)

        item1.setPos(item1.scenePos() + vect + point)
        item1.setTransformOriginPoint(item1.boundingRect().topLeft())
        item1.setRotation(rot)
        self.afficher_selection(self.selectionner_plateau())


    def tour_suivant(self):
        joueur_suivant = self.joueurs[self.k%2]
        print(self.tour)
        print(self.plateau)
        print(joueur_suivant)
        self.changerVue(3)
        self.k += 1





    def get_coord(self,item):
        pos = item.mapToScene(self.rectPlateau.rect().center())
        return pos

    @pyqtSlot(int)
    def on_horizontalSliderZoom_valueChanged(self,nouvZoomPctVue):
        f = (nouvZoomPctVue/100.) / self.zoomPctVue
        self.vuePlateau.scale(f,f)
        self.vuePlateau.centerOn(self.rectPlateau.rect().center())
        self.zoomPctVue = nouvZoomPctVue/100.

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
            if len(itemsSelectionnes)==2:
                for item in itemsSelectionnes:
                    if item in self.selectionner_main(1) or item in self.selectionner_main(2):
                        item1 = itemsSelectionnes.pop(itemsSelectionnes.index(item))
                        self.choix = self.reco_tuile(item1)
                        print(self.choix)
                item2 = itemsSelectionnes.pop(0)
                self.jouer(item1,item2)
                self.tour_suivant()
            elif len(itemsSelectionnes)==1 and len(self.plateau.plateau)<=1:
                item = itemsSelectionnes[0]
                self.premier_tour(item)
                self.tour_suivant()







    @pyqtSlot()
    def on_pushButtonNouvellePartie_clicked(self):
        self.close()
        self.__init__()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
