#gestion des murs temporaire pas encore fait
#gestion d'une fonction qui renvoie le resultat pas fait (à implémenter à la fois dans le presenter la vue et le model)



from functools import *
import numpy as np
import random
from abc import ABC, abstractmethod
# taille de la carte
tailleMap = 9
matriceVide = np.zeros((tailleMap*2-1, tailleMap*2-1))
# Argent de début pour acheter murs
nbrPointAchatMur = 15
#couple type de mur et cout de ce mur
murEtCout = {0:1,1:2,2:3,3:3,4:2}


#temps de rechargements qui peuvent être modifiés si besoin
temps_rechargement_sapeur =4
temps_rechargement_sprinteur =4
temps_rechargement_jumper =4




class QuorridorModel:
    def __init__(self):
        self.taille = tailleMap * 2 - 1
        self.plateau =  [[-1 if (i % 2 == 0 and j % 2 == 0) else -2 for j in range(self.taille)] for i in range(self.taille)]
        self.murs = []
        self.positions_murs=dict()
        self.joueur= UniteSapeur(0,0,2,self) #on initialise pour les 2 joueurs à 2 sapeurs mais dès le début ce choix sera modifié
        self.adversaire = UniteSapeur(0,0,2,self)
        self.current_player=self.joueur



    def __str__(self):
        for i in range (len(self.plateau)):
            print(self.plateau[i])

    def lien_presenter(self,nb,player=None,x=None,y=None,direction=None,type_mur=None):
        pass

    def initialiser_jeu(self):
        for player in [self.joueur,self.adversaire]:
            unit_type =self.choix_unite()
            self.attribuer_type_unite(player, unit_type)
        self.init_pos()
        self.initialiser_plateau()
        self.actualiser_vue()
        for player in [self.joueur,self.adversaire]:
            player.murs_poss=self.choix_mur(player)
            print(player.murs_poss)

        self.current_player=self.joueur

        victoire = False
        while not victoire:
            if self.current_player.temps <self.current_player.temps_rechargement:
                self.temps+=1
            action= self.choix_action()
            if action ==1:
                x,y=self.choix_deplacement
                while not self.deplacement_legal(player,x,y):
                    x, y = self.choix_deplacement
                if self.verif_deplacement(player,x,y):
                    self.move_player(player,x,y)
            elif action ==2:
                direction, type, x, y=self.choix_placement_mur()
                while not self.placement_mur_legal(x,y,direction):
                    direction, type_mur, x, y = self.choix_placement_mur()
                if self.verif_mur(type_mur,x,y,direction):
                    self.placer_mur(self.current_player,type_mur,x,y,direction)


            elif action ==3:
                if not self.current_plater.verif_pouvoir_recharge():
                    pass #le pouvoir n'est pas rechargé on ne peut pas l'utiliser


                elif self.current_player.unit_type =="S":
                    x_mur,y_mur=self.choix_pouvoir_sapeur()
                    if x_mur==self.current_player.pos_x and y_mur-1 == self.current_player.pos_y:
                        x,y=x_mur,y_mur+2
                    elif x_mur==self.current_player.pos_x and y_mur+1 == self.current_player.pos_y:
                        x,y=x_mur,y_mur-2
                    elif x_mur-1==self.current_player.pos_x and y_mur == self.current_player.pos_y:
                        x,y=x_mur+2,y_mur
                    elif x_mur+1==self.current_player.pos_x and y_mur == self.current_player.pos_y:
                        x,y=x_mur-2,y_mur
                    if self.verif_pouvoir(self.current_player,x,y):
                        self.current_player.pouvoir(x_mur,y_mur)
                        self.move_player(self.current_player,x,y)


                elif self.current_player.unit_type =="J":
                    x, y = self.choix_deplacement
                    if self.verif_pouvoir(self.current_player,x,y):
                        self.current_player.pouvoir(x,y)

                elif self.current_player.unit_type == "P":
                    x, y = self.choix_deplacement
                    if self.verif_pouvoir(self.current_player,x,y):
                        self.current_player.pouvoir(x,y)

            self.actualiser_vue()
            if self.check_win(self.current_player):
                print(f'{self.current_player} a gagné ') #faire une fonction pour écrire ce résultat
                break
            self.demander_priorite()
            tour = (tour + 1) % 2
            self.changer_joueur(tour)

    def choix_mur(self,player):

        pass

    def Set_lien_presenter(self,function,nb,player=None,x=None,y=None,direction=None,type_mur=None):
        if nb==1:
            self.choix_unite = partial(function)
        elif nb==2:
            self.choix_mur = partial(function)

        elif nb==3:
            self.actualiser_vue=partial(function)
        elif nb==4:
            self.choix_action=partial(function)
        elif nb==5:
            self.choix_placement_mur=partial(function)
        elif nb==6:
            self.verif_mur=partial(function,type_mur,x,y,direction)
        elif nb==7:
            self.choix_deplacement=partial(function)
        elif nb==8:
            self.verif_deplacement=partial(function,player,x,y)
        elif nb==9:
            self.choix_pouvoir_sapeur=partial(function)
        elif nb==10:
            self.verif_pouvoir=partial(function,player,x,y)
        elif nb==11:
            self.demander_priorite=partial(function)




    def attribuer_type_unite(self, player, unit_type):
        if player == self.joueur:
            if unit_type == 'S':
                self.joueur = UniteSapeur(player.pos_x, player.pos_y, temps_rechargement_sapeur,self)
            elif unit_type == 'P':
                self.joueur = UniteSprinter(player.pos_x, player.pos_y, temps_rechargement_sprinteur,self)
            elif unit_type == 'J':
                self.joueur = UniteJumper(player.pos_x, player.pos_y, temps_rechargement_jumper,self)
            self.plateau[self.joueur.pos_x][self.joueur.pos_y] = self.joueur.type
        elif player == self.adversaire:
            if unit_type == 'S':
                self.adversaire = UniteSapeur(player.pos_x, player.pos_y, temps_rechargement_sapeur,self)
            elif unit_type == 'P':
                self.adversaire = UniteSprinter(player.pos_x, player.pos_y, temps_rechargement_sprinteur,self)
            elif unit_type == 'J':
                self.adversaire = UniteJumper(player.pos_x, player.pos_y, temps_rechargement_jumper,self)
            self.plateau[self.adversaire.pos_x][self.adversaire.pos_y] = self.adversaire.type
        else:
            print("Invalid player. Please choose the correct player.")

    def initialiser_plateau(self):
        players = [self.adversaire,self.joueur]
        for player in players:
            self.plateau[player.pos_x][player.pos_y]= player.type



    def init_pos(self): #initialisation des 2 joueurs avec leurs positions

        if self.plateau[0][self.taille//2]==0:
            self.joueur.pos_x,self.joueur.pos_y = self.taille-1,self.taille//2
            self.adversaire.pos_x,self.adversaire.pos_y = 0,self.taille//2
            self.plateau[0][0]=0
        else:
            self.joueur.pos_x, self.joueur.pos_y = self.taille - 1, (self.taille // 2)-1
            self.adversaire.pos_x, self.adversaire.pos_y = 0, (self.taille // 2)-1
            self.plateau[0][0] = 0

    def liste_pos_place_mur(self):
        #liste des positions où l'on peut placer des murs afin de couvrir 2 cases de joueurs (dans le cas inverse cela couvre seulement une case de joueur)
        return [(i, j) for i in range(tailleMap) for j in range(tailleMap) if (i % 2 == 1) != (j % 2 == 1)]

    def placement_mur_legal(self,x,y,direction):
        return True
    def move_player(self, player,x,y):
        if player == self.joueur:
            self.plateau[self.joueur.pos_x][self.joueur.pos_y] = 0
            self.joueur.pos_x,self.joueur.pos_y=x,y
            self.plateau[self.joueur.pos_x][self.joueur.pos_y] = self.joueur.type
        else:
            self.plateau[self.adversaire.pos_x][self.adversaire.pos_y] = 0
            self.adversaire.pos_x,self.adversaire.pos_y=x,y
            self.plateau[self.adversaire.pos_x][self.adversaire.pos_y] = self.adversaire.type
        return self.plateau

    def changer_joueur(self, tour):
        if tour == 1:

            self.current_player = self.model.adversaire
        elif tour == 0:

            self.current_player = self.model.joueur

    def placer_mur(self, player,type_mur, x, y, orientation):
        if type_mur==0:
            new_wall = MurClassique(x, y, orientation)
        elif type_mur==1:
            new_wall = MurIncassable(x,y,orientation)
        elif type_mur == 2:
            new_wall = GrandMur(x,y,orientation)
        elif type_mur == 4:
            new_wall = MurTemporaire(x,y,orientation,player)
        elif type_mur == 3:
            new_wall = MurAvecPorte(x,y,orientation,player)

        for (x,y) in new_wall.positions:
            print(x,y)
            self.plateau[x][y] = new_wall.pouvoir
        self.murs.append(new_wall)

        """if orientation == 0:  #vers le haut
            for i in range(new_wall.longueur):
                self.plateau[ x - i ][ y ] = new_wall.pouvoir
        elif orientation == 1:  #vers la droite
            for i in range(new_wall.longueur):
                self.plateau[ x ][y + i] = new_wall.pouvoir
        elif orientation == 2:  #vers le bas
            for i in range(new_wall.longueur):
                self.plateau[ x + i ][ y ] = new_wall.pouvoir
        elif orientation == 3:  #vers la gauche
            for i in range(new_wall.longueur):
                self.plateau[ x ][ y - i ] = new_wall.pouvoir"""


    def supprimer_mur(self,x,y):
        if (x,y) in self.positions_murs.keys():
            mur = self.positions_murs[(x,y)]
            del self.positions_murs[(x,y)]
            self.murs.remove(mur)



    def recursion(self,pos,player):
        visite =set()
        visite.add((pos[0],pos[1]))
        return self.chemin_restant(pos,visite,player)
    def chemin_restant (self,pos,visite,player):
        if player== self.joueur:
            arrivee = 0
        else:
            arrivee = self.taille-1
        if pos[0] == arrivee:
            return True
        voisin = set()
        for i, j in [(0,2),(2,0),(-2,0),(0,-2)] :
            if 0<= pos[0]+i < self.taille and 0<= j+pos[1] < self.taille :
                if (i !=0 and self.plateau[int(pos[0]+(i/2))][pos[1]] == -1) or (j !=0 and self.plateau[pos[0]][int(pos[1]+(j/2))] == -1):
                    voisin.add((pos[0]+i, j+pos[1]))
        disponible = voisin - visite
        if len(disponible)==0:
            return
        for pos2 in disponible :
                visite.add(pos2)
                reponse = self.chemin_restant(pos2,visite,player)
                if reponse:
                    return True
                visite.remove(pos2)

    def voisin(self,x,y):
        return[(x-1,y),(x+1,y),(x,y-1),(x,y+1)] #renvoie toutes les postions voisines en excluant les cases diagonales en coin

    def parametrer_set_murs(self):
        for mur in self.murs:
            for position in mur.positions:
                self.positions_murs[position]=mur
        #print(self.positions_murs)

    def deplacement_legal(self,player,x,y):
        if x<player.pos_x and y==player.pos_y:
            direction=0
        elif x>player.pos_x and y==player.pos_y:
            direction=2
        elif y<player.pos_y and x==player.pos_x:
            direction=3
        elif y>player.pos_y and x==player.pos_x:
            direction=1
        else:
            raise ValueError("il n'y a pas de changement de position du joueur ou changement en diagonale")
        if direction ==0:
            if player.pos_x ==0:
                return False
            if (player.pos_x-1,player.pos_y) in self.positions_murs.keys(): #si il y a un mur devant le joueur, mouvement impossible
                return False
        elif direction ==1:
            if player.pos_y ==self.taille-1:
                return False
            if (player.pos_x,player.pos_y+1) in self.positions_murs.keys(): #si il y a un mur devant le joueur, mouvment impossible
                return False
        elif direction ==2:
            if player.pos_x ==self.taille-1:
                return False
            if (player.pos_x+1,player.pos_y) in self.positions_murs.keys(): #si il y a un mur devant le joueur, mouvment impossible
                return False
        elif direction ==3:
            if player.pos_y ==0:
                return False
            if (player.pos_x,player.pos_y-1) in self.positions_murs.keys(): #si il y a un mur devant le joueur, mouvment impossible
                return False
        else:
            print("erreur dans le numéro de la direction")
            raise ValueError
        return True



    def get_state(self):
        # Retourne l'état actuel du jeu
        return self.plateau, self.joueur, self.adversaire

    def check_win(self, player):
        if player == self.joueur:
            if self.joueur.pos_x == 0:
                return True
        elif player == self.adversaire:
            if self.adversaire.pos_x == self.taille-1:
                return True
        return False

    def choix_action_aleatoire(self):
        actions = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2]
        return random.choice(actions)

    def deplacement_aleatoire(self, player):
        if player == self.joueur:  # si cest le joueur
            directions = [0, 0, 0, 0, 0, 2, 2, 1, 1, 3, 3]
        else:  # si cest l'adversaire
            directions = [2, 2, 2, 2, 2, 2, 0, 1, 1, 3, 3]


        return random.choice(directions)

    def mur_aleatoire(self):
        # Type de mur
        wall_types = [1, 2, 3, 4, 5]
        wall_type = random.choice(wall_types)

        # On utilise la fonction listepospacemur pour tirer les coords
        possible_positions = self.liste_pos_place_mur()
        position = random.choice(possible_positions)
        x, y = position

        # orientation
        orientations = [0, 1, 2, 3]
        orientation = random.choice(orientations)

        return wall_type, x, y, orientation

############################################################
#Classes pour les unités et les murs
############################################################
#pour les murs, 0 classique, 1
class Mur(ABC):
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.longueur =3
        self.pouvoir =0
        self.positions=[(x,y)]
        self.positions_occup()
    def positions_occup(self):
        for i in range(1,self.longueur):
            if self.direction ==0:
                self.positions.append((self.x-i,self.y))
            elif self.direction ==1:
                self.positions.append((self.x,self.y+i))
            elif self.direction ==2:
                self.positions.append((self.x+i,self.y))
            elif self.direction ==3:
                self.positions.append((self.x,self.y-i))



class MurIncassable(Mur):
    def __init__(self,x,y,direction):
        Mur.__init__(self,x,y,direction)
        self.pouvoir =1

class MurClassique(Mur):
    def __init__(self,x,y,direction):
        Mur.__init__(self,x,y,direction)


class MurAvecPorte(Mur):
    def __init__(self,x,y,direction,joueur):
        Mur.__init__(self, x, y, direction)
        self.pouvoir=3
        self.PosePar = joueur

class GrandMur(Mur):
    def __init__(self,x,y,direction):
        Mur.__init__(self,x,y,direction)
        self.longueur =5
        self.pouvoir =2

class MurTemporaire(Mur):
    def __init__(self,x,y,direction,joueur):
        Mur.__init__(self, x, y, direction)
        self.pouvoir=4
        self.temps_restant =3

class Unite(ABC):
    def __init__(self, x, y, temps_rechargement,model):
        self.pos_x = x
        self.pos_y = y
        self.temps_rechargement =temps_rechargement
        self.temps = 0
        self.credits = nbrPointAchatMur
        self.type ="?" #le type n'est pas encore connu, il sera modifié plus tard
        self.model =model
        self.murs_poss=[0,0,0,0,0]
    def verif_pouvoir_recharge(self):
        if self.temps_rechargement==self.temps:
            return True
        return False




    @abstractmethod
    def pouvoir(self):
        pass

class UniteSapeur(Unite):
    def __init__(self,x,y,temps_rechargement_sapeur,model):
        Unite.__init__(self,x, y, temps_rechargement_sapeur,model)
        self.unit_type = None
        self.type = "S"

    def pouvoir(self,x,y):
        voisin = self.model.voisin(self,x,y)
        self.temps=0
        if (self.pos_x,self.pos_y) in voisin:#il peut utiliser son pouvoir que si il est a coté du mur
            self.model.supprimer_mur(x,y)

class UniteSprinter(Unite):
    def __init__(self,x,y,temps_rechargement_sprinteur,model):
        Unite.__init__(self,x, y, temps_rechargement_sprinteur,model)
        self.type = "P"



    def pouvoir(self,x,y):
        self.temps = 0
        dx= x-self.pos_x
        dy=y-self.pos_y

        if self.model.deplacement_legal(self,self.pos_x+dx//2,self.pos_y+dy//2)==True:
            self.model.move_player(self, self, self.pos_x+dx//2,self.pos_y+dy//2)

        if self.model.deplacement_legal(self,x,y)==True:
            self.model.move_player(self, self, x,y)


class UniteJumper(Unite):
    def __init__(self,x,y,temps_rechargement_jumper,model):
        Unite.__init__(self,x, y, temps_rechargement_jumper,model)
        self.type = "J"

    def pouvoir(self,x,y):
        self.temps=0 #même si le mouvement est potentiellement invalide
        self.model.move_player(self,x,y)















