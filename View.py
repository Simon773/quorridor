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
                elif plateau[i][j] == 1 :  #MUR CLASSIQUE BLUE
                    print(Fore.BLUE + '#' + Style.RESET_ALL, end=' ')
                elif plateau[i][j] == 2 :  #MUR INCASSABLE RED
                    print(Fore.RED + '#' + Style.RESET_ALL, end=' ')
                elif plateau[i][j] == 3:  #GRAND MUR
                    print(Fore.BLUE + '#' + Style.RESET_ALL, end=' ')
                elif plateau[i][j] ==4:  #MUR REUTILISABLE
                    print(Fore.GREEN + '#' + Style.RESET_ALL, end=' ')
                elif plateau[i][j] ==5:  #MURAVECPORTE
                    print(Fore.YELLOW + '#' + Style.RESET_ALL, end=' ')
                elif plateau[i][j] == 0:  #Si il y a un 0 on affiche un 0
                    print('0', end=' ')
                elif plateau[i][j] == -1:  # Si il un -1 on affiche un -1
                    print(Fore.BLACK + '1' + Style.RESET_ALL, end=' ')
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
        while type < 1 or type > 5:
            type = int(input("Entrez le type de mur que vous souhaitez jouer"))

        return(direction,type,x,y)

    def demander_déplacement(self):
        direction = -1
        while 0 > direction or direction > 3:
            direction = int(input("Entrez la direction que vous souhaitez faire : haut(0), droite(1),bas(2), gauche(3)-->>"))
        return direction


    def demander_pvSapeur(self):
        x,y= input("entrez les coordonnes du mur juste en a cote de vous que vous souhaitez exploser")
        axe =input("Le mur que vous souhaitez exploser est horizontale (h) ou verticale (v) ?")
        return axe,x,y


