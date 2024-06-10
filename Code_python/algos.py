import numpy as np
import math

from graphe import GrapheValue



class AlgoPlusCourtChemin:
    """
    Classe abstraite qui représente un algorithme de calcul de plus court chemin, sur un graphe valué.
    On stocke les résultats du calcul de la distance et du prédécesseur sur le plus court chemin,
    pour chacune des paires de sommets du graphe.
    --> cette classe n'est pas à modifier.
    """
    
    def __init__(self, g:GrapheValue):
        """
        Constructeur à partir d'un graphe valué.
        Les 2 matrices contenant les distances et les prédécesseurs sur les plus courts
        chemins sont initialisées dans ce constructeur.
        Paramètres :
            g : graphe valué.
        """
        self.graphe = g
        (self.distances, self.predecesseurs) = self.calculPCCTousSommets()
 

    def __str__(self):
        """
        Représentation de l'algorithme de calcul de plus court chemin, par la matrice des distances.
        Retour :
            chaîne de caractères contenant les valeurs des distances.
        """
        return str(self.distances)
    
    
    
    def calculPCCSommet(self, s:int):
        """
        Calcule le plus court chemin, en partant du sommet s, et
        en allant vers chacun des autres sommets du graphe.
        Retour :
            (matrice des distances, matrice des prédécesseurs sur le plus court chemin).
        """
        return ([], [])
    
    
    def calculPCCTousSommets(self):
        """
        Calcule les plus courts chemins, en partant de chacun des sommets du graphe, et
        en allant vers chacun des sommets du graphe.
        Retour :
            (matrice des distances, matrice des prédécesseurs sur le plus court chemin).
        """
        return ([], [])
        
        
        

class AlgoDijkstra(AlgoPlusCourtChemin):
    """
    Classe qui représente l'algorithme de Dijkstra, pour le calcul de plus court chemin, sur un graphe valué.
    On stocke les résultats du calcul de la distance et du prédécesseur sur le plus court chemin,
    pour chacune des paires de sommets du graphe.
    """
    
    def __init__(self, g):
        """
        Constructeur à partir d'un graphe valué.
        Les 2 matrices contenant les distances et les prédécesseurs sur les plus courts
        chemins sont initialisées dans ce constructeur.
        Paramètres :
            g : graphe valué.
        """
        super().__init__(g)
 

    def calculPCCSommet(self, s:int):
        """
        Calcule le plus court chemin, en partant du sommet s, et
        en allant vers chacun des autres sommets du graphe.
        Retour :
            (matrice des distances, matrice des prédécesseurs sur le plus court chemin).
        """
        n = self.graphe.nb_sommets()
        distances = [math.inf] * n
        predecesseurs = [None] * n
        distances[s] = 0
        unvisited = set(range(n))

        while unvisited:
            current = min(unvisited, key=lambda node: distances[node])
            unvisited.remove(current)

            for neighbour in range(n):
                if self.graphe.matrice[current][neighbour] != math.inf:
                    alt_distance = distances[current] + self.graphe.matrice[current][neighbour]
                    if alt_distance < distances[neighbour]:
                        distances[neighbour] = alt_distance
                        predecesseurs[neighbour] = current

        return distances, predecesseurs
    
    
    def calculPCCTousSommets(self):
        """
        Calcule les plus courts chemins, en partant de chacun des sommets du graphe, et
        en allant vers chacun des sommets du graphe.
        Retour :
            (matrice des distances, matrice des prédécesseurs sur le plus court chemin).
        """
        n = self.graphe.nb_sommets()
        distances = []
        predecesseurs = []

        for s in range(n):
            dist, pred = self.calculPCCSommet(s)
            distances.append(dist)
            predecesseurs.append(pred)

        return distances, predecesseurs



if __name__ == "__main__":
    matrice = np.array([[math.inf, 1,math.inf,1,math.inf,math.inf,math.inf],
                        [1,math.inf,1,1,math.inf,math.inf,math.inf],
                        [math.inf,1,math.inf,1,1,math.inf,math.inf],
                        [1,1,1,math.inf,1,math.inf,math.inf],
                        [math.inf,math.inf,1,1,math.inf,1,math.inf],
                        [math.inf,math.inf,math.inf,math.inf,1,math.inf,1],
                        [math.inf,math.inf,math.inf,math.inf,math.inf,1,math.inf],
                        ])
    g = GrapheValue(matrice)
    algoDijkstra = AlgoDijkstra(g)
    print(algoDijkstra.calculPCCSommet(0))