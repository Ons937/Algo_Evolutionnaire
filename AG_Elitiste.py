import random
import math

# --- Fonctions Utilitaires ---

def calculer_distance_totale(individu, matrice_distances):
    distance_totale = 0
    for i in range(len(individu) - 1):
        distance_totale += matrice_distances[individu[i]][individu[i + 1]]
    distance_totale += matrice_distances[individu[-1]][individu[0]]
    return distance_totale

def generer_population_initiale(taille_population, taille_individu):
    population = []
    for _ in range(taille_population):
        individu = list(range(taille_individu))
        random.shuffle(individu)
        population.append(individu)
    return population

# --- Opérateurs de Croisement ---

def croisement_permutation_valide(individu1, individu2):
    """
    Croisement adapté aux problèmes de permutation (comme le TSP - type OX/PMX).
    Garantit que l'enfant est une permutation valide sans doublons.
    """
    taille = len(individu1)
    debut, fin = sorted(random.sample(range(taille), 2))
    enfant = [None] * taille
    enfant[debut:fin] = individu1[debut:fin]

    position = fin
    for gene in individu2:
        if gene not in enfant:
            if position >= taille:
                position = 0
            enfant[position] = gene
            position += 1
    return enfant

def croisement_simple(individu1, individu2):
    """
    Croisement simple (Single Point Crossover).
    AVERTISSEMENT: Inadapté aux problèmes de permutation (TSP).
    """
    taille = len(individu1)
    point_de_coupe = random.randint(1, taille - 1)
    enfant = individu1[:point_de_coupe] + individu2[point_de_coupe:]
    return enfant

def croisement_double(individu1, individu2):
    """
    Croisement double (Two-Point Crossover).
    AVERTISSEMENT: Inadapté aux problèmes de permutation (TSP).
    """
    taille = len(individu1)
    point1, point2 = sorted(random.sample(range(1, taille), 2))
    enfant = individu1[:point1] + individu2[point1:point2] + individu1[point2:]
    return enfant

def croisement_uniforme(individu1, individu2):
    """
    Croisement uniforme (Uniform Crossover).
    AVERTISSEMENT: Inadapté aux problèmes de permutation (TSP).
    """
    taille = len(individu1)
    enfant = [None] * taille
    for i in range(taille):
        if random.random() < 0.5:
            enfant[i] = individu1[i]
        else:
            enfant[i] = individu2[i]
    return enfant

# --- Opérateur de Mutation ---

def mutation(individu, taux_mutation):
    if random.random() < taux_mutation:
        i, j = random.sample(range(len(individu)), 2)
        individu[i], individu[j] = individu[j], individu[i]
    return individu

# --- Algorithme Génétique Principal ---

def algorithme_genetique(matrice_distances, taille_population, taux_elitism, taux_mutation, generations, type_croisement="permutation"):
    taille_individu = len(matrice_distances)
    population = generer_population_initiale(taille_population, taille_individu)

    # Sélectionne la fonction de croisement à utiliser
    if type_croisement == "permutation":
        fonction_croisement = croisement_permutation_valide
    elif type_croisement == "simple":
        fonction_croisement = croisement_simple
    elif type_croisement == "double":
        fonction_croisement = croisement_double
    elif type_croisement == "uniforme":
        fonction_croisement = croisement_uniforme
    else:
        raise ValueError("Type de croisement non reconnu. Choisissez parmi 'permutation', 'simple', 'double', 'uniforme'.")

    meilleure_individu = min(population, key=lambda ind: calculer_distance_totale(ind, matrice_distances))
    meilleure_distance = calculer_distance_totale(meilleure_individu, matrice_distances)

    for generation in range(generations):
        population_triee = sorted(population, key=lambda ind: calculer_distance_totale(ind, matrice_distances))

        # Conservation des élites
        nombre_elites = max(1, int(taille_population * taux_elitism))
        elites = population_triee[:nombre_elites]
        nouvelle_generation = elites[:]

        # Sélection des parents pour la reproduction (basée sur les meilleurs classés)
        nombre_parents_pool = max(2, int(taille_population * (1 - taux_elitism/2))) # Pool de reproduction
        parents_pool = population_triee[:nombre_parents_pool]

        # Remplir le reste de la nouvelle génération
        while len(nouvelle_generation) < taille_population:
            parent1, parent2 = random.sample(parents_pool, 2)
            
            enfant = fonction_croisement(parent1, parent2) # Utilisation de la fonction de croisement choisie
            enfant = mutation(enfant, taux_mutation)
            nouvelle_generation.append(enfant)

        population = nouvelle_generation

        # Mise à jour de la meilleure solution globale
        candidat = min(population, key=lambda ind: calculer_distance_totale(ind, matrice_distances))
        distance_candidat = calculer_distance_totale(candidat, matrice_distances)

        if distance_candidat < meilleure_distance:
            meilleure_individu = candidat
            meilleure_distance = distance_candidat
        
        # print(f"Génération {generation+1}: Meilleure distance = {meilleure_distance:.2f}, Type Croisement: {type_croisement}")

    return meilleure_individu, meilleure_distance

# --- Données du Problème (TSP) ---
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

# --- Paramètres Communs ---
taille_population_param = 100
taux_elitism_param = 0.1
taux_mutation_param = 0.1
generations_param = 500

# --- Exécution avec différents types de croisement ---

print("--- Algorithme Génétique avec différents types de croisement ---")
print(f"Paramètres communs: Pop={taille_population_param}, Elitism={taux_elitism_param}, Mut={taux_mutation_param}, Gens={generations_param}\n")

# 1. Croisement adapté aux permutations (recommandé pour TSP)
meilleure_ind_perm, meilleure_dist_perm = algorithme_genetique(
    matrice_distances, taille_population_param, taux_elitism_param, taux_mutation_param, generations_param,
    type_croisement="permutation"
)
print(f"Type Croisement: PERMUTATION VALIDE")
print(f"  Meilleur individu: {meilleure_ind_perm}")
print(f"  Distance minimale: {meilleure_dist_perm:.2f}\n")

# 2. Croisement Simple
meilleure_ind_simple, meilleure_dist_simple = algorithme_genetique(
    matrice_distances, taille_population_param, taux_elitism_param, taux_mutation_param, generations_param,
    type_croisement="simple"
)
print(f"Type Croisement: SIMPLE (ATTENTION: peut générer des individus invalides pour TSP)")
print(f"  Meilleur individu: {meilleure_ind_simple}")
print(f"  Distance minimale: {meilleure_dist_simple:.2f}\n")

# 3. Croisement Double
meilleure_ind_double, meilleure_dist_double = algorithme_genetique(
    matrice_distances, taille_population_param, taux_elitism_param, taux_mutation_param, generations_param,
    type_croisement="double"
)
print(f"Type Croisement: DOUBLE (ATTENTION: peut générer des individus invalides pour TSP)")
print(f"  Meilleur individu: {meilleure_ind_double}")
print(f"  Distance minimale: {meilleure_dist_double:.2f}\n")

# 4. Croisement Uniforme
meilleure_ind_uni, meilleure_dist_uni = algorithme_genetique(
    matrice_distances, taille_population_param, taux_elitism_param, taux_mutation_param, generations_param,
    type_croisement="uniforme"
)
print(f"Type Croisement: UNIFORME (ATTENTION: très susceptible de générer des individus invalides pour TSP)")
print(f"  Meilleur individu: {meilleure_ind_uni}")
print(f"  Distance minimale: {meilleure_dist_uni:.2f}\n")