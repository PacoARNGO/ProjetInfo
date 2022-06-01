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
        if not joueurs[i].ordi :
            choix= int(input(f"{joueurs[i].nom} - Choisissez, si possible, un double le plus élevé possible : ")) -1
            choix = joueurs[i].pieces[choix]
        else:
            choix = joueurs[i].jouer_ordi(plateau)
        start =choix
        self.start = start
        plateau += [start]
        joueurs[i].pieces.remove(choix)
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
        if len(joueur.tuiles_jouables(gauche,droite)) != 0:
            if joueur.ordi == 0:
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
                # Select a side if the user can play from both
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
                time.sleep(3)
                choix = joueur.jouer_ordi(plateau.plateau)
                jouable_gauche = False
                jouable_droite = False
                # Vérifie toutes les façons possibles pour un joueur de jouer.
                for num in choix:
                    if num == gauche and num == droite:
                        jouable_gauche = True
                        jouable_droite = True
                    elif num == gauche:
                        jouable_gauche = True
                    elif num == droite:
                        jouable_droite = True
                if jouable_gauche and jouable_droite:
                    count_gauche = 0
                    count_droite = 0
                    for tuile in joueur.pieces:
                        if gauche in tuile:
                            count_gauche += 1
                        elif droite in tuile:
                            count_droite += 1
                    if count_gauche > count_droite:
                        cote = "gauche"
                    else:
                        cote = "droite"
                    if cote == "gauche":
                        jouable_droite = False
                    elif cote == "droite":
                        jouable_gauche = False

                if jouable_gauche:
                    ret ="Jouer à gauche"
                    print(ret)
                    plateau.plateau.insert(0, choix)
                    joueur.pieces.pop(joueur.pieces.index(choix))
                elif jouable_droite:
                    ret = "Jouer à droite"
                    print(ret)
                    plateau.plateau.append(choix)
                plateau.dispositionPlateau(self.start)
        else:
            if plateau.jeu_pioche:
                if len(plateau.pioche) > 1:
                    if joueur.ordi == 0:
                        print("Vous êtes bloqués, vous piochez : "\
                          +str(plateau.pioche[0])+'\n'+'et attendez le prochain tour')
                        joueur.pieces.insert(0,plateau.pioche.pop(0))
                    else:
                        print("L'ordinateur pioche : "\
                              +str(plateau.pioche[0])+'\n'+'et attend le prochain tour')
                        joueur.pieces.append(plateau.pioche.pop(0))

                elif len(plateau.pioche) == 1:
                    if joueur.ordi == 0:
                        print("Vous êtes bloqués, vous piochez et attendez le prochain tour : " \
                              + str(plateau.pioche[0]) + '\n' + 'La pioche est desormais vide.')
                        joueur.pieces.insert(0, plateau.pioche.pop(0))
                    else:
                        print("L'ordinateur pioche et attend le prochain tour : " \
                              + str(plateau.pioche[0]) + '\n' + 'La pioche est desormais vide.')
                        joueur.pieces.append(plateau.pioche.pop(0))
                else:
                    if joueur.ordi == 0:
                        print("Vous êtes bloqués, vous attendez le prochain tour")
                        print("Il n'y a plus de pioche, avec un peu de chance vous pourrez jouer au prochain tour")
                    else:
                        print("L'ordinateur attend le prochain tour")
                        print("Il n'y a plus de pioche, avec un peu de chance il pourra jouer au prochain tour")
                joueur.passer_la_main = 1
                time.sleep(3)
            else:
                if joueur.ordi == 0:
                    print("Vous êtes bloqués, attendez le prochain tour")
                else:
                    print("L'ordinateur est bloqué et attend le prochain tour")
                joueur.passer_la_main = 1
                time.sleep(3)

if __name__ == '__main__':
    print("hi")