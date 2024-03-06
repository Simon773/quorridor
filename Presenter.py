
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
    def utilisationPouvoir(self, player,x,y):

        return 0

class QuorridorPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_presenter(self)
        self.current_player = self.model.joueur  #on ajoute une variable pour connaitre le joueur courant
        self.client = Client()
        #self.bot =None
        #self.mode_de_jeux()
        self.bot=True
        for i in range(12):
            self.lien_model(i)
        self.model.initialiser_jeu()

    def lien_model(self,nb):
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
            self.model.Set_lien_presenter(self.verif_placement_mur,6)
        elif nb==7: #recuperer direction du déplacement
            self.model.Set_lien_presenter(self.recuper_direction_deplacement,7)
        elif nb==8: #verifier le deplacement
            self.model.Set_lien_presenter(self.verif_deplacement,8)
        elif nb==9: #demander la case à détruire pour le sapeur
            self.model.Set_lien_presenter(self.pouvoir_sapeur,9)
        elif nb==10: #verifier que l'on peut bien réaliser le pouvoir
            self.model.Set_lien_presenter(self.verifier_utilisation_pouvoir,10)
        elif nb==11: #demander ask_priority
            self.model.Set_lien_presenter(self.client.askPriority, 11)


    def mode_de_jeux(self):
        if self.view.demander_mode_jeu()==True:
            self.bot= True
        else:
            self.bot = False
    def gerer_choix_unite(self):
        unit_type_choice = self.view.choix_unite()
        return unit_type_choice

    def update_view(self):
        state = self.model.get_state()
        self.view.display(*state)

    def recup_placement_mur(self):
        if self.bot:
            direction,type,x,y = self.model.mur_aleatoire()
        else:
            direction, type, x, y = self.view.demander_placement_mur()
        return direction,type,x,y

    def verif_placement_mur(self,type_mur,x,y,direction):
        if self.client.placementMur(self.current_player, type_mur, x, y,direction) == 0:  # si le placement est possible
            return True
        else:
            return False

    def recuperer_action(self):
        if self.bot:
            mouvement= self.model.choix_action_aleatoire()
        else:
            mouvement = self.view.get_input()
        return mouvement

    def recuper_direction_deplacement(self,player):
        if self.bot:
            direction=self.model.deplacement_aleatoire(player)
        else:
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


