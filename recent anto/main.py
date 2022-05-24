from plateau import *
from tour import *

def main():
    end = False
    plateau = Plateau()
    plateau.bienvenue()
    pieces = plateau.generation(7)
    plateau.pioche = pieces[2]

    joueurs = []
    k = plateau.premier_joueur(pieces) #k est l'indice du joueur commencant la partie (plus grand double)
    nom = input(f"Entrez le nom du joueur {1}: ")
    joueurs.append(Joueur(nom, pieces[k]))
    nom = input(f"Entrez le nom du joueur {2}: ")
    joueurs.append(Joueur(nom, pieces[abs(k-1)]))


    tour = Tour(plateau)
    plateau.plateau = tour.mise_en_jeu(plateau.plateau, joueurs,k)
    arret = 0
    while end == False:

        for joueur in range(2):

            print(tour)
            print(plateau)
            print(joueurs[joueur])
            tour.jouer(joueurs[joueur],plateau)
            passe = joueurs[joueur].passer_la_main

            if len(joueurs[joueur].pieces) == 0:
                end = True
                print("---------------------------------------------")
                print(str(joueurs[joueur].nom)+" a gagné !!!")
                print("---------------------------------------------")
                break

            if passe == 0:
                arret =0
            else :
                arret += passe

            if arret >= 3 and len(plateau.pioche)==0:
                end = True
                if joueurs[0].score()<joueurs[1].score():
                    victorieux = joueurs[1].nom
                elif joueurs[0].score()>joueurs[1].score():
                    victorieux = joueurs[0].nom
                else:
                    victorieux = "égalité"

                print("---------------------------------------------")
                print("Vous vous êtes bien battus, voici les scores :")
                print(str(joueurs[0].score())+"pour "+joueurs[0].nom)
                print(str(joueurs[0].score())+"pour "+joueurs[0].nom+"\n")
                if victorieux != "égalité":
                    print("La victoire est à "+victorieux+" !!")
                else:
                    print("Et c'est donc une égalité !!")


                break


            tour.numeroTour += 1
            print('------------------------------------------------------- \n')





if __name__ == '__main__':
    main()