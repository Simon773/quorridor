
from colorama import Fore, Back, Style, init
import tkinter
import tkinter as tk
class QuorridorView:
    def __init__(self):
        self.canvas = None
        self.root = tkinter.Tk()

        self.mode_jeu = tkinter.BooleanVar(self.root)
        self.unite_choisie = tkinter.StringVar(self.root)

        self.root.geometry("600x600")
        self.canvas = tkinter.Canvas(self.root, width=500, height=500)
        self.canvas.grid(row=0, column=0, columnspan=1)

    def start(self):
        if self.root is not None:
            self.root.mainloop( )

    def demander_mode_jeu(self):

        bot_mode_button = tkinter.Button(self.canvas, text="Bot Mode",
                                         command=lambda: [ self.mode_jeu.set(True), bot_mode_button.destroy( ),
                                                           player_mode_button.destroy( ) ], height=2, width=20)
        bot_mode_button.grid(row=1, column=1)

        player_mode_button = tkinter.Button(self.canvas, text="Player Mode",
                                            command=lambda: [ self.mode_jeu.set(False), bot_mode_button.destroy( ),
                                                              player_mode_button.destroy( ) ], height=2, width=20)
        player_mode_button.grid(row=1, column=2)

        self.root.wait_variable(self.mode_jeu)

        return self.mode_jeu.get( )


    def choix_unite(self):
        self.canvas.delete("all")
        sap_button = tkinter.Button(self.canvas, text="Sapeur",
                                    command=lambda: [ self.unite_choisie.set('S'), sap_button.destroy( ),
                                                      jump_button.destroy( ), sprinter_button.destroy( ) ], height=2,
                                    width=20)
        sap_button.grid(row=1, column=1)

        jump_button = tkinter.Button(self.canvas, text="Jumper",
                                     command=lambda: [ self.unite_choisie.set('J'), sap_button.destroy( ),
                                                       jump_button.destroy( ), sprinter_button.destroy( ) ], height=2,
                                     width=20)
        jump_button.grid(row=1, column=2)

        sprinter_button = tkinter.Button(self.canvas, text="Sprinter",
                                         command=lambda: [ self.unite_choisie.set('P'), sap_button.destroy( ),
                                                           jump_button.destroy( ), sprinter_button.destroy( ) ],
                                         height=2, width=20)
        sprinter_button.grid(row=1, column=3)

        self.root.wait_variable(self.unite_choisie)

        return self.unite_choisie.get( )

    def choix_murs(self, player):
        self.canvas.delete("all")
        self.mur_classique = tk.StringVar(self.canvas, value="0")
        self.mur_incassable = tk.StringVar(self.canvas, value="0")
        self.mur_long = tk.StringVar(self.canvas, value="0")
        self.mur_porte = tk.StringVar(self.canvas, value="0")
        self.mur_temporel = tk.StringVar(self.canvas, value="0")

        # Crear objeto StringVar para almacenar el resultado
        result_var = tk.StringVar( )

        classique_label = tk.Label(self.canvas, text="Classique")
        classique_entry = tk.Entry(self.canvas, textvariable=self.mur_classique)
        classique_label.grid( )
        classique_entry.grid( )

        incassable_label = tk.Label(self.canvas, text="Incassable")
        incassable_entry = tk.Entry(self.canvas, textvariable=self.mur_incassable)
        incassable_label.grid( )
        incassable_entry.grid( )

        long_label = tk.Label(self.canvas, text="Long")
        long_entry = tk.Entry(self.canvas, textvariable=self.mur_long)
        long_label.grid( )
        long_entry.grid( )

        porte_label = tk.Label(self.canvas, text="Porte")
        porte_entry = tk.Entry(self.canvas, textvariable=self.mur_porte)
        porte_label.grid( )
        porte_entry.grid( )

        temporel_label = tk.Label(self.canvas, text="Temporel")
        temporel_entry = tk.Entry(self.canvas, textvariable=self.mur_temporel)
        temporel_label.grid( )
        temporel_entry.grid( )

        def clear_entries():
            self.mur_classique.set("0")
            self.mur_incassable.set("0")
            self.mur_long.set("0")
            self.mur_porte.set("0")
            self.mur_temporel.set("0")

        clear_button = tk.Button(self.canvas, text="Effacer", command=clear_entries)
        clear_button.grid( )

        self.validated = tk.BooleanVar(self.canvas, value=False)

        def validate():
            result = int(self.mur_classique.get( )) + int(self.mur_incassable.get( )) * 2 + int(
                self.mur_long.get( )) * 3 + int(self.mur_porte.get( )) * 3 + int(self.mur_temporel.get( )) * 2
            # Actualizar el objeto StringVar con el resultado
            result_var.set("Result: " + str(result))
            if result == 15:
                self.validated.set(True)
                # Destruir los botones de los muros
                self.canvas.delete("all")

        validate_button = tk.Button(self.root, text="Valider", command=validate)
        validate_button.grid( )

        # Crear el label para mostrar el resultado
        result_label = tk.Label(self.root, textvariable=result_var)
        result_label.grid( )

        self.root.wait_variable(self.validated)

        murs = [ int(self.mur_classique.get( )), int(self.mur_incassable.get( )), int(self.mur_long.get( )),
                 int(self.mur_porte.get( )), int(self.mur_temporel.get( )) ]
        self.canvas.delete("all")

        return murs

    def display(self, plateau, joueur, adversaire):
        self.canvas.delete("all")
        marge = 5
        taille = 50
        for i in range(len(plateau)):
            for j in range(len(plateau[ i ])):
                if (i, j) == (joueur.pos_x, joueur.pos_y):  # joueur 1
                    self.canvas.create_rectangle((marge + taille) * (j // 2), (marge + taille) * (i // 2),
                                                 (marge + taille) * (j // 2) + taille,
                                                 (marge + taille) * (i // 2) + taille, fill="green")
                elif (i, j) == (adversaire.pos_x, adversaire.pos_y):  # joueur 2
                    self.canvas.create_rectangle((marge + taille) * (j // 2), (marge + taille) * (i // 2),
                                                 (marge + taille) * (j // 2) + taille,
                                                 (marge + taille) * (i // 2) + taille, fill="pink")
                if plateau[ i ][ j ] == -1:
                    self.canvas.create_rectangle((marge + taille) * (j // 2), (marge + taille) * (i // 2),
                                                 (marge + taille) * (j // 2) + taille,
                                                 (marge + taille) * (i // 2) + taille, fill="tan")
                elif plateau[ i ][ j ] == -2 and i % 2 == 0 and j % 2 == 1:
                    self.canvas.create_rectangle(50 * ((j // 2) + 1) + 5 * (j // 2), 50 * ((i // 2)) + 5 * (i // 2),
                                                 50 * ((j // 2) + 1) + 5 * (j // 2) + 5,
                                                 50 * ((i // 2)) + 5 * (i // 2) + 50, fill="white")
                elif plateau[ i ][ j ] == -2 and i % 2 == 1 and j % 2 == 0:
                    self.canvas.create_rectangle(50 * ((j // 2)) + 5 * (j // 2), 50 * ((i // 2) + 1) + 5 * (i // 2),
                                                 50 * ((j // 2)) + 5 * (j // 2) + 50,
                                                 50 * ((i // 2) + 1) + 5 * (i // 2) + 5, fill="white")
                elif plateau[ i ][ j ] == 0 and i % 2 == 0 and j % 2 == 1:
                    self.canvas.create_rectangle(50 * ((j // 2) + 1) + 5 * (j // 2), 50 * ((i // 2)) + 5 * (i // 2),
                                                 50 * ((j // 2) + 1) + 5 * (j // 2) + 5,
                                                 50 * ((i // 2)) + 5 * (i // 2) + 50, fill="blue")
                elif plateau[ i ][ j ] == 0 and i % 2 == 1 and j % 2 == 0:
                    self.canvas.create_rectangle(50 * ((j // 2)) + 5 * (j // 2), 50 * ((i // 2) + 1) + 5 * (i // 2),
                                                 50 * ((j // 2)) + 5 * (j // 2) + 50,
                                                 50 * ((i // 2) + 1) + 5 * (i // 2) + 5, fill="blue")
                elif plateau[ i ][ j ] == 1 and i % 2 == 0 and j % 2 == 1:
                    self.canvas.create_rectangle(50 * ((j // 2) + 1) + 5 * (j // 2), 50 * ((i // 2)) + 5 * (i // 2),
                                                 50 * ((j // 2) + 1) + 5 * (j // 2) + 5,
                                                 50 * ((i // 2)) + 5 * (i // 2) + 50, fill="red")
                elif plateau[ i ][ j ] == 1 and i % 2 == 1 and j % 2 == 0:
                    self.canvas.create_rectangle(50 * ((j // 2)) + 5 * (j // 2), 50 * ((i // 2) + 1) + 5 * (i // 2),
                                                 50 * ((j // 2)) + 5 * (j // 2) + 50,
                                                 50 * ((i // 2) + 1) + 5 * (i // 2) + 5, fill="red")
                elif plateau[ i ][ j ] == 2 and i % 2 == 0 and j % 2 == 1:
                    self.canvas.create_rectangle(50 * ((j // 2) + 1) + 5 * (j // 2), 50 * ((i // 2)) + 5 * (i // 2),
                                                 50 * ((j // 2) + 1) + 5 * (j // 2) + 5,
                                                 50 * ((i // 2)) + 5 * (i // 2) + 50, fill="blue")
                elif plateau[ i ][ j ] == 2 and i % 2 == 1 and j % 2 == 0:
                    self.canvas.create_rectangle(50 * ((j // 2)) + 5 * (j // 2), 50 * ((i // 2) + 1) + 5 * (i // 2),
                                                 50 * ((j // 2)) + 5 * (j // 2) + 50,
                                                 50 * ((i // 2) + 1) + 5 * (i // 2) + 5, fill="blue")
                elif plateau[ i ][ j ] == 3 and i % 2 == 0 and j % 2 == 1:
                    self.canvas.create_rectangle(50 * ((j // 2) + 1) + 5 * (j // 2), 50 * ((i // 2)) + 5 * (i // 2),
                                                 50 * ((j // 2) + 1) + 5 * (j // 2) + 5,
                                                 50 * ((i // 2)) + 5 * (i // 2) + 50, fill="green")
                elif plateau[ i ][ j ] == 3 and i % 2 == 1 and j % 2 == 0:
                    self.canvas.create_rectangle(50 * ((j // 2)) + 5 * (j // 2), 50 * ((i // 2) + 1) + 5 * (i // 2),
                                                 50 * ((j // 2)) + 5 * (j // 2) + 50,
                                                 50 * ((i // 2) + 1) + 5 * (i // 2) + 5, fill="green")
                elif plateau[ i ][ j ] == 4 and i % 2 == 0 and j % 2 == 1:
                    self.canvas.create_rectangle(50 * ((j // 2) + 1) + 5 * (j // 2), 50 * ((i // 2)) + 5 * (i // 2),
                                                 50 * ((j // 2) + 1) + 5 * (j // 2) + 5,
                                                 50 * ((i // 2)) + 5 * (i // 2) + 50, fill="yellow")
                elif plateau[ i ][ j ] == 4 and i % 2 == 1 and j % 2 == 0:
                    self.canvas.create_rectangle(50 * ((j // 2)) + 5 * (j // 2), 50 * ((i // 2) + 1) + 5 * (i // 2),
                                                 50 * ((j // 2)) + 5 * (j // 2) + 50,
                                                 50 * ((i // 2) + 1) + 5 * (i // 2) + 5, fill="yellow")
        self.root.update( )

