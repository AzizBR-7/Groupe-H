# inference.py
# Generateur de progression sur 6 semaines
# Concepts: representation des connaissances, logique et inference, agents intelligents

# ─────────────────────────────────────────────
# KNOWLEDGE BASE
# ─────────────────────────────────────────────

# Paliers de reps autorises — jamais de chiffres hors de cette liste
PALIERS_REPS = [6, 8, 10, 12, 15]
PLAFOND_SETS = 4

# Progression secondes : +5s par etape, plafond 60s puis on monte les sets
PLAFOND_SECONDES = 60
INCREMENT_SECONDES = 5

SEMAINES_VARIANTE = {3, 6}

# Regles par (niveau, semaine)
# reps_steps : combien de paliers monter dans PALIERS_REPS
# sets_bonus  : sets a ajouter a la base de l'exercice
# variante    : tenter d'introduire la variante
PROGRESSION_RULES = {
    ("Débutant", 1): {"sets_bonus": 0, "reps_steps": 0, "variante": False},
    ("Débutant", 2): {"sets_bonus": 0, "reps_steps": 1, "variante": False},
    ("Débutant", 3): {"sets_bonus": 0, "reps_steps": 1, "variante": True},
    ("Débutant", 4): {"sets_bonus": 0, "reps_steps": 2, "variante": True},
    ("Débutant", 5): {"sets_bonus": 1, "reps_steps": 1, "variante": True},
    ("Débutant", 6): {"sets_bonus": 1, "reps_steps": 2, "variante": True},

    ("Avancé", 1):   {"sets_bonus": 0, "reps_steps": 0, "variante": False},
    ("Avancé", 2):   {"sets_bonus": 1, "reps_steps": 0, "variante": False},
    ("Avancé", 3):   {"sets_bonus": 1, "reps_steps": 1, "variante": True},
    ("Avancé", 4):   {"sets_bonus": 1, "reps_steps": 2, "variante": True},
    ("Avancé", 5):   {"sets_bonus": 2, "reps_steps": 1, "variante": True},
    ("Avancé", 6):   {"sets_bonus": 2, "reps_steps": 2, "variante": True},
}


# ─────────────────────────────────────────────
# UTILITAIRES
# ─────────────────────────────────────────────

def get_variante(ex: dict, all_exos: list) -> dict | None:
    nom_variante = ex.get("variante_progression")
    if not nom_variante:
        return None
    return next((e for e in all_exos if e["nom"] == nom_variante), None)


def est_en_secondes(ex: dict) -> bool:
    return ex.get("unite") == "secondes"


def progresser_reps(reps_base: int, reps_steps: int) -> int:
    """
    Monte de reps_steps paliers dans PALIERS_REPS a partir de reps_base.
    Si reps_base n'est pas dans la liste, on prend le palier superieur le plus proche.
    Plafonne a 15.
    """
    # Trouver l'index de depart — palier >= reps_base
    idx = 0
    for i, p in enumerate(PALIERS_REPS):
        if p >= reps_base:
            idx = i
            break
    idx_final = min(idx + reps_steps, len(PALIERS_REPS) - 1)
    return PALIERS_REPS[idx_final]


def progresser_secondes(reps_base: int, sets_base: int, reps_steps: int, sets_bonus: int):
    """
    Progression pour exercices en secondes :
    - Chaque step = +5s jusqu'a 60s
    - Une fois a 60s, on augmente les sets a la place
    Retourne (secondes_final, sets_final)
    """
    secondes = reps_base + (reps_steps * INCREMENT_SECONDES)

    if secondes > PLAFOND_SECONDES:
        # Depasse le plafond : on plafonne les secondes et on compense en sets
        sets_bonus_extra = (secondes - PLAFOND_SECONDES) // INCREMENT_SECONDES
        secondes = PLAFOND_SECONDES
        sets_bonus = sets_bonus + sets_bonus_extra

    sets_final = min(sets_base + sets_bonus, PLAFOND_SETS)
    return secondes, sets_final


# ─────────────────────────────────────────────
# MOTEUR D'INFERENCE
# ─────────────────────────────────────────────

def progresser_exercice(ex: dict, semaine: int, niveau: str, all_exos: list) -> dict:
    """
    Chainage avant :
    1. Lire la regle (niveau, semaine)
    2. Si variante demandee ET disponible -> reset a la base de la variante, pas de reps_steps
    3. Sinon -> progresser sur l'exercice de base
    4. Appliquer sets_bonus et plafonds
    """
    regle = dict(PROGRESSION_RULES.get(
        (niveau, semaine),
        {"sets_bonus": 0, "reps_steps": 0, "variante": False}
    ))

    exo_final = ex
    sets_base = ex.get("sets", 3)
    reps_base = ex.get("reps", 10)
    variante_utilisee = False
    reps_steps = regle["reps_steps"]

    # Regle variante
    if regle["variante"]:
        variante = get_variante(ex, all_exos)
        if variante:
            exo_final = variante
            sets_base = variante.get("sets", sets_base)
            reps_base = variante.get("reps", reps_base)
            variante_utilisee = True
            reps_steps = 0  # on repart de la base de la variante, pas de bonus reps

    # Calcul volume selon unite
    if est_en_secondes(exo_final):
        reps_final, sets_final = progresser_secondes(reps_base, sets_base, reps_steps, regle["sets_bonus"])
    else:
        reps_final = progresser_reps(reps_base, reps_steps)
        sets_final = min(sets_base + regle["sets_bonus"], PLAFOND_SETS)

    return {
        "nom": exo_final["nom"],
        "muscle": exo_final.get("muscle", ex.get("muscle", "")),
        "equipement": exo_final.get("equipement", ex.get("equipement", "")),
        "sets": sets_final,
        "reps": reps_final,
        "unite": exo_final.get("unite", "reps"),
        "est_variante": variante_utilisee,
        "exercice_original": ex["nom"],
    }


def generer_progression(exos_du_programme: list, semaine: int, niveau: str, all_exos: list) -> list:
    """
    Agent principal : percoit le programme + semaine + niveau,
    applique les regles, retourne le programme progresse.
    """
    return [progresser_exercice(ex, semaine, niveau, all_exos) for ex in exos_du_programme]