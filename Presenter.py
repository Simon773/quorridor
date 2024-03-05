
#QUESTIONS
#pour le client actuellement le utilisation pouvoir recoit orientation, mais il ne doit pas recevoir player x et y ?
#si un pouvoir est invalide ou en partie comment faire, exemple avec le sprinter qui peut avancer de seulement une case, que se passe-t-il avec le client ???

import numpy as np
tailleMap = 9
matriceVide = np.zeros((tailleMap*2-1, tailleMap*2-1))
# Argent de début pour acheter murs
nbrPointAchatMur = 15
#couple type de mur et cout de ce mur
murEtCout = {0:2,1:2,3:2,4:2}

from typing import List
import time
import numpy as np

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
        for i in range(12):
            self.lien_model(i,self.current_player,i)
        self.model.initialiser_jeu()

    def lien_model(self,nb,player=None,x=None,y=None,direction=None,type_mur=None):
        if nb==1: #choix des unites
            self.model.Set_lien_presenter(self.gerer_choix_unite,1)
        elif nb==2: #choix des murs
            self.model.Set_lien_presenter(self.choix_murs,2)
        elif nb==3: #actualisation de la vue:
            self.model.Set_lien_presenter(self.update_view,3)
        elif nb==4: #recuper l'action choisi:
            self.model.Set_lien_presenter(self.recuperer_action,4)
        elif nb==5: #recuper le placement d'un mur:
            self.model.Set_lien_presenter(self.recup_placement_mur,5)
        elif nb==6: #Verifier le placement d'un mur:
            self.model.Set_lien_presenter(self.verif_placement_mur,6,type_mur,x,y,direction)
        elif nb==7: #recuperer direction du déplacement
            self.model.Set_lien_presenter(self.recuper_direction_deplacement,7)
        elif nb==8: #verifier le deplacement
            self.model.Set_lien_presenter(self.verif_deplacement,8,player,x,y)
        elif nb==9: #demander la case à détruire pour le sapeur
            self.model.Set_lien_presenter(self.pouvoir_sapeur,9)
        elif nb==10: #verifier que l'on peut bien réaliser le pouvoir
            self.model.Set_lien_presenter(self.verifier_utilisation_pouvoir,10,player,x,y)
        elif nb==11: #demander ask_priority
            self.model.Set_lien_presenter(self.verifier_utilisation_pouvoir, 11)



    def gerer_choix_unite(self):
        unit_type_choice = self.view.choix_unite()
        return unit_type_choice

    def update_view(self):
        state = self.model.get_state()
        self.view.display(*state)

    def recup_placement_mur(self):
        direction, type, x, y = self.view.demander_placement_mur()
        return direction,type,x,y

    def verif_placement_mur(self,type_mur,x,y,direction):
        if self.client.placementMur(self.current_player, type_mur, x, y,direction) == 0:  # si le placement est possible
            return True
        else:
            return False

    def recuperer_action(self):
        mouvement = self.view.get_input()
        return mouvement

    def recuper_direction_deplacement(self):
        direction =self.view.demander_déplacement()
        x,y = self.direction_en_xy(direction)
        return x,y

    def verif_deplacement(self,player,x,y):
        if self.client.deplacement(player,x,y)==0:
            return True
        else:
            return False

    def pouvoir_sapeur(self):
        x,y=self.view.demander_pvSapeur()
        return x,y

    def verifier_utilisation_pouvoir(self,player,x,y):
        if self.client.utilisationPouvoir(player,x,y)==0:
            return True
        else:
            return False

    def choix_murs(self,player):
        mur_dispo=self.view.choix_murs(player)
        return mur_dispo

    def demander_priority(self):
        self.client.askPriority()







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


    def direction_en_xy(self,direction):
        if direction == 0:
            x, y = self.current_player.pos_x - 2, self.current_player.pos_y
        elif direction == 1:
            x, y = self.current_player.pos_x, self.current_player.pos_y + 2
        elif direction == 2:
            x, y = self.current_player.pos_x + 2, self.current_player.pos_y
        elif direction == 3:
            x, y = self.current_player.pos_x, self.current_player.pos_y - 2
        else:
            raise ValueError
        return x,y

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

