# -*- coding: utf-8 -*-
# scene.py
# integration avec les widgets

import sys

from joueurs import Joueur
from game import Ui_MainWindow
from PyQt5.QtCore import Qt, pyqtSlot, QPointF, QRectF, QSize
from PyQt5.QtGui import QBrush, QPen, QPainter, QTransform, QPainterPath
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QGraphicsScene, QGraphicsView, QGraphicsItem, QDialog, \
    QGraphicsEllipseItem, QColorDialog, QGraphicsItemGroup, QGraphicsRectItem
from VariablesEtConstantes import *
from plateau import Plateau
from tour import Tour


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Cette classe hérite de QMainWindow et de Ui_MainWindow
    permettant de créer une fenêtre principale à partir de Qt Designer
    et d'intégrer les widgets de la fenêtre principale pour interagir
    avec l'utilisateur
    """
    def __init__(self, parent=None):
        """
        Constructeur de la classe MainWindow
        :param parent:
        """
        super(MainWindow, self).__init__(parent)
        self.zoomPctVue = 1 # zoom par défaut
        self.k = 0  # indice du joueur courant
        self.setupUi(self)  # initialisation de la fenêtre principale
        self.scene = QGraphicsScene()   # création de la scène
        self.plateau = Plateau()    # création du plateau
        self.tour = Tour(self.plateau)  # création du tour
        self._joueurs = [Joueur("Joueur 1"), Joueur("Joueur 2")]  # Liste des joueurs
        self.choix = None   # choix du joueur
        self.remplirScene() # remplissage de la scène

        self.show() # affichage de la fenêtre principale

        for vue in (self.vuePlateau, self.vueMain):
            vue.setScene(self.scene)    # association de la scène à la vue
            vue.setRenderHints(QPainter.Antialiasing)   # activation de l'antialiasing
            if vue == self.vuePlateau:
                vue.fitInView(self.rectPlateau, Qt.KeepAspectRatio) # ajustement de la vue
        self.vueMain.centerOn(self.rectPlateau.rect().center()) # centrer la vue sur le plateau
        self.vueMain.scale(1,1.25)  # zoomer la vue sur le plateau

    @property
    def joueurs(self):
        """
        Getter de la liste des joueurs
        :return: liste des joueurs
        """
        return self._joueurs

    def remplirScene(self):
        """
        Méthode permettant de remplir la scène avec le plateau,
        les consignes d'accueil et les mains des joueurs
        :return:
        """
        scene = self.scene  # récupération de la scène
        rectPlateau = scene.addRect(0, 0, H_PLATEAU, L_PLATEAU, brush=QBrush(Qt.lightGray)) # création du plateau
        self.rectPlateau = rectPlateau  # association du rectangle au plateau
        self.plateau.bienvenue()    # affichage des consignes d'accueil
        self.dessinerMains(self.plateau)    # affichage des mains des joueurs




        self.texte = scene.addText("Domino's game \n"\
                                   "by Antoine&Paco\n"\
                                      "\n"\
                                   "Jouer en mode 2 joueurs\n"
                                   "Pour Jouer: sélectionner un domino dans la main du joueur,\n"\
                                   "puis sélectionner (Ctr+clic) un domino \n"
                                   " sur le plateau et appuyer sur Jouer\n"
                                   "Tourner le domino avant de le bouger \n"
                                   "pour l'ajuster à la place imaginée sur le plateau") # affichage du texte d'accueil
        self.texte.setPos(QPointF(L_PLATEAU/4, H_PLATEAU/4))    # positionnement du texte d'accueil
        self.texte.setDefaultTextColor(Qt.black)    # couleur du texte d'accueil
        scene.addItem(self.texte)   # ajout du texte d'accueil à la scène


    def dessiner_Tuile(self, domino, pos, rot = 0):
        """
        Méthode permettant de dessiner une tuile sur la scène
        :param domino: list  # tuile à dessiner
        :param pos: QPointF, list # position de la tuile
        :param rot: float # angle de rotation de la tuile
        :return:
        """

        try:    # test récupération de la tuile
            x, y = pos[0], pos[1]
        except:
            x, y = pos.x(), pos.y()

        tuile = QGraphicsRectItem(0, 0, L_TUILE, H_TUILE,parent=self.rectPlateau)   # création de la tuile
        tuile.setPos(x, y)  # positionnement de la tuile
        tuile.setBrush(QBrush(Qt.color0))   # couleur de la tuile
        tuile.setFlag(QGraphicsItem.ItemIsMovable)  # activation de la possibilité de déplacement de la tuile
        tuile.setFlag(QGraphicsItem.ItemIsSelectable)   # activation de la possibilité de sélection de la tuile
        mediatrice = QGraphicsRectItem(0,0,L_TUILE, H_TUILE / 40, parent=tuile)  # création de la médiatrice du domino
        mediatrice.setPos(mediatrice.mapToParent(0,0).x(), mediatrice.mapToParent(0,0).y() + H_TUILE / 2 - H_TUILE / 80)    # positionnement de la médiatrice
        brush = QBrush(Qt.black)    # couleur de la médiatrice
        mediatrice.setBrush(brush)  # affectation de la médiatrice à la tuile
        tuileA = QGraphicsRectItem(0,0, H_TUILE / 2,H_TUILE / 2, parent=tuile)  # création du rectangle A de la tuile
        tuileA.setPos(tuileA.mapToParent(0,0).x(),tuileA.mapToParent(0,0).y())  # positionnement du rectangle A
        tuileA.setBrush(QBrush(Qt.color0))  # couleur du rectangle A
        tuileB = QGraphicsRectItem(0,0, H_TUILE / 2,H_TUILE / 2, parent=tuile)  # création du rectangle B de la tuile
        tuileB.setPos(tuileB.mapToParent(0,0).x(), tuileB.mapToParent(0,0).y()+H_TUILE / 2) # positionnement du rectangle B
        tuileB.setBrush(QBrush(Qt.color0))  # couleur du rectangle B

        dx = -D / 2  # décalage des points des dominos
        dy = -D / 3 # décalage des points des dominos
        num = domino[0]     # récupération de la partie haute (A) de la tuile
        if num == 0:    # test si la partie haute est 0
            pass
        elif num == 1:  # test si la partie haute est 1
            A1 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A1
            A1.setPos(A1.mapToParent(0,0).x() +dx+ L_TUILE / 2, A1.mapToParent(0,0).y()+dy + L_TUILE / 2)   # positionnement du point A1
            A1.setBrush(brush)  # couleur du point A1
        elif num == 2:  # test si la partie haute est 2
            A1 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A1
            A1.setPos(A1.mapToParent(0,0).x()+dx + L_TUILE / 4, A1.mapToParent(0,0).y()+dy + L_TUILE / 4)   # positionnement du point A1
            A1.setBrush(brush)  # couleur du point A1
            A2 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A2
            A2.setPos(A2.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A2.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4)   # positionnement du point A2
            A2.setBrush(brush)  # couleur du point A2

        elif num == 3:  # test si la partie haute est 3
            A1 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A1
            A1.setPos(A1.mapToParent(0,0).x()+dx + L_TUILE / 4, A1.mapToParent(0,0).y()+dy + L_TUILE / 4)   # positionnement du point A1
            A1.setBrush(brush)  # couleur du point A1
            A2 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A2
            A2.setPos(A2.mapToParent(0,0).x()+dx + L_TUILE * 2 / 4, A2.mapToParent(0,0).y()+dy + L_TUILE * 2 / 4)   # positionnement du point A2
            A2.setBrush(brush)  # couleur du point A2
            A3 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A3
            A3.setPos(A3.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A3.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4)   # positionnement du point A3
            A3.setBrush(brush)  # couleur du point A3

        elif num == 4:  # test si la partie haute est 4
            A1 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A1
            A1.setPos(A1.mapToParent(0,0).x()+dx + L_TUILE / 4, A1.mapToParent(0,0).y()+dy + L_TUILE / 4)   # positionnement du point A1
            A1.setBrush(brush)  # couleur du point A1
            A2 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A2
            A2.setPos(A2.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A2.mapToParent(0,0).y()+dy + L_TUILE / 4)   # positionnement du point A2
            A2.setBrush(brush)  # couleur du point A2
            A3 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A3
            A3.setPos(A3.mapToParent(0,0).x()+dx + L_TUILE * 1 / 4, A3.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4 )  # positionnement du point A3
            A3.setBrush(brush)  # couleur du point A3
            A4 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A4
            A4.setPos(A4.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A4.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4)   # positionnement du point A4
            A4.setBrush(brush)  # couleur du point A4

        elif num == 5:  # test si la partie haute est 5
            A1 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A1
            A1.setPos(A1.mapToParent(0,0).x()+dx + L_TUILE / 4, A1.mapToParent(0,0).y() +dy+ L_TUILE / 4)   # positionnement du point A1
            A1.setBrush(brush)  # couleur du point A1
            A2 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A2
            A2.setPos(A2.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A2.mapToParent(0,0).y()+dy + L_TUILE / 4)   # positionnement du point A2
            A2.setBrush(brush)  # couleur du point A2
            A3 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A3
            A3.setPos(A3.mapToParent(0,0).x()+dx + L_TUILE * 1 / 4, A3.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4)   # positionnement du point A3
            A3.setBrush(brush)  # couleur du point A3
            A4 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A4
            A4.setPos(A4.mapToParent(0,0).x() +dx+ L_TUILE * 3 / 4, A4.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4)   # positionnement du point A4
            A4.setBrush(brush)  # couleur du point A4
            A5 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A5
            A5.setPos(A5.mapToParent(0,0).x()+dx + L_TUILE * 2 / 4, A5.mapToParent(0,0).y()+dy + L_TUILE * 2 / 4)   # positionnement du point A5
            A5.setBrush(brush)  # couleur du point A5

        elif num == 6:  # test si la partie haute est 6
            A1 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A1
            A1.setPos(A1.mapToParent(0,0).x()+dx + L_TUILE / 4, A1.mapToParent(0,0).y()+dy + L_TUILE / 4)   # positionnement du point A1
            A1.setBrush(brush)  # couleur du point A1
            A2 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A2
            A2.setPos(A2.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A2.mapToParent(0,0).y()+dy + L_TUILE / 4)   # positionnement du point A2
            A2.setBrush(brush)  # couleur du point A2
            A3 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A3
            A3.setPos(A3.mapToParent(0,0).x()+dx + L_TUILE * 1 / 4, A3.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4)   # positionnement du point A3
            A3.setBrush(brush)  # couleur du point A3
            A4 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A4
            A4.setPos(A4.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A4.mapToParent(0,0).y()+dy + L_TUILE * 3 / 4)   # positionnement du point A4
            A4.setBrush(brush)  # couleur du point A4
            A5 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A5
            A5.setPos(A5.mapToParent(0,0).x()+dx + L_TUILE * 1 / 4, A5.mapToParent(0,0).y()+dy + L_TUILE * 2 / 4)   # positionnement du point A5
            A5.setBrush(brush)  # couleur du point A5
            A6 = QGraphicsEllipseItem(0,0,D, D, parent=tuileA)  # création du point A6
            A6.setPos(A6.mapToParent(0,0).x()+dx + L_TUILE * 3 / 4, A6.mapToParent(0,0).y()+dy + L_TUILE * 2 / 4)   # positionnement du point A6
            A6.setBrush(brush)  # couleur du point A6


        num = domino[1] # récupération du numéro de la partie basse de la tuile

        if num == 0:    # test si la partie basse est 0
            pass
        elif num == 1:  # test si la partie basse est 1
            B1 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B1.setPos(B1.mapToParent(0, 0).x()+dx + L_TUILE / 2, B1.mapToParent(0, 0).y()+dy + L_TUILE / 2)
            B1.setBrush(brush)
        elif num == 2:  # test si la partie basse est 2
            B1 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B1.setPos(B1.mapToParent(0, 0).x()+dx + L_TUILE / 4, B1.mapToParent(0, 0).y()+dy + L_TUILE / 4)
            B1.setBrush(brush)
            B2 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B2.setPos(B2.mapToParent(0, 0).x()+dx + L_TUILE * 3 / 4, B2.mapToParent(0, 0).y()+dy + L_TUILE * 3 / 4)
            B2.setBrush(brush)

        elif num == 3:  # test si la partie basse est 3
            B1 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B1.setPos(B1.mapToParent(0, 0).x()+dx + L_TUILE / 4, B1.mapToParent(0, 0).y()+dy + L_TUILE / 4)
            B1.setBrush(brush)
            B2 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B2.setPos(B2.mapToParent(0, 0).x()+dx + L_TUILE * 2 / 4, B2.mapToParent(0, 0).y()+dy + L_TUILE * 2 / 4)
            B2.setBrush(brush)
            B3 = QGraphicsEllipseItem(0, 0, D, D, parent=tuileB)
            B3.setPos(B3.mapToParent(0, 0).x()+dx + L_TUILE * 3 / 4, B3.mapToParent(0, 0).y()+dy + L_TUILE * 3 / 4)
            B3.setBrush(brush)

        elif num == 4:  # test si la partie basse est 4
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

        elif num == 5:  # test si la partie basse est 5
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

        elif num == 6:  # test si la partie basse est 6
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

        self.scene.addItem(tuile)   # ajout de la tuile dans la scene
        tuile.setRotation(rot)    # rotation de la tuile


    def dessinerMains(self,plateau):
        """
        Dessine les mains des joueurs
        :param plateau: objet Plateau
        :return:
        """
        tuiles = plateau.generation(7)  # génération des tuiles
        main_j1, main_j2, pioche = tuiles   # déclaration des mains des joueurs
        self.plateau.pioche = pioche    # ajout de la pioche dans le plateau
        self.joueurs[0].pieces = main_j1    # ajout des mains des joueurs dans leur liste de pièces
        self.joueurs[1].pieces = main_j2    # ajout des mains des joueurs dans leur liste de pièces
        self.k = self.plateau.premier_joueur(main_j1, main_j2)  # détermination du premier joueur
        k = self.k  # définition de la variable k du premier joueur
        print(f"{self.joueurs[k].nom} - Choisissez, si possible, un double le plus élevé possible : ")
        print('------------------------------------------------------- \n')

        dx = 0
        for domino in main_j1:  # placement de la main du joueur 1
            pos = [self.rectPlateau.rect().bottomLeft().x()+ dx, self.rectPlateau.rect().bottomLeft().y()+10]
            self.dessiner_Tuile(domino,pos)
            dx += 20 + L_TUILE
        dx = L_TUILE
        for domino in main_j2:  # placement de la main du joueur 2
            pos = [self.rectPlateau.rect().bottomRight().x()- dx, self.rectPlateau.rect().bottomRight().y()+10]
            self.dessiner_Tuile(domino,pos)
            dx += 20 + L_TUILE
        return main_j1, main_j2

    def reco_tuile(self,item, a = 0, b = 0):
        """
        Recherche la tuile correspondant à l'item
        :param item: QGraphicsItem
        :return:
        """
        tuileA = item.childItems()[1]   # tuile A
        tuileB = item.childItems()[2]   # tuile B
        a = len(tuileA.childItems())    # nombre de points trouvés sur tuile A
        b = len(tuileB.childItems())    # nombre de points trouvés sur la tuile B
        return [a,b]

    def selectionner_main(self,joueur):
        """
        Permet de sélectionner la main du joueur
        :param joueur: objet Joueur
        :return:
        """
        path = QPainterPath()   # création du chemin
        if joueur == 1: # si le joueur est le joueur 1
            rect = QRectF(self.rectPlateau.rect().bottomLeft().x(), self.rectPlateau.rect().bottomLeft().y()+8, \
                          H_PLATEAU/2-10,L_TUILE+5) # création du rectangle de sélection
        elif joueur == 2:   # si le joueur est le joueur 2
            rect = QRectF(self.rectPlateau.rect().bottomRight().x(), self.rectPlateau.rect().bottomRight().y()+8, \
                          -H_PLATEAU/2+10,L_TUILE+5)    # création du rectangle de sélection

        path.addRect(rect)  # ajout du rectangle dans le chemin
        self.scene.setSelectionArea(path)   # sélection de la zone
        mains_items = self.scene.selectedItems()    # récupération des items sélectionnés
        return mains_items

    def selectionner_plateau(self):
        """
        Permet de sélectionner le plateau
        :return:
        """
        path = QPainterPath()   # création du chemin
        rect = QRectF(self.rectPlateau.rect())  # création du rectangle de sélection
        path.addRect(rect)  # ajout du rectangle dans le chemin
        self.scene.setSelectionArea(path)   # sélection de la zone
        plateau_items = self.scene.selectedItems()  # récupération des items sélectionnés
        return plateau_items

    def afficher_selection(self,dominos):
        """
        Permet d'afficher les dominos sélectionnés
        :param dominos:
        :return:
        """
        for item in dominos:    # pour chaque item sélectionné
            print(self.reco_tuile(item))    # affichage de la tuile correspondante

    def changerVue(self, i):
        """
        Permet de changer de vue
        :param i:
        :return:
        """
        if i == 1:  # si la vue est la vue du joueur 1
            self.vueMain.centerOn(self.rectPlateau.rect().bottomLeft().x(), self.rectPlateau.rect().bottomLeft().y()+10)
        elif i == 2:    # si la vue est la vue du joueur 2
            self.vueMain.centerOn(self.rectPlateau.rect().bottomRight().x(), self.rectPlateau.rect().bottomRight().y()+10)
        elif i == 3:    # si la vue est la vue du plateau
            self.vueMain.centerOn(self.rectPlateau.rect().center())

    def premier_tour(self,item):
        """
        Permet de lancer le premier tour du jeu
        :param item: QGraphicsItem
        :return:
        """
        a,b = self.reco_tuile(item)   # récupération de la valeur de la tuile
        item.setPos(self.rectPlateau.rect().center())       # déplacement de la tuile sur le plateau
        self.choix = [a,b]  # définition de la valeur de la tuile choisie dans la variable choix
        joueur1 = self.joueurs[0]   # définition du joueur 1
        joueur2 = self.joueurs[1]       # définition du joueur 2
        self.k = self.plateau.premier_joueur(joueur1.pieces,joueur2.pieces)  # détermination du premier joueur
        self.plateau.plateau = self.tour.mise_en_jeu(self.plateau.plateau, self.joueurs, self.k,
                                                self.choix)  # On met les pièces sur le plateau
        self.changerVue(3)  # on change de vue
        self.scene.removeItem(self.texte)   # on supprime le texte


    def jouer(self,item1,item2):
        """
        Pose la tuile sélectionner dans la main du joueur
        pour la poser sur le plateau
        :param item1: QGraphicsItem
        :param item2: QGraphicsItem
        :return:
        """
        [a,b] = self.reco_tuile(item1)  # récupération de la valeur de la tuile
        c,d = self.reco_tuile(item2)    # récupération de la valeur de la tuile
        rot1 = item1.rotation() # récupération de la rotation de la tuile 1
        rot2 = item2.rotation() # récupération de la rotation de la tuile 2
        item1.setRotation(0)    # rotation de la tuile 1 à 0
        pos1 = item1.scenePos() # récupération de la position de la tuile 1
        pos2 = item2.scenePos() # récupération de la position de la tuile 2
        vect = pos2 - pos1  # définition du vecteur


        if rot2 == 0:   # si la rotation de la tuile 2 est à 0
            rot = rot1  # rotation de la tuile 1
            if a==c:    # si les valeurs de la tuile 1 et 2 sont les mêmes
                point = QPointF(0,-5)   # définition du point
                if rot == 0:    # si la rotation de la tuile 1 est à 0
                    point = QPointF(0, 10+H_TUILE)  # définition du point
                elif rot == 90:
                    point += QPointF(L_TUILE,-L_TUILE)
                elif rot == 180:
                    point += QPointF(L_TUILE,0)
                elif rot1 == 270:
                    point += QPointF(0,0)
            elif a == d:
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
                    point += QPointF(H_TUILE, -L_TUILE)
                elif rot == 180:
                    point += QPointF(0, 2*H_TUILE)
                elif rot == 270:
                    point += QPointF(0, L_TUILE)

            elif b == d:
                point = QPointF(0,5)
                if rot == 90:
                    point += QPointF(H_TUILE, H_TUILE)
                if rot == 180:
                    point += QPointF(L_TUILE,H_TUILE+ L_TUILE)
                if rot == 270:
                    point += QPointF(0, H_TUILE+L_TUILE)

            item1.setPos(item1.scenePos() + vect + point)   # déplacement de la tuile 1
            item1.setTransformOriginPoint(item1.boundingRect().topLeft())   # définition du point d'origine de la transformation
            item1.setRotation(rot1) # rotation de la tuile 1 à sa valeur initiale

        elif rot2 == 90:
            item2.setRotation(0)
            if rot1 ==0:
                rot = rot2
                if a==c:
                    point = QPointF(0,-5)
                    if rot == 0:
                        point = QPointF(0, 10+H_TUILE)
                    elif rot == 90:
                        point += QPointF(L_TUILE,-L_TUILE)
                    elif rot == 180:
                        point += QPointF(L_TUILE,0)
                    elif rot1 == 270:
                        point += QPointF(0,0)
                elif a == d:
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
                        point += QPointF(5, -L_TUILE +5)
                    elif rot == 180:
                        point += QPointF(0, 2*H_TUILE)
                    elif rot == 270:
                        point += QPointF(0, L_TUILE)

                elif b == d:
                    point = QPointF(0,5)
                    if rot == 90:
                        point += QPointF(H_TUILE, H_TUILE)
                    if rot == 180:
                        point += QPointF(L_TUILE,H_TUILE+ L_TUILE)
                    if rot == 270:
                        point += QPointF(0, H_TUILE+L_TUILE)

            item2.setTransformOriginPoint(item2.boundingRect().topLeft())
            item2.setRotation(rot2)
            item1.setPos(item1.scenePos() + vect + point)
            item1.setTransformOriginPoint(item1.boundingRect().topLeft())
            item1.setRotation(rot1)

        self.afficher_selection(self.selectionner_plateau())


    def tour_suivant(self):
        """
        Prépare le plateau pour le tour suivant
        :return:
        """
        joueur_suivant = self.joueurs[self.k%2] # récupération du joueur suivant
        print(self.tour)    # affichage du tour
        print(self.plateau) # affichage du plateau
        print(joueur_suivant)   # affichage du joueur suivant
        self.changerVue(3)  # changement de la vue
        self.k += 1 # incrémentation de la variable k




    def pop_msgbox(self, msg):

        msgbox= QDialog.QMessageBox()
        msgbox.setText(msg)
        msgbox.setStandardButtons(QDialog.QMessageBox.Yes | QDialog.QMessageBox.No)
        msgbox.setDefaultButton(QDialog.QMessageBox.Yes)
        ret = msgbox.exec_()


    def get_coord(self,item):
        pos = item.mapToScene(self.rectPlateau.rect().center())
        return pos

    @pyqtSlot(int)
    def on_horizontalSliderZoom_valueChanged(self,nouvZoomPctVue):
        """
        Zoom sur le plateau
        :param nouvZoomPctVue:
        :return:
        """
        f = (nouvZoomPctVue/100.) / self.zoomPctVue # calcul du facteur de zoom
        self.vuePlateau.scale(f,f)  # zoom sur la vue
        self.vuePlateau.centerOn(self.rectPlateau.rect().center())  # centrer la vue sur le centre du plateau
        self.zoomPctVue = nouvZoomPctVue/100.   # mise à jour du zoom

    @pyqtSlot()
    def on_pushButtonJoueur1_clicked(self):
        """
        Affiche la main du joueur 1
        :return:
        """
        self.changerVue(1)  # changement de la vue
        print("joueur 1")

    @pyqtSlot()
    def on_pushButtonJoueur2_clicked(self):
        """
        Affiche la main du joueur 2
        :return:
        """
        self.changerVue(2)  # changement de la vue
        print("joueur 2")

    @pyqtSlot()
    def on_pushButtonTourner_clicked(self):
        """
        Tourne la tuile sélectionnée
        :return:
        """
        itemsSelectionnes = self.scene.selectedItems()  # récupération des items sélectionnés
        item = itemsSelectionnes[0] # récupération du premier item sélectionné
        item.setTransformOriginPoint(item.boundingRect().center())
        item.setRotation(item.rotation()+90)    # rotation de la tuile
        print("je tourne")

    @pyqtSlot()
    def on_pushButtonJouer_clicked(self):
        """
        Joue la tuile sélectionnée dans la main du joueur
        et lance la pose de la tuile près de l'autre tuile
        sélectionnée
        :return:
        """
        itemsSelectionnes = self.scene.selectedItems()  # récupération des items sélectionnés
        print(itemsSelectionnes)    # affichage des items sélectionnés
        if len(itemsSelectionnes)>0:    # si un item est sélectionné
            print("button")
            if len(itemsSelectionnes)==2:   # si deux items sont sélectionnés
                for item in itemsSelectionnes:  # pour chaque item sélectionné
                    if item in self.selectionner_main(1) or item in self.selectionner_main(2):      # si l'item est dans la main d'un joueur
                        i = itemsSelectionnes.index(item)   # récupération de l'index de l'item
                        item1 = itemsSelectionnes.pop(i)    # suppression de l'item de la liste et récupération de l'item
                        self.choix = self.reco_tuile(item1) # récupération de la tuile correspondante
                        print(self.choix)
                item2 = itemsSelectionnes.pop(0)    # suppression de l'item de la liste et récupération de l'item
                self.jouer(item1,item2)   # jouer la tuile
                self.tour_suivant() # lancer le tour suivant
                self.joueurs[self.k].pieces.pop(self.joueurs[self.k].pieces.index(self.choix))   # suppression de la tuile de la main du joueur
            elif len(itemsSelectionnes)==1 and len(self.plateau.plateau)<=1:    # si un item est sélectionné et que le plateau est vide
                item = itemsSelectionnes[0] # récupération de l'item sélectionné
                self.premier_tour(item) # pose de la première tuile
                self.tour_suivant() # lancer le tour suivant



    @pyqtSlot()
    def on_pushButtonNouvellePartie_clicked(self):
        """
        Crée une nouvelle partie
        :return:
        """
        self.close()    # fermeture de la fenêtre
        self.__init__() # réinitialisation de la fenêtre



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
