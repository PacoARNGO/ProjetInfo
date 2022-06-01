from plateau import Plateau
from final.tour import Tour
from final.joueurs import Joueur
from final.ordinateur import Ordinateur

def main():
    end = False
    plateau = Plateau()  # Création d'un plateau
    plateau.bienvenue() # Lancer l'affichage de bienvenue
    pieces = plateau.generation()   # Génération des pièces
    plateau.pioche = pieces[2]  # Pioche = liste des pièces restantes

    jeu_pioche = input("Voulez-vous jouer avec la pioche ? (O/N) : ")   # Choix jeu avec pioche ou sans
    if jeu_pioche == "O":
        plateau.jeu_pioche =True
    homme_machine = input("Voulez-vous jouer contre l'ordinateur ? (O/N) : ")  # Choix jeu contre l'ordinateur

    joueurs = []
    k = plateau.premier_joueur(pieces)  #k est l'indice du joueur commencant la partie (plus grand double)
    if homme_machine == "N":
        nom1 = input(f"Entrez le nom du joueur {1}: ")  # Demande du nom du joueur 1
        joueurs.append(Joueur(nom1, pieces[0])) # Ajout du joueur 1 dans la liste des joueurs
        nom2 = input(f"Entrez le nom du joueur {2}: ")  # Demande du nom du joueur 2
        joueurs.append(Joueur(nom2, pieces[1])) # Ajout du joueur 2 dans la liste des joueurs
    else:
        nom1 = input("Entrez le nom du joueur humain: ")
        joueurs.append(Joueur(nom1, pieces[0]))
        nom2 = "Dominator de l'Ordinateur"
        joueurs.append(Ordinateur(nom2, pieces[1],0,1))
        print("Vous affrontez : "+nom2)


    tour = Tour(plateau)    # Création d'un tour
    plateau.plateau = tour.mise_en_jeu(plateau.plateau, joueurs,k)  # Mise en jeu des pièces
    arret = 0   # Variable d'arrêt

    while end == False:

        for joueur in range(2):
            print(tour) # Affichage du tour
            print(plateau)  # Affichage du plateau
            print(joueurs[joueur])  # Affichage du joueur
            tour.jouer(joueurs[joueur],plateau) # Lancement du tour
            passe = joueurs[joueur].passer_la_main  # Variable de passe

            if len(joueurs[joueur].pieces) == 0:    # Si le joueur n'a plus de pièces il gagne
                end = True
                print("---------------------------------------------")
                print(str(joueurs[joueur].nom)+" a gagné !!!")
                print("---------------------------------------------")
                break

            if passe == 0:  # Si le joueur n'a pas passé la main
                arret =0    # On réinitialise la variable d'arrêt
            else :
                arret += passe  # Sinon on incrémente la variable d'arrêt

            if jeu_pioche :   # Si le joueur veut jouer avec la pioche

                if arret >= 3 and len(plateau.pioche)==0:   # Si le joueur a passé 3 fois la main et qu'il n'y a plus de pièces dans la pioche
                    end = True  # On met la variable d'arrêt à True
                    if joueurs[0].score()<joueurs[1].score():   # Si le score du joueur 1 est inférieur au score du joueur 2
                        victorieux = joueurs[1].nom
                    elif joueurs[0].score()>joueurs[1].score():  # Si le score du joueur 1 est supérieur au score du joueur 2
                        victorieux = joueurs[0].nom
                    else:   # Si le score du joueur 1 est égal au score du joueur 2
                        victorieux = "égalité"

                    print("---------------------------------------------")
                    print("Vous vous êtes bien battus, voici les scores :")
                    print(str(joueurs[0].score())+"pour "+joueurs[0].nom)   # Affichage du score du joueur 1
                    print(str(joueurs[0].score())+"pour "+joueurs[0].nom+"\n")  # Affichage du score du joueur 2
                    if victorieux != "égalité":     # Si victoire on affiche le nom du joueur gagnant
                        print("La victoire est à "+victorieux+" !!")
                    else:
                        print("Et c'est donc une égalité !!")   # Sinon on affiche "égalité"


                    break

            else:     # Si le joueur ne veut pas jouer avec la pioche
                if arret >= 2:  # Si le joueur a passé 2 fois la main
                    end = True  # On met la variable d'arrêt à True
                    if joueurs[0].score() < joueurs[1].score():
                        victorieux = joueurs[1].nom
                    elif joueurs[0].score() > joueurs[1].score():
                        victorieux = joueurs[0].nom
                    else:
                        victorieux = "égalité"

                    print("---------------------------------------------")
                    print("Vous vous êtes bien battus, voici les scores :")
                    print(str(joueurs[0].score()) + "pour " + joueurs[0].nom)
                    print(str(joueurs[0].score()) + "pour " + joueurs[0].nom + "\n")
                    if victorieux != "égalité":
                        print("La victoire est à " + victorieux + " !!")
                    else:
                        print("Et c'est donc une égalité !!")

                    break

            tour.numeroTour += 1    # Incrémentation du numéro de tour
            print('------------------------------------------------------- \n')

        k = 0   # On réinitialise la variable k utile dans la première boucle pour lancer le tour 1 (après le tour 0)



if __name__ == '__main__':
    main()