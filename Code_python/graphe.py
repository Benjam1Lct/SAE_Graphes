import numpy as np
import math


class GrapheValue:
    """
    Classe qui représente des graphes valués non orientés.
    Les graphes valués sont représentés par leur matrice de valuation.
    Les sommets sont numérotés de 0 à n-1 (n étant le nombre de sommets).
    """

    def __init__(self, mat):
        """
        Constructeur d'un graphe valué, à partir de sa matrice de valuation.
        Paramètres :
            m : matrice de valuation du graphe.
        """
        self.matrice = mat

    def __str__(self):
        """
        Représentation du graphe valué, par une chaîne de caractères.
        Retour :
            chaîne de caractères contenant les valeurs de la matrice
            de valuation du graphe.
        """
        return str(self.matrice)

    def nb_sommets(self):
        """
        Calcul le nombre de sommets du graphe.
        Retour :
            nombre de sommets du graphe.
        """
        return len(self.matrice)

    def nb_aretes(self):
        """
        Calcul le nombre d'arêtes du graphe.
        Retour :
            nombre d'arêtes du graphe.
        """
        nb_aretes = 0
        for i in range(len(self.matrice)):
            for j in range(len(self.matrice[i])):
                if self.matrice[i][j] != math.inf:
                    nb_aretes += 1
        return nb_aretes / 2

    def degre_sommet(self, s: int):
        """
        Calul du degré du sommet d'indice donné.
        Paramètres :
            s : indice du sommet considéré.
        Retour :
            degré du sommet s.
        """
        deg = 0
        for i in range(len(self.matrice[s])):
            if self.matrice[s][i] != math.inf:
                deg += 1
        return deg

    def degres_sommets(self):
        """
        Calcul de la liste des degrés des sommets du graphe.
        Retour :
            liste des degrés des sommets du graphe.
        """
        lst_degres = []
        for i in range(len(self.matrice)):
            lst_degres.append(self.degre_sommet(i))
        return lst_degres

    def successeurs(self, s):
        succs = []
        for i in range(self.nb_sommets()):
            if self.matrice[s][i] != math.inf:
                succs.append(i)
        return succs

    def predecesseurs(self, s):
        preds = []
        for i in range(self.nb_sommets()):
            if self.matrice[i][s] != math.inf:
                preds.append(i)
        return preds

    def descendants(self, s):
        descs = set()
        file = []

        file.append(s)
        while len(file) > 0:
            scour = file[0]
            file = file[1:]
            succs = self.successeurs(scour)
            for i in range(len(succs)):
                if (succs[i] not in descs):
                    file.append(succs[i])
                    descs.add(succs[i])
        return descs

    def ascendants(self, s):
        ascs = set()
        file = []

        file.append(s)
        while len(file) > 0:
            scour = file[0]
            file = file[1:]
            preds = self.predecesseurs(scour)
            for i in range(len(preds)):
                if (preds[i] not in ascs):
                    file.append(preds[i])
                    ascs.add(preds[i])
        return ascs

    def cfc_sommet(self, g, s):
        graphe = GrapheValue(g)
        return graphe.descendants(s).intersection(graphe.ascendants(s)).union({s})

    def cfc_graphe(self):
        return [self.cfc_sommet(self.matrice, s) for s in range(len(self.matrice)) if
                [self.cfc_sommet(self.matrice, s_bis) for s_bis in range(s)].count(
                    self.cfc_sommet(self.matrice, s)) < 1]

    @staticmethod
    def graphe_vide(size):
        return np.array([[math.inf for _ in range(size)] for _ in range(size)])

    def graphe_symetrique(self):
        sym = self.graphe_vide(self.nb_sommets())
        for i in range(self.nb_sommets()):
            for j in range(self.nb_sommets()):
                if self.matrice[i][j] != math.inf:
                    sym[i][j] = self.matrice[i][j]
                    sym[j][i] = self.matrice[i][j]
        return GrapheValue(sym)

    def cc_sommet(self, s):
        return self.cfc_sommet(self.graphe_symetrique().matrice, s)

    def est_connexe(self):
        """
        Test de la connexité du graphe courant.
        Retour :
            vrai si le graphe est connexe ; faux sinon.
        """
        return len(self.cc_graphe()) == 1

    def cc_graphe(self):
        """
        Calcule les composantes connexes du graphe et retourne la liste des sommets
        de chaque composante.
        Retour :
            liste des composantes connexes.
        """
        return [self.cc_sommet(s) for s in range(self.nb_sommets()) if
                [self.cc_sommet(s_bis) for s_bis in range(s)].count(self.cc_sommet(s)) < 1]

    def plus_grosse_cc(self):
        """
        Calcule les composantes connexes du graphe et retourne le sous-graphe
        correspondant à la plus grosse d'entre elles (en termes de nombre de sommets).
        Retour :
            le sous-graphe correspondant à la plus grosse composante connexe
            (la numérotation des sommets n'est plus la même que dans le graphe de départ).
        """
        composantes = self.cc_graphe()
        plus_grosse = max(composantes, key=len)
        n = len(plus_grosse)
        mat = self.graphe_vide(n)

        index_map = {old_index: new_index for new_index, old_index in enumerate(plus_grosse)}

        for old_index in plus_grosse:
            new_index = index_map[old_index]
            for succ in self.successeurs(old_index):
                if succ in plus_grosse:
                    mat[new_index][index_map[succ]] = self.matrice[old_index][succ]

        return GrapheValue(mat)


if __name__ == "__main__":
    m = np.array([[math.inf, math.inf, math.inf],
                  [math.inf, math.inf, math.inf],
                  [math.inf, math.inf, math.inf],
                  ])
    g = GrapheValue(m)
    print(g)

    m2 = np.array([[math.inf, 3, 2.5, 8],
                   [3, math.inf, math.inf, 7],
                   [2.5, math.inf, math.inf, 1.5],
                   [8, 7, 1.5, math.inf],
                   ])

    m3 = np.array([[math.inf, 3, 5, math.inf],
                   [3, math.inf, 8, math.inf],
                   [5, 8, math.inf, math.inf],
                   [math.inf, math.inf, math.inf, math.inf]
                   ])
    g3 = GrapheValue(m3)
    g2 = GrapheValue(m2)
    print(g2)
    print("degré(0) :", g2.degre_sommet(0))
    print("degré(1) :", g2.degre_sommet(1))
    print(g2.degres_sommets())
    print("Nb sommets :", g2.nb_sommets())
    print("Nb arêtes :", g2.nb_aretes())
    print(g2.est_connexe())
    print(g.est_connexe())
    print(g2.plus_grosse_cc())
