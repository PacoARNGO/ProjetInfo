import numpy as np
from numpy.random import randint
from joueurs import *
from tour import *

"""
Ce module contient la définition de la classe Plateau où sont déposés les dominos
"""

class Plateau():
    '''
    Classe gérant le plateau de dominos
    '''
    def __init__(self, plateau=[], pioche=[]):
        self.plateau = plateau
        self.pioche = pioche

    def __str__(self):
        l = len(self.plateau)
        if l<=12:
            return str(self.plateau)+"\n"
        else :
            return str(self.plateau[:5])+"..."+str(self.plateau[l-1-5:])

    def bienvenue(self):
        """
        Méthode s'occupant d'afficher une bannière avec le nom du jeu
        :return: print(str)
        """
        return print("----------------------------------------------\n",\
              "         BIENVENUE DANS [DOMINOS,LITE]        \n",\
              "----------------------------------------------\n")



    def generation(self,Nb_dominos):
        """Création des 28 dominos (case blanche = 0) ainsi qu'une liste de liste
        telle que liste 1 = main J1, liste 2 = main J2, liste 3 = pioche)

        Paramètres
        ----------
        Nb_dominos : int
        Nombre de dominos par joueurs (7,8,9)

        Renvoie
        -------
        mains: list
            La liste de liste comprenant la main du joueur 1, du joueur 2 et la pioche

        Notes
        -----

        """

        dominos = []
        for dots1 in range(0, Nb_dominos):
            for dots2 in range(dots1, Nb_dominos):
                dominos.append([dots1, dots2])

        mains = [[] for x in range(3)]

        # On remplit final_list de tuples aléatoires
        for i in range(0, Nb_dominos):
            for j in range(2):
                random_number = np.random.randint(0, len(dominos))
                mains[j].append(dominos.pop(random_number))
        mains[2] = dominos
        return mains

    def dispositionPlateau(self, start):
        """
        S'occupe d'aligner les dominos dans le bon sens sur le plateau
        :param plateau: list
        :param start: list
        :return: pas de retour
        """
        startIndex = self.plateau.index(start)
        #Vérifier à droite
        for x in range(startIndex,len(self.plateau)-1):
            if self.plateau[x][-1] != self.plateau[x+1][0]:
                self.plateau[x+1].insert(len(self.plateau[x+1]),self.plateau[x+1].pop(0))

        #Vérifier à gauche
        for x in range(startIndex,0,-1):
            if self.plateau[x][0] != self.plateau[x-1][-1] :
                self.plateau[x-1].insert(len(self.plateau[x-1]),self.plateau[x-1].pop(0))

    def premier_joueur(self,pieces):
        """
        Renvoie l'indice du joueur 1 possédant un double élevé
        :param pieces: list
        :return: int
        """
        i=0
        for k in range(6,-1,-1):
                if [k,k] in pieces[0]:
                    break
                elif [k,k] in pieces[1]:
                    i = 1
                    break
        return i



if __name__ == '__main__':
    print("hi")
