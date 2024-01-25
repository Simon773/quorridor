######################""
#probleme avec le client:
#pour le deplacement joueur, prends en paramètre le position et non l'orentation du déplacement (pas forcèment un problème)
# pour le placement mur, le numéro associé aux murs et mal fait et ne prends pas en compte le mur classique
#pour l'instant le code peut renvoyer des erreurs et des index out of range sans les vérifs client


#credits par type de mur, modifiable si besoin
credits_mur_classique =2
credits_mur_incassable =2
credits_mur_long =2
credits_mur_porte =2
credits_mur_reutilisable =2


import numpy as np
tailleMap = 9
matriceVide = np.zeros((tailleMap*2-1, tailleMap*2-1))
# Argent de début pour acheter murs
nbrPointAchatMur = 15
#couple type de mur et cout de ce mur
murEtCout = {0:2,1:2,3:2,4:2}



from colorama import Fore, Style
from typing import List
import time
import numpy as np

#SERVER DU PROF PAS IMPPLEMENTÉ ENCORE

# Classe qui va permettre la communication avec le serveur.
# Version non fonctionnelle du client, uniquement la pour que vous puissiez le prendre en considération
# pour permettre une transition plus facile au 2eme semestre.
class Client:

    # ------------------------------------------------------------------------
    # FONCTION UTILISEES AU DEBUT DU JEU
    # -----------------------------------------------------------------------

    # enregistre l'équipe auprès du serveur, avec un nom d'équipe et un type de pion
    # type de pion 0:pionSappeur, 1:pion Jumper, 2:pion sprinter
    def registerTeam(self, name:str, pionChoisi:int):
        return True

    # choisi un ensemble de mur pour commencer la partie
    # error 0:trop cher en point
    # Version locale de ce qui se fera sur le serveur
    def choixMur(self, murs:List[int]):
        totalCout = 0
        try :
            for mur in murs :
                totalCout += murEtCout.get(mur)
        except ValueError:
            print("mur n'existe pas dans la liste des murs dispos")

        return True



    # ------------------------------------------------------------------------
    # FONCTION UTILISEES PENDANT LE JEU
    # ------------------------------------------------------------------------

    # Fonction à appeler dans une boucle While, qui est bloquante. C'est a dire que la fonction est en
    # "pause" tant que l'autre joueur est en train de jouer
    def askPriority(self):
        # Temps d'attente en seconde
        time.sleep(1)
        # Renvoi une matrice contenant les cases du jeu.
        return matriceVide




    # return 0 si s'est bien passé
    # Code erreur  1:, 2:obstacle mur, 3:sortie de terrain, 10:mauvais input
    def deplacement(self, joueur, positionX:int, positionY:int):
        if not isinstance(positionX, int) or not isinstance(positionY, int):
            raise TypeError()

        if 0> positionX or positionX >=17 or 0> positionY or positionY >=17:
            return 3
        return 0

    # Orientation : 0 : vers le haut, 1 vers la droite, 2 vers le bas, 3 vers la gauche
    # type mur : 0:mur incassable 1:mur long 2:mur réutilisable 3:murTemporaire 4:mur "porte"
    # return 0 si ok
    # Code erreur : 1:mur sort map, 2:mur croise autre mur, 3:mur enferme joueur 4:mur non disponible 10:mauvais input
    def placementMur(self, joueur , typeMur:int , positionX:int, positionY:int, orientation: int):
        if  not isinstance(typeMur, int) or not isinstance(positionX, int) or not isinstance(positionY, int) or not isinstance(orientation, int):
            raise TypeError()
        return 0

    # utilisation du pouvoir de l'unité
    # Sauter par dessus
    # return 0 si ok
    # code erreur 1:pouvoir en rechargement  10:mauvais input
    def utilisationPouvoir(self, orientation):
        if isinstance(orientation, int):
            raise TypeError()
        return 0

class QuorridorPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_presenter(self)
        self.current_player = self.model.joueur  #on ajoute une variable pour connaitre le joueur courant
        self.client = Client()

    def gerer_choix_unite(self):
        for player in [self.model.joueur, self.model.adversaire]:
            unit_type_choice = self.view.choix_unite()
            self.model.attribuer_type_unite(player, unit_type_choice)

    def gerer_input(self): #pas utile dans la boucle de jeu mais nous permet de tester nos fonctions
        while True:
            mouvement = self.view.get_input()
            if mouvement==1:
                direction = self.view.demander_direction()
                self.model.move_player(self.model.joueur, direction)
            elif mouvement==2:
                orientation = self.view.demander_direction()
                x,y = self.view.demander_coordonnes()
                type = self.view.demander_type_mur()
                self.model.placer_mur(self.model.joueur, type, x, y, orientation)

            elif mouvement==3:
                if self.model.joueur.type=="S":
                    axe,x,y=self.view.demander_pvSapeur()
                    pouvoir =-1
                    while pouvoir ==-1:
                        pouvoir =self.model.joueur.pouvoir(x,y,axe,self.model.joueur,self.model)
                else:
                    pass
            self.update_view()


    def update_view(self):
        state = self.model.get_state()
        print(state)
        self.view.display(*state)

    def changer_joueur(self,tour):
        if tour==1:
           
            self.current_player = self.model.adversaire
        elif tour==0:

            self.current_player = self.model.joueur

    def recup_placement_mur(self,bot):#recupere les informations pour placer un mur et si possible essaie de la placer
        if bot:
            direction, type, x, y = self.view.demander_placement_mur()

        else:
            type, x, y, direction= self.model.mur_aleatoire()

        if self.client.placementMur(self.current_player, type_mur, x, y,
                                    orientation) == 0:  # si le placement est possible
            self.model.placer_mur(self.current_player, type_mur, x, y, orientation)
            return True
        else:
            return False

    def recuperer_action(self,bot):
        if bot:
            mouvement = self.model.choix_action()
        else:
            mouvement = self.view.get_input()

    def recuper_direction_deplacement(self,bot):
        if bot:
            direction = self.deplacement_aleatoire(self.current_player)
        else:
            direction =self.view.demander_déplacement()


    def deplacement_joueur(self,direction):
        if direction == 0:
            x, y = self.current_player.pos_x - 2, self.current_player.pos_y
        elif direction == 1:
            x, y = self.current_player.pos_x, self.current_player.pos_y + 2
        elif direction == 2:
            x, y = self.current_player.pos_x + 2, self.current_player.pos_y
        elif direction == 3:
            x, y = self.current_player.pos_x, self.current_player.pos_y - 2
        verif_deplacement = self.client.deplacement(self.current_player, x, y)
        if verif_deplacement != 0:
            return False
        else:  # si le mouvement est valide
            self.model.move_player(self.current_player, direction)
            return True

    def verifier_victoire(self):
        verif_victoire = self.model.check_win(self.current_player)

        if verif_victoire == True:
            print("le joueur", self.current_player, " a gagné")
            return True
        else:
            return False





    def deplacer_player_aléatoire(self,):
        while True:  # tant que le déplacement n'est pas fait:
            direction = self.model.deplacement_aleatoire(self.current_player)
            if direction == 0:
                x, y = self.current_player.pos_x - 2, self.current_player.pos_y
            elif direction == 1:
                x, y = self.current_player.pos_x, self.current_player.pos_y + 2
            elif direction == 2:
                x, y = self.current_player.pos_x + 2, self.current_player.pos_y
            elif direction == 3:
                x, y = self.current_player.pos_x, self.current_player.pos_y - 2
            verif_deplacement = self.client.deplacement(self.current_player, x, y)

            if verif_deplacement != 0:
                print("Mouvement impossible, il y a une erreur, un mur sur le passage, une sortie de terrain ou un mauvais input()")
            else:  # si le mouvement est valide
                self.model.move_player(self.current_player, direction)
                break
    def placer_mur_aléatoire(self): #dans le cas ou c'est le bot qui joue, celui ci récupére les informations de déplacement, les vérifie dans le client et exécute
        while True:
            type_mur, x, y, orientation = self.model.mur_aleatoire()
            if self.client.placementMur(self.current_player, type_mur, x, y,
                                        orientation) == 0:  # si le placement est possible
                self.model.placer_mur(self.current_player, type_mur, x, y, orientation)
                break


    def lancer_boucle(self):
        tour = 1
        while True:
            action = self.model.choix_action()
            if action ==1:
                while True: #tant que le déplacement n'est pas fait:
                    direction = self.model.deplacement_aleatoire(self.current_player)
                    if direction ==0:
                        x,y= self.current_player.pos_x-2,self.current_player.pos_y
                    elif direction ==1:
                        x, y = self.current_player.pos_x, self.current_player.pos_y+2
                    elif direction ==2:
                        x, y = self.current_player.pos_x+2, self.current_player.pos_y
                    elif direction ==3:
                        x, y = self.current_player.pos_x, self.current_player.pos_y-2
                    verif_deplacement = self.client.deplacement(self.current_player,x,y)
                    print(x,y)
                    if verif_deplacement !=0:
                        print("Mouvement impossible, il y a une erreur, un mur sur le passage, une sortie de terrain ou un mauvais input()")
                    else: #si le mouvement est valide
                        self.model.move_player(self.current_player,direction)
                        break
            elif action ==2:
                while True:
                    # placementMur(self, joueur : str, typeMur:int , positionX:int, positionY:int, orientation: int):
                    #print(self.client.placementMur(self.model.joueur,1,10,10,1))
                    type_mur,x,y,orientation = self.model.mur_aleatoire()
                    if self.client.placementMur(self.current_player,type_mur,x,y,orientation)==0: #si le placement est possible
                        self.model.placer_mur(self.current_player,type_mur,x,y,orientation)
                        break

            verif_victoire=self.model.check_win(self.current_player)
            print(verif_victoire)
            if verif_victoire==True:
                print("le joueur",self.current_player," a gagné")
                break

            self.update_view()

            self.client.askPriority()
            tour = (tour+1)%2
            self.changer_joueur(tour)




    def lancer_jeu(self):


        self.gerer_choix_unite()
        self.model.init_pos()
        self.update_view()
        self.model.initialiser_plateau()
        #self.model.liste_pos_place_mur()
        #self.model.get_state()

        # Affiche l'état initial du jeu
        #self.update_view()

        #self.gerer_input()

        #self.lancer_boucle()
