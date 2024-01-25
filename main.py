from Model import *
from Presenter import *
from View import *

def main():
    model = QuorridorModel()
    view = QuorridorView()
    client = Client()
    presenter = QuorridorPresenter(model, view)

    mode=int(input("bot qui joue(1), joueur humain(2)"))
    if mode ==1:
        bot = True
    else:
        bot = False
    victoire= False
    tour = 1
    presenter.lancer_jeu()
    while not victoire:
        action=presenter.recuperer_action(bot)
        if action ==1:
            direction = presenter.recuper_direction_deplacement()
            while not presenter.deplacement_joueur(direction):
                direction = presenter.recuper_direction_deplacement()
        if action ==2:
            placement=presenter.recup_placement_mur(bot)
            while not placement:
                presenter.recup_placement_mur(bot)
        if action ==3:
            pass
        victoire= presenter.verifier_victoire()
        print(victoire)
        presenter.update_view()
        client.askPriority()
        tour = (tour + 1) % 2
        presenter.changer_joueur(tour)



main()

#Commandes à introduire dans la console pour placer un mur ou se déplacer
#(joueur 0 ou 1, x, y)
#move,1,1
#place_wall,1,1,3,4,2

