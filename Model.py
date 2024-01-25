




#toujours pas d'utilisation du serveur client pour vérifier si l'on peut faire le mouvement

import numpy as np
import random
from abc import ABC, abstractmethod
# taille de la carte
tailleMap = 9
matriceVide = np.zeros((tailleMap*2-1, tailleMap*2-1))
# Argent de début pour acheter murs
nbrPointAchatMur = 15
#couple type de mur et cout de ce mur
murEtCout = {0:2,1:2,3:2,4:2}


#temps de rechargements qui peuvent être modifiés si besoin
temps_rechargement_sapeur =4
temps_rechargement_sprinteur =4
temps_rechargement_jumper =4




class QuorridorModel:
    def __init__(self):
        self.taille = tailleMap * 2 - 1
        self.plateau =  [[0 if (i % 2 == 0 and j % 2 == 0) else -1 for j in range(self.taille)] for i in range(self.taille)]
        self.murs = []
        self.joueur= UniteSapeur(0,0,2) #on initialise pour les 2 joueurs à 2 sapeurs mais dès le début ce choix sera modifié
        self.adversaire = UniteSapeur(0,0,2)

    def __str__(self):
        for i in range (len(self.plateau)):
            print(self.plateau[i])


    def attribuer_type_unite(self, player, unit_type):
        if player == self.joueur:
            if unit_type == 'S':
                self.joueur = UniteSapeur(player.pos_x, player.pos_y, temps_rechargement_sapeur)
            elif unit_type == 'P':
                self.joueur = UniteSprinter(player.pos_x, player.pos_y, temps_rechargement_sprinteur)
            elif unit_type == 'J':
                self.joueur = UniteJumper(player.pos_x, player.pos_y, temps_rechargement_jumper)
            self.plateau[self.joueur.pos_x][self.joueur.pos_y] = self.joueur.type
        elif player == self.adversaire:
            if unit_type == 'S':
                self.adversaire = UniteSapeur(player.pos_x, player.pos_y, temps_rechargement_sapeur)
            elif unit_type == 'P':
                self.adversaire = UniteSprinter(player.pos_x, player.pos_y, temps_rechargement_sprinteur)
            elif unit_type == 'J':
                self.adversaire = UniteJumper(player.pos_x, player.pos_y, temps_rechargement_jumper)
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

    def move_player(self, player, direction):
        print(player)
        if player == self.joueur:
            self.plateau[self.joueur.pos_x][self.joueur.pos_y] = 0
            if direction == 0:
                self.joueur.pos_x -= 2
            elif direction == 2:
                self.joueur.pos_x += 2
            elif direction == 3:
                self.joueur.pos_y -= 2
            elif direction == 1:
                self.joueur.pos_y += 2
            print(self.joueur.pos_x, self.joueur.pos_y)
            self.plateau[self.joueur.pos_x][self.joueur.pos_y] = self.joueur.type
        else:
            self.plateau[self.adversaire.pos_x][self.adversaire.pos_y] = 0
            if direction == 0:
                self.adversaire.pos_x -= 2
            elif direction == 2:
                self.adversaire.pos_x += 2
            elif direction == 3:
                self.adversaire.pos_y -= 2
            elif direction == 1:
                self.adversaire.pos_y += 2
            print(self.adversaire.pos_x,self.adversaire.pos_y)
            self.plateau[self.adversaire.pos_x][self.adversaire.pos_y] = self.adversaire.type
        return self.plateau



    def placer_mur(self, player,type_mur, x, y, orientation):
        if type_mur==1:
            new_wall = MurClassique(x, y, orientation)
        elif type_mur==2:
            new_wall = MurIncassable(x,y,orientation)
        elif type_mur == 3:
            new_wall = GrandMur(x,y,orientation)
        elif type_mur == 4:
            new_wall = MurReutilisable(x,y,orientation,player)
        elif type_mur == 5:
            new_wall = MurAvecPorte(x,y,orientation,player)


        self.murs.append(new_wall)

        if orientation == 0:  #vers le haut
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
                self.plateau[ x ][ y - i ] = new_wall.pouvoir

        return self.plateau
    def supprimer_mur(self,x,y,axe):
        if axe == 'v':
            for mur in self.murs:
                if (x-1,y) ==(mur.x,mur.y) or (x+1,y)==(mur.x,mur.y):
                    self.murs.remove(mur)
                    for i in range(-1,2):
                        self.plateau[x+i][y]=-1
                elif ((x-2, y) == (mur.x, mur.y) or (x+2, y) == (mur.x, mur.y)) and mur.longueur == 5: #cas pour le mur de longueur 5
                    self.murs.remove(mur)
                    for i in range(-2, 3):
                        self.plateau[x + i][y] = -1
                else:
                    return -1 #il n'y a pas de mur en face du joueur
                return self.plateau
        elif axe == 'h':
            for mur in murs:
                if (x,y-1) ==(mur.x,mur.y) or (x,y+1)==(mur.x,mur.y):
                    self.murs.remove(mur)
                    for i in range(-1,2):
                        self.plateau[x][y+i]=-1
                elif ((x, y-2) == (mur.x, mur.y) or (x+2, y) == (mur.x, mur.y)) and mur.longueur == 5: #cas pour le mur de longueur 5
                    self.murs.remove(mur)
                    for i in range(-2, 3):
                        self.plateau[x + i][y] = -1
                else:
                    return -1
                return self.plateau


    def recursion(self,pos,player):
        visite =set()
        visite.add((pos[0],pos[1]))
        return self.chemin_restant(pos,visite,us)
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
                if (i !=0 and self.plateau[int(pos[0]+(i/2))][pos[1]] == -1) or (j !=0 and plateau[pos[0]][int(pos[1]+(j/2))] == -1):
                    voisin.add((pos[0]+i, j+pos[1]))
        disponible = voisin - visite
        if len(dispo)==0:
            return
        for pos2 in disponible :
                visite.add(pos2)
                reponse = self.chemin_restant(pos2,visite,player)
                if reponse:
                    return True
                visite.remove(new_pos)

    def voisin(self,x,y):
        return[(x-1,y),(x+1,y),(x,y-1),(x,y+1)] #renvoie toutes les postions voisines en excluant les cases diagonales en coin

    def get_state(self):
        # Retourne l'état actuel du jeu
        return self.plateau, self.joueur, self.adversaire

    def check_win(self, player):
        if player == self.joueur:
            if self.joueur.pos_x == 0:
                return True
        elif player == self.adversaire:
            if self.adversaire.pos_x == 16:
                return True
        return False

    def choix_action(self):
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
        self.pouvoir =1
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
        self.pouvoir =2

