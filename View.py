import tkinter
import tkinter as tk
class QuorridorView:
    def __init__(self):
        self.canvas = None
        self.root = tkinter.Tk()

        self.mode_jeu = tkinter.BooleanVar(self.root)
        self.unite_choisie = tkinter.StringVar(self.root)
        self.choix_nom_equipe = tkinter.StringVar(self.root)

        self.root.geometry("600x600")
        self.canvas = tkinter.Canvas(self.root, width=500, height=500)
        self.canvas.grid(row=0, column=0, columnspan=1)

    def start(self):
        if self.root is not None:
            self.root.mainloop( )


    def nom_equipe(self):

        label_jeu = tkinter.Label(self.root, text="TEAM SELECTOR")
        label_jeu.grid(row=0, column=1)

        demander_equipe_entry = tkinter.Entry(self.root, text="INTRODUIRE NOM DE L'EQUIPE")
        nom_equipe_button = tkinter.Button(self.root, text="Bot Mode",
                                         command=lambda: [ nom_equipe_button.destroy(),
                                                          label_jeu.destroy()], height=2, width=20)

        demander_equipe_entry.grid(row=0, column=2)

        self.root.wait_variable(self.choix_nom_equipe)
        nom_equipe=demander_equipe_entry.get()
        return nom_equipe



    def demander_mode_jeu(self):

        bot_mode_button = tkinter.Button(self.root, text="Bot Mode",
                                         command=lambda: [ self.mode_jeu.set(True), bot_mode_button.destroy( ),
                                                           player_mode_button.destroy( ) ], height=2, width=20)
        bot_mode_button.grid(row=0, column=1)

        player_mode_button = tkinter.Button(self.root, text="Player Mode",
                                            command=lambda: [ self.mode_jeu.set(False), bot_mode_button.destroy( ),
                                                              player_mode_button.destroy( ) ], height=2, width=20)
        player_mode_button.grid(row=0, column=2)

        self.root.wait_variable(self.mode_jeu)

        return self.mode_jeu.get( )


    def choix_unite(self):
        sap_button = tkinter.Button(self.root, text="Sapeur",
                                    command=lambda: [ self.unite_choisie.set('S'), sap_button.destroy( ),
                                                      jump_button.destroy( ), sprinter_button.destroy( ) ], height=2,
                                    width=20)
        sap_button.grid(row=0, column=1)

        jump_button = tkinter.Button(self.root, text="Jumper",
                                     command=lambda: [ self.unite_choisie.set('J'), sap_button.destroy( ),
                                                       jump_button.destroy( ), sprinter_button.destroy( ) ], height=2,
                                     width=20)
        jump_button.grid(row=0, column=2)

        sprinter_button = tkinter.Button(self.root, text="Sprinter",
                                         command=lambda: [ self.unite_choisie.set('P'), sap_button.destroy( ),
                                                           jump_button.destroy( ), sprinter_button.destroy( ) ],
                                         height=2, width=20)
        sprinter_button.grid(row=0, column=3)

        self.root.wait_variable(self.unite_choisie)

        return self.unite_choisie.get( )

    def choix_murs(self, player):
        self.canvas.delete("all")
        self.mur_classique = tk.StringVar(self.root, value="0")
        self.mur_incassable = tk.StringVar(self.root, value="0")
        self.mur_long = tk.StringVar(self.root, value="0")
        self.mur_porte = tk.StringVar(self.root, value="0")
        self.mur_temporel = tk.StringVar(self.root, value="0")

        # Crear objeto StringVar para almacenar el resultado
        result_var = tk.StringVar( )

        classique_label = tk.Label(self.root, text="Classique")
        classique_entry = tk.Entry(self.root, textvariable=self.mur_classique)
        classique_label.grid(row=1, column=1)  # Cambiado aquí
        classique_entry.grid(row=1, column=2)  # Cambiado aquí

        incassable_label = tk.Label(self.root, text="Incassable")
        incassable_entry = tk.Entry(self.root, textvariable=self.mur_incassable)
        incassable_label.grid(row=2, column=1)  # Cambiado aquí
        incassable_entry.grid(row=2, column=2)  # Cambiado aquí

        long_label = tk.Label(self.root, text="Long")
        long_entry = tk.Entry(self.root, textvariable=self.mur_long)
        long_label.grid(row=3, column=1)  # Cambiado aquí
        long_entry.grid(row=3, column=2)  # Cambiado aquí

        porte_label = tk.Label(self.root, text="Porte")
        porte_entry = tk.Entry(self.root, textvariable=self.mur_porte)
        porte_label.grid(row=4, column=1)  # Cambiado aquí
        porte_entry.grid(row=4, column=2)  # Cambiado aquí

        temporel_label = tk.Label(self.root, text="Temporel")
        temporel_entry = tk.Entry(self.root, textvariable=self.mur_temporel)
        temporel_label.grid(row=5, column=1)  # Cambiado aquí
        temporel_entry.grid(row=5, column=2)  # Cambiado aqu

        def clear_entries():
            self.mur_classique.set("0")
            self.mur_incassable.set("0")
            self.mur_long.set("0")
            self.mur_porte.set("0")
            self.mur_temporel.set("0")

        clear_button = tk.Button(self.root, text="Effacer", command=clear_entries)
        clear_button.grid( )

        self.validated = tk.BooleanVar(self.root, value=False)

        def validate():
            result = int(self.mur_classique.get( )) + int(self.mur_incassable.get( )) * 2 + int(
                self.mur_long.get( )) * 3 + int(self.mur_porte.get( )) * 3 + int(self.mur_temporel.get( )) * 2
            # Actualizar el objeto StringVar con el resultado
            result_var.set("Result: " + str(result))
            if result == 15:
                self.validated.set(True)
                # Destruir los botones de los muros
                classique_label.destroy( )
                classique_entry.destroy( )
                incassable_label.destroy( )
                incassable_entry.destroy( )
                long_label.destroy( )
                long_entry.destroy( )
                porte_label.destroy( )
                porte_entry.destroy( )
                temporel_label.destroy( )
                temporel_entry.destroy( )
                clear_button.destroy( )

        validate_button = tk.Button(self.root, text="Valider", command=validate)
        validate_button.grid( )

        # Crear el label para mostrar el resultado
        result_label = tk.Label(self.root, textvariable=result_var)
        result_label.grid( )

        self.root.wait_variable(self.validated)

        murs = [ int(self.mur_classique.get( )), int(self.mur_incassable.get( )), int(self.mur_long.get( )),
                 int(self.mur_porte.get( )), int(self.mur_temporel.get( )) ]

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

