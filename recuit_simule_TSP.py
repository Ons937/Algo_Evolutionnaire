import random
import math

def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

def generer_voisin(solution):
    i, j = random.sample(range(len(solution)), 2)
    voisin = solution[:]
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin

def recuit_simule(matrice_distances, temperature_initiale, taux_refroidissement, iterations_max):
    nombre_villes = len(matrice_distances)
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)
    distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)

    meilleure_solution = solution_actuelle[:]
    meilleure_distance = distance_actuelle

    temperature = temperature_initiale

    for _ in range(iterations_max):
        voisin = generer_voisin(solution_actuelle)
        distance_voisin = calculer_distance_totale(voisin, matrice_distances)
        delta = distance_voisin - distance_actuelle

        if delta < 0 or random.random() < math.exp(-delta / temperature):
            solution_actuelle = voisin
            distance_actuelle = distance_voisin

            if distance_actuelle < meilleure_distance:
                meilleure_solution = solution_actuelle[:]
                meilleure_distance = distance_actuelle

        temperature *= taux_refroidissement

    return meilleure_solution, meilleure_distance
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

temperature_initiale = 1000
taux_refroidissement = 0.995
iterations_max = 1000

meilleure_solution, meilleure_distance = recuit_simule(
    matrice_distances,
    temperature_initiale,
    taux_refroidissement,
    iterations_max
)

print("Meilleure solution trouvée (Recuit simulé):", meilleure_solution)
print("Distance minimale:", meilleure_distance)
