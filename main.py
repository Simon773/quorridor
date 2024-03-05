from Model import *
from Presenter import *
from View import *

def main():
    model = QuorridorModel()
    view = QuorridorView()
    client = Client()
    presenter = QuorridorPresenter(model, view)


main()

#Commandes à introduire dans la console pour placer un mur ou se déplacer
#(joueur 0 ou 1, x, y)
#move,1,1
#place_wall,1,1,3,4,2

