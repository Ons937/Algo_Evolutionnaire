import random

# --- Fonction pour calculer la distance totale d'un chemin ---
def calculer_distance_totale(chemin, matrice):
    """
    Calcule la distance totale d'un chemin donné en sommant les distances
    entre chaque ville consécutive, y compris le retour à la ville de départ.
    """
    return sum(matrice[chemin[i]][chemin[(i+1)%len(chemin)]] for i in range(len(chemin)))

# --- Génération d'une solution initiale aléatoire ---
def generer_solution_initiale(n):
    """
    Génère une permutation aléatoire des villes comme solution initiale.
    """
    solution = list(range(n))
    random.shuffle(solution)
    return solution

# --- Génération des voisins par échange de deux villes ---
def generer_voisins(solution):
    """
    Génère tous les voisins possibles d'une solution en échangeant deux villes.
    Chaque voisin est accompagné du mouvement (i, j) utilisé pour l'obtenir.
    """
    voisins = []
    for i in range(len(solution)):
        for j in range(i+1, len(solution)):
            voisin = solution.copy()
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append((voisin, (i, j)))  # inclure le mouvement
    return voisins

# --- Algorithme de recherche tabou ---
def recherche_tabou(matrice, iterations, taille_tabou):
    """
    Implémente la recherche tabou pour le TSP :
    - Explore les voisins d'une solution courante
    - Évite les mouvements récemment utilisés (liste tabou)
    - Met à jour la meilleure solution globale si une amélioration est trouvée
    """
    n = len(matrice)

    # Initialisation : solution aléatoire
    solution_courante = generer_solution_initiale(n)
    meilleure_solution = solution_courante[:]
    meilleure_distance = calculer_distance_totale(meilleure_solution, matrice)

    tabou = []  # Liste des mouvements interdits temporairement

    for it in range(iterations):
        # Générer tous les voisins de la solution courante
        voisins = generer_voisins(solution_courante)

        # Initialiser le meilleur voisin
        meilleur_voisin = None
        meilleure_dist_voisin = float('inf')
        meilleur_move = None

        # Parcourir les voisins pour trouver le meilleur non-tabou
        for voisin, move in voisins:
            if move in tabou:
                continue  # Ignorer les mouvements tabous

            dist = calculer_distance_totale(voisin, matrice)
            if dist < meilleure_dist_voisin:
                meilleur_voisin = voisin
                meilleure_dist_voisin = dist
                meilleur_move = move

        # Si tous les mouvements sont tabous, on arrête
        if meilleur_voisin is None:
            break

        # Mise à jour de la solution courante
        solution_courante = meilleur_voisin

        # Mise à jour de la meilleure solution globale si amélioration
        if meilleure_dist_voisin < meilleure_distance:
            meilleure_solution = meilleur_voisin
            meilleure_distance = meilleure_dist_voisin

        # Mise à jour de la liste tabou (FIFO)
        tabou.append(meilleur_move)
        if len(tabou) > taille_tabou:
            tabou.pop(0)

    return meilleure_solution, meilleure_distance
# Matrice de distances entre 10 villes
matrice_distances = [
    [0, 2, 2, 7, 15, 2, 5, 7, 6, 5],
    [2, 0, 10, 4, 7, 3, 7, 15, 8, 2],
    [2, 10, 0, 1, 4, 3, 3, 4, 2, 3],
    [7, 4, 1, 0, 2, 15, 7, 7, 5, 4],
    [7, 10, 4, 2, 0, 7, 3, 2, 2, 7],
    [2, 3, 3, 7, 7, 0, 1, 7, 2, 10],
    [5, 7, 3, 7, 3, 1, 0, 2, 1, 3],
    [7, 7, 4, 7, 2, 7, 2, 0, 1, 10],
    [6, 8, 2, 5, 2, 2, 1, 1, 0, 15],
    [5, 2, 3, 4, 7, 10, 3, 10, 15, 0]
]

# Exécution de la recherche tabou
solution, distance = recherche_tabou(matrice_distances, iterations=500, taille_tabou=20)

# Affichage des résultats
print("\n--- Résultats de la Recherche Tabou ---")
print("Meilleur chemin trouvé :", solution)
print("Distance minimale :", distance)
