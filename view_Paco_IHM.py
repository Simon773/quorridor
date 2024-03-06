from colorama import Fore, Back, Style, init
import tkinter
import tkinter as tk
class QuorridorView:
    def __init__(self):
        self.canvas = None
        self.root = tkinter.Tk()

        self.mode_jeu = tkinter.BooleanVar(self.root)
        self.unite_choisie = tkinter.StringVar(self.root)

        self.root.geometry("800x800")
        self.canvas = tkinter.Canvas(self.root, width=400, height=400)
        self.canvas.grid(row=0, column=0, columnspan=3)

    def start(self):
        if self.root is not None:
            self.root.mainloop( )

    def demander_mode_jeu(self):

        bot_button = tkinter.Button(self.root, text="Bot Mode", command=lambda: self.mode_jeu.set(True), height=2,
                                    width=20)
        player_button = tkinter.Button(self.root, text="Player Mode", command=lambda: self.mode_jeu.set(False),
                                       height=2, width=20)
        bot_button.grid(row=1, column=2)
        player_button.grid(row=1, column=3)

        self.root.wait_variable(self.mode_jeu)

        return self.mode_jeu.get()
    def choix_unite(self):

        sap_button = tkinter.Button(self.root, text="Sapeur", command=lambda: self.unite_choisie.set('S'), height=2,
                                    width=20)
        sap_button.grid(row=1, column=1)
        jump_button = tkinter.Button(self.root, text="Jumper", command=lambda: self.unite_choisie.set('J'), height=2,
                                     width=20)
        jump_button.grid(row=1, column=2)
        sprinter_button = tkinter.Button(self.root, text="Sprinter", command=lambda: self.unite_choisie.set('P'),
                                         height=2, width=20)
        sprinter_button.grid(row=1, column=3)
        self.root.wait_variable(self.unite_choisie)

        return self.unite_choisie.get()

    def choix_murs(self,player):
        pass

        """
        class LOSMIOSQUORRIDORView(tk.Frame):
            def __init__(self, master=None):
                super( ).__init__(master)
                self.master = master
                self.grid( )
                self.create_widgets( )

            def create_widgets(self):
                self.move_button = tk.Button(self)
                self.move_button[ "text" ] = "Move"
                self.move_button.grid(row=0, column=0)

                self.place_wall_button = tk.Button(self)
                self.place_wall_button[ "text" ] = "Place Wall"
                self.place_wall_button.grid(row=0, column=2)

                self.use_power_button = tk.Button(self)
                self.use_power_button[ "text" ] = "Use Power"
                self.use_power_button.grid(row=0, column=4)

                self.canvas = tk.Canvas(self, width=1000, height=1000)
                self.canvas.grid(row=5, column=10, columnspan=3)

    def set_presenter(self, presenter):
        self.presenter = presenter

    def choix_unite(self):
        print("Enter your unit type choice (format: 'S' for Sapeur, 'P' for Sprinter, or 'J' for Jumper):")
        return input()

    def display(self, plateau, joueur, adversaire):
        for i in range(len(plateau)):
            for j in range(len(plateau[ i ])):
                if (i, j) == (joueur.pos_x, joueur.pos_y):  #joueur 1
                    self.canvas.create_oval(j*40, i*40, j*40+40, i*40+40, fill="blue")
                elif (i, j) == (adversaire.pos_x, adversaire.pos_y):  # joueur 2
                    self.canvas.create_oval(j*40, i*40, j*40+40, i*40+40, fill="red")
                elif plateau[ i ][ j ] == 0:  # MUR CLASSIQUE BLUE
                    self.canvas.create_rectangle(j*40, i*40, j*40+40, i*40+40, fill="black")
                elif plateau[ i ][ j ] == 1:  # MUR INCASSABLE RED
                    self.canvas.create_rectangle(j*40, i*40, j*40+40, i*40+40, fill="red")
                elif plateau[ i ][ j ] == 2:  # GRAND MUR
                    self.canvas.create_rectangle(j*40, i*40, j*40+40, i*40+40, fill="black")
                elif plateau[ i ][ j ] == 4:  # MUR TEMPO
                    self.canvas.create_rectangle(j*40, i*40, j*40+40, i*40+40, fill="black")
                elif plateau[ i ][ j ] == 3:  # MURAVECPORTE
                    self.canvas.create_rectangle(j*40, i*40, j*40+40, i*40+40, fill="orange")
                elif plateau[ i ][ j ] == -1:  #place pour pions
                    self.canvas.create_rectangle(j*40, i*40, j*40+40, i*40+40, fill="grey")
                elif plateau[ i ][ j ] == -2:  #place pour les murs
                    print(i,j)
                    if i % 2 == 0 and j % 2 == 1:

                        self.canvas.create_rectangle(j * 15+40, i * 40+40,j * 15+40+15 , i * 40+40+40, fill="blue")

                    if i % 2 == 1 and j % 2 == 1:
                        self.canvas.create_rectangle(j * 40, i * 15, j * 40 + 40, i * 15 + 15, fill="white")
                    if i % 2 == 1 and j % 2 == 0:
                        self.canvas.create_rectangle(j * 15, i * 15, j * 15 + 15, i * 15 + 15, fill="white")

            print( )


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





root = tk.Tk()
view = QuorridorView()


# Crear un estado de juego de prueba
game_state = [[-1, -2, -1, -2, -1],
              [1, 1, 1, -2, -2],
              [-1, -2, -1, 2, -1],
              [-2, -2, -2, 2, -2],
              [-1, -2, -1, 2, -1]]

class Player:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

joueur = Player(0, 2)
adversaire = Player(4, 2)

# Llamar al método display con el estado de juego de prueba
view.display(game_state, joueur, adversaire)
root.mainloop()
"""
