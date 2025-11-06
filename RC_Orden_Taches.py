import random
import math

# --- Données du Problème (Tâches) ---
# Chaque tâche est un tuple: (temps_traitement, date_livraison, poids)
# Index 0: Temps de traitement (p_j)
# Index 1: Date de livraison (d_j)
# Index 2: Poids (w_j)
TACHES = [
    (5, 10, 3), # Tâche 0
    (3, 8, 2),  # Tâche 1
    (8, 20, 4), # Tâche 2
    (2, 5, 5),  # Tâche 3
    (6, 15, 1)  # Tâche 4
]
NOMBRE_TACHES = len(TACHES)

# --- 1. Fonction de Coût (Objectif) ---
def calculer_twt(ordre_taches):
    """
    Calcule le Total Weighted Tardiness (TWT) pour un ordre de tâches donné.
    ordre_taches est une liste d'indices de tâches, ex: [3, 0, 4, 1, 2]
    """
    twt = 0
    temps_achevement_machine = 0 # Temps où la machine est libre après la tâche précédente

    for indice_tache in ordre_taches:
        p_j, d_j, w_j = TACHES[indice_tache] # Récupère les données de la tâche
        
        temps_achevement_machine += p_j # Le temps d'achèvement de cette tâche
        
        retard = max(0, temps_achevement_machine - d_j) # Calcul du retard
        
        twt += w_j * retard # Ajout du retard pondéré
        
    return twt

# --- 2. Génération de Voisin ---
def generer_voisin_simple(ordre_taches_actuel):
    """
    Crée un voisin en échangeant deux tâches aléatoires dans l'ordre.
    """
    voisin = ordre_taches_actuel[:] # Copie l'ordre actuel
    
    # Sélectionne deux positions aléatoires
    idx1, idx2 = random.sample(range(NOMBRE_TACHES), 2)
    
    # Échange les tâches
    voisin[idx1], voisin[idx2] = voisin[idx2], voisin[idx1]
    
    return voisin

# --- 3. Algorithme de Recuit Simulé ---
def recuit_simule_ordonnancement_simple(temp_initiale, taux_refroidissement, max_iterations):
    """
    Algorithme de Recuit Simulé pour minimiser le TWT.
    """
    # Initialisation
    solution_actuelle = list(range(NOMBRE_TACHES)) # Ordre initial: [0, 1, 2, ..., N-1]
    random.shuffle(solution_actuelle) # Mélange aléatoirement pour avoir un point de départ différent
    
    cout_actuel = calculer_twt(solution_actuelle)

    meilleure_solution_globale = solution_actuelle[:]
    meilleur_cout_global = cout_actuel

    temperature = temp_initiale

    # Boucle d'optimisation
    for _ in range(max_iterations):
        voisin = generer_voisin_simple(solution_actuelle)
        cout_voisin = calculer_twt(voisin)

        delta = cout_voisin - cout_actuel # Différence de coût

        # Critère d'acceptation (Metropolis)
        # Accepte le voisin s'il est meilleur OU s'il est moins bon avec une probabilité
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            solution_actuelle = voisin
            cout_actuel = cout_voisin

            # Mise à jour de la meilleure solution globale trouvée
            if cout_actuel < meilleur_cout_global:
                meilleure_solution_globale = solution_actuelle[:]
                meilleur_cout_global = cout_actuel

        # Refroidissement
        temperature *= taux_refroidissement

    return meilleure_solution_globale, meilleur_cout_global

# --- Paramètres du Recuit Simulé ---
TEMPERATURE_INITIALE = 1000.0
TAUX_REFROIDISSEMENT = 0.995
MAX_ITERATIONS = 50000

# --- Exécution ---
ordre_optimal_indices, min_twt = recuit_simule_ordonnancement_simple(
    TEMPERATURE_INITIALE, TAUX_REFROIDISSEMENT, MAX_ITERATIONS
)

# --- Affichage des Résultats ---
print("--- Ordonnancement des Tâches (Recuit Simulé Simplifié) ---")
print(f"Nombre de tâches : {NOMBRE_TACHES}")
print(f"Paramètres RS : T_init={TEMPERATURE_INITIALE}, alpha={TAUX_REFROIDISSEMENT}, Iter_max={MAX_ITERATIONS}")

# Conversion des indices en noms de tâches pour l'affichage (si vous aviez des noms)
# Pour cet exemple, nous allons juste afficher les indices dans l'ordre
ordre_final_lisible = [f"Tâche {idx}" for idx in ordre_optimal_indices]

print(f"\nMeilleur ordonnancement trouvé (indices des tâches) : {ordre_optimal_indices}")
print(f"Meilleur ordonnancement trouvé (description) : {ordre_final_lisible}")
print(f"Coût minimal (Total Weighted Tardiness - TWT) : {min_twt:.2f}")

# Pour vérifier le détail du TWT pour l'ordre optimal
print("\nDétail du TWT pour l'ordonnancement optimal:")
temps_final_machine = 0
for indice in ordre_optimal_indices:
    p, d, w = TACHES[indice]
    temps_final_machine += p
    retard_tache = max(0, temps_final_machine - d)
    penalite_tache = w * retard_tache
    print(f"  Tâche {indice} (p={p}, d={d}, w={w}): C_j={temps_final_machine}, Retard={retard_tache}, Pénalité={penalite_tache}")

# Ici, nous pourrions inclure une image pour illustrer le concept d'ordonnancement des tâches :