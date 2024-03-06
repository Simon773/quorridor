from colorama import Fore, Back, Style, init

class QuorridorView:
    def __init__(self):
        self.presenter = None


    def set_presenter(self, presenter):
        self.presenter = presenter

    def choix_unite(self):
        print("Enter your unit type choice (format: 'S' for Sapeur, 'P' for Sprinter, or 'J' for Jumper):")
        return input()


    def display(self, plateau, joueur, adversaire):
        for i in range(len(plateau)):
            for j in range(len(plateau[i])):
                if (i, j) == (joueur.pos_x, joueur.pos_y):  # Si es el jugador 1
                    print(Fore.MAGENTA + joueur.type + Style.RESET_ALL, end=' ')
                elif (i, j) == (adversaire.pos_x, adversaire.pos_y):  # Si es el jugador 2
                    print(Fore.YELLOW + adversaire.type + Style.RESET_ALL, end=' ')
                elif plateau[i][j] == 0 :  #MUR CLASSIQUE BLUE
                    print(Fore.BLUE + '#' + Style.RESET_ALL, end=' ')
                elif plateau[i][j] == 1 :  #MUR INCASSABLE RED
                    print(Fore.RED + '#' + Style.RESET_ALL, end=' ')
                elif plateau[i][j] == 2:  #GRAND MUR
                    print(Fore.BLUE + '#' + Style.RESET_ALL, end=' ')
                elif plateau[i][j] ==3:  #MUR REUTILISABLE
                    print(Fore.GREEN + '#' + Style.RESET_ALL, end=' ')
                elif plateau[i][j] ==4:  #MURAVECPORTE
                    print(Fore.YELLOW + '#' + Style.RESET_ALL, end=' ')
                elif plateau[i][j] == -1:  #Si il y a un 0 on affiche un 0
                    print('1', end=' ')
                elif plateau[i][j] == -2:  # Si il un -1 on affiche un -1
                    print(Fore.BLACK + '2' + Style.RESET_ALL, end=' ')
            print()  # Nueva línea al final de cada fila

    def get_input(self):
        mouvement=-1
        while 1>mouvement or mouvement >3:
            mouvement=int(input("Entrez le mouvement que vous souhaitez faire : deplacement(1),poser mur(2),utiliser pouvoir (3)-->>"))
        return mouvement
    def demander_placement_mur(self):
        direction = -1
        while 0 > direction or direction > 3:
            direction = int(input("Entrez la direction que vous souhaitez faire : haut(0), droite(1),bas(2), gauche(3)-->>"))
        x = int(input("Entrez la coord x que vous souhaitez faire"))
        y = int(input("Entrez la coord y que vous souhaitez faire"))
        type = -1
        while type < 0 or type > 4:
            type = int(input("Entrez le type de mur que vous souhaitez jouer"))

        return(direction,type,x,y)

    def demander_déplacement(self):
        direction = -1
        while 0 > direction or direction > 3:
            direction = int(input("Entrez la direction que vous souhaitez faire : haut(0), droite(1),bas(2), gauche(3)-->>"))
        return direction


    def demander_pvSapeur(self):
        x= int(input("entrez les coordonnes x du mur juste en a cote de vous que vous souhaitez exploser"))
        y = int(input("entrez les coordonnes y du mur juste en a cote de vous que vous souhaitez exploser"))
        #axe =input("Le mur que vous souhaitez exploser est horizontale (h) ou verticale (v) ?")
        return x,y #axe en plus ?

    def choix_murs(self,player):
        murEtCout = {0:1,1:2,2:3,3:3,4:2}
        liste_mur=[0,0,0,0,0]
        while player.credits!=0:
            print("Vous avez le choix entre 5 murs : classique(0), incassable(1), long(2),  porte(3) et temporaire(4)")
            a=-1
            while a<0 or a>4 :
                a=int(input("quel murs souhaitez vous prendre ?"))
            nb=int(input(f'ce mur coute {murEtCout[a]} credits, combien souhaitez vous en prendre ? '))
            while nb*murEtCout[a]>player.credits or nb*murEtCout[a]<0:
                nb=int(input(f"nombre incorrecte au vu de vos credits restant ({player.credits} credits restants) veuillez en choisir un autre nombre"))
            liste_mur[a]+=nb

            player.credits-=nb*murEtCout[a]
        return liste_mur
