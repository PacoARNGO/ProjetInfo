import numpy as np
from plateau import *

"""
Ce module contient la définition de la classe Joueur servant à gérer le comportement des joueurs
"""

class Joueur():
    '''
    Classe définissant les attributs d'un joueur
    '''
    def __init__(self, nom, main, passer_la_main=0,ordi=0):
        self.nom = nom
        self.pieces = main
        self.passer_la_main = passer_la_main
        self.ordi = ordi


    def __str__(self):
        return f"{self.nom} - pièces : \n"+\
                str(self.pieces) if self.ordi==0 else f"{self.nom} - {len(self.pieces)} pièces dans sa main"

    def tuiles_jouables(self, gauche, droite):
        """
        Cette fonction renvoie une liste de tuiles appropriées à jouer
        """
        tuiles_jouables = []

        for tuile in self.pieces:
            if (gauche in tuile) or (droite in tuile):
                tuiles_jouables.append(tuile)

        return tuiles_jouables

    def verif(self, plateau):
        """
        Vérifie que si le joueur est en mesure de jouer
        :param plateau: list
        :return: bool
        """
        gauche = plateau.plateau[0][0]
        droite = plateau.plateau[-1][-1]
        for piece in self.pieces:
            for num in piece:
                if num == gauche or num == droite:
                    return True
        return False

    def score(self):
        """
        En fin de partie calcule le score de chaque joueur en additionnant les points
        de chaque tuile
        :return: int
        """
        score = 0
        for tuile in self.pieces:
            score += sum(tuile)
        return score




if __name__ == "__main__":
    jo=Joueur("rr",[[6,3]])
    print(jo.verif([[3,2],[2,2]]))