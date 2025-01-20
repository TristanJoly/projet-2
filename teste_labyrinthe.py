import random
from random import randint as rnt

class Graphe:
    def __init__(self, oriente=True):
        self.A = {}
        self.oriente = oriente

    def __repr__(self):
        return str(self.A)

    def __len__(self):
        return len(self.A)

    def construire(self, A):
        self.w = self.h = 0
        self.A = A
        for s in A:
            self.w = max(self.w, s[1] + 1)
            self.h = max(self.h, s[0] + 1)

    def ajouter_sommet(self, x):
        if not x in self.A:
            self.A[x] = set()

    def ajouter_arete(self, x, y):
        self.ajouter_sommet(x)
        self.ajouter_sommet(y)
        self.A[x].add(y)
        if not self.oriente:
            self.A[y].add(x)

    def voisins(self, x):
        return self.A[x]

    def arete(self, x, y):
        return y in self.A[x]
"""
classe de graphe pondere vue en classe avec toutes les fonctions usuelles associe.
"""

class Labyrinthe(Graphe):
    coins = [" ", "═", "║", "╚", "═", "═", "╝", "╩", "║", "╔", "║", "╠", "╗", "╦", "╣", "╬"]

    def __init__(self, w=0, h=0):
        """
        Fonction permettant de construire l'object labyrinthe 
        """
        Graphe.__init__(self, oriente=False)
        self.w = w
        self.h = h
        self.reset()
        self.repr = [["*"] * (2 * self.w + 1) for _ in range(2 * self.h + 1)]
        self.effacer_repr()
        self.ouvertures = []
        

    def reset(self):
        #fonction permettant de renitialiser le labyrinthe pour qu' il ne soit plus compôse d'aucun mur.
        self.A = {}
        for l in range(self.h):
            for c in range(self.w):
                self.ajouter_sommet((l, c))

    def retourne_sommet(self):
        temp = []
        for i in  self.A:
            temp.append (i)
        return temp
    
    def __repr__(self):
        self.construire_repr()
        L = []
        for l in self.repr:
            L.append("".join(l))
        return "\n".join(L)

    def construire_repr(self):
        #fonction permettant d'afficher le labyrtinthe dans le terminal
        #elle marche par la matrice du graphe , mais egalement avec un dictionnaire ou est represente des zelements asci permettant de dessiner des murs.
        for c in range(self.w):
            self.repr[0][2 * c + 1] = Labyrinthe.coins[5]
        for l in range(self.h):
            self.repr[2 * l + 1][0] = Labyrinthe.coins[10]
            for c in range(self.w):
                if l + 1 < self.h and self.arete((l, c), (l + 1, c)):
                    self.repr[2 * l + 2][2 * c + 1] = Labyrinthe.coins[0]
                else:
                    self.repr[2 * l + 2][2 * c + 1] = Labyrinthe.coins[5]

                if c + 1 < self.w and self.arete((l, c), (l, c + 1)):
                    self.repr[2 * l + 1][2 * c + 2] = Labyrinthe.coins[0]
                else:
                    self.repr[2 * l + 1][2 * c + 2] = Labyrinthe.coins[10]
        for l in range(0, len(self.repr), 2):
            for c in range(0, len(self.repr[0]), 2):
                code = 1 * (c + 1 < len(self.repr[0]) and self.repr[l][c + 1] != " ")
                code += 2 * (l != 0 and self.repr[l - 1][c] != " ")
                code += 4 * (c != 0 and self.repr[l][c - 1] != " ")
                code += 8 * (l + 1 < len(self.repr) and self.repr[l + 1][c] != " ")
                self.repr[l][c] = Labyrinthe.coins[code]
        for o in self.ouvertures:
            l, c = o
            if c == 0:
                self.repr[2 * l + 1][2 * c] = " "
            elif c == self.w - 1:
                self.repr[2 * l + 1][2 * c + 2] = " "
            elif l == 0:
                self.repr[2 * l][2 * c + 1] = " "
            elif l == self.h - 1:
                self.repr[2 * l + 2][2 * c + 1] = " "

    def effacer_repr(self):
        for l in range(self.h):
            for c in range(self.w):
                self.repr[2 * l + 1][2 * c + 1] = " "

    def remplir_chemin(self, lst):
        i = 0
        for s in lst:
            l, c = s
            self.repr[2 * l + 1][2 * c + 1] = str(i)[-1]
            i += 1

    def generer_labyrinthe_growing_tree(self):
        #permet de creer un labyrinthe selon la methode de growing tree
        def voisins_valides(cell):
            #cette sous fonction permet de definir si des voisin sont valides pour etre dans le labyrinthe. 
            l, c = cell
            voisins = []
            if l > 0 and (l - 1, c) not in visited:
                voisins.append((l - 1, c))
            if l < self.h - 1 and (l + 1, c) not in visited:
                voisins.append((l + 1, c))
            if c > 0 and (l, c - 1) not in visited:
                voisins.append((l, c - 1))
            if c < self.w - 1 and (l, c + 1) not in visited:
                voisins.append((l, c + 1))
            return voisins

        start_cell = (random.randint(0, self.h - 1), random.randint(0, self.w - 1))
        active_cells = [start_cell]
        visited = {start_cell}

        while active_cells:
            current_cell = active_cells[-1]
            voisins = voisins_valides(current_cell)
            if voisins:
                next_cell = random.choice(voisins)
                self.ajouter_arete(current_cell, next_cell)
                visited.add(next_cell)
                active_cells.append(next_cell)
            else:
                active_cells.pop()

    def select_random_case(self):
        a = rnt(0,(self.w-1))
        b = rnt(0,(self.h-1))
        c = rnt(0,(self.w-1))
        d = rnt(0,(self.h-1))
        return ((a,b),(c,d))

def Dijkstra(g, src):
    #fonction de djikstra vue en classe 
    dist = {sommet: float('inf') for sommet in g.retourne_sommet()}
    dist[src] = 0
    pred = {sommet: None for sommet in g.retourne_sommet()}
    non_visites = set(g.retourne_sommet())

    while non_visites:
        u = min(non_visites, key=lambda sommet: dist[sommet])
        non_visites.remove(u)
        for k in g.voisins(u):
            voisin = k
            alt = dist[u] + 1
            if alt < dist[voisin]:
                dist[voisin] = alt
                pred[voisin] = u

    return dist, pred

def plus_court_chemin_D2(g, u, v):
    #focntion permettant de retourner le plus court chemin selon djikstra
    dist, pred = Dijkstra(g, u)
    chemin = []
    actuel = v
    while actuel is not None:
        chemin.insert(0, actuel)
        actuel = pred[actuel]
    if chemin[0] == u:
        return chemin
    else:
        return None

def labyrinthe_to_game_map(labyrinthe):
    #permet de modifier le labyrinthe en un element compatible pour la map du ray casting.
    game_map = [[1] * (labyrinthe.w * 2 + 1) for _ in range(labyrinthe.h * 2 + 1)]
    for l in range(labyrinthe.h):
        for c in range(labyrinthe.w):
            game_map[2 * l + 1][2 * c + 1] = 0
            if labyrinthe.arete((l, c), (l + 1, c)):
                game_map[2 * l + 2][2 * c + 1] = 0
            if labyrinthe.arete((l, c), (l, c + 1)):
                game_map[2 * l + 1][2 * c + 2] = 0
    return game_map
