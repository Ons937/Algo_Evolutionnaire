import random

# --- Fonction pour calculer le coût d'un ordre de tâches ---
def calculer_cout_ordonnancement(ordre, durees):
    """
    Calcule le coût total d'un ordre de tâches.
    Ici, on utilise le temps d'achèvement cumulé (flow time).
    """
    temps = 0
    cout_total = 0
    for tache in ordre:
        temps += durees[tache]
        cout_total += temps
    return cout_total

# --- Génération d'une solution initiale aléatoire ---
def generer_solution_initiale(n):
    """
    Génère un ordre aléatoire de n tâches.
    """
    solution = list(range(n))
    random.shuffle(solution)
    return solution

# --- Génération des voisins par permutation de deux tâches ---
def generer_voisins(solution):
    """
    Génère tous les voisins en échangeant deux tâches dans l'ordre.
    Chaque voisin est accompagné du mouvement (i, j).
    """
    voisins = []
    for i in range(len(solution)):
        for j in range(i+1, len(solution)):
            voisin = solution.copy()
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append((voisin, (i, j)))
    return voisins

# --- Algorithme de recherche tabou ---
def recherche_tabou_ordonnancement(durees, iterations, taille_tabou):
    """
    Applique la recherche tabou pour optimiser l'ordre des tâches.
    Objectif : minimiser le coût total (makespan ou flow time).
    """
    n = len(durees)
    solution_courante = generer_solution_initiale(n)
    meilleure_solution = solution_courante[:]
    meilleure_cout = calculer_cout_ordonnancement(meilleure_solution, durees)

    tabou = []

    for it in range(iterations):
        voisins = generer_voisins(solution_courante)

        meilleur_voisin = None
        meilleur_cout_voisin = float('inf')
        meilleur_move = None

        for voisin, move in voisins:
            if move in tabou:
                continue
            cout = calculer_cout_ordonnancement(voisin, durees)
            if cout < meilleur_cout_voisin:
                meilleur_voisin = voisin
                meilleur_cout_voisin = cout
                meilleur_move = move

        if meilleur_voisin is None:
            break  # tous les mouvements sont tabous

        solution_courante = meilleur_voisin

        if meilleur_cout_voisin < meilleure_cout:
            meilleure_solution = meilleur_voisin
            meilleure_cout = meilleur_cout_voisin

        tabou.append(meilleur_move)
        if len(tabou) > taille_tabou:
            tabou.pop(0)

    return meilleure_solution, meilleure_cout
# Durées des tâches (exemple : 10 tâches)
durees_taches = [5, 2, 8, 4, 3, 6, 7, 1, 9, 2]

# Exécution de la recherche tabou
solution, cout = recherche_tabou_ordonnancement(durees_taches, iterations=300, taille_tabou=15)

# Affichage des résultats
print("\n--- Résultats de la Recherche Tabou pour l'Ordonnancement ---")
print("Meilleur ordre de tâches :", solution)
print("Coût total (flow time) :", cout)