class MurClassique(Mur):
    def __init__(self,x,y,direction):
        Mur.__init__(self,x,y,direction)


class MurAvecPorte(Mur):
    def __init__(self,x,y,direction,joueur):
        Mur.__init__(self, x, y, direction)
        self.pouvoir=5
        self.PosePar = joueur

class GrandMur(Mur):
    def __init__(self,x,y,direction):
        Mur.__init__(self,x,y,direction)
        self.longueur =5
        self.pouvoir =3

class MurTemporaire(Mur):
    def __init__(self,x,y,direction,joueur):
        Mur.__init__(self, x, y, direction)
        self.pouvoir=4
        self.temps_restant =4

class Unite(ABC):
    def __init__(self, x, y, temps_rechargement):
        self.pos_x = x
        self.pos_y = y
        self.temps_rechargement =temps_rechargement
        self.temps = temps_rechargement
        self.credits = nbrPointAchatMur
        self.type ="?" #le type n'est pas encore connu, il sera modifié plus tard



    @abstractmethod
    def pouvoir(self):
        pass

class UniteSapeur(Unite):
    def __init__(self,x,y,temps_rechargement_sapeur):
        Unite.__init__(self,x, y, temps_rechargement_sapeur)
        self.type = "S"



    def pouvoir(self,x,y,axe,player,jeu):#axe vertical ='v', horizontal ='h
        voisin = jeu.voisin(self,x,y)
        if (player.pos_x,player.pos_y) in voisin:#il peut utiliser son pouvoir que si il est a coté du mur
            plateau =jeu.supprimer_mur(x,y,axe)
            if plateau ==-1:
                return -1
            else:
                jeu.plateau  = plateau
                return(plateau)
        else:
            return(-1) #cas si le joueur n'est pas voisin au mur



class UniteSprinter(Unite):
    def __init__(self,x,y,temps_rechargement_sprinteur):
        Unite.__init__(self,x, y, temps_rechargement_sprinteur)
        self.type = "P"



    def pouvoir(self,player,direction,jeu):
        for i in range(2):
            plateau=jeu.move_player(self, player, direction) #on se déplace de deux cases dans la meme direction,
            return plateau
            #les vérifications sont faits dans le presenter afin qu'il n'y ai pas d'erreur



class UniteJumper(Unite):
    def __init__(self,x,y,temps_rechargement_jumper):
        Unite.__init__(self,x, y, temps_rechargement_jumper)
        self.type = "J"

    def pouvoir(self,player,direction,jeu):
        #on vérifie qu'il y a bien un mur devant soit
        obstacle=False
        if direction ==0 or direction==2:
            for mur in jeu.murs:
                if (x-1,y) ==(mur.x,mur.y) or (x+1,y)==(mur.x,mur.y):
                    obstacle=True
                elif ((x-2, y) == (mur.x, mur.y) or (x+2, y) == (mur.x, mur.y)) and mur.longueur == 5: #cas pour le mur de longueur 5
                    obstacle=True
        elif direction==1 or direction==3:
            for mur in jeu.murs:
                if (x,y-1) ==(mur.x,mur.y) or (x,y+1)==(mur.x,mur.y):
                    obstacle = True
                elif ((x, y-2) == (mur.x, mur.y) or (x+2, y) == (mur.x, mur.y)) and mur.longueur == 5: #cas pour le mur de longueur 5
                    obstacle = True


        if obstacle : #si il y a bien un obstacle on utilise bien le pouvoir
            jeu.move_player(player,direction)
            return True
        else:
            return False










