from Model import *
from Presenter import *
from View import *

def main():
    model = QuorridorModel()
    view = QuorridorView()
    client = Client()
    presenter = QuorridorPresenter(model, view)

main()


