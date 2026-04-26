import json
import os

def charger_donnees(nom_fichier):
    chemin = os.path.join('data', nom_fichier)
    if not os.path.exists(chemin): return []
    with open(chemin, 'r', encoding='utf-8') as f:
        return json.load(f)

def splitprog(jours, niveau, objectif, lieu):
    splits = charger_donnees('Splits.json')

    options = [s for s in splits if s['jours_min'] <= jours and s['niveau_requis'] == niveau and s['objectif'] == objectif and s['lieu'] == lieu]
    return max(options, key=lambda x: x['jours_min']) if options else None

def xercices(muscles_du_jour, niveau_user, matos_dispo, lieu_user, hooper_score=None):
    tous_les_exos = charger_donnees('Exercice.json')
    resultats = []
    for ex in tous_les_exos:
        if ex['muscle'] in muscles_du_jour and ex['niveau'] == niveau_user:
            if lieu_user == "Gym":
                if ex['equipement'] != "aucun" and ex['equipement'] in matos_dispo:
                    resultats.append(ex['nom'])
            else:
                if ex['equipement'] == "aucun" or ex['equipement'] in matos_dispo:
                    resultats.append(ex['nom'])
    if hooper_score is not None:
        if hooper_score > 20:
            return ["Repos recommandé"]
        elif hooper_score > 14:
            return resultats[:2]  # séance très light
        elif hooper_score > 8:
            return resultats[:4]  # séance modérée
        else:
            return resultats  # séance complète
    return resultats