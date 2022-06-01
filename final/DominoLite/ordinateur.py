from joueurs import Joueur
from plateau import Plateau

class Ordinateur(Joueur):
    '''
    Cette classe représente l'ordinateur, y compris toutes les
    fonctions responsables des décisions de l'IA
    '''
    def __init__(self, nom, main=[], passer_la_main=0, ordi=1):
        '''
        Le Constructeur prend une liste de tuples qui
        représente la main de l'ordinateur
        '''
        super().__init__(nom, main, passer_la_main, ordi =1)

    def jouer_ordi(self, plateau):
        """
        Cette fonction permet à l'ordinateur de jouer
        elle renvoie la meilleure tuile à jouer. ou renvoie "PASS" si
        il n'y a pas de tuiles appropriées.
        """


        if len(plateau) == 0 : #Si c'est la première tuile à être jouée, jouez la plus grande tuile.
            tuileMax = self.tuile_la_plus_grande()
            return tuileMax


        else : #Si ce n'est pas la première tuile à être jouée...

            #vérification des tuiles appropriées à jouer
            tuiles_jouables = self.tuiles_jouables(plateau[0][0], plateau[-1][1])

            #il n'y a pas de tuiles appropriées, retournez "PASS".
            if len(tuiles_jouables) == 0 :
                return "PASS"

            #Il n'y a qu'une seule tuile convenable, renvoyez-la.
            elif len(tuiles_jouables) == 1 :
                return tuiles_jouables[0]

            #S'il y a plus d'une tuile appropriée, demandez la méthode "meilleur_tuile".
            else :
                tuileMax=self.meilleure_tuile(plateau, tuiles_jouables)
                return tuileMax

    def tuile_la_plus_grande(self):
        """Cette fonction renvoie la tuile la plus grande
        de la main de l'ordinateur"""

        tuileMax = [0,0]
        sommeMax = 0
        for tuile in self.pieces:
            somme = sum(tuile)
            if somme > sommeMax:
                tuileMax = tuile
                sommeMax = somme
        return tuileMax



    def meilleure_tuile(self, plateau, tuiles_jouables):
        """
        Cette fonction renvoie la meilleure tuile à jouer selon 5 critères:
        1. la tuile avec le plus de points
        2. la tuile est un double
        3. garder les plus de tuiles différentes
        4. vérifier que la tuile n'a pas été jouée six fois
        5. la tuile la plus grande favorisée

        :param plateau:
        :param tuiles_jouables:
        :return:
        """
        valeur_gauche = plateau[0][0]
        valeur_droite = plateau[-1][-1]

        #construire la liste des priorités
        liste_prioritaire =[0 for x in tuiles_jouables ]

        #remplir la liste des priorités
        for j in range(len(tuiles_jouables)) :

            compte_point =tuiles_jouables[j][0] + tuiles_jouables[j][1]
            DUO = 0

            #Vérifier la première condition (le nombre total est grand).
            if compte_point > 7:
                liste_prioritaire[j] += (compte_point - 7) + 3

            # vérifier la deuxième condition (la tuile est DUO
            # et je peux jouer sur les deux côtés)
            if tuiles_jouables[j][0] == tuiles_jouables[j][1]:

                DUO = 1

                valeur_gauche_verif = 0
                valeur_droite_verif = 0

                for tile in tuiles_jouables :
                    if valeur_gauche in tile :
                        valeur_gauche_verif = 1
                    if valeur_droite in tile:
                        valeur_droite_verif = 1

                if (valeur_gauche_verif == 1) and (valeur_droite_verif == 1):
                    liste_prioritaire[j] += 5
                else :
                    liste_prioritaire[j] += 2

            # Vérifier la troisième condition, "Garder le jeu ouvert".
            # Uniquement au début de la partie
            # DOIT ÊTRE ADAPTÉ AU NOMBRE DE JOUEURS.
            if len(self.pieces) > 4 :
                x, y =tuiles_jouables[j]
                x_count = 0
                y_count = 0

                for tuile in self.pieces:
                    if x in tuile:
                        x_count += 1
                    if y in tuile:
                        y_count += 1

                if (x_count == 1) or (y_count == 1):
                    liste_prioritaire[j] -= 3

            #verifie la quatrième condition, attention si la
            #tuile est joué 6 fois
            x,y = tuiles_jouables[j]

            x_count = 0
            y_count = 0

            for tile in plateau :
                if x in tile:
                    x_count += 1
                if y in tile:
                    y_count += 1

            if (x_count == 6) or (y_count == 6):
                liste_prioritaire[j] -= 10

        #Vérifie la cinquième condition, la plus grande tuile
        #obtient 2 points supplémentaires
        somme_liste=[]
        for tuile in tuiles_jouables :
            somme_liste.append(sum(tuile))

        max_tile = somme_liste.index(max(somme_liste))
        liste_prioritaire[max_tile] += 2

        #FINALEMENT, renvoyer la meilleure tuile
        index_meilleur_tuile = liste_prioritaire.index(max(liste_prioritaire))
        return tuiles_jouables[index_meilleur_tuile]

if __name__ == "__main__":
    ordi = Ordinateur("Ordi", [], True)
    plateau = Plateau()

    ordi.pieces, joueur, pioche = plateau.generation(7)
    print("Main Ordi :",ordi.pieces)
    print("Valeurs gauches/droites ",joueur[0][0],"  /  ", joueur[1][1])
    print("Dominos jouables",ordi.tuiles_jouables(joueur[0][0], joueur[1][1]))
    print("Tuile la plus grande", ordi.tuile_la_plus_grande())
    print("Meilleure tuile", ordi.meilleure_tuile(pioche, ordi.tuiles_jouables(joueur[0][0], joueur[1][1])))
