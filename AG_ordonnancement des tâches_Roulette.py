import random

# --- Fonction de coût : temps d'achèvement cumulé (flow time) ---
def calculer_cout_ordonnancement(ordre, durees):
    temps = 0
    cout_total = 0
    for tache in ordre:
        temps += durees[tache]
        cout_total += temps
    return cout_total

# --- Génération de la population initiale ---
def generer_population(taille_pop, nb_taches):
    return [random.sample(range(nb_taches), nb_taches) for _ in range(taille_pop)]

# --- Sélection par roulette ---
def selection_roulette(population, durees, k):
    fitness = [1 / (calculer_cout_ordonnancement(ind, durees) + 1e-6) for ind in population]
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
    compteur = {}
    for v in enfant:
        compteur[v] = compteur.get(v, 0) + 1
    doublons = [i for i, v in enumerate(enfant) if compteur[v] > 1]
    manquantes = list(set(range(taille)) - set(enfant))
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
def algo_genetique_ordonnancement(durees, taille_pop, taux_sel, taux_mut, generations, type_croisement):
    nb_taches = len(durees)
    population = generer_population(taille_pop, nb_taches)
    meilleur = min(population, key=lambda ind: calculer_cout_ordonnancement(ind, durees))
    meilleur_cout = calculer_cout_ordonnancement(meilleur, durees)

    for gen in range(generations):
        parents = selection_roulette(population, durees, max(2, int(taille_pop * taux_sel)))
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
        candidat = min(population, key=lambda ind: calculer_cout_ordonnancement(ind, durees))
        cout_candidat = calculer_cout_ordonnancement(candidat, durees)
        if cout_candidat < meilleur_cout:
            meilleur, meilleur_cout = candidat, cout_candidat

    return meilleur, meilleur_cout
# Durées des tâches
durees_taches = [5, 2, 8, 4, 3, 6, 7, 1, 9, 2]

# Test avec les trois croisements
for croisement in ["simple", "double", "uniforme"]:
    meilleur, cout = algo_genetique_ordonnancement(
        durees_taches,
        taille_pop=100,
        taux_sel=0.3,
        taux_mut=0.1,
        generations=300,
        type_croisement=croisement
    )
    print(f"\n--- Croisement {croisement} ---")
    print("Meilleur ordre de tâches :", meilleur)
    print("Coût total (flow time) :", cout)
