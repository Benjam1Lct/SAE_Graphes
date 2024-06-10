import numpy as np
import math

from graphe import GrapheValue
from algos import AlgoPlusCourtChemin, AlgoDijkstra

class ReseauSocial:
    """
    Classe qui représente un réseau social, représenté par un graphe valué 
    (par défaut, les valuations des arêtes présentes dans le graphe sont égales à 1).
    On peut également indiquer les noms des sommets du graphe, définis dans un dictionnaire.
    """
    
    def __init__(self, g:GrapheValue, algo:AlgoPlusCourtChemin, noms:dict=[]):
        """
        Constructeur à partir d'un graphe valué et d'un algorithme de calcul de plus court chemin.
        Paramètres :
            g : graphe valué.
            algo : algorithme de calcul de plus court chemin.
            sommets : les noms associés aux sommets du graphe.
        """
        self.graphe = g
        self.algoPCC = algo
        self.sommets = noms
 

    def __str__(self):
        """
        Représentation de l'algorithme de calcul de plus court chemin, par la matrice des distances.
        Retour :
            chaîne de caractères contenant les valeurs des distances.
        """
        return str(self.graphe)
    
    
    def densite(self):
        """
        Densité du graphe, c'est-à-dire ratio du nombre d'arêtes sur le nombre d'arêtes d'un graphe complet.
        Retour :
            densité du graphe.
        """
        total_edges = self.graphe.nb_aretes()
        total_nodes = self.graphe.nb_sommets()
        max_edges = total_nodes * (total_nodes - 1) / 2
        return total_edges / max_edges
    
    
    def degre_sommet(self, s:int):
        """
        Degré du sommet s donné.
        Paramètre :
            s : indice du sommet considéré.
        Retour :
            degré du sommet s.
        """
        return len([i for i in range(self.graphe.nb_sommets()) if self.graphe.matrice[s][i] != math.inf])
    
    
    def degre_moyen(self):
        """
        Degré moyen du graphe, c'est-à-dire moyenne des degrés du graphe.
        Retour :
            degré moyen du graphe.
        """
        return sum(self.degre_sommet(i) for i in range(self.graphe.nb_sommets())) / self.graphe.nb_sommets()
        
    
    def proximite_sommet(self, s:int):
        """
        Proximité du sommet s donné, c'est-à-dire distance moyenne du sommet aux autres sommets du graphe.
        Paramètre :
            s : indice du sommet considéré.
        Retour :
            proximité du sommet s.
        """
        distances, _ = self.algoPCC.calculPCCSommet(s)
        return sum(distances) / (self.graphe.nb_sommets() - 1)
    
    
    def diametre(self):
        """
        Diamètre du graphe, c'est-à-dire plus grande des distances entre deux sommets du graphe.
        Retour :
            diamètre du graphe.
        """
        max_distance = 0
        for s in range(self.graphe.nb_sommets()):
            distances, _ = self.algoPCC.calculPCCSommet(s)
            max_distance = max(max_distance, max(distances))
        return max_distance
    
    
    def longueur_moyenne(self):
        """
        Longueur moyenne du graphe, c'est-à-dire distance moyenne pour chaque paire de sommets du graphe.
        Retour :
            longueur moyenne du graphe.
        """
        total_distance = 0
        for s in range(self.graphe.nb_sommets()):
            distances, _ = self.algoPCC.calculPCCSommet(s)
            total_distance += sum(distances)
        return total_distance / (self.graphe.nb_sommets() * (self.graphe.nb_sommets() - 1))

    def afficher_metriques(self):
        """
        Affichage des différentes métriques du graphe. 
        Pour les métriques sur les sommets, on affiche les valeurs des métriques, pour chaque sommet
        (en triant les valeurs par valeur croissante ou décroissante, selon les métriques).
        Si le réseau n'est pas connexe, on l'indique et on affiche ces métriques sur la plus grosse composante
        connexe du réseau.
        """
        print("Densité du réseau :", self.densite())
        print("Degré moyen du réseau :", self.degre_moyen())
        print("Diamètre du réseau :", self.diametre())
        print("Longueur moyenne du réseau :", self.longueur_moyenne())
        for s in range(self.graphe.nb_sommets()):
            print(f"Proximité du sommet {s} :", self.proximite_sommet(s))



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
    r = ReseauSocial(g, AlgoDijkstra(g))
    print(r)
    r.afficher_metriques()
