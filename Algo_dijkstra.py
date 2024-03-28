#prendre ne compte la destionation quand on l'ajoutera dans la vue'


class Jeu():
    def __init__(self,plateau,player, mur,):

        self.plateau = plateau

        self.destination = (0, 0)
        self.positions_murs = dict()

    def getVoisinage(self, x,y):
        vois = set()
        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            x2, y2 = x+dx, y + dy #par rapport aux cases des murs on vérfie que l'on ne dépasse pas les limites du plateau
            # et que les positions ne sont pas dans la liste des positions occupées
            if 0 <= x2 <self.taille and 0 <= y2 < self.taille and (x2, y2) not in self.positions_murs.keys():
                x3,y3 =x+(dx*2),y+(dy*2)
                vois.add((x3, y3))
        return vois

    def retiremin(self, file): #parcourt la file et retire l'élement minimale
        if not file:
            return None
        indice_min, minimum = 0, file[0][1]
        for i in range(1, len(file)):
            if file[i][1] < minimum:
                indice_min, minimum = i, file[i][1]
        return file.pop(indice_min)

    def ajoutouremplace(self, file, pos):
        for i in range(len(file)): #on cherche dans tous les noeuds , si il y a un noeuds en coordonnées pos
            if file[i][0] == pos[0]:       #si c'est le cas on lui actualise sa distance (pos[1])
                file[i][1] = pos[1]
                return
        file.append(pos) #sinon on creer ce noeud

    def relacher(self, courant, v, distance, old_pos):
        if courant in distance and (v not in distance or distance[v] > distance[courant] + 1):
            #si on respecte ces conditions on sait qu'il existe un chemin plus court pour aller à v ou que cette distance n'a pas été encore défini
            distance[v] = distance[courant] + 1 #on actualise maintenant cette distance pour aller à v
            old_pos[v] = courant #puisque ce chemin actuellement est le plus court, pour aller a v , on passer par cette case
            return True
        return False

    def dijkstra_modifie( self,destination, depart):
        old_pos = {}  # Dictionnaire des prédécesseurs de chaque position
        distance = {}  # Dictionnaire des distances de chaque position
        termine = set()  # Ensemble des positions dont on connaît la meilleure distance
        distance[depart] = 0
        old_pos[depart] = None
        file = [(depart, 0)]  # File contenant le sommet de départ et sa distance

        while file:
            courant = self.retiremin(file)[0]
            if courant[0] == destination: #on regarde si on est sur la ligne d'arrivée
                break

            vois = self.getVoisinage(courant[0], courant[1])
            for pos in vois:
                if pos not in termine:
                    if self.relacher(courant, pos, distance, old_pos):
                        self.ajoutouremplace(file, (pos, distance[pos]))
            termine.add(courant)

        # Reconstruire le chemin
        chemin = []
        if courant in old_pos:
            while courant:
                chemin.append(courant)
                courant = old_pos[courant]
            chemin.reverse()  #pour obtenir le chemin inverse

        return distance[chemin[-1]], chemin  #retourne la distance la plus courte(dernière distnace trouver et le chemin le plus court)



    def dijkstra(self,player,destination):
        old_pos = {}  #le dict des prédécesseurs de chaque position connue
        distance = {}  #le dict des distances de chaque position connue (mais pas nécessairement la meilleure)
        termine = set()  #l'ensemble des positions dont on connaît la meilleure distance
        distance[(player.pos_x, player.pos_y)] = 0
        old_pos[(player.pos_x, player.pos_y)] = None
        file = [((player.pos_x, player.pos_y), 0)]  # la file ne contient au départ que le sommet de départ et sa distance

        while file:
            courant = self.retiremin(file)[0]
            if courant == self.destination:
                break

            vois = self.getVoisinage(courant[0],courant[1]) #on regarde le voisinage à la position courante
            for pos in vois:
                if pos not in termine:
                    if self.relacher(courant, pos, distance, old_pos):
                        self.ajoutouremplace(file, (pos, distance[pos]))
            termine.add(courant)



        if self.destination in old_pos:
            pos = self.destination
            while pos and pos != (0, 0):
                pos = old_pos[pos]


def trouver_chemin(predecesseurs, depart, arrivee):
    chemin = []
    current = arrivee
    while current != depart:
        chemin.append(current)
        current = predecesseurs[current]
    chemin.append(depart)
    chemin.reverse()
    return chemin

def dijkstra_avec_chemin(player,destination):

    depart = (player.pos_x, player.pos_y)
    destination = self.taille-1
    distances = { (x, y): 1000 for x in range(self.taille) for y in range(self.taille) } #on initialise le dictionnaire
    #toutes les positins avec une distance arbitraire mais assez grande pour ne pas être pris en compte dasn l'algo :1000
    distances[depart] = 0
    predecesseurs = {}

    file_priorite = [(0, depart)]

    while file_priorite:
        distance_actuelle, noeud_actuel = heapq.heappop(file_priorite)

        if noeud_actuel[0] == destination:
            return distance_actuelle, trouver_chemin(predecesseurs, depart, noeud_actuel)

        for voisin in self.getVoisinage(noeud_actuel[0],noeud_actuel[1]):
            distance = distance_actuelle + 1
            if distance < distances[voisin]:
                distances[voisin] = distance
                predecesseurs[voisin] = noeud_actuel
                heapq.heappush(file_priorite, (distance, voisin))
