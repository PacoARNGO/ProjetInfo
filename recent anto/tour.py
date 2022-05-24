import numpy as np
from numpy.random import randint
from joueurs import *
from plateau import *
import time

"""
Ce module contient la définition de la classe principale servant à gérer le tour de chaque joueur
"""

class Tour():
    '''
    Classe principale permettant à chaque joueur de jouer leur coup
    '''
    def __init__(self, plateau, N=1):
        self.plateau = plateau
        self.numeroTour = N
        self.start = None


    def __str__(self):
        return "------------------------------------------------------- \n" + \
                f"Tour n°: {self.numeroTour} \n"

    def mise_en_jeu(self, plateau, joueurs,i):
        """
        Lance le "tour 0" où le premier joueur et renvoie l'état initial du plateau
        :param plateau: list
        :param joueurs: list
        :param i : int
        :return: list
        """

        print(f"{joueurs[i].nom} - pièces: ")
        print(joueurs[i].pieces)
        choix = int(input(f"{joueurs[i].nom} - Choisissez, si possible, un double le plus élevé possible : ")) -1
        start = joueurs[i].pieces[choix]
        self.start = start
        plateau += [joueurs[i].pieces[choix]]
        joueurs[i].pieces.pop(choix)
        joueurs.insert(len(joueurs),joueurs.pop(0))
        print('------------------------------------------------------- \n')
        return plateau



    def jouer(self, joueur, plateau):
        """
        Permet au joueur de jouer s'il le peut ou de piocher dans le cas contraire.
        Méthode utilisant la récursivité
        :param joueur: list
        :param plateau: list
        :return:
        """
        gauche = plateau.plateau[0][0]
        droite = plateau.plateau[-1][-1]

        # s'il y a des pièces jouables dans la main du joueur permettre à l'utilisateur de choisir
        if joueur.verif(plateau):
            choix = int(input(f"{joueur.nom} - Choisissez une pièce: ")) - 1
            jouable_gauche = False
            jouable_droite = False
            # Vérifie toutes les façons possibles pour un joueur de jouer.
            for num in joueur.pieces[choix]:
                if num == gauche and num == droite:
                    jouable_gauche = True
                    jouable_droite = True
                elif num == gauche:
                    jouable_gauche = True
                elif num == droite:
                    jouable_droite = True
            # Choisir côté gauche/droite dans le cas où les deux positions sont accessibles
            if jouable_gauche and jouable_droite:
                cote = input("Choisissez un côté (gauche/droite) : ")
                if cote == "gauche":
                    jouable_droite = False
                elif cote == "droite":
                    jouable_gauche = False
            # jouer sur un côté ou choisir une autre pièce s'il y avait une entrée invalide
            if jouable_gauche:
                ret ="Jouer à gauche"
                print(ret)
                plateau.plateau.insert(0, joueur.pieces[choix])
                joueur.pieces.pop(choix)

            elif jouable_droite:
                ret = "Jouer à droite"
                print(ret)
                plateau.plateau.append(joueur.pieces[choix])
                joueur.pieces.pop(choix)
            else:
                print(f"{joueur.pieces[choix]} n'est pas valable. Choisissez une autre pièce")
                # rappelle la fonction de jeu au cas où le joueur choisirait une mauvaise pièce.
                self.jouer(joueur, plateau)
            plateau.dispositionPlateau(self.start)
            joueur.passer_la_main = 0
        else:
            if len(plateau.pioche) > 1:
                print("Vous êtes bloqués, vous piochez : "\
                  +str(plateau.pioche[0])+'\n'+'et attendez le prochain tour')
                joueur.pieces.insert(0,plateau.pioche.pop(0))

            elif len(plateau.pioche) == 1:
                print("Vous êtes bloqués, vous piochez et attendez le prochain tour : " \
                      + str(plateau.pioche[0]) + '\n' + 'La pioche est desormais vide.')
                joueur.pieces.insert(0, plateau.pioche.pop(0))
            else:
                print("Il n'y a plus de pioche, avec un peu de chance vous pourrez jouer au prochain tour")
            joueur.passer_la_main = 1
            time.sleep(3)

if __name__ == '__main__':
    print("hi")