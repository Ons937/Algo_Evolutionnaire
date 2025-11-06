import random

# --- Calcul de la distance totale ---
def calculer_distance_totale(individu, matrice):
    return sum(matrice[individu[i]][individu[(i+1)%len(individu)]] for i in range(len(individu)))

# --- Génération de la population initiale ---
def generer_population(taille_pop, taille_individu):
    return [random.sample(range(taille_individu), taille_individu) for _ in range(taille_pop)]

# --- Sélection par roulette ---
def selection_roulette(population, matrice, k):
    fitness = [1 / (calculer_distance_totale(ind, matrice) + 1e-6) for ind in population]
    total = sum(fitness)
    probabilites = [f / total for f in fitness]
    return random.choices(population, weights=probabilites, k=k)

# --- Croisement simple (1 point) ---
def croisement_simple(p1, p2):
    point = random.randint(1, len(p1)-2)
    enfant = p1[:point] + [v for v in p2 if v not in p1[:point]]
    return enfant

# --- Croisement double (2 points) ---
def croisement_double(p1, p2):
    a, b = sorted(random.sample(range(len(p1)), 2))
    segment = p1[a:b]
    reste = [v for v in p2 if v not in segment]
    return reste[:a] + segment + reste[a:]

# --- Croisement uniforme avec réparation ---
def croisement_uniforme(p1, p2):
    taille = len(p1)
    enfant = [p1[i] if random.random() < 0.5 else p2[i] for i in range(taille)]

    # Comptage des occurrences
    compteur = {}
    for v in enfant:
        compteur[v] = compteur.get(v, 0) + 1

    # Identifier les doublons (indices à corriger) et les villes manquantes
    doublons = [i for i, v in enumerate(enfant) if compteur[v] > 1]
    toutes_villes = set(range(taille))
    presentes = set(enfant)
    manquantes = list(toutes_villes - presentes)

    # Remplacer les doublons par les villes manquantes
    for i in doublons:
        v = enfant[i]
        if compteur[v] > 1 and manquantes:
            enfant[i] = manquantes.pop()
            compteur[v] -= 1
            compteur[enfant[i]] = 1

    return enfant


# --- Mutation par échange ---
def mutation(individu, taux):
    if random.random() < taux:
        i, j = random.sample(range(len(individu)), 2)
        individu[i], individu[j] = individu[j], individu[i]
    return individu

# --- Algorithme génétique principal ---
def algo_genetique(matrice, taille_pop, taux_sel, taux_mut, generations, type_croisement):
    taille_ind = len(matrice)
    population = generer_population(taille_pop, taille_ind)
    meilleur = min(population, key=lambda ind: calculer_distance_totale(ind, matrice))
    meilleure_dist = calculer_distance_totale(meilleur, matrice)

    for gen in range(generations):
        parents = selection_roulette(population, matrice, max(2, int(taille_pop * taux_sel)))
        nouvelle_gen = []

        while len(nouvelle_gen) < taille_pop:
            p1, p2 = random.sample(parents, 2)
            if type_croisement == "simple":
                enfant = croisement_simple(p1, p2)
            elif type_croisement == "double":
                enfant = croisement_double(p1, p2)
            elif type_croisement == "uniforme":
                enfant = croisement_uniforme(p1, p2)
            else:
                raise ValueError("Type de croisement inconnu")
            enfant = mutation(enfant, taux_mut)
            nouvelle_gen.append(enfant)

        population = nouvelle_gen
        candidat = min(population, key=lambda ind: calculer_distance_totale(ind, matrice))
        dist_candidat = calculer_distance_totale(candidat, matrice)
        if dist_candidat < meilleure_dist:
            meilleur, meilleure_dist = candidat, dist_candidat

    return meilleur, meilleure_dist
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

for croisement in ["simple", "double", "uniforme"]:
    meilleur, dist = algo_genetique(
        matrice_distances,
        taille_pop=100,
        taux_sel=0.3,
        taux_mut=0.1,
        generations=500,
        type_croisement=croisement
    )
    print(f"\n--- Croisement {croisement} ---")
    print("Meilleur chemin :", meilleur)
    print("Distance minimale :", dist)
